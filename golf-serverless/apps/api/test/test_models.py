import pytest
import json

from apps.api.models import Course
from .factories import create_app_course

pytestmark = pytest.mark.django_db

f = open('./apps/api/test/data/course.json')

data = json.load(f)

@pytest.fixture
def course_A(db) -> Course:
    return create_app_course(**data)

def test_course_model_methods(course_A: Course):
    assert course_A.city_url == "cincinnati"
    assert course_A.name_url == "tpc-reeves"