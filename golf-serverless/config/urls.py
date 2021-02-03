from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.auth import logout


from apps.api import views
from apps.users.views import UserTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from config.api_router import api_router

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticatedOrReadOnly,),
)

urlpatterns = [
    path("", views.landing, name="landing_page"),
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
    # Swagger API Docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG == True:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
