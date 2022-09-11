from graphene_django.types import DjangoObjectType
from .models import (SkillBadge, TechnicianDetails, TechnicianSpecializations, Specialization,
    ShopFeedbackRating)


class TechnicianDetailType(DjangoObjectType):
    class Meta: 
        model = TechnicianDetails
        fields = '__all__'

class TechnicianSpecializationsType(DjangoObjectType):

    class Meta:
        model = TechnicianSpecializations
        filds = "__all__"

class SpecializationType(DjangoObjectType):
    class Meta:
        model = Specialization
        fields = '__all__'

class SkillBadgeType(DjangoObjectType):
    class Meta: 
        model = SkillBadge
        fields = '__all__'

class ShopFeedbackRatingType(DjangoObjectType):
    class Meta: 
        model = ShopFeedbackRating
        fields = '__all__'
