from django.shortcuts import render
from django.db.models import Prefetch
from django.http import JsonResponse

from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.pagination import LimitOffsetPagination

from .mixins import MultipleFieldLookupMixin

from .serializers import *
from .models import Course, Tee
# Create your views here.


@permission_classes([IsAdminUser])
class AllCourseEditorViewSet(viewsets.ModelViewSet):
    """ Define an end point to edit the all Course Data

    - A Nested Serializer for api.GPSHole
    - A Double Nested Serailizer for api.Tee -> api.Hole

    - Purpose: To allow the coursescraper to post to a single end point 
    """
    gps_holes = GPSHole.objects.prefetch_related('course').all()
    tees = Tee.objects.prefetch_related('tee_holes').all()

    queryset = Course.objects.prefetch_related(
        Prefetch('gps_holes', queryset=gps_holes)).prefetch_related(
        Prefetch('tees', queryset=tees)).all()

    serializer_class = AllCourseDetailsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'city', 'state']


@permission_classes([IsAuthenticated])
class CourseLookupViewSet(generics.ListAPIView):
    """ Define an end point for a user search to for courses. Implemented within the Search Bar of the front end app """
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    filter_backends = [filters.SearchFilter]
    pagination_class = LimitOffsetPagination
    search_fields = ['name', 'city', 'state']


@permission_classes([IsAuthenticated])
class CourseDetailsViewSet(MultipleFieldLookupMixin,
                           generics.RetrieveAPIView):
    """ Define an end point to retrieve all course data as read_only

    Usage: once a user clicks on a searched course, the data is passed to this end point to update the front end

    """
    gps_holes = GPSHole.objects.prefetch_related('course').all()
    tees = Tee.objects.prefetch_related('tee_holes').all()

    queryset = Course.objects.prefetch_related(
        Prefetch('gps_holes', queryset=gps_holes)).prefetch_related(
        Prefetch('tees', queryset=tees)).all()

    serializer_class = AllCourseDetailsSerializer
    lookup_fields = ['id', 'name_url', 'city_url']


@permission_classes([IsAuthenticated])
class UserRoundDataViewSet(viewsets.ReadOnlyModelViewSet):
    """ Define an endpoint for a user to gather all round data

    - Usage: end point is used to track stats and round summaries
    """
    serializer_class = UserRoundSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=user.pk)


@permission_classes([IsAuthenticated])
class UserShotDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    """ Define an endpoint for a user to gather all round data

    - Usage: end point is used to track stats and round summaries
    """
    serializer_class = UserShotDetailsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=user.pk) # potentially update to self.request.user.pk or maybe id


@permission_classes([IsAuthenticated])
class UserPracticeViewSet(viewsets.ReadOnlyModelViewSet):
    """ Define an endpoint for a user to gather all practice data

    - Usage: end point is used to track practice data
    """
    serializer_class = UserPracticeDataSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PracticeData.objects.all()
        else:
            return PracticeData.objects.filter(user=user.pk)

def landing(request):
    data = {
        'message': 'Hello API',
        'is_active': True,
    }
    return JsonResponse(data)