# Steach - Smart Teacher-Student Management Platform

Steach is a Django-based student management system designed to simplify communication and administration between schools, teachers, students, and parents.

The platform provides role-based access control, student-teacher management, attendance tracking, and secure authentication workflows.

---

## 🚀 Features

### 🔐 Authentication & Authorization

- Role-based authentication for:
  - Admin
  - Teacher
  - Student

- Secure user login and session management
- Password hashing
- UUID-based password recovery system
- Protected routes using custom authorization decorators

---

### 👨‍🏫 Teacher Management

- Manage teacher profiles
- Assign students to teachers
- View allocated students
- Track teacher-related information

---

### 🎒 Student Management

- Student profile management
- Parent information handling
- Teacher allocation system
- Student dashboard

---

### 📅 Attendance Management

- Teacher attendance tracking
- Store and manage attendance records
- Database-driven attendance system

---

## 🛠 Tech Stack

**Backend**

- Python
- Django

**Database**

- SQLite
- Django ORM

**Frontend**

- HTML
- CSS
- JavaScript
- Django Templates

**Tools**

- Git
- GitHub
- VS Code

---

## 🏗 System Architecture

```text
              User
               |
               v

        Django Application

               |
    -------------------------
    |           |           |

 Authentication  Views   Templates

    |
    v

Business Logic Layer

    |
    v

Django ORM

    |
    v

SQLite Database


Tables:

Users
Students
Teachers
Parents
Attendance
```

---

## Database Design

The project uses relational database concepts through Django ORM.

Relationships implemented:

- One-to-One relationships
- ForeignKey relationships
- Many-to-Many relationships

Example:

```text
Teacher
   |
   |
Many Students


Student
   |
   |
Parent Details


Users
   |
   |
Role Based Profiles
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Sparsh015/Steach.git
```

Move into project:

```bash
cd Steach
```

Create virtual environment:

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## Key Learnings

- Django MVC/MVT architecture
- Authentication and authorization
- ORM relationships
- Database modeling
- Session management
- Secure user workflows
- Query optimization

---

Django application focusing on authentication, database design, and role-based management systems.
