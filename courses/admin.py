from django.contrib import admin
from django.apps import apps
from .models import Course, Video
from .forms import MentorUserOnlyForm,CourseUserOnlyForm
from .models import Mentor


# Auto-register all models except Course and Video (which have custom admins)
app_models = apps.get_app_config('courses').get_models()
for model in app_models:
    if model.__name__ not in ["Course", "Video","Mentor"]:
        admin.site.register(model)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'mentor')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'mentor_profile'):
            return qs.filter(mentor=request.user.mentor_profile)
        return qs.none()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and hasattr(request.user, 'mentor_profile'):
            return obj.mentor == request.user.mentor_profile
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and hasattr(request.user, 'mentor_profile'):
            return obj.mentor == request.user.mentor_profile
        return hasattr(request.user, 'mentor_profile')

    def has_module_permission(self, request):
        return request.user.is_superuser or hasattr(request.user, 'mentor_profile')

    def has_add_permission(self, request):
        return request.user.is_superuser or hasattr(request.user, 'mentor_profile')

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['mentor']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if hasattr(request.user, 'mentor_profile'):
            fields = [field for field in fields if field != 'is_popular']
        return fields

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(request.user, 'mentor_profile'):
            obj.mentor = request.user.mentor_profile
        super().save_model(request, obj, form, change)
        
            



@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course','duration')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        mentor_profile = getattr(request.user, 'mentor_profile', None)
        if mentor_profile:
            return qs.filter(course__mentor=mentor_profile)
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course" and hasattr(request.user, 'mentor_profile'):
            kwargs["queryset"] = Course.objects.filter(mentor=request.user.mentor_profile)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and hasattr(request.user, 'mentor_profile'):
            return obj.course.mentor == request.user.mentor_profile
        return False

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and hasattr(request.user, 'mentor_profile'):
            return obj.course.mentor == request.user.mentor_profile
        return hasattr(request.user, 'mentor_profile')

    def has_module_permission(self, request):
        return request.user.is_superuser or hasattr(request.user, 'mentor_profile')

    def has_add_permission(self, request):
        return request.user.is_superuser or hasattr(request.user, 'mentor_profile')

    def get_readonly_fields(self, request, obj=None):
        return []

 
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None: 
            fields = [field for field in fields if field != 'duration']
        return fields



    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        



@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'course_count','rate')

    def full_name(self, obj):
        return obj.user.full_name
    full_name.short_description = 'Name'

    def email(self, obj):
        return obj.user.email
    email.short_description = 'Email'

    
    def rate(self, obj):
        return obj.rating
    rate.short_description = 'Rate'

    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = "Course Count"

    form = MentorUserOnlyForm 




