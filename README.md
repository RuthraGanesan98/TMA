# TMA – Task Manager Application

A simple Task Manager REST API built using **Python, FastAPI, SQLAlchemy, and MySQL**.

This project is designed to understand backend application development, CRUD operations, database relationships, API development, and database migrations.

## 1. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API development |
| MySQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Alembic | Database migrations |
| Pydantic | Request and response validation |
| bcrypt | Password hashing |
| Uvicorn | ASGI application server |

## 2. Project Features

### User Management
- Create/register users.
- Store password hashes instead of plain-text passwords.
- Validate unique usernames and email addresses.

### Project Management
- Create projects.
- Retrieve all projects.
- Retrieve project details by ID.
- Update existing projects.

### Task Management
- Create tasks under projects.
- Assign tasks to users.
- Update task details.
- Update task status.
- Retrieve all tasks.
- Filter tasks by project, assigned user, status, and task type.
- Search tasks by title.
- Support pagination.
- Delete tasks.

### Task Types

- EPIC
- STORY
- TASK
- BUG

### Task Statuses

- TODO
- IN_PROGRESS
- DONE

### Comments
- Comment model associated with tasks and users.
- Comment schemas prepared.
- Comment APIs are not implemented yet.

## 3. Database Structure

The application currently has four main tables.

### Users

| Column | Description |
|---|---|
| id | Primary key |
| username | Unique username |
| email | Unique email address |
| password_hash | Hashed password |
| created_at | Creation timestamp |
| updated_at | Last updated timestamp |

### Projects

| Column | Description |
|---|---|
| id | Primary key |
| name | Project name |
| description | Project description |
| owner_id | Foreign key referencing users |
| created_at | Creation timestamp |
| updated_at | Last updated timestamp |

### Tasks

| Column | Description |
|---|---|
| id | Primary key |
| title | Task title |
| description | Task description |
| task_type | EPIC, STORY, TASK, BUG |
| status | TODO, IN_PROGRESS, DONE |
| project_id | Foreign key referencing projects |
| assigned_to | Foreign key referencing users |
| created_by | Foreign key referencing users |
| created_at | Creation timestamp |
| updated_at | Last updated timestamp |

### Comments

| Column | Description |
|---|---|
| id | Primary key |
| content | Comment content |
| task_id | Foreign key referencing tasks |
| created_by | Foreign key referencing users |
| created_at | Creation timestamp |
| updated_at | Last updated timestamp |

## 4. API Documentation

Interactive API documentation is available through Swagger UI.

`http://localhost:8000/docs`

### User APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/users/` | Register a new user |

### Project APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/projects/` | Create a project |
| GET | `/projects/` | Retrieve all projects |
| GET | `/projects/{project_id}` | Retrieve project by ID |
| PUT | `/projects/{project_id}` | Update project |

### Task APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tasks/` | Create a task |
| GET | `/tasks/` | Retrieve all tasks |
| PATCH | `/tasks/{task_id}` | Update task |
| DELETE | `/tasks/{task_id}` | Delete task |

### Task Listing Filters

The task listing API supports the following query parameters:

| Parameter | Description | Example |
|---|---|---|
| project_id | Filter by project | `project_id=1` |
| assigned_to | Filter by assigned user | `assigned_to=2` |
| status | Filter by task status | `status=TODO` |
| task_type | Filter by task type | `task_type=BUG` |
| search | Search by task title | `search=login` |
| skip | Number of records to skip | `skip=0` |
| limit | Maximum records to return | `limit=10` |

Example:

`GET /tasks/?project_id=1&assigned_to=2&status=IN_PROGRESS&skip=0&limit=10`

## 5. Installation and Setup

### Prerequisites

- Python 3.10+
- MySQL 8+
- pip
- Virtual environment

### Clone the repository

```bash
git clone <repository-url>
cd TMA
```

### Create virtual environment

```bash
python -m venv venv
```

Activate the environment:

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pymysql alembic bcrypt email-validator
```

### Create MySQL database

```sql
CREATE DATABASE task_manager;
```

### Configure database connection

Update the MySQL connection URL in `database.py` or your environment configuration.

Example:

```text
mysql+pymysql://root:password@localhost:3306/tma
```

### Initialize and run migrations

```bash
alembic upgrade head
```

For future model changes:

```bash
alembic revision --autogenerate -m "migration description"
alembic upgrade head
```

### Start the application

```bash
uvicorn main:app --reload
```

Application URL:

`http://localhost:8000`

Swagger documentation:

`http://localhost:8000/docs`

## 6. Application Architecture

```text
                Client / Swagger UI
                         |
                         v
                    FastAPI
                         |
              +----------+----------+
              |                     |
              v                     v
           Routers               Schemas
              |
              v
             CRUD
              |
              v
           SQLAlchemy
              |
              v
             MySQL
```

Database migrations are managed separately through Alembic.

## 7. Project Structure

```text
TMA/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
│
├── crud/
│   ├── user.py
│   ├── project.py
│   └── task.py
│
├── routers/
│   ├── user.py
│   ├── project.py
│   └── task.py
│
├── utils/
│   └── security.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── alembic.ini
└── README.md
```


**Project:** TMA – Task Manager Application  
**Backend:** Python + FastAPI  
**Database:** MySQL  
**ORM:** SQLAlchemy  
**Migration Tool:** Alembic