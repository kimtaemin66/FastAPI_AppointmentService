from fastapi import APIRouter, status, UploadFile, File
from sqlmodel import select
from appserver.apps.account.models import User
from appserver.apps.calendar.models import Calendar
from appserver.db import DbSessionDep
from appserver.apps.account.deps import CurrentUserOptionalDep
from .schemas import CalendarDetailOut, CalendarOut, CalendarUpdateIn, CalendarCreateIn
from .exception import CalendarNotFoundError, HostNotFoundError, CalendarAlreadyExistsError, GuestPermissionError
from sqlalchemy.exc import IntegrityError

from appserver.apps.account.deps import CurrentUserDep
from typing import Annotated

from .deps import UtcNow

router = APIRouter()

@router.get("/calendar/{host_username}", status_code=status.HTTP_200_OK)
async def host_calendar_detail(
    host_username: str,
    user: CurrentUserOptionalDep,
    session: DbSessionDep
) -> CalendarOut | CalendarDetailOut:
    stmt = select(User).where(User.username == host_username)
    result = await session.execute(stmt)
    host = result.scalar_one_or_none
    if host is None:
        raise HostNotFoundError()
    
    stmt = select((Calendar).where(Calendar.host_id) == host.id)
    result = await session.execute(stmt)
    calendar = result.scalar_one_or_none()
    if calendar is None:
        raise CalendarNotFoundError()
    
    if user is not None and user.id == host.id:
        return CalendarDetailOut.model_validate(calendar)
    
    return CalendarOut.model_validate(calendar)

@router.post(
    "/calendar",
    status_code=status.HTTP_201_CREATED,
    response_model=CalendarDetailOut,
)
async def create_calendar(
    user: CurrentUserDep,
    session: DbSessionDep,
    payload: CalendarCreateIn,
) -> CalendarDetailOut:
    calendar = Calendar(
        host_id=user.id,
        topics=payload.topics,
        description=payload.description,
        google_calendar_id=payload.google_calendar_id,
    )
    session.add(calendar)
    try:
        await session.commit()
    except IntegrityError as exc:
        raise CalendarAlreadyExistsError() from exc
    return calendar

@router.patch(
    "/calendar",
    status_code=status.HTTP_200_OK,
    response_model=CalendarDetailOut,
)

async def update_calendar(
    user: CurrentUserDep,
    session: DbSessionDep,
    payload: CalendarUpdateIn
) -> CalendarDetailOut:
    #호스트가 아니면 캘린더를 수정할 수 없다.
    if not user.is_host:
        raise GuestPermissionError()
    
    #사용자에게 캘린더가 없으면 HTTP 404 응답을 한다.
    if user.calendar is None:
        raise CalendarNotFoundError()
    
    #topics 값이 있으면 변경하고
    if payload.topics is not None:
        user.calendar.topics = payload.topics
    #description 값이 있으면 변경하고
    if payload.description is not None:
        user.calendar.description = payload.description
    #구글 캘린더 ID 값이 있으면 변경하고
    if payload.google_calendar_id is not None:
        user.calendar.google_calendar_id = payload.google_calendar_id
    
    #데이터베이스에 반영한다.
    await session.commit()
    
    return user.calendar

@router.post(
    "/bookings/{booking_id}/upload",
    status_code=status.HTTP_201_CREATED,
    response_model=BookingOut,
)
async def upload_booking_files(
    user: CurrentUserDep,
    booking_id: int,
    files: Annotated[list[UploadFile], File(min_length=1, max_length=3)],
    session: DbSessionDep,
    now: UtcNow
) -> BookingOut:
    stmt = (
        select(Booking)
        .where(Booking_id == booking_id)
        .where(Booking.guest_id == user.id)
    )
    result = await session.execute(stmt)
    booking = result.scalar_one_or_none()
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="예약 내역이 없습니다.")
    
    for file in files:
        session.add(BookingFile(booking_id=booking.id, file=file))
    await session.commit()
    await session.refresh(booking, ["files"])
    
    return booking