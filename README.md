![Screenshot 2025-06-21 200017](https://github.com/user-attachments/assets/7bb02237-f31f-4ae5-8fb2-245dd07e6012)
# 🎓 E-Learning Django REST API

A Django REST Framework-based backend for an E-Learning system.

---

## 🚀 Quick Start


### 1. Clone the Repository

```bash
git clone https://github.com/AbdulHadi-2/E-Learning-Django.git
cd E-Learning-Django
```

---

### 2. Set Up Virtual Environment

#### Windows:

```bash
python -m venv env
env\Scripts\activate
```

#### macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

---

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

### 4. Set Up PostgreSQL

Make sure PostgreSQL is installed and running.

Create a database:

```sql
CREATE DATABASE elearning;
```

Use these credentials in your settings:

```
DB_NAME=elearning
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

Alternatively, this is already hardcoded in `settings.py`.

---

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6. Create a Superuser (optional)

```bash
python manage.py createsuperuser
```

---

### 7. Run the Development Server

```bash
python manage.py runserver
```

Your API is now running at:

```
http://127.0.0.1:8000/
```

---

## ✅ Project Features

- JWT authentication
- User registration and login
- Course and lesson management
- Admin panel support
- chat
---

