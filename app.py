"""
Personal Blog Website - Main Application
A professional Flask-based blog application with user authentication and CRUD operations.

Author: [Your Name]
Date: [Current Date]
Company: [Your Company]
"""

import os
from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import markdown
import bleach

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Make utility functions available in templates
@app.context_processor
def utility_processor():
    return {
        'format_local_time': format_local_time,
        'get_local_time': get_local_time
    }

# Utility functions
def get_local_time(utc_time):
    """Convert UTC time to local timezone (IST for India)."""
    if utc_time is None:
        return None
    # IST is UTC+5:30
    ist_offset = timedelta(hours=5, minutes=30)
    return utc_time.replace(tzinfo=timezone.utc).astimezone(timezone(ist_offset))

def format_local_time(utc_time):
    """Format UTC time to local timezone string."""
    local_time = get_local_time(utc_time)
    if local_time:
        return local_time.strftime('%B %d, %Y at %I:%M %p')
    return utc_time.strftime('%B %d, %Y at %I:%M %p') if utc_time else ''

# Database Models
class User(UserMixin, db.Model):
    """User model for authentication and user management."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify user password."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    """Blog post model for content management."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    featured_image = db.Column(db.String(200))
    slug = db.Column(db.String(200), unique=True, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

    def __repr__(self):
        return f'<Post {self.title}>'

class Tag(db.Model):
    """Tag model for categorizing blog posts."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Tag {self.name}>'

# Association table for many-to-many relationship between posts and tags
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Contact(db.Model):
    """Contact form submission model."""
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)
    replies = db.relationship('Reply', backref='contact', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Contact {self.first_name} {self.last_name}>'

class Reply(db.Model):
    """Admin reply to contact messages."""
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.relationship('User', backref='replies')

    def __repr__(self):
        return f'<Reply {self.id} to Contact {self.contact_id}>'

@login_manager.user_loader
def load_user(user_id):
    """Load user for Flask-Login."""
    return User.query.get(int(user_id))

# Utility functions
def allowed_file(filename):
    """Check if uploaded file is allowed."""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_slug(title):
    """Create URL-friendly slug from title."""
    import re
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug

def sanitize_html(html_content):
    """Sanitize HTML content for security."""
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                   'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img']
    allowed_attrs = {'a': ['href'], 'img': ['src', 'alt', 'title']}
    return bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attrs)

# Routes
@app.route('/')
def index():
    """Home page displaying published blog posts."""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(status='published').order_by(Post.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    return render_template('index.html', posts=posts)

@app.route('/post/<slug>')
def post(slug):
    """Display individual blog post."""
    post = Post.query.filter_by(slug=slug, status='published').first_or_404()
    return render_template('post.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login functionality."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration functionality."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout functionality."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard for managing posts."""
    if current_user.is_admin:
        # Admin can see all posts from all users
        all_posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template('dashboard.html', posts=all_posts, is_admin=True)
    else:
        # Regular users see only their own posts
        user_posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).all()
        return render_template('dashboard.html', posts=user_posts, is_admin=False)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    """Create new blog post."""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        status = request.form.get('status', 'draft')
        
        if not title or not content:
            flash('Title and content are required.', 'error')
            return render_template('new_post.html')
        
        slug = create_slug(title)
        if Post.query.filter_by(slug=slug).first():
            flash('A post with this title already exists.', 'error')
            return render_template('new_post.html')
        
        post = Post(
            title=title,
            content=sanitize_html(content),
            excerpt=excerpt,
            slug=slug,
            status=status,
            user_id=current_user.id
        )
        
        # Handle file upload
        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                post.featured_image = filename
        
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('new_post.html')

@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit existing blog post."""
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        status = request.form.get('status')
        
        if not title or not content:
            flash('Title and content are required.', 'error')
            return render_template('edit_post.html', post=post)
        
        post.title = title
        post.content = sanitize_html(content)
        post.excerpt = excerpt
        post.status = status
        post.updated_at = datetime.utcnow()
        
        # Handle file upload
        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                post.featured_image = filename
        
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete blog post."""
    post = Post.query.get_or_404(post_id)
    
    if post.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling."""
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if not all([first_name, last_name, email, subject, message]):
            flash('All fields are required.', 'error')
            return render_template('contact.html')
        
        # Create new contact submission
        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message
        )
        
        db.session.add(contact)
        db.session.commit()
        
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/admin/contacts')
@login_required
def admin_contacts():
    """Admin page to view contact form submissions."""
    if not current_user.is_admin:
        abort(403)
    
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin_contacts.html', contacts=contacts)

@app.route('/admin/contact/<int:contact_id>')
@login_required
def view_contact(contact_id):
    """View individual contact message."""
    if not current_user.is_admin:
        abort(403)

    contact = Contact.query.get_or_404(contact_id)
    contact.is_read = True
    db.session.commit()

    return render_template('view_contact.html', contact=contact)

@app.route('/admin/contact/<int:contact_id>/reply', methods=['GET', 'POST'])
@login_required
def reply_contact(contact_id):
    """Reply to a contact message."""
    if not current_user.is_admin:
        abort(403)

    contact = Contact.query.get_or_404(contact_id)
    
    if request.method == 'POST':
        reply_message = request.form.get('reply_message')
        if not reply_message:
            flash('Reply message is required.', 'error')
            return render_template('reply_contact.html', contact=contact)
        
        # Create and store the reply
        reply = Reply(
            contact_id=contact.id,
            admin_id=current_user.id,
            message=reply_message
        )
        
        db.session.add(reply)
        db.session.commit()
        
        flash(f'Reply sent to {contact.email}!', 'success')
        return redirect(url_for('view_contact', contact_id=contact_id))
    
    return render_template('reply_contact.html', contact=contact)

@app.route('/my-messages')
@login_required
def my_messages():
    """User's own contact messages and replies."""
    # Get all contact messages from this user's email
    user_messages = Contact.query.filter_by(email=current_user.email).order_by(Contact.created_at.desc()).all()
    return render_template('my_messages.html', messages=user_messages)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

# Initialize database and create admin user
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@blog.com',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username='admin', password='admin123'")

# Initialize the database
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 