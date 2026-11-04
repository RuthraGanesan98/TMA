from fastapi import FastAPI
from routers.user import router as user_router
from routers.project import router as project_router
from routers.tasks import router as task_router

app = FastAPI(title="TMA", description="Task Manager Application")

app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)


