from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Mentor, Course, Enrollment, Review,Video
from .serializers import CategorySerializer, MentorSerializer, CourseDetailSerializer,CourseSerializer,EnrollmentSerializer, ReviewSerializer,VideoSerializer, TopMentorSerializer, TopCourseSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.http import HttpResponse
from django.conf import settings
import stripe
from .models import Payment
from django.db.models import Avg, Count



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'category__name', 'mentor__user__full_name']

class CoursesDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
class CourseDetailView(APIView):
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            return Response(CourseSerializer(course, context={'request': request}).data)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

class MentorSearchView(generics.ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__full_name', 'bio']

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
class CourseReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Review.objects.filter(course_id=course_id)


class EnrollmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get('payment_id')
        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
            if payment.payment_status != 'completed':
                return Response({"error": "Payment not completed"}, status=400)

            # Create enrollment
            enrollment = Enrollment.objects.create(
                user=request.user,
                course=payment.course,
                payment_status=True
            )
            return Response({
                "message": "Enrolled successfully",
                "enrollment_id": enrollment.id,
            })
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)


stripe.api_key = "sk_test_51Q3cprGdR9qlor6Wu8EbW6c3q0EPwxG6uZexluIJ0L1gpIb8yctQ2hKWKF9ZoaeeTxjPrF0TQXBUfFchhQQ5PqOF001OVWR7Hf"

class PaymentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
            # Create Stripe PaymentIntent without redirect-based payment methods
            intent = stripe.PaymentIntent.create(
                amount=int(course.price * 100),  # Amount in cents
                currency='usd',
                metadata={
                    'course_id': course.id,
                    'user_id': request.user.id,
                },
                automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'never',  # Disable redirect-based payment methods
                },
            )
            # Save payment to DB
            payment = Payment.objects.create(
                user=request.user,
                course=course,
                amount=course.price,
                stripe_payment_intent=intent.id,
                payment_status="pending"
            )
            return Response({
                'client_secret': intent.client_secret,
                'payment_id': payment.id,
            })
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

class CourseVideosAPIView(APIView):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
            videos = Video.objects.filter(course=course).order_by('created_at')
            
            return Response({
                'course': {
                    'id': course.id,
                    'title': course.title,
                    'thumbnail': course.thumbnail.url if course.thumbnail else None,
                },
                'videos': VideoSerializer(videos, many=True, context={'request': request}).data
            })
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get('payment_id')
        payment_method_id = request.data.get('payment_method_id')

        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)

            # Confirm with Stripe
            intent = stripe.PaymentIntent.confirm(
                payment.stripe_payment_intent,
                payment_method=payment_method_id,
            )

            if intent.status == 'succeeded':
                payment.payment_status = 'completed'
                payment.save()

                
                Enrollment.objects.get_or_create(
                    user=request.user,
                    course=payment.course,
                    defaults={'payment_status': True}
                )

                return Response({"message": "Payment succeeded and enrollment completed!"})
            else:
                payment.payment_status = 'failed'
                payment.save()
                return Response({"error": "Payment failed"}, status=400)

        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)
        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=400)

        
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        # Verify the webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Update payment status in the database
        payment = Payment.objects.filter(stripe_payment_intent=payment_intent['id']).first()
        if payment:
            payment.payment_status = 'completed'
            payment.save()

    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        # Update payment status in the database
        payment = Payment.objects.filter(stripe_payment_intent=payment_intent['id']).first()
        if payment:
            payment.payment_status = 'failed'
            payment.save()

    return HttpResponse(status=200)


class TopMentorsView(APIView):
    """Get top 5 mentors based on stored rating field"""
    
    def get(self, request):
        queryset = Mentor.objects.filter(rating__gt=0).order_by("rating")[:4]
        serializer = TopMentorSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

# class TopCoursesView(APIView):
#     """Get top courses based on average rating and enrollments"""
#     def get(self, request):
#         courses = Course.objects.annotate(
#             average_rating=Avg("reviews__rating"),
#             enrollment_count=Count("enrollments")
#         ).filter(average_rating__isnull=False).order_by("-average_rating", "-enrollment_count")[:5]  # Top 5 courses

class TopCoursesView(APIView):
    def get(self, request):
        queryset = Course.objects.annotate(
            enrollment_count=Count('enrollments') 
        ).order_by('-enrollment_count')[:5]  

        serializer = TopCourseSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    

class CheckEnrollmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        is_enrolled = Enrollment.objects.filter(
            user=request.user,
            course_id=course_id,
            payment_status=True
        ).exists()
        
        return Response({'has_access': is_enrolled})