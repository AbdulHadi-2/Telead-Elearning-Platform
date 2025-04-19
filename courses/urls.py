from django.urls import path
from .views import (
    CategoryListView, CourseListView, CoursesDetailView,
    MentorSearchView, ReviewCreateView, PaymentCreateView, EnrollmentCreateView
    ,CourseVideosAPIView,ConfirmPaymentView,CourseDetailView,CourseReviewListView
    , TopMentorsView, TopCoursesView
)
from .views import  stripe_webhook

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CoursesDetailView.as_view(), name='course-detail'),
    path('mentors/', MentorSearchView.as_view(), name='mentor-search'),
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:course_id>/reviews/', CourseReviewListView.as_view(), name='course-reviews'),
    path('enrollment/create/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('payment/create/', PaymentCreateView.as_view(), name='payment-create'),
    path('payment/confirm/', ConfirmPaymentView.as_view(), name='payment-confirm'),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
    path('courses/<int:course_id>/videos/', CourseVideosAPIView.as_view(), name='course_videos'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path("top-mentors/", TopMentorsView.as_view(), name="top-mentors"),
    path("top-courses/", TopCoursesView.as_view(), name="top-courses"),
    


]



