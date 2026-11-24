# TaskFlow — Team Task Management REST API

A backend REST API developed using **Python, Django, and Django REST Framework** for managing team projects and tasks securely.

TaskFlow supports JWT authentication, project ownership, role-based access control, task management, filtering, searching, pagination, and interactive API documentation.

## Features

- **JWT Authentication:** Secure API authentication using access and refresh tokens.
- **Project Management:** Create projects and retrieve projects owned by the authenticated user.
- **Role-Based Access Control:** Manager and Member roles for project-level task permissions.
- **Task Management:** Create, view, update, assign, and delete tasks.
- **Task Status:** To Do, In Progress, and Done.
- **Task Priority:** Low, Medium, High, and Urgent.
- **Filtering:** Filter tasks by status, priority, project, and assigned user.
- **Searching:** Search tasks by title and description.
- **Pagination:** Paginated task listing.
- **Swagger Documentation:** Interactive API documentation.
- **Automated Testing:** API authentication, permissions, and validation tests.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| Django REST Framework | REST API development |
| Simple JWT | JWT authentication |
| django-filter | API filtering |
| drf-spectacular | Swagger/OpenAPI documentation |
| SQLite | Local development database (if configured) |
| Postman | API testing |
| Git & GitHub | Version control |

## Project Structure

```text
TaskFlow/
├── accounts/
├── projects/
├── tasks/
├── notifications/
├── config/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/Rupeshpatil99/taskflow-django-rest-api.git
cd taskflow-django-rest-api/TaskFlow
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

**3. Activate the environment (Windows)**

```powershell
.\.venv\Scripts\Activate.ps1
```

**4. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**5. Apply migrations**

```bash
python manage.py migrate
```

**6. Start the development server**

```bash
python manage.py runserver
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/token/` | Obtain JWT tokens |
| POST | `/api/token/refresh/` | Refresh access token |
| GET | `/api/projects/` | List owned projects |
| POST | `/api/projects/` | Create project |
| GET | `/api/tasks/` | List accessible tasks |
| POST | `/api/tasks/` | Create task |
| GET | `/api/tasks/{id}/` | Retrieve task |
| PATCH | `/api/tasks/{id}/` | Partially update task |
| PUT | `/api/tasks/{id}/` | Update task |
| DELETE | `/api/tasks/{id}/` | Delete task |

## Filtering and Searching

```http
GET /api/tasks/?status=todo
GET /api/tasks/?priority=high
GET /api/tasks/?search=TaskFlow
GET /api/tasks/?page=1
```

## API Documentation

Run the Django server and open:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI Schema: `http://127.0.0.1:8000/api/schema/`

## Automated Testing

Run all automated tests:

```bash
python manage.py test
```

## Future Enhancements

- Task assignment notifications
- Project member management APIs
- React frontend dashboard
- Production deployment using cloud infrastructure
- CI/CD integration

## Author

**Rupesh Patil**

GitHub: [Rupeshpatil99](https://github.com/Rupeshpatil99)
