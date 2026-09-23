# Grocery Management System

A Django web application for managing a grocery store. It provides separate areas for owners, staff, and customers, including product and category management, ordering, delivery areas, feedback, and wishlists.

## Features

- Owner dashboard for managing products, categories, sections, staff, customers, orders, and delivery areas
- Staff dashboard for operational tasks
- Customer registration, login, profile management, shopping cart, checkout, order history, feedback, and wishlist
- Product images and media uploads
- Django admin interface

## Technology

- Python
- Django
- MySQL
- HTML, CSS, and JavaScript

## Project structure

```text
grocery/
├── grocery/       # Django project configuration
├── owner/         # Owner dashboard and store management
├── staff/         # Staff-facing features
├── user/          # Customer-facing features
├── templates/     # Shared HTML templates
├── static/        # Shared CSS and JavaScript assets
├── media/         # Uploaded media files
└── manage.py
```

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django mysqlclient
```

### 4. Configure the database

Create a MySQL database, then update the local `DATABASES` configuration in `grocery/settings.py` with your own database name, username, and password.

Never commit real credentials. Use environment variables or a local `.env` file for secrets in a production-ready setup.

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Start the server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. The application routes are available under `/owner/`, `/staff/`, and `/user/`.

## Admin access

Create an admin user with:

```bash
python manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin/`.

## Security note

Before publishing this repository, remove or replace any hard-coded secret key and database password in `grocery/settings.py`. Do not upload `.env` files, database dumps, or credentials.

## License

Add a license for this project if you intend to share or reuse it publicly.
