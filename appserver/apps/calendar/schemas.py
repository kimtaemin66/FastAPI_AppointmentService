from datetime import date, time
from pydantic import AwareDatetime, EmailStr, AfterValidator, model_validator
from sqlmodel import SQLModel, Field
from typing import Annotated
from appserver.libs.collections.sort import deduplicate_and_sort
from .enums import AttendanceStatus
from sqlmodel.main import SQLModelConfig
from fastapi_storages import StorageFile
from appserver.apps.account.schemas import UserOut

class CalendarOut(SQLModel):
    topics: list[str]
    description: str
    
class CalendarDetailOut(CalendarOut):
    host_id: int
    google_calendar_id: str
    created_at: AwareDatetime
    updated_at: AwareDatetime
    
Topics = Annotated[list[str], AfterValidator(deduplicate_and_sort)]

class CalendarCreateIn(SQLModel):
    topics: Topics = Field(min_length=1, description="게스트와 나눌 주제들")
    description: str = Field(min_length=1, description="게스트에게 보여 줄 설명")
    google_calendar_id: EmailStr = Field(description="Google Calendar ID")
    
class CalendarUpdateIn(SQLModel):
    topics: Topics | None = Field(
        default=None,
        min_length=1,
        description="게스트와 나눌 주제들",
    )
    description: str | None = Field(
        default=None,
        min_length=10,
        description="게스트에게 보여 줄 설명",
    )
    google_calendar_id: EmailStr | None = Field(
        default=None,
        min_length=20,
        description="Google Calendar ID", 
    )
class BookingFileOut(SQLModel):
    id: int
    file: StorageFile
    
    model_config = SQLModelConfig(
        arbitrary_types_allowed=True,
    )

class TimeSlotOut(SQLModel):
    id: int
    start_time: time
    end_time: time
    weekdays: list[int]
    created_at: AwareDatetime
    updated_at: AwareDatetime

class BookingOut(SQLModel):
    id: int
    when: date
    topic: str
    description: str
    time_slot: TimeSlotOut
    host: UserOut
    attendance_status: AttendanceStatus
    files: list[BookingFileOut]
    created_at: AwareDatetime
    updated_at: AwareDatetime

class SimpleBookingOut(SQLModel):
    id: int
    when: date
    time_slot: TimeSlotOut

class PaginatedBookingOut(SQLModel):
    bookings: list[BookingOut]
    total_count: int

def validate_weekdays(weekdays: list[int]) -> list[int]:
    weekday_range = range
    for weekday in weekdays:
        if weekday not in weekday_range:
            raise ValueError(f"요일 값은 0부터 6까지의 값이어야 합니다. 현재 값: {weekday}")
    
    return weekdays

Weekdays = Annotated[list[int], AfterValidator(validate_weekdays)]
class TimeSlotOut(SQLModel):
    start_time: time
    end_time: time
    weekdays: list[int]
    created_at: AwareDatetime
    updated_at: AwareDatetime

class TimeSlotCreateIn(SQLModel):
    start_time: time
    end_time: time
    weekdays: Weekdays
    
    @model_validator(mode="after")
    def validate_time_slot(self):
        if self.start_time >= self.end_time:
            raise ValueError("시작 시간은 종료 시간보다 빨라야 합니다.")
        return self
    
class BookingCreateIn(SQLModel):
    when: date
    topic: str
    description: str
    time_slot_id: int

class BookingOut(SQLModel):
    id: int
    when: date
    topic: str
    description: str
    time_slot: TimeSlotOut
    created_at: AwareDatetime
    updated_at: AwareDatetime
    
class HostBookingUpdateIn(SQLModel):
    when: date | None = Field(default=None, description="예약 일자")
    time_slot_id: int | None = Field(default=None, description="타임 슬롯 ID")