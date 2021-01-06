import pytest

from apps.users.models import User
from .factories import create_app_user

pytestmark = pytest.mark.django_db

@pytest.fixture
def user_A(db) -> User:
    return create_app_user(email="dummyemail@fakeremail.com")

def test_user_model_methods(user_A: User):
    assert user_A.get_full_name() == "John Doe"
    assert user_A.get_short_name() == "Doe J."

def test_user_is_active(user_A: User):
    assert user_A.is_active == True

def test_user_is_staff(user_A: User):
    assert user_A.is_staff == False

def test_user_is_superuser(user_A: User):
    assert user_A.is_superuser == False
