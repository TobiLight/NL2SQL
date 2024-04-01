#!/usr/bin/env python3
"""Init init"""

from fastapi import APIRouter
from app.routers.index import index_router as IndexRouter
from app.routers.auth import auth_router as AuthRouter
from app.routers.database import database_router as DatabaseRouter
from app.routers.query import query_router as QueryRouter
# from src.routers.product import seed_data_router as SeedRouter

api = APIRouter()
api.include_router(AuthRouter)
api.include_router(IndexRouter)
api.include_router(DatabaseRouter)
api.include_router(QueryRouter)
# api.include_router(ConversationRouter)
# api.include_router(SeedRouter)
__all__ = ["api"]
