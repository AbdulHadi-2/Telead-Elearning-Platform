from django import forms
from .models import Mentor,Course

class MentorUserOnlyForm(forms.ModelForm):
    class Meta:
        model = Mentor
        fields = ['user','bio']  # Keep only the User field



class CourseUserOnlyForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ['is_popular']