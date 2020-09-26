from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from passlib.context import CryptContext
from tortoise.contrib.fastapi import HTTPNotFoundError
from datetime import datetime, timedelta

from src.models.models import Users
from src.schema.user import User_Pydantic, UserIn_Pydantic
from src.schema.token import Token, TokenData, Status
from src.auth.users import validate_user
from src.auth.jwthandler import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.get("/users", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.post("/register", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user.password = pwd_context.encrypt(user.password)
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get(
    "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.post(
    "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}, dependencies=[Depends(get_current_user)])
async def update_user(user_id: int, user: UserIn_Pydantic):
    db_user = await User_Pydantic.from_queryset_single(Users.get(id=user_id))
    if db_user.author.id == current_user.id:
        await Users.filter(id=user_id).update(**user.dict(exclude_unset=True))
        return await User_Pydantic.from_queryset_single(Users.get(id=user_id))
    raise HTTPException(status_code=403, detail=f"No authorization to update")

@router.delete("/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}}, dependencies=[Depends(get_current_user)])
async def delete_user(user_id: int):
    db_user = await User_Pydantic.from_queryset_single(Users.get(id=user_id))
    if db_user.author.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")
    raise HTTPException(status_code=403, detail=f"No authorization to delete")

@router.post("/login", response_model=Token)
async def login(user: HTTPBasicCredentials = Body(...)):
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
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User_Pydantic, dependencies=[Depends(get_current_user)])
async def read_users_me(current_user: User_Pydantic = Depends(get_current_user)):
    return current_user
