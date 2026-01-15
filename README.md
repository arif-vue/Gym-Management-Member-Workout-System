# Gym Management & Member Workout System

A backend REST API for managing gym branches, trainers, members, and workout plans using Django + Django REST Framework.

## Features

- **Multi-branch gym management**
- **Role-based access control** (Admin, Manager, Trainer, Member)
- **JWT authentication** (access + refresh tokens)
- **Workout plan and task management**
- **Branch-level data isolation**

## Tech Stack

- Python 3.x
- Django 
- Django REST Framework
- Simple JWT

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gym-management
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/auth/login/` | Login | Public |
| POST | `/api/auth/refresh-token/` | Refresh token | Public |
| GET | `/api/auth/profile/` | Get profile | Authenticated |

### Users
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/auth/users/` | List users | Admin, Manager |
| POST | `/api/auth/users/` | Create user | Admin, Manager |

### Gym Branches
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/branches/` | List branches | Admin |
| POST | `/api/branches/` | Create branch | Admin |

### Workout Plans
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/workouts/plans/` | List plans | Admin, Manager, Trainer |
| POST | `/api/workouts/plans/` | Create plan | Trainer |

### Workout Tasks
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/workouts/tasks/` | List tasks | All (filtered by role) |
| POST | `/api/workouts/tasks/` | Assign task | Trainer |
| PATCH | `/api/workouts/tasks/<id>/` | Update status | Trainer, Member |

## User Roles

| Role | Permissions |
|------|-------------|
| **Admin** | Full access to all data across branches |
| **Manager** | Manage users and view workouts in their branch |
| **Trainer** | Create workout plans, assign/update tasks in their branch |
| **Member** | View and update their own assigned tasks |

## Business Rules

- Max 3 trainers per branch
- Trainer can only assign tasks to members in their branch
- Member can only update their own tasks
- Manager can only create users for their branch
- Member cannot view workout plans directly
- Admin bypasses all branch restrictions

## Project Structure

```
gym_management/
├── authentications/     # User authentication & management
├── branches/           # Gym branch management
├── workouts/           # Workout plans & tasks
├── gym_management/     # Project settings
├── manage.py
├── requirements.txt
└── README.md
```

## Testing with Postman

### Login
```json
POST /api/auth/login/
{
    "email": "admin@gym.com",
    "password": "admin123"
}
```

### Create Branch
```json
POST /api/branches/
Headers: Authorization: Bearer <token>
{
    "name": "Downtown Fitness",
    "location": "123 Main Street"
}
```

### Create User
```json
POST /api/auth/users/
Headers: Authorization: Bearer <token>
{
    "email": "trainer@gym.com",
    "password": "password123",
    "role": "trainer",
    "gym_branch_id": 1
}
```

### Create Workout Plan
```json
POST /api/workouts/plans/
Headers: Authorization: Bearer <trainer_token>
{
    "title": "Strength Training",
    "description": "4-week strength program"
}
```

### Assign Task
```json
POST /api/workouts/tasks/
Headers: Authorization: Bearer <trainer_token>
{
    "workout_plan_id": 1,
    "member_id": 4,
    "status": "pending",
    "due_date": "2026-01-20"
}
```

### Update Task Status
```json
PATCH /api/workouts/tasks/1/
Headers: Authorization: Bearer <token>
{
    "status": "completed"
}
```

## License

MIT License
