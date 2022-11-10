from rest_framework import serializers
from django.contrib.auth import get_user_model

from technician.models import (SkillBadge, TechnicianDetails, Specialization, TechnicianSpecializations,
                               ShopFeedbackRating,)

User = get_user_model()


class RegisterTechnicianSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')
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
            'first_name', 'last_name', 'photo', 'email', 'password', 'is_technician',
        )
        extra_kwargs = {'password': {'write_only': True}}


class SkillBadgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillBadge
        fields = "__all__"


class TechnicianSerializer(serializers.ModelSerializer):
    # secondary_details = TechnicianDetailsSerializer()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'photo', 'email', 'is_technician',
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


class TechnicianDetailsSerializer(serializers.ModelSerializer):
    technician_specialization = TechnicianSpecializationsSerializer(many=True)
    technician_feedback = ShopFeedbackRatingSerializer(many=True, read_only=True)
    skill_badge = SkillBadgeSerializer()

    class Meta:
        model = TechnicianDetails
        fields = "__all__"
        depth = 1
