from rest_framework import viewsets

from .serializers import ProfileSerializer
from .models import Profile
# Create your views here.


class ProfileViewSet(viewsets.ModelViewSet):
    # queryset = Profile.objects.select_related('user')
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(pk=user.pk)
