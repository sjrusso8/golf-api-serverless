from django.db import models

from apps.core.models import TimestampedModel
from django.utils.translation import gettext_lazy as _

# Create your models here.


GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("N", "Prefer Not to Say")
)


class Profile(TimestampedModel):
    """User Profile

    A model that adds to the overall user model

    Define a Bio, Gender, Home Course, Favorite Course

    """
    user = models.OneToOneField("users.User", verbose_name=_(
        "User ID"), on_delete=models.CASCADE)

    bio = models.TextField(_("Personal Bio"), blank=True)

    gender = models.CharField(
        _("Gender"), choices=GENDER_CHOICES, max_length=50, default='N')

    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False
    )

    favorites = models.ManyToManyField(
        'api.Course',
        related_name='favorited_courses'
    )

    # home_course = models.ForeignKey(
    #     "api.Course", verbose_name=_("Home Course"), on_delete=models.DO_NOTHING, blank=True)

    # favorite_course = models.ForeignKey(
    #     "api.Course", verbose_name=_("Favorite"), on_delete=models.DO_NOTHING, blank=True)

    # TODO add in clubs

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profile")

    def __str__(self):
        return self.user.get_full_name()

    def follow(self, profile):
        """ Follow a profile """
        self.follows.add(profile)

    def unfollow(self, profile):
        """ unfollow a profile """
        self.follows.remove(profile)

    def is_following(self, profile):
        """ Check if we are already following a profile: Otherwise False """
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """ Check if profile is following us: Otherwise False """
        return self.followed_by.filter(pk=profile.pk).exists()

    def favorite(self, course):
        """ Favorite a Course """
        self.favorites.add(course)

    def unfavorite(self, course):
        """ Unfavorite a Course """
        self.favorites.remove(course)

    def has_favorited(self, course):
        """ Check if a Course has been favorited already: otherwise false """
        return self.favorites.filter(pk=course.pk).exists()
