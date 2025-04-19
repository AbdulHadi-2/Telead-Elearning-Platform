from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from pymediainfo import MediaInfo
import cv2
import os


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='category_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField(default="This is Bio")
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name_plural = "Mentors"


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='courses')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_popular = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']



class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='course_videos/')
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)  
    is_preview = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Automatically calculate video duration"""
        super().save(*args, **kwargs)
        if self.video_file:
            self.duration = self.get_video_duration()
            super().save(update_fields=["duration"])

    def get_video_duration(self):
        """Extracts video duration using OpenCV"""
        video = cv2.VideoCapture(self.video_file.path)
        fps = video.get(cv2.CAP_PROP_FPS)  
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT)) 
        video.release()
        if fps > 0:
            return frame_count / fps  
        return 0

    def __str__(self):
        return f"{self.title} ({self.course.title}) - {self.duration}s"

    class Meta:
        ordering = ["id"]
        
        
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    progress = models.PositiveIntegerField(default=0)  
    payment_status = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Enrollment for {self.user} in {self.course}"
    
    def has_access(self):
        return self.payment_status 

    class Meta:
        unique_together = ('user', 'course')


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review by {self.user.full_name} for {self.course.title}"

    class Meta:
        ordering = ['-created_at']


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=100, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')],
        default='pending'
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment {self.stripe_payment_intent} - {self.payment_status}"

    class Meta:
        ordering = ['-created_at']
