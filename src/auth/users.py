from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.jwthandler import OAuth2PasswordBearerCookie
from passlib.context import CryptContext

from src.models.models import Users
from src.schema.user import User_Pydantic, UserIn_Pydantic, DB_User_Pydantic


security = OAuth2PasswordBearerCookie(tokenUrl="/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    return await DB_User_Pydantic.from_queryset_single(Users.get(username=username))


async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    db_user = await get_user(user.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return db_user
