from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import logout


from rest_framework.authtoken.views import obtain_auth_token
from apps.api import views
from apps.users.views import UserTokenObtainPairView

from rest_framework_simplejwt.views import TokenRefreshView


from config.api_router import api_router


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('logout/', logout, {'next_page': '/'}, name='logout'),

    # JWT Stuff
    path('api/token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

# API URLS
urlpatterns += [
    # API base url
    path("api/", include(api_router.urls)),
    path("api/courselookup",
         views.CourseLookupViewSet.as_view(), name='CourseLookup'),
    path("api/coursedetails/<id>/<name_url>/<city_url>/",
         views.CourseDetailsViewSet.as_view(), name='CourseDetails'),
]


if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
