from django.shortcuts import render

from rest_framework import viewsets

from .serializers import ProfileSerializer
from .models import Profile
# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer
