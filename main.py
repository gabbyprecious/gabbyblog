from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

Tortoise.init_models(["src.models.models"], "models")

from src.database.register import register_tortoise
import logging

from src.route import users, posts
from src.database.config import TORTOISE_ORM

app = FastAPI(title="Tortoise ORM FastAPI example")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(posts.router)


log = logging.getLogger(__name__)


register_tortoise(app,
                config= TORTOISE_ORM,
                generate_schemas=False)
        
