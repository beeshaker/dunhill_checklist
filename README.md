# Dunhill Checklist Website (Django + MySQL)

This version is configured for **MySQL** and works well with **MySQL Workbench**.

## 1. Create the database in MySQL Workbench
Create a schema named:

```sql
CREATE DATABASE dunhill_checklist CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 2. Create `.env`
Copy `.env.example` to `.env` and update the MySQL password.

## 3. Install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Create admin user
```bash
python manage.py createsuperuser
```

## 6. Run
```bash
python manage.py runserver
```

## Notes
- Photo capture on mobile browsers uses:
  - `accept="image/*"`
  - `capture="environment"`
- This encourages live camera usage from the phone browser.
- For local development, media uploads are stored in `media/checklist_evidence/`.

## Heroku note
Heroku does not provide native MySQL like Heroku Postgres.  
If you deploy to Heroku with MySQL, you will need an external MySQL provider.

For the easiest MySQL deployment, **DigitalOcean App Platform** or a **VPS** is usually the cleaner choice.
