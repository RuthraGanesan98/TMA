from sqlalchemy.orm import Session

from models import Task, Project, User
from schemas import TaskCreate, TaskUpdate, TaskStatus, TaskType


def create_task(db: Session, task_data: TaskCreate, created_by: int):

    project = db.query(Project).filter(
        Project.id == task_data.project_id
    ).first()

    if not project:
        raise ValueError("Project not found")

    # Check whether assigned user exists
    assigned_user = db.query(User).filter(
        User.id == task_data.assigned_to
    ).first()

    if not assigned_user:
        raise ValueError("Assigned user not found")

    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        task_type=task_data.task_type,
        project_id=task_data.project_id,
        assigned_to=task_data.assigned_to,
        created_by=created_by
    )

    try:
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

    except Exception:
        db.rollback()
        raise

    return db_task

def update_task(
    db: Session,
    task_id: int,
    task_data: TaskUpdate
):
    # Find existing task
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        raise ValueError("Task not found")

    # Get only fields provided in request
    update_data = task_data.model_dump(exclude_unset=True)

    # Validate assigned user if assignment is changed
    if "assigned_to" in update_data:
        assigned_user = db.query(User).filter(
            User.id == update_data["assigned_to"]
        ).first()

        if not assigned_user:
            raise ValueError("Assigned user not found")

    # Update task fields
    for key, value in update_data.items():
        setattr(task, key, value)

    try:
        db.commit()
        db.refresh(task)

    except Exception:
        db.rollback()
        raise

    return task

def get_all_tasks(
    db: Session,
    project_id: int | None = None,
    assigned_to: int | None = None,
    status: TaskStatus | None = None,
    task_type: TaskType | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(Task)

    # Filter by project
    if project_id is not None:
        query = query.filter(Task.project_id == project_id)

    # Filter by assigned user
    if assigned_to is not None:
        query = query.filter(Task.assigned_to == assigned_to)

    # Filter by status
    if status is not None:
        query = query.filter(Task.status == status)

    # Filter by task type
    if task_type is not None:
        query = query.filter(Task.task_type == task_type)

    # Search by task title
    if search:
        query = query.filter(
            Task.title.ilike(f"%{search}%")
        )

    # Pagination
    return (
        query
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def delete_task(db: Session, task_id: int):

    # Find task
    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return None

    try:
        db.delete(task)
        db.commit()

    except Exception:
        db.rollback()
        raise

    return task