# from rest_framework.permissions import BasePermission
# from .models import Enrollment, Video

# class HasPaidForCourse(BasePermission):
#     """Permission to check if user has paid for the course"""
#     def has_permission(self, request, view):
#         # Allow GET requests for all (handled in serializer)
#         if request.method == 'GET':
#             return True
#         return False

#     def has_object_permission(self, request, view, obj):
#         # Allow access to preview videos
#         if obj.is_preview:
#             return True
            
#         # Check if user has paid for the course
#         if request.user.is_authenticated:
#             return Enrollment.objects.filter(
#                 user=request.user,
#                 course=obj.course,
#                 payment_status=True
#             ).exists()
#         return False