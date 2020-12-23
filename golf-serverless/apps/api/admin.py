from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import *

# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin Model for the :model:'api.Course'

    - List Display contains the fields to be displayed on the overview table
    - Fieldsets are broken down into 8 areas
        - ID, Details, Contact Info, Url, Hole Info, Ext Fields, Additional Info, and Admin Review

    """
    list_display = ['id', 'name', 'city', 'name_url', 'city_url']
    fieldsets = (
        (None, {
            "fields": (
                'id',
            ),
        }),
        ("Course Details", {
            "fields": (
                'name',
                'course_name',
                'description',
                'price',
                'fee',
            ),
        }),
        ("Course Contact Info", {
            "fields": (
                'phone',
                'website',
                'address',
                'streetaddress',
                'city',
                'state',
                'zip',
                'county',
                'lat',
                'lon'
            )
        }),
        ("Url", {
            "fields": (
                'name_url',
                'city_url',
            )
        }),
        ("Holes Info", {
            "fields": (
                'holes',
                'ext_holetype',
                'ext_cat',
                'ext_type',
                'ext_fips',
            )
        }),
        ("Ext Fields", {
            "fields": (
                'ext_fid',
                'ext_cid',
                'ext_company',
                'ext_course'
            )
        }),
        ("Additional Info", {
            "fields": (
                'opdate',
                'archname',
                'facility_id',
                'status',
                'whs_course_id'
            )
        }),
        ("Admin Review", {
            "fields": (
                "to_confirm",
                "tg_data_is_correct"
            )
        })
    )


@admin.register(Tee)
class TeeAdmin(admin.ModelAdmin):
    """
    Admin Model for :model:'api.Tee' and is related to :model:'api.Course' and :model:'api.Hole'

    - Contains the course and tees as the list display
    - A Tee needs to be associated with a course, color, rating, and slope

    """
    list_display = ['course', 'tees']
    fieldsets = (
        ("Course Info", {
            "fields": (
                'course',
                'tees',
            ),
        }),
        ("Course Rating/Slope", {
            "fields": (
                'rating',
                'slope',
            ),
        }),
    )


@admin.register(Hole)
class HoleAdmin(admin.ModelAdmin):
    """
    Hole Admin for :model:'api.Hole' and is associated with :model:'api.Tee' and :model:'api.RoundData'

    - Every Hole is associated with a tee, a hole number, a par, index, and distance
    - Exceptions are made for "IN" "OUT" and "TOT" which are the summary of front 9, back 9, and total 18

    """
    list_display = ['tee', 'hole']
    fieldsets = (
        ("Hole Details", {
            "fields": (
                'tee',
                'hole',
                'index',
                'par',
                'distance'
            ),
        }),
    )


@admin.register(GPSHole)
class GPSHoleAdmin(admin.ModelAdmin):
    """
    Admin Model for the :model:'api.GPSHole' and is associated with :model:'api.Course'

    - The GPS Hole model contains the lon and lat data for each hole on a course
    - This is maintained seperately from the Hole model because it is only for the 'tips'

    """

    list_display = ['course', 'id_map_element', 'hole']
    fieldsets = (
        (None, {
            "fields": (
                'course',
                'id_map_element',
                'id_type'
            ),
        }),
        ("GPS Data", {
            "fields": (
                'hole',
                'latitude',
                'longitude',
                'id_marker',
                'name',
                'description'
            )
        })
    )


class ShotDataPenaltiesInline(admin.TabularInline):
    """ This is created so that there is an inline form on the :model:'api.ShotData' """
    model = ShotDataPenalties


@admin.register(ShotData)
class ShotDataAdmin(admin.ModelAdmin):
    """
    Admin model for :model:'api.ShotData' and is associated with :model:'api.Rounds' and :model:'api.User'

    - This model also allows for import/export based on the resource class from the module django_import_export
    - Contains the inline form of the ShotData Penalties
    - Every shot is assicated with one user and one round

    """
    list_display = ['user', 'round_data', 'hole', 'nr_strokes']
    inlines = [ShotDataPenaltiesInline, ]
    fieldsets = (
        (None, {
            "fields": (
                'user',
            ),
        }),
        ("Round Details", {
            "fields": (
                'round_data',
                'hole',
            ),
        }),
        ("Shot Details", {
            "fields": (
                'nr_strokes',
                'nr_putts',
                'fairway_hit',
                'gir_flag',
                'putt_accuracy',
            ),
        }),
    )


@admin.register(RoundData)
class RoundDataAdmin(admin.ModelAdmin):
    """
    Model Admin for the :model:'api.RoundData' and is associated with :model:'users.User', :model:'api.Course;, and :model:'api.Tee'

    - Every Round is associated with one user, every round is played at one course, and that round is played from a selected course tee
    - Extra details are captured for the starting hole and round type (9f, 9b, or 18)
    """
    list_display = ['user', 'date', 'tees']
    fieldsets = (
        ("Round Data", {
            "fields": (
                'user',
                'date',
                'course',
                'tees',
                'starting_hole',
                'round_type'
            ),
        }),
    )


@admin.register(PracticeData)
class PracticeDataAdmin(admin.ModelAdmin):
    """
    Model Admin for the :model:'api.PracticeData' and is associated with :model:'users.User'

    - Currently just captures swing data
    """
    list_display = ['user', 'club', 'created_at']
    fieldsets = (
        ("Practice Info", {
            "fields": (
                'user',
                'club'
            ),
        }),
        ("Shot Data", {
            "fields": (
                'carry',
                'total',
                'swing_speed',
                'ball_speed',
                'launch_angle',
                'smash_factor',
                'apex',
                'spin_rate',
                'shot_shape'
            ),
        }),
    )
