import graphene 
from graphene_django import DjangoObjectType
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery 

from .models import AutoUser, AutoUserFavourite
from technician.models import TechnicianDetails, TechnicianSpecializations, Specialization
from .types import AutoUserFavouriteType, AutoUserType
from technician.types import TechnicianDetailType, TechnicianSpecializationsType, SpecializationType

class AutoUserQuery(graphene.ObjectType):
    autouser = graphene.List(AutoUserType)

class AutoUserFavouriteQuery(graphene.ObjectType):
    favourites = graphene.List(AutoUserFavouriteType)

    def resolve_favourites(root, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authenticated credentials were not provided")
        return AutoUserFavourite.objects.filter(auto_user=user)


# Mutations
class FavouriteInput(graphene.InputObjectType):
    id = graphene.ID()
    auto_user = graphene.ID()
    tech_id = graphene.ID()


class FavouriteTech(graphene.Mutation):
    class Arguments:
        favourite_data = FavouriteInput(required=True) 
    
    favourite = graphene.Field(AutoUserFavouriteType)

    def mutate(root, info, favourite_data=None):

        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Authenticated credentials required")

        tech = AutoUser.objects.get(id=favourite_data.tech_id, is_technician=True )
        # Search for pre-existing relationship 
        if_favoured = AutoUserFavourite.objects.filter(auto_user=user, technician=tech).exists()
        if if_favoured:
            raise Exception("Relationship already exists.")

        favourite_instance = AutoUserFavourite(
            auto_user = user, technician=tech, 
        )
        favourite_instance.save()
        return FavouriteTech(favourite=favourite_instance)


class AutoUserMutations(graphene.ObjectType):
    favourite_tech = FavouriteTech.Field()