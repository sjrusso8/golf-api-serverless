from rest_framework import viewsets

from .serializers import ProfileSerializer
from .models import Profile
class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(pk=user.pk)
