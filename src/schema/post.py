from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.models import Posts

Post_Pydantic = pydantic_model_creator(Posts, name="Post", exclude = (["modified_at", "author.password", "author.created_at", "author.modified_at"]))
PostIn_Pydantic = pydantic_model_creator(Posts, name="PostIn",exclude=["author_id"], exclude_readonly=True)