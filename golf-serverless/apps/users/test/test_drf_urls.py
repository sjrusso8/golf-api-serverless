import pytest
from django.urls import resolve, reverse

from apps.users.models import User
from .factories import create_app_user

pytestmark = pytest.mark.django_db


@pytest.fixture
def user_A(db) -> User:
    return create_app_user(email="dummyemail@fakeremail.com")

def test_user_detail(user_A: User):
    assert resolve(f"/api/users/{user_A.pk}/").view_name == "users-detail"


def test_user_list():
    assert reverse("users-list") == "/api/users"
    assert resolve("/api/users/").view_name == "users-list"
