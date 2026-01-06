from sqladmin import ModelView
from .models import User, OAuthAccount
from datetime import datetime
import wtforms as wtf
from appserver.apps.account.utils import hash_password
from fastapi import Request
from typing import Any

class UserAdmin(ModelView, model=User):
    category = "계정"
    icon = "fa-solid fa-user"
    name = "사용자"
    name_plural = "사용자"
    column_list = [
        User.id,
        User.email,
        User.username,
        User.display_name,
        User.is_host,
        User.created_at,
        User.updated_at,
    ]
    column_searchable_list = [User.id, User.username, User.created_at]
    column_sortable_list = [
        User.id,
        User.email,
        User.username,
        User.created_at,
        User.updated_at,
    ]
    column_labels = {
        User.id: "ID",
        User.email: "이메일",
        User.username: "사용자 계정 ID",
        User.display_name: "표시 이름",
        User.is_host: "호스트 여부",
        User.created_at: "생성 일시",
        User.updated_at: "수정 일시",
    }
    column_default_sort = (User.created_at, True)
    
    form_columns = [
        User.email, 
        User.username, 
        User.display_name, 
        User.is_host, 
        User.hashed_password]
    
    form_overrides = {
        "email": wtf.EmailField,
    }
    column_type_formatters = {
        datetime: lambda m: m.strftime("%Y년 %m월 %d일 %H:%M:%S") if m else "-",
    }
    form_ajax_refs = {
        "calendar": {
            "fields": ["id", "description"],
            "order_by": "id",
        },
    }
    
    async def insert_model(self, request: Request, data: dict) -> Any:
        data["hashed_password"] = hash_password(data["hashed_password"])
        return await super().insert_model(request, data)
    
    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        async with self.session_maker() as session:
            obj: User = await session.get(User, pk)
            
        if obj.hashed_password != data["hashed_password"]:
            data["hashed_password"] = hash_password(data["hashed_password"])
        return await super().update_model(request, pk, data)

class OAuthAccountAdmin(ModelView, model=OAuthAccount):
    category = "계정"
    icon = "fa-solid fa-user"
    name = "소셜 계정"
    name_plural = "소셜 계정"
    column_list = [
        OAuthAccount.id,
        OAuthAccount.user,
        OAuthAccount.provider,
        OAuthAccount.provider_account_id,
        OAuthAccount.created_at,
        OAuthAccount.updated_at,
    ]
    column_searchable_list = [User.id, User.username, User.created_at]
    column_sortable_list = [
        User.id,
        User.email,
        User.username,
        User.created_at,
        User.updated_at,
    ]
    column_type_formatters = {
        datetime: lambda v: v.strftime("Y년 %m월 %d일 %H:%M:%S") if v else "-",
    }
    column_labels = {
        User.id: "사용자",
        User.email: "OAuth 제공자",
        User.username: "OAuth 제공자 계정 ID",
        User.display_name: "표시 이름",
        User.created_at: "생성 일시",
        User.updated_at: "수정 일시",
    }  
    form_columns = [OAuthAccount.user, OAuthAccount.provider, OAuthAccount.provider_account_id]
    form_ajax_refs = {
        "user": {
            "fields": ["id", "username"],
            "order_by": "id",
        },
    }