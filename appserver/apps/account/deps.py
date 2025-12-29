from typing import Annotated
from datetime import datetime, timezone, timedelta
from sqlmodel import select
from fastapi import Depends, Cookie, HTTPException, status
from appserver.db import DbSessionDep
from .exceptions import InvalidTokenError, ExpiredTokenError
from .models import User
from .utils import decode_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .exceptions import InvalidTokenError, ExpiredTokenError, UserNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user(auth_token: str | None, db_session: AsyncSession) -> User | None:
    if not auth_token:
        return None
    
    try:
        decoded = decode_token(auth_token)
    except Exception as e:
        raise InvalidTokenError() from e
    
    expires_at = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    now = datetime.now(timezone.utc)
    if now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) < expires_at:
        raise ExpiredTokenError()
    
    stmt = select(User).where(User.username == decoded["sub"])
    result = await db_session.execute(stmt)
    
    return result.scalar_one_or_none()

async def get_current_user(
    auth_token: Annotated[str, Cookie(...)],
    db_session: DbSessionDep,
):
    user = await get_user(auth_token, db_session)
    
    # if auth_token is None:
    #     raise InvalidTokenError()
    
    # try:
    #     decoded = decode_token(auth_token)
    # except Exception as e:
    #     raise InvalidTokenError() from e
    
    # expires_at = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    # now = datetime.now(timezone.utc)
    # if now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) < expires_at:
    #     raise ExpiredTokenError()
    
    # stmt = select(User).where(User.username == decoded["sub"])
    # result = await db_session.execute(stmt)
    # user = result.scalar_one_or_none()
    
    if user in None:
        raise UserNotFoundError()
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]

async def get_current_user_optional(
    db_session: DbSessionDep,
    auth_token: Annotated[str | None, Cookie()] = None,
):
    user = await get_user(auth_token, db_session)
    return user

CurrentUserOptionalDep = Annotated[User | None, Depends(get_current_user_optional)]