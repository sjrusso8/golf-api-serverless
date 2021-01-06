import pytest
import json
from django.urls import resolve, reverse

from apps.api.models import Course
from .factories import create_app_course

pytestmark = pytest.mark.django_db

f = open('./apps/api/test/data/course.json')

data = json.load(f)

@pytest.fixture
def course_A(db) -> Course:
    return create_app_course(**data)

def test_course_details_editor(course_A: Course):
    assert resolve(f"/api/course_details_editor/{course_A.pk}/").view_name == "course_details_editor-detail"

def test_course_details_editor_list():
    assert reverse("course_details_editor-list") == "/api/course_details_editor"
    assert resolve("/api/course_details_editor/").view_name == "course_details_editor-list"

# def test_course_details_editor(course_A: Course):
#      assert reverse("CourseDetails", 
#                     kwargs={"id":course_A.id, "name_url":course_A.name_url,"city_url":course_A.city_url}) == "/api/coursedetails/" + course_A.id +"/"+ course_A.name_url +"/"+ course_A.city_url
