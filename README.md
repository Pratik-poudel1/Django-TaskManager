# Django Task Manager

A personal task management app built with Django. You can create tasks, assign priorities and categories, track overdue items, and see a dashboard of what you've actually been doing.

Live demo: [django-taskmanager.onrender.com](https://django-taskmanager.onrender.com)

---

## What it does

- Create, update, and delete tasks with due dates, priority levels (High / Medium / Low), and categories
- Drag and drop to reorder tasks manually
- Mark tasks complete or push them back to pending
- See overdue tasks in one place
- Dashboard with a 7-day completion chart and priority breakdown
- Activity log — every create, update, complete, and delete is recorded
- User accounts with registration, login, password reset via email, and an editable profile (bio, photo, links)
- Category management — create, rename, delete

---

## Tech stack

- Python 3 / Django 5.2
- SQLite (local) / PostgreSQL (production via Supabase)
- Whitenoise for static files
- Pillow for profile picture uploads
- django-widget-tweaks for form styling
- Deployed on Render

---

## Running locally

```bash
git clone https://github.com/Pratik-poudel1/Django-TaskManager.git
cd Django-TaskManager
pip install -r requirements.txt
```

Create a `.env` file in the root:

```
SECRET_KEY=your-secret-key-here
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Then:

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000` in your browser.

---

## Project structure

```
Django-TaskManager/
├── todoapp/
│   ├── models.py       # Task, Category, UserProfile, ActivityLog
│   ├── views.py        # All view logic
│   ├── urls.py         # URL routing
│   ├── forms.py        # Task and profile forms
│   └── templates/      # HTML templates
├── todoprj/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/css/
├── requirements.txt
├── Procfile
└── build.sh
```

---

## Deployment (Render + Supabase)

The app is configured for Render. On deploy, `build.sh` runs migrations, collects static files, and creates an admin user if one doesn't exist.

Environment variables needed on Render:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | Supabase PostgreSQL connection string |
| `EMAIL_HOST_USER` | Gmail address for password reset emails |
| `EMAIL_HOST_PASSWORD` | Gmail app password |

---

## Author

Pratik Poudel  
[GitHub](https://github.com/Pratik-poudel1)
