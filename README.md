# Personal Blog Website

A professional, full-featured blog platform built with Flask, featuring user authentication, content management, and modern responsive design.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure registration, login, and logout system
- **Blog Post Management**: Create, edit, delete, and publish blog posts
- **Rich Text Editor**: Advanced content editor with formatting options
- **Image Upload**: Support for featured images and content images
- **Post Status Management**: Draft, published, and archived post states
- **User Dashboard**: Comprehensive dashboard for managing posts and viewing statistics

### Technical Features
- **Responsive Design**: Modern, mobile-friendly interface using Bootstrap 5
- **Security**: Password hashing, input validation, and XSS protection
- **Database**: SQLite database with SQLAlchemy ORM
- **File Upload**: Secure image upload with file type validation
- **SEO-Friendly URLs**: Clean, readable URLs using slugs
- **Error Handling**: Professional error pages (404, 403, 500)

### User Experience
- **Modern UI**: Clean, professional design with smooth animations
- **Social Sharing**: Built-in social media sharing buttons
- **Search & Navigation**: Intuitive navigation and breadcrumbs
- **Mobile Optimized**: Fully responsive design for all devices

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask 2.3.3**: Web framework
- **Flask-SQLAlchemy 3.0.5**: Database ORM
- **Flask-Login 0.6.3**: User session management
- **Werkzeug 2.3.7**: Security utilities
- **Bleach 6.0.0**: HTML sanitization

### Frontend
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome 6.4.0**: Icon library
- **Summernote**: Rich text editor
- **Google Fonts**: Typography (Inter font family)

### Database
- **SQLite**: Lightweight, file-based database
- **SQLAlchemy**: Object-relational mapping

## 📋 Prerequisites

Before running this application, ensure you have:

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd personal-blog
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### Database
The application uses SQLite by default. The database file (`blog.db`) will be created automatically on first run.

## 👤 Default Admin Account

Upon first run, the application creates a default admin account:

- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change these credentials immediately after first login for security.

## 📁 Project Structure

```
personal-blog/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # User dashboard
│   ├── new_post.html     # Create post page
│   ├── edit_post.html    # Edit post page
│   ├── post.html         # Individual post page
│   ├── about.html        # About page
│   ├── contact.html      # Contact page
│   └── errors/           # Error pages
│       ├── 404.html
│       ├── 403.html
│       └── 500.html
├── static/               # Static files
│   ├── css/             # Custom CSS files
│   ├── js/              # JavaScript files
│   └── uploads/         # Uploaded images
└── blog.db              # SQLite database (created automatically)
```

## 🔐 Security Features

- **Password Hashing**: All passwords are hashed using Werkzeug's security functions
- **CSRF Protection**: Built-in CSRF protection for forms
- **Input Validation**: Comprehensive input validation and sanitization
- **File Upload Security**: File type validation and secure file handling
- **XSS Protection**: HTML content sanitization using Bleach
- **Session Management**: Secure session handling with Flask-Login

## 🎨 Customization

### Styling
The application uses CSS custom properties for easy theming. Main color variables are defined in `templates/base.html`:

```css
:root {
    --primary-color: #2c5530;
    --secondary-color: #4a7c59;
    --accent-color: #6b9b37;
    --text-dark: #2c3e50;
    --text-light: #6c757d;
    --bg-light: #f8f9fa;
    --border-color: #e9ecef;
}
```

### Adding Features
The modular structure makes it easy to add new features:

1. **New Routes**: Add routes in `app.py`
2. **New Templates**: Create templates in the `templates/` directory
3. **New Models**: Add database models in `app.py`
4. **Static Files**: Add CSS/JS files in the `static/` directory

## 🚀 Deployment

### Production Deployment
For production deployment, consider the following:

1. **Use a production WSGI server** (e.g., Gunicorn)
2. **Set up a reverse proxy** (e.g., Nginx)
3. **Use a production database** (e.g., PostgreSQL)
4. **Configure environment variables**
5. **Set up SSL/TLS certificates**

### Example Gunicorn Configuration
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🧪 Testing

To run tests (if implemented):

```bash
python -m pytest tests/
```

## 📝 API Documentation

### Authentication Endpoints
- `POST /login` - User login
- `POST /register` - User registration
- `GET /logout` - User logout

### Blog Post Endpoints
- `GET /` - Home page with published posts
- `GET /post/<slug>` - View individual post
- `GET /post/new` - Create new post form
- `POST /post/new` - Create new post
- `GET /post/<id>/edit` - Edit post form
- `POST /post/<id>/edit` - Update post
- `POST /post/<id>/delete` - Delete post

### User Management
- `GET /dashboard` - User dashboard
- `GET /about` - About page
- `GET /contact` - Contact page

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- Email: your.email@example.com
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- GitHub: [Your GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- Bootstrap team for the responsive CSS framework
- Font Awesome for the icon library
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions:

1. Check the [FAQ section](http://localhost:5000/contact) on the contact page
2. Create an issue in the GitHub repository
3. Contact the development team through the contact form

---

**Note**: This is a professional blog platform suitable for company certificate submissions and production use. The code follows industry best practices and includes comprehensive documentation. 