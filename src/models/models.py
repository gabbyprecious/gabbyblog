from datetime import datetime, timezone

now = datetime.now(timezone.utc)

from tortoise import Tortoise, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Users(models.Model):
    """
    The User model
    """

    id = fields.IntField(pk=True)
    #: This is a username
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)


class Posts(models.Model):
    """
    The Post model
    """

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=225)
    write_up = fields.TextField()
    author = fields.ForeignKeyField("models.Users", related_name="post")
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}, {self.author_id} on {self.created_at}"
