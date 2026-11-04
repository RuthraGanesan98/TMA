from sqlalchemy.orm import Session

from schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from models import Project

def create_project(db: Session, project:ProjectCreate) -> ProjectResponse:
    existing_project = (
            db.query(Project)
            .filter(
                (Project.name == project.name) 
            )
            .first()
        )
    if existing_project:
        if existing_project.name == project.name:
            raise ValueError("Project already exists")
    db_project = Project(
            name=project.name,
            description=project.description,
        )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def update_project(
    db: Session,
    project_id: int,
    project_data: ProjectUpdate
):
    # Find existing project
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        return None

    # Get only fields provided in request
    update_data = project_data.model_dump(exclude_unset=True)

    # Update project fields
    for key, value in update_data.items():
        setattr(project, key, value)

    try:
        db.commit()
        db.refresh(project)

    except Exception:
        db.rollback()
        raise

    return project

def get_projects(db: Session):
    return db.query(Project).order_by(
        Project.created_at.desc()
    ).all()


def get_project_by_id(db: Session, project_id: int):
    return db.query(Project).filter(
        Project.id == project_id
    ).first()