from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TaskType(str, Enum):
    EPIC = "EPIC"
    STORY = "STORY"
    TASK = "TASK"
    BUG = "BUG"


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


# -----------------
# User
# -----------------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------
# Project
# -----------------

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# -----------------
# Task
# -----------------

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    task_type: TaskType
    project_id: int
    assigned_to: int


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    task_type: TaskType | None = None
    status: TaskStatus | None = None
    assigned_to: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    task_type: TaskType
    status: TaskStatus
    project_id: int
    assigned_to: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    task_id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)