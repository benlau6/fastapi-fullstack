#from fastapi import APIRouter
#from starlette.graphql import GraphQLApp
#from graphene import ObjectType, String, Schema
#
#
#class Query(ObjectType):
#    # this defines a Field `hello` in our Schema with a single Argument `name`
#    hello = String(name=String(default_value="stranger"))
#    goodbye = String()
#
#    # our Resolver method takes the GraphQL context (root, info) as well as
#    # Argument (name) for the Field and returns data for the query Response
#    def resolve_hello(root, info, name):
#        return f'Hello {name}!'
#
#    def resolve_goodbye(root, info):
#        return 'See ya!'
#
#schema = Schema(query=Query)
#
#router = APIRouter()
#router.add_route('/', GraphQLApp(schema=schema))



from fastapi import APIRouter, Security
from starlette.requests import Request

from starlette.graphql import GraphQLApp
from graphene import ObjectType, String, Schema
from app import schemas
from app.api import deps


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'

schema = Schema(query=Query)

router = APIRouter()

graphql_app = GraphQLApp(schema=schema)

# https://github.com/tiangolo/fastapi/issues/1279
#@router.get("/gql")
#async def graphiql(request: Request, current_user: schemas.User = Security(deps.get_current_active_user, scopes=['me'])):
#    request._url = URL("/gql")
#    return await graphql.render_playground(request=request)

#@router.post('/gql')
#async def graphql(request: Request, current_user: schemas.User = Security(deps.get_current_active_user, scopes=['me'])):
#    request.state.dep = current_user
#    return await graphql_app.handle_graphql(request=request)