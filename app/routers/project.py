from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from crud.project import create_project, update_project, get_project_by_id, get_projects


router = APIRouter(
    prefix="/projects",
    tags=["Project"]
)


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=201
)
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_project(db, project)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )



@router.put(
    "/{project_id}",
    response_model=ProjectResponse
)
def edit_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db)
):
    try:
        project = update_project(
            db,
            project_id,
            project_data
        )

        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )

        return project

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to update project"
        )

@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = get_project_by_id(db, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    return project

@router.get(
    "/",
    response_model=list[ProjectResponse]
)
def get_all_projects(
    db: Session = Depends(get_db)
):
    return get_projects(db)