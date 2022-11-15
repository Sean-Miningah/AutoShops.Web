import graphene 
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations

from technician.schema import TechMutations, TechnicianQuery
from autouser.schema import AutoUserMutations


# Mutations

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.SendSecondaryEmailActivation.Field()

class Query(UserQuery, MeQuery, TechnicianQuery,graphene.ObjectType):
    pass


class Mutation(AuthMutation, TechMutations, AutoUserMutations, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)