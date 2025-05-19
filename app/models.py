from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
import uuid

class User(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    fullname = fields.CharField(max_length=255, null=True)
    password_hash = fields.CharField(max_length=255)
    refresh_token = fields.CharField(max_length=255, null=True)
    refresh_token_exp = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username

# Pydantic models for API
User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)