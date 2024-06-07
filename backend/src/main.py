import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.database import Base, engine
from src.graphql.mutations import Mutation
from src.graphql.queries import Query
from src.settings import add_cors_middleware
from src.utils.context import get_context
from src.websocket.endpoints import websocket_endpoint

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware
add_cors_middleware(app)

# GraphQL router with the schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

# WebSocket endpoint
app.websocket("/ws")(websocket_endpoint)
