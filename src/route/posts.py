from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List

from src.models.models import Posts
from src.schema.post import Post_Pydantic, PostIn_Pydantic
from src.schema.user import User_Pydantic
from src.schema.token import Status
from src.auth.jwthandler import get_current_user

router = APIRouter()


@router.get(
    "/posts",
    response_model=List[Post_Pydantic],
    dependencies=[Depends(get_current_user)],
)
async def get_posts():
    return await Post_Pydantic.from_queryset(Posts.all())


@router.post(
    "/post", response_model=Post_Pydantic, dependencies=[Depends(get_current_user)]
)
async def create_post(
    post: PostIn_Pydantic, current_user: User_Pydantic = Depends(get_current_user)
):
    post_dict = post.dict(exclude_unset=True)
    post_dict["author_id"] = current_user.id
    post_obj = await Posts.create(**post_dict)
    return await Post_Pydantic.from_tortoise_orm(post_obj)
