from django.conf import settings
from apps.users.views import UserViewSet
from apps.profiles.views import ProfileViewSet
# from apps.api.views import RoundDataViewSet, ShotDataViewSet, TeeViewSet, HoleViewSet, CourseDataViewSet, CourseDetailsViewSet
from apps.api.views import UserRoundDataViewSet, UserShotDetailsViewSet, UserPracticeViewSet, AllCourseEditorViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

if settings.DEBUG:
    api_router = DefaultRouter()
else:
    api_router = SimpleRouter()

# Settings
api_router.trailing_slash = '/?'

# Users API
api_router.register(r'users', UserViewSet, basename='users')
api_router.register(r'profiles', ProfileViewSet, basename='profiles')
api_router.register(r'users_rounds', UserRoundDataViewSet,
                    basename='users_rounds')
api_router.register(r'users_shots', UserShotDetailsViewSet,
                    basename='users_shots')
api_router.register(r'course_details_editor', AllCourseEditorViewSet,
                    basename='course_details_editor')
api_router.register(r'users_practice', UserPracticeViewSet,
                    basename="users_practice")

app_name = "api"
urlpatterns = api_router.urls
