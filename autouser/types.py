from graphene_django import DjangoObjectType
from autouser.models import AutoUser

class AutoUserType(DjangoObjectType):
    class Meta:
        model = AutoUser
        fields = '__all__'