from tortoise.contrib.pydantic import pydantic_model_creator

from src.models.models import Users

User_Pydantic = pydantic_model_creator(
    Users, name="UserOut", exclude=["password", "modified_at"]
)
DB_User_Pydantic = pydantic_model_creator(
    Users, name="User", exclude=["created_at", "modified_at"]
)
UserIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
