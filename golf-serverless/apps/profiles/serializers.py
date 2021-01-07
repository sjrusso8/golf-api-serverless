from django.http import request
from apps.profiles.models import Profile

from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    """Gather the data for the user profiles"""

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    bio = serializers.CharField(allow_blank=True, required=False)
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'gender', 'following',)

    def get_following(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        follower = request.user.profile
        followee = instance

        return follower.is_following(followee)
