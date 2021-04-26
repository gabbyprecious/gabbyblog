from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2, OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from tortoise.contrib.fastapi import HTTPNotFoundError
from datetime import datetime, timedelta

from src.models.models import Users
from src.schema.user import User_Pydantic, UserIn_Pydantic
from src.schema.token import Token, TokenData, Status
from src.auth.users import validate_user
from src.auth.jwthandler import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.post("/register", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user.password = pwd_context.encrypt(user.password)
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.delete(
    "/user/{user_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_user(
    user_id: int, current_user: User_Pydantic = Depends(get_current_user)
):
    db_user = await User_Pydantic.from_queryset_single(Users.get(id=user_id))
    if db_user.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")
    raise HTTPException(status_code=403, detail=f"No authorization to delete")


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    db_user = await validate_user(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You've sucessfully logged in"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="None",
        secure=True,
    )
    return response
