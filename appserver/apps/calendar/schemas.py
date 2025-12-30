from datetime import date
from pydantic import AwareDatetime, EmailStr, AfterValidator
from sqlmodel import SQLModel, Field
from typing import Annotated
from appserver.libs.collections.sort import deduplicate_and_sort
from .enums import AttendanceStatus
from sqlmodel.main import SQLModelConfig
from fastapi_storages import StorageFile

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

class BookingOut(SQLModel):
    id: int
    when: date
    topic: str
    description: str
    time_slot: TimeSlotOut
    attendance_status: AttendanceStatus
    files: list[BookingFileOut]
    created_at: AwareDatetime
    updated_at: AwareDatetime