# InvestGram Full Django Project

A glossy Instagram-style investor and entrepreneur networking website.

## Features

- Landing page
- Investor/startup registration
- Login/logout
- Explore/search profiles
- Profile detail page
- Connection request system
- Accept/reject connection requests
- Internal messaging/chat
- Contact reveal logging
- Startup pitch post creation
- Admin management
- Glossy glassmorphism UI

## Setup

```bash
cd investgram_full_project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Admin

```text
http://127.0.0.1:8000/admin/
```

## Important

This is a starter project. For production add:
- Strong SECRET_KEY
- DEBUG=False
- PostgreSQL
- Email verification
- Payment/subscription system
- Legal Terms, Privacy Policy, Anti-Circumvention Policy
