import pytest
from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from django.test import RequestFactory

from apps.users.models import User
from .factories import UserFactory
from apps.users.views import UserViewSet

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    """
    TODO:
        extracting view initialization code as class-scoped fixture
        would be great if only pytest-django supported non-function-scoped
        fixture db access -- this is a work-in-progress for now:
        https://github.com/pytest-dev/pytest-django/pull/258
    """

    def test_get_success_url(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/users/{user.username}/"

    def test_get_object(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserRedirectView:
    def test_get_redirect_url(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/users/{user.username}/"


class TestUserDetailView:
    def test_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory()

        response = UserViewSet(request, username=user.username)

        assert response.status_code == 200

    def test_not_authenticated(self, user: User, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()  # type: ignore

        response = UserViewSet(request, username=user.username)

        assert response.status_code == 302
        assert response.url == "/accounts/login/?next=/fake-url/"

    def test_case_sensitivity(self, rf: RequestFactory):
        request = rf.get("/fake-url/")
        request.user = UserFactory(username="UserName")

        with pytest.raises(Http404):
            UserViewSet(request, username="username")
