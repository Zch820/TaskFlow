# Django Backend Project

## Project Name

**TaskFlow – Project & Task Management Backend API**

---

## 🎯 Objective

The goal of this practice is to help you **practice real-world backend development** using **Python & Django**, with a strong focus on:

* Django ORM
* REST API design
* Authentication & permissions
* Automated testing
* API documentation (Swagger)
* Docker & Docker Compose

By the end of this assignment, you should have a **production-style backend project** that can run fully inside Docker.


---

## 🧰 Tech Stack (Required)

* Python 3.11+
* Django 5+
* Django REST Framework (DRF)
* PostgreSQL
* JWT Authentication (SimpleJWT)
* Swagger / OpenAPI (drf-spectacular)
* pytest + pytest-django
* Docker & Docker Compose

---

## 📦 Features to Implement

### 1️⃣ User Authentication

* User registration
* User login using JWT
* Access token & refresh token
* Authenticated profile endpoint

**Fields:**

* email (unique)
* password (hashed)
* first_name
* last_name

---

### 2️⃣ Project Management

Each user can create and manage projects.

**Project Model:**

* name (required)
* description
* owner (User)
* created_at

**APIs:**

* Create project
* List own projects
* Retrieve project details
* Update project
* Delete project

**Rules:**

* Only the owner can update or delete a project

---

### 3️⃣ Task Management

Each project can have multiple tasks.

**Task Model:**

* title (required)
* description
* status: TODO | IN_PROGRESS | DONE
* priority: LOW | MEDIUM | HIGH
* due_date
* project (FK)
* assigned_to (User, optional)

**APIs:**

* Create task under a project
* List tasks per project
* Update task
* Delete task

---

## 🔐 Permissions

* All project & task APIs require authentication
* Users must not access other users’ data
* Only project owners can modify projects & tasks

---

## 🧪 Testing Requirements

You must write tests for:

* User registration & login
* Project CRUD operations
* Task CRUD operations
* Permission checks

**Minimum:**

* 10 meaningful tests

Tests must pass using:

```bash
docker-compose run web pytest
```

---

## 📄 API Documentation (Swagger)

* Swagger UI must be available
* Document request & response schemas
* Show authentication method

Expected URL:

```
/api/schema/swagger-ui/
```

---

## 🐳 Docker Requirements

### Services

* **web** – Django application
* **db** – PostgreSQL

### Required Files

```
Dockerfile
docker-compose.yml
.env
```

### Expectations

* PostgreSQL data must persist using volumes
* Environment variables must be used for secrets
* Django must start using Docker

---

## 📁 Recommended Project Structure

```
backend/
├── config/
├── apps/
│   ├── users/
│   ├── projects/
│   └── tasks/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---