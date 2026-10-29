# TaskFlow — Team Task Management REST API

TaskFlow is a backend REST API built with Django REST Framework to manage projects and team tasks. It includes JWT authentication, role-based permissions, task filtering, searching, pagination, and interactive Swagger documentation.

## Features

- User authentication using JSON Web Tokens (JWT)
- Project creation and ownership management
- Project membership with Manager and Member roles
- Task creation, retrieval, updating, and deletion
- Role-based access control for task operations
- Filtering tasks by status, priority, project, and assignee
- Search tasks by title and description
- Pagination for task lists
- Interactive Swagger API documentation
- Automated API and permission tests

## Tech Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- django-filter
- drf-spectacular
- SQLite for local development (if configured)

## Project Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/taskflow-django-rest-api.git
cd taskflow-django-rest-api
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create an administrator account

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/projects/` | List owned projects |
| POST | `/api/projects/` | Create a project |
| GET | `/api/tasks/` | List accessible tasks |
| POST | `/api/tasks/` | Create a task |
| GET | `/api/tasks/{id}/` | Retrieve a task |
| PATCH | `/api/tasks/{id}/` | Partially update a task |
| PUT | `/api/tasks/{id}/` | Update a task |
| DELETE | `/api/tasks/{id}/` | Delete a task |
| POST | `/api/token/` | Obtain JWT tokens |
| POST | `/api/token/refresh/` | Refresh an access token |

## API Documentation

After starting the server, open:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- Schema: `http://127.0.0.1:8000/api/schema/`
- Django Admin: `http://127.0.0.1:8000/admin/`

## Filtering, Searching, and Pagination

Examples:

```text
/api/tasks/?status=todo
/api/tasks/?priority=high
/api/tasks/?search=TaskFlow
/api/tasks/?page=1
```

You can combine filters and search parameters.

## Running Tests

Run all discovered Django tests:

```bash
python manage.py test
```

Run task-specific tests:

```bash
python manage.py test tasks
```

Run project-specific tests:

```bash
python manage.py test projects
```

## Security Notes

- Do not commit passwords, access tokens, refresh tokens, or environment secrets.
- Keep production secrets in environment variables.
- Configure production database settings and secure deployment settings before hosting the API.

## Future Improvements

- Notification system for task assignments and status changes
- Additional project membership management endpoints
- Production deployment
- Expanded automated test coverage

## Author

Rupesh Patil

GitHub: https://github.com/Rupeshpatil99