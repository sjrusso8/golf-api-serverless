from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import *
from apps.users.serializers import UserSerializer
from apps.users.models import User

'''
Creation of the various Serializers for the GOLF Project

'''


class CourseListSerializer(serializers.ModelSerializer):
    """ Additional model to add the ability to search on a read-only """
    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'city',
            'state',
            'name_url',
            'city_url',
        )


class CourseHolesSerializer(serializers.ModelSerializer):
    """ This feeds into the CourseTeesSerializer """
    class Meta:
        model = Hole
        fields = (
            'hole',
            'index',
            'par',
            'distance',
        )


class CourseTeesSerializer(serializers.ModelSerializer):
    """ This is used in the AllCourseDetailsSerializer """
    tee_holes = CourseHolesSerializer(many=True)

    class Meta:
        model = Tee
        fields = (
            'tees',
            'rating',
            'slope',
            'tee_holes',
        )


class GPSHoleSerializer(serializers.ModelSerializer):
    """ This is used in the AllCourseDetailsSerializer """
    class Meta:
        model = GPSHole
        fields = (
            'id_map_element',
            'hole',
            'latitude',
            'longitud',
            'id_marker',
            'id_type',
            'name',
            'image',
            'description'
        )


class AllCourseDetailsSerializer(serializers.ModelSerializer):
    """ A serializer that contains all of the course details

    - Nest Relations for GPSHole, and Tee
    - Nested Relation for Tee -> Hole
    """
    gps_holes = GPSHoleSerializer(many=True)
    tees = CourseTeesSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'name',
            'course_name',
            'address',
            'phone',
            'website',
            'description',
            'price',
            'ext_fid',
            'ext_cid',
            'ext_company',
            'ext_course',
            'city',
            'state',
            'zip',
            'streetaddress',
            'county',
            'lat',
            'lon',
            'holes',
            'ext_holetype',
            'ext_cat',
            'ext_type',
            'ext_fips',
            'opdate',
            'archname',
            'fee',
            'facility_id',
            'status',
            'whs_course_id',
            'to_confirm',
            'tg_data_is_correct',
            'season_start',
            'season_end',
            'gps_holes',
            'tees'
        )

    def create(self, validated_data):
        """Custom create method to accept nest json"""
        gps_holes = validated_data.pop('gps_holes')
        tees = validated_data.pop('tees')
        course = Course.objects.create(**validated_data)

        for hole in gps_holes:
            GPSHole.objects.create(course=course, **hole)

        for tee in tees:
            tee_holes = tee.pop('tee_holes')
            course_tee = Tee.objects.create(course=course, **tee)
            for hole in tee_holes:
                Hole.objects.create(tee=course_tee, **hole)

        return course


class ShotDataPenaltiesSerializer(serializers.ModelSerializer):
    """ serializer for Shot Data Penalties. Feeds into ShotDataSerializer """
    class Meta:
        model = ShotDataPenalties
        fields = (
            'penalties',
        )


class ShotDataSerializer(serializers.ModelSerializer):
    """ Serializer for ShotData and feds into RoundDataSerializer """

    shot_penalties = ShotDataPenaltiesSerializer(many=True)

    class Meta:
        model = ShotData
        fields = (
            'nr_strokes',
            'nr_putts',
            'fairway_hit',
            'gir_flag',
            'putt_accuracy',
            'nr_strokes',
            'shot_penalties',
        )


class HoleDataSerializer(CourseHolesSerializer):
    """ Holes Serializer that feed into Tee_holes """
    shots = ShotDataSerializer(many=True)

    class Meta:
        model = Hole
        fields = (
            'hole',
            'index',
            'par',
            'distance',
            'shots',
        )


class TeeDataSerializer(CourseTeesSerializer):
    """ Tee_holes feeds into Rounds """
    tee_holes = HoleDataSerializer(many=True)

    class Meta:
        model = Tee
        fields = (
            'tees',
            'rating',
            'slope',
            'tee_holes',
        )


class RoundDetailSerializer(serializers.ModelSerializer):
    """ Shot by Shot Details of the round data """

    tees = TeeDataSerializer()

    class Meta:
        model = RoundData
        fields = (
            'date',
            'course',
            'round_type',
            'starting_hole',
            'tees',
        )


class RoundSummarySerializer(serializers.ModelSerializer):
    """
    Round Summary contains all of the stats for a round by User

    The stats call the overall model methods:
        - Total Score for a round
        - Total Putts for a round
        - Scoring average by hole par
        - Total percentages for fairways/greens/putts

    """
    score_total = serializers.SerializerMethodField()
    putts_total = serializers.SerializerMethodField()
    par3s_average = serializers.SerializerMethodField()
    par4s_average = serializers.SerializerMethodField()
    par5s_average = serializers.SerializerMethodField()
    pars_percent = serializers.SerializerMethodField()
    birdie_or_better_percent = serializers.SerializerMethodField()
    bogey_percent = serializers.SerializerMethodField()
    double_bogey_percent = serializers.SerializerMethodField()
    triple_bogey_or_worse_percent = serializers.SerializerMethodField()
    fairways_hit_percent = serializers.SerializerMethodField()
    fairways_long_percent = serializers.SerializerMethodField()
    fairways_short_percent = serializers.SerializerMethodField()
    fairways_left_percent = serializers.SerializerMethodField()
    fairways_right_percent = serializers.SerializerMethodField()
    fairways_shank_percent = serializers.SerializerMethodField()
    approach_gir_percent = serializers.SerializerMethodField()
    approach_long_percent = serializers.SerializerMethodField()
    approach_short_percent = serializers.SerializerMethodField()
    approach_left_percent = serializers.SerializerMethodField()
    approach_right_percent = serializers.SerializerMethodField()
    approach_shank_percent = serializers.SerializerMethodField()
    putts_hit_percent = serializers.SerializerMethodField()
    putts_long_percent = serializers.SerializerMethodField()
    putts_short_percent = serializers.SerializerMethodField()
    putts_left_percent = serializers.SerializerMethodField()
    putts_right_percent = serializers.SerializerMethodField()
    putts_shank_percent = serializers.SerializerMethodField()

    class Meta:
        model = RoundData
        fields = (
            'date',
            'course',
            'round_type',
            'starting_hole',
            'score_total',
            'putts_total',
            'par3s_average',
            'par4s_average',
            'par5s_average',
            'pars_percent',
            'birdie_or_better_percent',
            'bogey_percent',
            'double_bogey_percent',
            'triple_bogey_or_worse_percent',
            'fairways_hit_percent',
            'fairways_long_percent',
            'fairways_short_percent',
            'fairways_left_percent',
            'fairways_right_percent',
            'fairways_shank_percent',
            'approach_gir_percent',
            'approach_long_percent',
            'approach_short_percent',
            'approach_left_percent',
            'approach_right_percent',
            'approach_shank_percent',
            'putts_hit_percent',
            'putts_long_percent',
            'putts_short_percent',
            'putts_left_percent',
            'putts_right_percent',
            'putts_shank_percent',
        )

    def get_score_total(self, obj):
        return obj.get_score_total()

    def get_putts_total(self, obj):
        return obj.get_putts_total()

    def get_par3s_average(self, obj):
        return obj.get_hole_average(3)

    def get_par4s_average(self, obj):
        return obj.get_hole_average(4)

    def get_par5s_average(self, obj):
        return obj.get_hole_average(5)

    def get_pars_percent(self, obj):
        return obj.get_score_percent('par')

    def get_birdie_or_better_percent(self, obj):
        return obj.get_score_percent('birdie_better')

    def get_bogey_percent(self, obj):
        return obj.get_score_percent(1)

    def get_double_bogey_percent(self, obj):
        return obj.get_score_percent(2)

    def get_triple_bogey_or_worse_percent(self, obj):
        return obj.get_score_percent('tbogey_worse')

    def get_fairways_hit_percent(self, obj):
        return obj.get_hit_percent('fairway', 'HT')

    def get_fairways_long_percent(self, obj):
        return obj.get_hit_percent('fairway', 'LO')

    def get_fairways_short_percent(self, obj):
        return obj.get_hit_percent('fairway', 'SH')

    def get_fairways_left_percent(self, obj):
        return obj.get_hit_percent('fairway', 'LT')

    def get_fairways_right_percent(self, obj):
        return obj.get_hit_percent('fairway', 'RT')

    def get_fairways_shank_percent(self, obj):
        return obj.get_hit_percent('fairway', 'SK')

    def get_approach_gir_percent(self, obj):
        return obj.get_hit_percent('approach', 'HT')

    def get_approach_long_percent(self, obj):
        return obj.get_hit_percent('approach', 'LO')

    def get_approach_short_percent(self, obj):
        return obj.get_hit_percent('approach', 'SH')

    def get_approach_left_percent(self, obj):
        return obj.get_hit_percent('approach', 'LT')

    def get_approach_right_percent(self, obj):
        return obj.get_hit_percent('approach', 'RT')

    def get_approach_shank_percent(self, obj):
        return obj.get_hit_percent('approach', 'SK')

    def get_putts_hit_percent(self, obj):
        return obj.get_hit_percent('putts', 'HT')

    def get_putts_long_percent(self, obj):
        return obj.get_hit_percent('putts', 'LO')

    def get_putts_short_percent(self, obj):
        return obj.get_hit_percent('putts', 'SH')

    def get_putts_left_percent(self, obj):
        return obj.get_hit_percent('putts', 'LT')

    def get_putts_right_percent(self, obj):
        return obj.get_hit_percent('putts', 'RT')

    def get_putts_shank_percent(self, obj):
        return obj.get_hit_percent('putts', 'SK')


class UserRoundSerializer(serializers.ModelSerializer):
    """
    Contains the specific Rounds for each user and all of the data
    """
    user_rounds = RoundSummarySerializer(many=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'user_rounds',
        )


class UserShotDetailsSerializer(serializers.ModelSerializer):
    """
    Contains the specific Rounds for each user and all of the data
    """
    user_rounds = RoundDetailSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'user_rounds',
        )


class UserPracticeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticeData
        fields = '__all__'
