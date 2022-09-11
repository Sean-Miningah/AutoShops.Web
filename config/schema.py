import graphene 

from autouser.models import AutoUser
from autouser.types import AutoUserType

class Query(graphene.ObjectType):
    all_autousers = graphene.List(AutoUserType)

    def resolve_all_autousers(root, info):
        return AutoUser.objects.all()


schema = graphene.Schema(query=Query)