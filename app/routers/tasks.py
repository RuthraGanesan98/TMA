from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas import TaskCreate, TaskResponse, TaskStatus, TaskType, TaskUpdate
from crud.tasks import create_task, update_task, get_all_tasks, delete_task


router = APIRouter(
    prefix="/tasks",
    tags=["Task"]
)

@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    try:
        # Temporary: use user ID 1 as creator
        created_by = 1

        return create_task(
            db=db,
            task_data=task_data,
            created_by=created_by
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create task"
        )

@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
def edit_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    try:
        return update_task(
            db=db,
            task_id=task_id,
            task_data=task_data
        )

    except ValueError as e:
        message = str(e)

        error_status = (
            status.HTTP_404_NOT_FOUND
            if message in ["Task not found", "Assigned user not found"]
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=error_status,
            detail=message
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update task"
        )    

@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    project_id: int | None = None,
    assigned_to: int | None = None,
    status: TaskStatus | None = None,
    task_type: TaskType | None = None,
    search: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        return get_all_tasks(
            db=db,
            project_id=project_id,
            assigned_to=assigned_to,
            status=status,
            task_type=task_type,
            search=search,
            skip=skip,
            limit=limit
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve tasks"
        )    

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def remove_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    try:
        task = delete_task(
            db=db,
            task_id=task_id
        )

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return {
            "message": "Task deleted successfully",
            "task_id": task_id
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to delete task"
        )    