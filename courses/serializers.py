from rest_framework import serializers
from .models import Category, Mentor, Course, Video, Enrollment, Review, Payment
from django.contrib.auth import get_user_model
import os


User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MentorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    email = serializers.CharField(source='user.email')
    bio = serializers.CharField()
    rating = serializers.DecimalField(max_digits=3, decimal_places=1)

    class Meta:
        model = Mentor
        fields = ['user', 'full_name', 'email', 'bio', 'rating']


class VideoSerializer(serializers.ModelSerializer):
    
    video_url = serializers.SerializerMethodField()  
    duration_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'id', 
            'title', 
            'video_url',  
            'thumbnail', 
            'duration', 
            'is_preview', 
            'duration_formatted'
        ]

    def get_video_url(self, obj):
        request = self.context.get('request')
    
        if obj.is_preview:
            if obj.video_file:
                return request.build_absolute_uri(obj.video_file.url) if request else obj.video_file.url
            return None
    
        if request and request.user.is_authenticated:
            has_paid = Enrollment.objects.filter(
                user=request.user,
                course=obj.course,
                payment_status=True
            ).exists()
        
            if has_paid and obj.video_file:  
                return request.build_absolute_uri(obj.video_file.url) if request else obj.video_file.url
    
        return None
    
    
    def get_duration_formatted(self, obj):
        """Convert duration (seconds) into HH:MM:SS format"""
        if obj.duration:
            hours, remainder = divmod(obj.duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        return "00:00:00"

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    mentor = MentorSerializer()
    videos = serializers.SerializerMethodField()  

    class Meta:
        model = Course
        fields = '__all__'

    def get_videos(self, obj):
        request = self.context.get('request')
        videos = obj.videos.all()
        return VideoSerializer(videos, many=True, context={'request': request}).data

class CourseDetailSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'category', 'mentor', 'price', 'is_popular', 'created_at', 'thumbnail', 'videos']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  
    
    class Meta:
        model = Review
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'




class TopMentorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name")
    profile_picture = serializers.SerializerMethodField()
    

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if obj.user.profile_picture and request:
            return request.build_absolute_uri(obj.user.profile_picture.url)
        return None

    class Meta:
        model = Mentor
        fields = ['id', 'full_name', 'profile_picture']
   
        
class TopCourseSerializer(serializers.ModelSerializer):
    mentor_name = serializers.CharField(source="mentor.user.full_name")
    enrollment_count = serializers.IntegerField()
    thumbnail = serializers.SerializerMethodField()

    def get_thumbnail(self, obj):
        request = self.context.get("request")
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)
        return None

    class Meta:
        model = Course
        fields = ["id", "title", "thumbnail", "mentor_name", "price", "enrollment_count"]   
        


from rest_framework import viewsets

class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    
    def get_queryset(self):
        return Video.objects.all()
    
    def get_serializer_context(self):
        return {'request': self.request}