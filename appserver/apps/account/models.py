from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, func, column, AutoString, String
from pydantic import EmailStr, AwareDatetime
from sqlalchemy import UniqueConstraint
from sqlalchemy_utc import UtcDateTime
from sqlalchemy.sql import func
from typing import TYPE_CHECKING, Union, Annotated
import random
import string
from pydantic import model_validator
from sqlmodel.main import SQLModelConfig
from sqlalchemy.ext.hybrid import hybrid_property
from .enums import AccountStatus

if TYPE_CHECKING:
    from appserver.apps.calendar.models import Calendar, Booking

class User(SQLModel, table=True):
    __tablename__="users" # 테이블 이름 지정
    __table_args__= (
        UniqueConstraint(
            "email", 
            name="uq_email"
        ), # Field의 unique 옵션을 사용하지않고 고유값 제약을 설정. name은 해당 고유값 제약의 이름
    )
    
    id: int = Field(default=None, primary_key=True) # 기본키 id, 데이터를 가져오기 전에는 None값이 Default
    username: str = Field(min_length=4, max_length=40, description="사용자 계정 ID") # 속성(Field) 선언부 unique 옵션으로 고유값 설정
    email: EmailStr = Field(unique=True, max_length=128, description="사용자 이메일")
    display_name: str = Field(min_length=4, max_length=40, description="사용자 표시 이름")
    hashed_password: str = Field(min_length=8, max_length=128, description="사용자 비밀번호")
    is_host: bool = Field(default=False, description="사용자가 호스트인지 여부")
    status: AccountStatus = Field(
        default=AccountStatus.ACTIVE.value,
        description="사용자 상태",
        sa_type=String,
    )
    # 자료형 각주에서 자료형을 문자열로 표기하면 해당 자료형을 지연 평가함. 이를 문자열 각주 혹은 전방 참조라고 함. 아직 정의되지않은 자료형을 참조할 때 사용
    oauth_accounts: list["OAuthAccount"] = Relationship(back_populates="user")
    calendar: Union["Calendar", None] = Relationship(
        back_populates="host",
        sa_relationship_kwargs={"uselist": False, "single_parent": True, "lazy": "joined"} # uselist = 관계의 다중성 여부
    )
    
    bookings: list["Booking"] = Relationship(back_populates="guest")
    
    created_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )
    
    updated_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )

    model_config = SQLModelConfig(
        ignored_types=(hybrid_property,),
    )

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"

    @hybrid_property
    def is_active(self) -> bool:
        return self.status in [AccountStatus.ACTIVE, AccountStatus.ACTIVE.value]

    @is_active.expression
    def is_active(cls) -> bool:
        statuses = [AccountStatus.ACTIVE.value]
        return cls.status.in_(statuses)

    @hybrid_property
    def is_deleted(self) -> bool:
        return self.status in [AccountStatus.DELETED, AccountStatus.DELETED.value]

    @is_deleted.expression
    def is_deleted(cls) -> bool:
        statuses = [AccountStatus.DELETED.value]
        return cls.status.in_(statuses)


class OAuthAccount(SQLModel, table=True):
    __tablename__="oauth_accounts"
    __table_args__= (
        UniqueConstraint(
           "provider", 
            "provider_account_id", 
            name="uq_provider_provider_account_id"
        ),
    )
    
    id: int = Field(default=None, primary_key=True)
    
    provider: str = Field(max_length=10, description="OAuth 제공자")
    provider_account_id: str = Field(max_length=128, description="OAuth 제공자 계정 ID")
    
    user_id: int = Field(foreign_key="users.id") # 외래키 지정
    user: User = Relationship(back_populates="oauth_accounts") # OAuthAccount 모델의 user 필드가 User 모델을 가리키도록 지정
    
    created_at: datetime 
    updated_at: datetime

    created_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
        },
    )

    updated_at: AwareDatetime = Field(
        default=None,
        nullable=False,
        sa_type=UtcDateTime,
        sa_column_kwargs={
            "server_default": func.now(),
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )
    def __str__(self) -> str:
        return f"{self.username} ({self.email})"