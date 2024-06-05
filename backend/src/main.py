import strawberry
from fastapi import FastAPI
from starlette.websockets import WebSocket
from strawberry.fastapi import GraphQLRouter

from src.database import Base, engine
from src.graphql.mutations import Mutation
from src.graphql.queries import Query
from src.settings import add_cors_middleware
from src.websocket import websocket_endpoint

Base.metadata.create_all(bind=engine)

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()

# Graphql schema
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

# CORS middleware
add_cors_middleware(app)


@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)
