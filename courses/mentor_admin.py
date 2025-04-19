from django.contrib.admin import AdminSite
from .models import Course
from .admin import CourseAdmin

class MentorAdminSite(AdminSite):
    def has_permission(self, request):
        return request.user.is_active and not request.user.is_superuser

mentor_admin_site = MentorAdminSite(name='mentoradmin')

mentor_admin_site.register(Course, CourseAdmin)