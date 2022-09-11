import graphene 
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from autouser.models import AutoUser
from autouser.types import AutoUserType

class Query(graphene.ObjectType):
    all_autousers = graphene.List(AutoUserType)

    def resolve_all_autousers(root, info):
        return AutoUser.objects.all()

# Mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.SendSecondaryEmailActivation.Field()

class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)