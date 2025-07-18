# Coders - June Sprint 1

A Django-based project developed to implement a simple user management and attendance tracking system with API support. This system is designed with two primary user types—**Staff** and **Community Members**—and supports daily sign-in/sign-out functionalities.

---

## Project Overview

This project aims to provide a foundational backend system where:

- **Community members** can check in and out daily.
- **Staff users** can manage attendance and oversee the system via the Django admin panel.
- APIs are exposed to support frontend integration for sign-ins and check-outs.

The project is divided into three main Django apps:

- `users` – Custom user model with roles
- `attendance` – Daily check-in and check-out system
- `dashboard` – (Optional/Bonus) Admin or insights dashboard

---

## Tech Stack

- **Backend**: Django 4.x
- **Language**: Python 3.10+
- **Database**: SQLite (default)
- **API**: Django REST Framework *(recommended)*
- **Testing**: Django built-in test suite

---

## 📂 Project Structure
coders-june-sprint1/
│
├── core/ # Django project root
├── users/ # App for custom user management
├── attendance/ # App for attendance check-in/checkout
├── dashboard/ # Optional app for stats or admin views
├── manage.py
└── requirements.txt


---

##  Features

## Users App
- Two user roles: **Staff** and **Community Member**
- Staff can access Django admin
- Community users can register, sign in, and check in/out

## Attendance App
- Check-in and check-out endpoints for daily attendance
- Attendance model using fields from the provided daily sign-in form
- Time-stamped records per user

## Dashboard (Optional)
- Views or endpoints for stats and summaries (e.g., number of check-ins per day)

---

## Local Setup Instructions

## 1. Clone the Project

git clone https://github.com/obonyodorice/Coders-June-Sprint1.git
cd `Coders-June-Sprint1`

```python -m venv venv
source venv/bin/activate```

```
pip install -r requirements.txt
```

```
python manage.py migrate
```

```
python manage.py createsuperuser
```

```
python manage.py runserver
```
