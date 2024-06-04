import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.database import Base, engine
from src.graphql.mutations import Mutation
from src.graphql.queries import Query

Base.metadata.create_all(bind=engine)

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
