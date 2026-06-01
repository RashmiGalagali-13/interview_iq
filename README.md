# Interview IQ 🎯
**Smart Job Matching, Application Tracking & Interview Practice Platform**

Built with Python, Django, HTML, CSS, JavaScript, and MySQL.

---

## Features
- **Dual User System** — Job Seekers and Companies with separate flows
- **Smart Job Matching** — Skill-based % match score between seeker and jobs
- **Application Pipeline** — Pending → Reviewing → Shortlisted → Accepted/Rejected
- **Interview Practice** — 500+ questions with scoring and AI feedback
- **Company Dashboard** — Post jobs, view/filter applicants, update status
- **Seeker Dashboard** — Recommended jobs, saved jobs, application tracker
- **Search & Filter** — By keyword, location, type, experience level

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database

**SQLite (default — works out of the box):**
No changes needed.

**MySQL (production):**
```bash
mysql -u root -p
CREATE DATABASE interview_iq_db CHARACTER SET utf8mb4;
GRANT ALL PRIVILEGES ON interview_iq_db.* TO 'your_user'@'localhost';
```
Then uncomment the MySQL block in `interview_iq/settings.py`.

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Load Sample Interview Questions
```bash
python manage.py loaddata interviews/fixtures/sample_questions.json
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**

---

## Project Structure
```
interview_iq/
├── accounts/         # User auth, seeker & company profiles
├── jobs/             # Job posts, applications, saved jobs
├── interviews/       # Interview question bank & practice engine
├── static/           # CSS, JS assets
├── templates/        # All HTML templates
├── media/            # User uploads (resumes, logos)
└── manage.py
```

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11 + Django 4.2 |
| Database | MySQL (SQLite for dev) |
| Frontend | HTML5, CSS3, Vanilla JS |
| Fonts | Syne + DM Sans (Google Fonts) |
| Auth | Django built-in auth |
| File Uploads | Django + Pillow |

## Admin Panel
Visit `/admin/` with your superuser credentials to manage all data.
