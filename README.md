# Gym Management & Member Workout System

A backend REST API for managing gym branches, trainers, members, and workout plans using Django + Django REST Framework.

---

## 🔑 Test Credentials

| Role | Email | Password |
|------|-------|----------|
| **Admin** | admin@gym.com | gym@7890 |
| **Manager** | manager@gym.com | gym@7890 |
| **Trainer** | trainer@gym.com | gym@7890 |
| **Member** | member@gym.com | gym@7890 |

---

## 🌐 Hosted API Base URL

```
https://your-deployed-url.com/api/
```

> Replace with your actual deployed URL (e.g., Heroku, Railway, Render, etc.)

---

## ✨ Features

- **Multi-branch gym management**
- **Role-based access control** (Admin, Manager, Trainer, Member)
- **JWT authentication** (access + refresh tokens)
- **Workout plan and task management**
- **Branch-level data isolation**
- **Pagination support**

---

## 🛠 Tech Stack

- Python 3.x
- Django 6
- Django REST Framework
- Simple JWT

---

## 🚀 Project Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd gym-management
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create superuser (Admin)
```bash
python manage.py createsuperuser
```
Enter email, password when prompted.

### 6. Run the development server
```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000/`

---

## 👥 Roles & Permissions

| Role | Permissions |
|------|-------------|
| **Admin** | Full access to all data across all branches. Can create branches, managers, trainers, members. Can create workout plans for any branch. |
| **Manager** | Can view and create users (trainers/members) in their own branch only. Can view workout plans in their branch. Cannot create workout plans. |
| **Trainer** | Can create workout plans for their branch. Can assign workout tasks to members in their branch. Can update task status. |
| **Member** | Can view their own profile and assigned tasks only. Can update status of their own tasks. |

### Business Rules
- Maximum **3 trainers** per branch
- Trainer can only assign tasks to members **in their branch**
- Member can only update **their own tasks**
- Manager can only create users **for their branch**
- Member **cannot view** workout plans directly
- Admin **bypasses all** branch restrictions

---

## 📁 Project Structure

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

---

## 📋 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/auth/login/` | User login | Public |
| POST | `/api/auth/refresh-token/` | Refresh JWT token | Public |
| GET | `/api/auth/profile/` | Get current user profile | Authenticated |

### User Management Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/auth/users/` | List all users | Admin, Manager |
| POST | `/api/auth/users/` | Create new user | Admin, Manager |

### Branch Management Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/branches/` | List all branches | Admin |
| POST | `/api/branches/` | Create new branch | Admin |

### Workout Plan Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/workouts/plans/` | List workout plans | Admin, Manager, Trainer |
| POST | `/api/workouts/plans/` | Create workout plan | Admin, Trainer |

### Workout Task Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/workouts/tasks/` | List workout tasks | All (filtered by role) |
| POST | `/api/workouts/tasks/` | Assign task to member | Admin, Trainer |
| PATCH | `/api/workouts/tasks/<id>/` | Update task status | Trainer, Member (own task) |

---

## 🧪 API Testing Guide (with JSON examples)

### 🔐 1. Login

**Endpoint:** `POST /api/auth/login/`

**Request:**
```json
{
    "email": "admin@gym.com",
    "password": "admin123"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 🔄 2. Refresh Token

**Endpoint:** `POST /api/auth/refresh-token/`

**Request:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 👤 3. Get Profile

**Endpoint:** `GET /api/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Profile fetched successfully",
    "data": {
        "id": 1,
        "email": "admin@gym.com",
        "role": "admin",
        "gym_branch": null,
        "created_at": "2026-01-15T14:50:00.000000Z"
    }
}
```

---

### 🏢 4. Create Branch (Admin Only)

**Endpoint:** `POST /api/branches/`

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Request:**
```json
{
    "name": "Downtown Fitness",
    "location": "123 Main Street, New York"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Gym branch created successfully",
    "data": {
        "id": 1,
        "name": "Downtown Fitness",
        "location": "123 Main Street, New York",
        "created_at": "2026-01-15T14:53:52.791227Z"
    }
}
```

---

### 📋 5. List Branches (Admin Only)

**Endpoint:** `GET /api/branches/`

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Response (200 OK):**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Downtown Fitness",
            "location": "123 Main Street, New York",
            "created_at": "2026-01-15T14:53:52.791227Z"
        }
    ]
}
```

---

### 👤 6. Create Manager (Admin Only)

**Endpoint:** `POST /api/auth/users/`

**Headers:**
```
Authorization: Bearer <admin_token>
```

**Request:**
```json
{
    "email": "manager@gym.com",
    "password": "password123",
    "role": "manager",
    "gym_branch_id": 1
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "User created successfully",
    "data": {
        "id": 2,
        "email": "manager@gym.com",
        "role": "manager",
        "gym_branch": {
            "id": 1,
            "name": "Downtown Fitness",
            "location": "123 Main Street, New York",
            "created_at": "2026-01-15T14:53:52.791227Z"
        },
        "created_at": "2026-01-15T14:55:00.000000Z"
    }
}
```

---

### 👤 7. Create Trainer (Admin or Manager)

**Endpoint:** `POST /api/auth/users/`

**Headers:**
```
Authorization: Bearer <admin_or_manager_token>
```

**Request:**
```json
{
    "email": "trainer@gym.com",
    "password": "password123",
    "role": "trainer",
    "gym_branch_id": 1
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "User created successfully",
    "data": {
        "id": 3,
        "email": "trainer@gym.com",
        "role": "trainer",
        "gym_branch": {
            "id": 1,
            "name": "Downtown Fitness",
            "location": "123 Main Street, New York",
            "created_at": "2026-01-15T14:53:52.791227Z"
        },
        "created_at": "2026-01-15T14:56:00.000000Z"
    }
}
```

---

### 👤 8. Create Member (Admin or Manager)

**Endpoint:** `POST /api/auth/users/`

**Headers:**
```
Authorization: Bearer <admin_or_manager_token>
```

**Request:**
```json
{
    "email": "member@gym.com",
    "password": "password123",
    "role": "member",
    "gym_branch_id": 1
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "User created successfully",
    "data": {
        "id": 4,
        "email": "member@gym.com",
        "role": "member",
        "gym_branch": {
            "id": 1,
            "name": "Downtown Fitness",
            "location": "123 Main Street, New York",
            "created_at": "2026-01-15T14:53:52.791227Z"
        },
        "created_at": "2026-01-15T14:57:00.000000Z"
    }
}
```

---

### 📋 9. List Users (Admin or Manager)

**Endpoint:** `GET /api/auth/users/`

**Headers:**
```
Authorization: Bearer <admin_or_manager_token>
```

**Response (200 OK):**
```json
{
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "admin@gym.com",
            "role": "admin",
            "gym_branch": null,
            "created_at": "2026-01-15T14:50:00.000000Z"
        },
        {
            "id": 2,
            "email": "manager@gym.com",
            "role": "manager",
            "gym_branch": {
                "id": 1,
                "name": "Downtown Fitness",
                "location": "123 Main Street, New York",
                "created_at": "2026-01-15T14:53:52.791227Z"
            },
            "created_at": "2026-01-15T14:55:00.000000Z"
        },
        {
            "id": 3,
            "email": "trainer@gym.com",
            "role": "trainer",
            "gym_branch": {
                "id": 1,
                "name": "Downtown Fitness",
                "location": "123 Main Street, New York",
                "created_at": "2026-01-15T14:53:52.791227Z"
            },
            "created_at": "2026-01-15T14:56:00.000000Z"
        },
        {
            "id": 4,
            "email": "member@gym.com",
            "role": "member",
            "gym_branch": {
                "id": 1,
                "name": "Downtown Fitness",
                "location": "123 Main Street, New York",
                "created_at": "2026-01-15T14:53:52.791227Z"
            },
            "created_at": "2026-01-15T14:57:00.000000Z"
        }
    ]
}
```

---

### 💪 10. Create Workout Plan (Trainer)

**Endpoint:** `POST /api/workouts/plans/`

**Headers:**
```
Authorization: Bearer <trainer_token>
```

**Request (as Trainer - branch auto-assigned):**
```json
{
    "title": "Strength Training",
    "description": "4-week program for building foundational strength"
}
```

**Request (as Admin - must specify branch):**
```json
{
    "title": "Strength Training",
    "description": "4-week program for building foundational strength",
    "gym_branch_id": 1
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Workout plan created successfully",
    "data": {
        "id": 1,
        "title": "Strength Training",
        "description": "4-week program for building foundational strength",
        "created_by": {
            "id": 3,
            "email": "trainer@gym.com"
        },
        "gym_branch": {
            "id": 1,
            "name": "Downtown Fitness",
            "location": "123 Main Street, New York",
            "created_at": "2026-01-15T14:53:52.791227Z"
        },
        "created_at": "2026-01-15T15:00:00.000000Z"
    }
}
```

---

### 📋 11. List Workout Plans

**Endpoint:** `GET /api/workouts/plans/`

**Headers:**
```
Authorization: Bearer <admin_or_manager_or_trainer_token>
```

**Response (200 OK):**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Strength Training",
            "description": "4-week program for building foundational strength",
            "created_by": {
                "id": 3,
                "email": "trainer@gym.com"
            },
            "gym_branch": {
                "id": 1,
                "name": "Downtown Fitness",
                "location": "123 Main Street, New York",
                "created_at": "2026-01-15T14:53:52.791227Z"
            },
            "created_at": "2026-01-15T15:00:00.000000Z"
        }
    ]
}
```

---

### ✅ 12. Assign Workout Task (Trainer)

**Endpoint:** `POST /api/workouts/tasks/`

**Headers:**
```
Authorization: Bearer <trainer_token>
```

**Request:**
```json
{
    "workout_plan_id": 1,
    "member_id": 4,
    "status": "pending",
    "due_date": "2026-01-25"
}
```

**Response (201 Created):**
```json
{
    "success": true,
    "message": "Workout task assigned successfully",
    "data": {
        "id": 1,
        "workout_plan": {
            "id": 1,
            "title": "Strength Training",
            "description": "4-week program for building foundational strength",
            "created_by": {
                "id": 3,
                "email": "trainer@gym.com"
            },
            "gym_branch": {
                "id": 1,
                "name": "Downtown Fitness",
                "location": "123 Main Street, New York",
                "created_at": "2026-01-15T14:53:52.791227Z"
            },
            "created_at": "2026-01-15T15:00:00.000000Z"
        },
        "member": {
            "id": 4,
            "email": "member@gym.com"
        },
        "status": "pending",
        "due_date": "2026-01-25",
        "created_at": "2026-01-15T15:05:00.000000Z"
    }
}
```

---

### 📋 13. List Workout Tasks

**Endpoint:** `GET /api/workouts/tasks/`

**Headers:**
```
Authorization: Bearer <token>
```

**Access Control:**
- **Admin**: Sees all tasks across all branches
- **Manager/Trainer**: Sees tasks in their branch only
- **Member**: Sees only their assigned tasks

**Response (200 OK):**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "workout_plan": {
                "id": 1,
                "title": "Strength Training",
                "description": "4-week program for building foundational strength",
                "created_by": {
                    "id": 3,
                    "email": "trainer@gym.com"
                },
                "gym_branch": {
                    "id": 1,
                    "name": "Downtown Fitness",
                    "location": "123 Main Street, New York",
                    "created_at": "2026-01-15T14:53:52.791227Z"
                },
                "created_at": "2026-01-15T15:00:00.000000Z"
            },
            "member": {
                "id": 4,
                "email": "member@gym.com"
            },
            "status": "pending",
            "due_date": "2026-01-25",
            "created_at": "2026-01-15T15:05:00.000000Z"
        }
    ]
}
```

---

### ✏️ 14. Update Task Status

**Endpoint:** `PATCH /api/workouts/tasks/<task_id>/`

**Headers:**
```
Authorization: Bearer <trainer_or_member_token>
```

**Request:**
```json
{
    "status": "in_progress"
}
```

**Valid Status Values:** `pending`, `in_progress`, `completed`

**Response (200 OK):**
```json
{
    "success": true,
    "message": "Task status updated successfully",
    "data": {
        "id": 1,
        "workout_plan": {
            "id": 1,
            "title": "Strength Training",
            "description": "4-week program for building foundational strength",
            "created_by": {
                "id": 3,
                "email": "trainer@gym.com"
            },
            "gym_branch": {
                "id": 1,
                "name": "Downtown Fitness",
                "location": "123 Main Street, New York",
                "created_at": "2026-01-15T14:53:52.791227Z"
            },
            "created_at": "2026-01-15T15:00:00.000000Z"
        },
        "member": {
            "id": 4,
            "email": "member@gym.com"
        },
        "status": "in_progress",
        "due_date": "2026-01-25",
        "created_at": "2026-01-15T15:05:00.000000Z"
    }
}
```

---

## ⚠️ Error Responses

### Unauthorized (No Token)
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Invalid Token
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid"
}
```

### Permission Denied
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### Validation Error
```json
{
    "success": false,
    "message": "Validation failed",
    "errors": {
        "email": ["This field is required."]
    }
}
```

### Max Trainers Exceeded
```json
{
    "success": false,
    "message": "Validation failed",
    "errors": {
        "gym_branch_id": "This branch already has 3 trainers"
    }
}
```

### Branch Restriction
```json
{
    "success": false,
    "message": "Validation failed",
    "errors": {
        "member_id": "You can only assign tasks to members in your branch"
    }
}
```

---

## 📝 Quick Test Flow

1. **Login as Admin** → Get access token
2. **Create Branch** → Note branch ID (1)
3. **Create Manager** → Assign to branch 1
4. **Create Trainer** → Assign to branch 1
5. **Create Member** → Assign to branch 1
6. **Login as Trainer** → Get trainer token
7. **Create Workout Plan** → Note plan ID (1)
8. **Assign Task** → Assign plan 1 to member
9. **Login as Member** → Get member token
10. **Update Task Status** → Mark as completed

---

## 📜 License

MIT License
