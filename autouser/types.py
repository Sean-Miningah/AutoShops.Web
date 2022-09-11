from graphene_django import DjangoObjectType
from autouser.models import AutoUser, AutoUserFavourite

class AutoUserType(DjangoObjectType):
    class Meta:
        model = AutoUser
        fields = '__all__'

class AutoUserFavouriteType(DjangoObjectType):
    class Meta:
        model = AutoUserFavourite
        fields = '__all__'