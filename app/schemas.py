from datetime import datetime
from enum import Enum, IntEnum
from pydantic import BaseModel, Field

class PriorityEnum(IntEnum):
    critical = 1
    very_important = 2
    important = 3
    normal = 4
    low = 5

class StatusEnum(IntEnum):
    work_in_progress = 1
    pending = 2
    blocked = 3
    done = 4

class SortEnum(str, Enum):
    created_at = "created_at"
    name =  "name"
    status = "status"
    priority = "priority"


class CreateTask(BaseModel):
    name: str = Field(..., min_length=1)
    description: str | None = None
    priority: PriorityEnum = PriorityEnum.normal
    status: StatusEnum = StatusEnum.work_in_progress


class Task(CreateTask):
    id: int
    created_at: datetime = datetime.now()
    class ConfigDict:
        from_attributes = True
    
