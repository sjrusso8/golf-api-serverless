from django.db import models
from django.db.models import Sum, Avg, F
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimestampedModel
from apps.core.utils import ROUND_TYPE, SHOT_SHAPE, OUTCOME, GENERIC_CLUBS, PENALTIES

# Create your models here.


class Course(TimestampedModel):
    """
    Stores a single course entry contained all of the details. 

    Related to :model:'api.Tee', :model:'api.GPSHole', and :model:'api.RoundData'

    The Course Model is primarily fed via the 'course_scraper' spider, coursespider_v3

    - On Save, the city_url and name_url are created via the slugify argument
    - Model is represented by the ID and Course Name
    """

    id = models.IntegerField(_("Course ID"), primary_key=True)

    # Generic Address / Info
    name = models.CharField(_("Course Name"), db_index=True, max_length=250)
    course_name = models.CharField(
        _("Course Type"), max_length=250, blank=True, null=True)
    address = models.CharField(
        _("Course Address"), max_length=250, blank=True, null=True)
    phone = models.CharField(
        _("Course Phone Number"), max_length=250, blank=True, null=True)
    website = models.CharField(
        _("Course Website"), max_length=250, blank=True, null=True)
    description = models.CharField(
        _("Descripton"), max_length=1025, blank=True, null=True)
    price = models.PositiveIntegerField(
        _("Course Price"), blank=True, null=True)

    # ext info
    ext_fid = models.CharField(
        _("ext_fid"), max_length=250, blank=True, null=True)
    ext_cid = models.CharField(
        _("ext_cid"), max_length=250, blank=True, null=True)
    ext_company = models.CharField(
        _("ext_company"), max_length=250, blank=True, null=True)
    ext_course = models.CharField(
        _("ext_course"), max_length=250, blank=True, null=True)

    # detailed address data
    city = models.CharField(_("Course City"), max_length=250)
    state = models.CharField(_("Course State"), db_index=True, max_length=100)
    zip = models.CharField(_("Zip Code"), max_length=250)
    streetaddress = models.CharField(
        _("Street Address"), max_length=250, blank=True, null=True)
    county = models.CharField(
        _("County"), max_length=250, blank=True, null=True)

    # Positional data
    lat = models.DecimalField(
        _("Tee Latitude"), max_digits=25, decimal_places=20, blank=True, null=True)
    lon = models.DecimalField(
        _("Tee Longitude"), max_digits=25, decimal_places=20, blank=True, null=True)

    # Holes data
    holes = models.PositiveIntegerField(_("Holes"), blank=True, null=True)
    ext_holetype = models.CharField(
        _("ext_holetype"), max_length=50, blank=True, null=True)
    ext_cat = models.CharField(
        _("ext_cat"), max_length=50, blank=True, null=True)
    ext_type = models.CharField(
        _("ext_type"), max_length=50, blank=True, null=True)
    ext_fips = models.CharField(
        _("ext_fips"), max_length=50, blank=True, null=True)

    # Additional Data
    opdate = models.CharField(
        _("opdate"), max_length=25, blank=True, null=True)
    archname = models.CharField(
        _("archname"), max_length=250, blank=True, null=True)
    fee = models.PositiveIntegerField(
        _("Course Fee"), blank=True, null=True)
    facility_id = models.CharField(
        _("Facility ID"), max_length=25, blank=True, null=True)
    status = models.CharField(
        _("Course Fee"), max_length=10, blank=True, null=True)
    whs_course_id = models.CharField(
        _("whs_course_id"), max_length=25, blank=True, null=True)

    # admin confirmation
    to_confirm = models.CharField(
        _("To be Confirmed"), max_length=10, blank=True, null=True)
    tg_data_is_correct = models.CharField(
        _("Course Data is Correct"), max_length=10, blank=True, null=True)

    name_url = models.SlugField(
        _("Course Name Url"), max_length=100, db_index=True, unique=True)

    city_url = models.SlugField(_("City Url"), db_index=True)

    # Additional fields
    season_start = models.CharField(
        _("Season Start"), max_length=10, blank=True, null=True)
    season_end = models.CharField(
        _("Season End"), max_length=10, blank=True, null=True)
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return f"{self.id} - {self.name}"

    def save(self, *args, **kwargs):
        self.name_url = slugify(self.name)
        self.city_url = slugify(self.city)
        super(Course, self).save(*args, **kwargs)


class Tee(TimestampedModel):
    """
    Stores the many Tees related to :model:'api.Course' and the many holes in :model:'api.Hole'

    Every Tee has:
        - One Course -> char
        - One rating -> decimal
        - One slope -> int
        - Many holes -> relational key to Hole model
    """

    course = models.ForeignKey("api.Course", verbose_name=_(
        "Course"), on_delete=models.CASCADE, related_name="tees")
    tees = models.CharField(_("Tee Color"), max_length=50)
    rating = models.DecimalField(_("Rating"), max_digits=5, decimal_places=2)
    slope = models.PositiveIntegerField(_("Slope"))

    class Meta:
        verbose_name = _("Tee")
        verbose_name_plural = _("Tees")

    def __str__(self):
        return f"{self.course} - {self.tees}"


class Hole(TimestampedModel):
    """
    Stores the many Holes associated with one :model:'api.Tee' on one :model:'api.Course'

    Holes are also related to :model:'api.ShotData' so that a user can track their shots on each hole

    Every Hole has:
        - Tee -> foreign key to :model:'api.Tee'
        - Hole number -> Char / (1 - 18) or In/Out/Total)
        - Index -> positive int / 1-18 or blank
        - Par -> positive int / 3,4,5
        - Distance -> positive int
        - One hole has any shots -> related to :model:'api.ShotData
    """

    tee = models.ForeignKey("api.Tee", verbose_name=_(
        "Tee"), on_delete=models.CASCADE, related_name='tee_holes')
    hole = models.CharField(_("Hole Number"), max_length=15)
    index = models.PositiveIntegerField(_("Hole Index"), blank=True, null=True)
    par = models.PositiveIntegerField(_("Hole Par"))
    distance = models.PositiveIntegerField(_("Distance"))

    class Meta:
        verbose_name = _("Holes")
        verbose_name_plural = _("Holes")

    def __str__(self):
        return f"{self.tee} - {self.hole}"


class GPSHole(TimestampedModel):
    """
    Contains the GPS Hole coordinates for :model:'api.Course'

    This is only one set of GPSHoles per course as the lon and lat distances are judged by the farthest tees

    Every GPSHole has:
        - A Course -> foreign key to :model:'api.Course'
        - id_map_element -> positive int 
        - hole -> positive int 
        - latitude -> coordinates
        - longitud -> coordinates
        - id_marker -> id for fields (id_type, name, image, description)
        - name -> classification of the id_market (teebox, fairway, etc.)
        - image -> char field of the image name (fairway.png)
        - description -> description of the name/image
    """

    course = models.ForeignKey("api.Course", verbose_name=_(
        "Course"), on_delete=models.CASCADE, related_name="gps_holes")

    id_map_element = models.IntegerField(_("Hole Map ID"), primary_key=True)

    hole = models.CharField(_("Hole Number"), max_length=15)
    latitude = models.DecimalField(
        _("Tee Latitude"), max_digits=25, decimal_places=20, blank=True, null=True)
    longitud = models.DecimalField(
        _("Tee Longitude"), max_digits=25, decimal_places=20, blank=True, null=True)

    id_marker = models.CharField(
        _("ID Marker"), max_length=50, blank=True, null=True)
    id_type = models.CharField(
        _("ID Type"), max_length=50)

    name = models.CharField(
        _("Name Category"), max_length=50, blank=True, null=True)
    image = models.CharField(_("GPS Helper Image"),
                             max_length=50, blank=True, null=True)
    description = models.CharField(
        _("Description"), max_length=250, blank=True, null=True)

    class Meta:
        verbose_name = _("GPS Hole Data")
        verbose_name_plural = _("GPS Hole Data")

    def __str__(self):
        return f"{self.course} - {self.hole}"


class ShotData(TimestampedModel):
    """
    Contains the user Shot Data for each hole.  Related to :model:'api.Hole', :model:'api.RoundData', and :model:'users.User'

    Every Shot has the following:
        - user -> foreign key to :model:'users.User'
        - round_data -> foreign key to :model:'api.RoundData'
        - hole -> foreign key to :model:'api.Hole'
        - nr_strokes -> int: number of strokes
        - nr_putts -> int: number of putts
        - fairway_hit -> char choice field
        - gir_flag -> char choice field
        - putt_accuracy -> char choice field

    #TODO create a exception notice so that nr_putts and not be greater than nr_strokes
    """
    user = models.ForeignKey("users.User", verbose_name=_(
        "Player"), on_delete=models.DO_NOTHING)

    round_data = models.ForeignKey("api.RoundData", verbose_name=_(
        "Round Information"), on_delete=models.DO_NOTHING, default=4)

    hole = models.ForeignKey("api.Hole", verbose_name=_(
        "Course Hole"), on_delete=models.DO_NOTHING, related_name='shots')

    nr_strokes = models.PositiveIntegerField(_("Number of Strokes"))

    nr_putts = models.PositiveIntegerField(
        _("Number of Putts"), null=True, blank=True)

    fairway_hit = models.CharField(_("Fairway Accuracy"), max_length=50, choices=OUTCOME,
                                   help_text='Fairway Accuracy', null=True, blank=True)

    gir_flag = models.CharField(_("Green Accuracy"), max_length=50, choices=OUTCOME,
                                help_text='Green Accuracy', null=True, blank=True)

    putt_accuracy = models.CharField(_("Putt Accuracy"), max_length=50, choices=OUTCOME,
                                     help_text='Putt Accuracy', null=True, blank=True)

    class Meta:
        verbose_name = _("Shot Data")
        verbose_name_plural = _("Shot Data")

    def __str__(self):
        return f"{self.hole}"


class ShotDataPenalties(TimestampedModel):
    """
    Contains a simple model for any penalties accured during the round
    Related to :model:'api.ShotData'

    - Penalties is a choice field
    """

    shot = models.ForeignKey("api.ShotData", verbose_name=_(
        "Shot Penalties"), on_delete=models.CASCADE, related_name="shot_penalties")

    penalties = models.CharField(_("Penalties"), max_length=50, choices=PENALTIES,
                                 help_text='Penalties', null=True, blank=True)

    class Meta:
        verbose_name = _("Shot Data Penalties")
        verbose_name_plural = _("Shot Data Penalties")

    def __str__(self):
        return f"{self.penalties}"


class RoundData(TimestampedModel):
    """
    Contains the Round Data for a user.  Related to :model:'users.User', :model:'api.Course', :model:'api.Tee', and a reverse relation to :model:'api.Holes'

    Round data has the following:
        - user -> related field to :model:'users.User'. This is the player
        - course -> relates to :model:'api.Course'
        - tees -> relates to the selected :model:'api.Tee' for the course
        - starting_hole -> int / 1 - 18
        - round_type -> char / 18, Front 9 or Back 9
    Methods:
        - The methods on the model gather stats about the round for the API
        - Total Score for a round
        - Total Putts for a round
        - Scoring average by hole par
        - Total percentages for fairways/greens/putts
    """

    user = models.ForeignKey("users.User", verbose_name=_(
        "Player"), on_delete=models.DO_NOTHING, related_name='user_rounds')
    date = models.DateTimeField(
        _("Date Played"), auto_now=False, auto_now_add=False)
    course = models.ForeignKey("api.Course", verbose_name=_(
        "Course Played"), on_delete=models.DO_NOTHING)
    tees = models.ForeignKey("api.Tee", verbose_name=_("Course Tees"),
                             on_delete=models.CASCADE)
    starting_hole = models.PositiveIntegerField(_("Starting Hole"))
    round_type = models.CharField(
        _("Round"), choices=ROUND_TYPE, max_length=50)

    class Meta:
        verbose_name = _("Round Data")
        verbose_name_plural = _("Round Data")

    def __str__(self):
        return f"{self.user} - {str(self.round_type)}"

    def get_score_total(self):
        return RoundData.objects.prefetch_related('shotdata').aggregate(Sum("shotdata__nr_strokes"))['shotdata__nr_strokes__sum']

    def get_putts_total(self):
        return RoundData.objects.prefetch_related('shotdata').aggregate(Sum("shotdata__nr_putts"))['shotdata__nr_putts__sum']

    def get_hole_average(self, num):
        return RoundData.objects.prefetch_related('shotdata').select_related('shotdata').filter(shotdata__hole__par=num).aggregate(Avg("shotdata__nr_strokes"))['shotdata__nr_strokes__avg']

    def get_score_percent(self, value):
        """
        get_score_percent takes 4 values and returns the percent of that value per round.

        - The prefetch_related queryset is predefined to same on duplicate code
        - The number of holes is defined by the round data of which the user selects either 9 or 18

        - Args:
            [value]: options: 
                        - 'par': The percent of which the nr_strokes on a hole is same as the hole par
                        - 'birdie_better': The percent of which the nr_strokes on a hole is less than the hole par
                        - 'tbogey_worse': The percent of which the nr_strokes on a hole is 3 more or greater than the hole par
                        - 'int': a number that is evaulated to get the precent of nr_strokes over the hole par.  this finds the bogeys and dbogeys basically

        - Returns:
            [int]: a percentage of the inputted value per round
        """
        qs_related = RoundData.objects.prefetch_related(
            'shotdata').select_related('shotdata')

        round_holes = int(self.round_type)

        if value == 'par':
            return round((qs_related.filter(shotdata__nr_strokes=F('shotdata__hole__par')).count()/round_holes), 2)
        if value == 'birdie_better':
            return round((qs_related.filter(shotdata__nr_strokes__lt=F('shotdata__hole__par')).count()/round_holes), 2)
        if value == 'tbogey_worse':
            return round((qs_related.filter(shotdata__nr_strokes__gte=F('shotdata__hole__par')+3).count()/round_holes), 2)
        if isinstance(value, int):
            return round((qs_related.filter(shotdata__nr_strokes=F('shotdata__hole__par') + value).count()/round_holes), 2)

    def get_hit_percent(self, area, value):
        """
        get_hit_percent takes 2 args and returns the percent of that 'hit' occurance per round

        - Total fairways is based on the number of par3's play in a round minus the total number of holes played

        - Args:
            [area]: options: 
                - 'fairway': The percent of which each 'choice' field occurs in a round based on the field 'fairway_hit'
                - 'approach': The percent of which each 'choice' field occurs in a round based on the field 'gir_flag'
                - 'putts': The percent of which each 'choice' field occurs in a round based on the field 'putt_accuracy'
            [value]: choice:
                - only accepts the values from the 'choice' field specificed in the model

        - Returns:
            [int]: percentage 
                - Based on the each choice field
        """
        qs_related = RoundData.objects.prefetch_related(
            'shotdata').select_related('shotdata')

        round_holes = int(self.round_type)

        if area == 'fairway':
            total_fairways = (int(self.round_type) -
                              qs_related.filter(shotdata__hole__par=3).count())

            return round(qs_related.filter(shotdata__fairway_hit=value).count()/total_fairways, 2)

        if area == 'approach':
            return round(qs_related.filter(shotdata__gir_flag=value).count()/round_holes, 2)

        if area == 'putts':
            return round(qs_related.filter(shotdata__putt_accuracy=value).count()/round_holes, 2)


class PracticeData(TimestampedModel):
    """
    This model captures practice data on club distances for each :model:'users.User'

    all captured by the SC200

    Each practice sessions has:
        - A user -> relates to :model:'users.User'
        - club -> int / club selection
        - carry -> int
        - total -> int
        - swing_speed -> int
        - ball_speed -> int
        - smash_factor -> int (it's a function of swing speed and ball speed)
        - shot_shape -> char
    """

    user = models.ForeignKey("users.User", verbose_name=_(
        "Player"), on_delete=models.DO_NOTHING)
    club = models.CharField(_("Club"), choices=GENERIC_CLUBS, max_length=50)
    carry = models.PositiveIntegerField(
        _("Carry Distance (yds)"), blank=True, null=True)
    total = models.PositiveIntegerField(
        _("Total Distance (yds)"), blank=True, null=True)
    swing_speed = models.PositiveIntegerField(
        _("Swing Speed (mph)"), blank=True, null=True)
    ball_speed = models.PositiveIntegerField(
        _("Ball Speed (mph)"), blank=True, null=True)
    launch_angle = models.DecimalField(
        _("Launch Angle (deg)"), max_digits=10, decimal_places=2, blank=True, null=True)
    smash_factor = models.DecimalField(
        _("Smash Factor"), max_digits=10, decimal_places=2, blank=True, null=True)
    apex = models.DecimalField(
        _("Apex (ft)"), max_digits=10, decimal_places=2, blank=True, null=True)
    spin_rate = models.PositiveIntegerField(
        _("Spin Rate (rpm)"), blank=True, null=True)
    shot_shape = models.CharField(
        _("Shot Shape"), choices=SHOT_SHAPE, max_length=50)

    class Meta:
        verbose_name = _("Practice Data")
        verbose_name_plural = _("Practice Data")

    def __str__(self):
        return f"{self.user} - {self.club}"

    def save(self, *args, **kwargs):
        self.smash_factor = (self.ball_speed / self.swing_speed)
        super(PracticeData, self).save(*args, **kwargs)
