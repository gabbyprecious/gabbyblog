from fastapi import APIRouter, Depends
from tortoise.contrib.fastapi import HTTPNotFoundError
from typing import List

from src.models.models import Posts
from src.schema.post import Post_Pydantic, PostIn_Pydantic
from src.schema.user import User_Pydantic
from src.schema.token import Status
from src.auth.jwthandler import get_current_user

router = APIRouter()

@router.get("/posts", response_model=List[Post_Pydantic], dependencies=[Depends(get_current_user)])
async def get_posts():
    return await Post_Pydantic.from_queryset(Posts.all())


@router.post("/post", response_model=Post_Pydantic, dependencies=[Depends(get_current_user)] )
async def create_post(post: PostIn_Pydantic, current_user: User_Pydantic = Depends(get_current_user)):
    post_dict = post.dict(exclude_unset=True)
    post_dict["author_id"] = current_user.id
    post_obj = await Posts.create(**post_dict)
    return await Post_Pydantic.from_tortoise_orm(post_obj)

@router.post(
    "/post/{post_id}", dependencies=[Depends(get_current_user)], response_model=Post_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_post(post_id: int, post: PostIn_Pydantic, current_user: User_Pydantic = Depends(get_current_user)):
    db_post = await Post_Pydantic.from_queryset_single(Posts.get(id=post_id))
    if db_post.author.id == current_user.id:
        await Posts.filter(id=post_id).update(**post.dict(exclude_unset=True))
        return await Post_Pydantic.from_queryset_single(Posts.get(id=post_id))
    raise HTTPException(status_code=403, detail=f"No authorization to update")

@router.delete("/post/{post_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}, dependencies=[Depends(get_current_user)])
async def delete_post(post_id: int):
    db_post = await Post_Pydantic.from_queryset_single(Posts.get(id=post_id))
    if db_post.author.id == current_user.id:
        deleted_count = await Post.filter(id=post_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
        return Status(message=f"Deleted post {post_id}")
    raise HTTPException(status_code=403, detail=f"No authorization to delete")