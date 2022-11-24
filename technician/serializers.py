from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.relations import SlugRelatedField

from technician.models import (SkillBadge, TechnicianDetails, Specialization, TechnicianSpecializations,
                               ShopFeedbackRating, Bookings)

User = get_user_model()


class RegisterTechnicianSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('is_technician')
        user = User(
            is_technician=True,
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'photo', 'email', 'password', 'is_technician',
        )
        extra_kwargs = {'password': {'write_only': True}}


class SkillBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillBadge
        fields = "__all__"


class TechnicianSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'photo', 'email', 'is_technician',
        )


class TechnicianLoginSerializer(serializers.ModelSerializer):
    autouser = TechnicianSerializer(read_only=True)
    shop_photo = serializers.ImageField(source='profile_picture')
    skill_badge = serializers.SlugRelatedField(read_only=True, slug_field='badge')

    class Meta:
        model = TechnicianDetails
        fields = (
            'id', 'autouser', 'lat', 'lng', 'region', 'shop_photo', 'shop_description', 'shop_goal', 'rating',
            'skill_badge'
        )


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class TechnicianSpecializationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicianSpecializations
        fields = "__all__"
        depth = 1


class ShopFeedbackRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopFeedbackRating
        fields = "__all__"
        depth = 1


class TechnicianReviewsSerializer(serializers.ModelSerializer):
    # reviewer_photo = serializers.SlugRelatedField(read_only, slug_field='auto')
    # reviewer = serializers.SerializerMethodField()


    # def get_reviewer(self, instance):
    #     return slugify(
    #         instance.technician.autouser.first_name + ' ' +instance.technician.autouser.last_name
    #     )
    #
    # def get_reviewer_photo(self, instance):
    #     return slugify(instance.technician.autouser.)

    autouser = TechnicianSerializer()

    class Meta:
        model = ShopFeedbackRating
        fields = ('id', 'autouser', 'description', 'rating', 'date', 'autouser')


class TechnicianDetailsSerializer(serializers.ModelSerializer):
    technician_specialization = TechnicianSpecializationsSerializer(many=True)
    technician_feedback = ShopFeedbackRatingSerializer(many=True, read_only=True)
    skill_badge = SkillBadgeSerializer()
    profile_picture = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = TechnicianDetails
        fields = "__all__"
        depth = 1


class TechnicianBookingsSerializer(serializers.ModelSerializer):
    auto_user = TechnicianSerializer()
    technician = TechnicianLoginSerializer()
    technician_description = serializers.CharField(allow_null=True)

    class Meta:
        model = Bookings
        fields = ('id', 'date', 'time', 'auto_user', 'technician', 'technician_description', 'autouser_description', 'status')
        extra_kwargs = {'autouser_description': {'read_only': True}}
        depth = 1


class AutoUserBookingsSerializer(serializers.ModelSerializer):
    technician = TechnicianLoginSerializer()

    class Meta:
        model = Bookings
        fields = ('id', 'date', 'time',
                  'auto_user', 'technician', 'technician_description', 'autouser_description', 'status')
        read_only_fields = ['technician_description', 'status']
        depth = 1


class TechnicianReviews(serializers.ModelSerializer):
    technician = TechnicianLoginSerializer()
    autouser = TechnicianSerializer()

    class Meta:
        model = ShopFeedbackRating
        fields = '__all__'


class BookingReportSerializer(serializers.ModelSerializer):
    customer_description = serializers.CharField(source="autouser_description")
    customer_email = serializers.SlugRelatedField(source="auto_user", read_only=True, slug_field="email")
    customer_first_name = serializers.SlugRelatedField(
        source="auto_user", read_only=True, slug_field="first_name")
    customer_last_name = serializers.SlugRelatedField(
        source="auto_user", read_only=True, slug_field="last_name")
    customer_phone_number = serializers.SlugRelatedField(
        source="auto_user", read_only=True, slug_field="phone_number"
    )

    class Meta:
        model = Bookings
        fields = (
            'id', 'date', 'time', 'status', 'technician_description', 'customer_description',
            'customer_email', 'customer_first_name', 'customer_last_name', 'customer_phone_number'
        )


class ReviewsReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopFeedbackRating
        fields = (
            'id', 'description', 'rating', 'date'
        )
