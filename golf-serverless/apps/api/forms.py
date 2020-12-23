from django import forms
from django.forms import ModelForm
from .models import Course

"""
Create a custom form so that you don't need to add in the Name URL or Ciy URL
"""


class CourseAdminForm(ModelForm):
    name_url = forms.SlugField(required=False)
    city_url = forms.SlugField(required=False)

    class Meta:
        model = Course
        fields = '__all__'
