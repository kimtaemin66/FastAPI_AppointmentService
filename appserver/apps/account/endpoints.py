from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, SQLModel
from appserver.db import create_async_engine, create_session
from .models import User
from appserver.db import DbSessionDep

router = APIRouter(prefix="/account")

@router.get("/users/{username}")
async def user_detail(username: str, session: DbSessionDep) -> User:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if user is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/signup")
async def signup(payload: dict, session: DbSessionDep) -> User:
    user = User.model_validate(payload)
    session.add(user)
    await session.commit()
    return user