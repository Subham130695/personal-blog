# Personal Blog - Flask

This is a Flask-based blog application with authentication, admin features, and post management.

## Environment Variables
Create a `.env` file in the project root (do NOT commit this file) with values like:

```
SECRET_KEY=change-this
ADMIN_USERNAME=change-admin-username
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=change-strong-password
DATABASE_URL=sqlite:///blog.db
```

Alternatively, configure these as environment variables in your hosting provider.

## Setup

1. Create a virtual environment and install dependencies:
```
pip install -r requirements.txt
```

2. Run the app:
```
python app.py
```

## Security Notes
- Do not commit real secrets. Use `.env` locally and environment variables in production.
- The `.gitignore` in this repo excludes `.env` and SQLite database files by default.

## Features

- ✅ **User Authentication** - Login/Register system
- ✅ **Blog Management** - Create, edit, delete posts
- ✅ **Contact System** - Contact form with admin replies
- ✅ **Responsive Design** - Works on all devices
- ✅ **Admin Dashboard** - Manage posts and messages
- ✅ **Modern UI** - Bootstrap 5 with custom styling

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite
- **Deployment**: Railway

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/Subham130695/personal-blog.git
   cd personal-blog
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Visit**: http://localhost:5000

## Admin Access

- Set the admin credentials via environment variables before first run. Do not commit secrets.
- Required variables: `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`.
- Login URL: `/login`

## Deployment

This project is configured for Railway deployment:

1. **Push to GitHub**
2. **Connect to Railway**
3. **Automatic deployment**

## Project Structure

```
personal-blog/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── railway.json       # Railway configuration
├── Procfile          # Railway process file
├── templates/         # HTML templates
├── static/           # CSS, JS, images
└── instance/         # Database files
```

## Live Demo

Visit: https://web-production-848f.up.railway.app

---

**Built with ❤️ by Subham Kumar Sahoo** 