# 🚀 PythonAnywhere Quick Start Guide

## ⚡ **5-Minute Deployment**

### **Step 1: Sign Up (1 minute)**
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Click "Create a Beginner account" (FREE)
3. Choose username, enter email, create password
4. Verify email

### **Step 2: Clone Repository (1 minute)**
1. Go to "Consoles" tab
2. Click "New console" → "Bash"
3. Run: `git clone https://github.com/Subham130695/personal-blog.git`

### **Step 3: Create Web App (1 minute)**
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose: Python 3.9, Flask
4. Source: `/home/yourusername/personal-blog`

### **Step 4: Configure (1 minute)**
1. Set virtual environment: `/home/yourusername/personal-blog/myenv`
2. Update WSGI file (see detailed guide)
3. Install dependencies in console

### **Step 5: Deploy (1 minute)**
1. Click "Reload" button
2. Your app is live at: `https://yourusername.pythonanywhere.com`

---

## 🔑 **Quick Commands**

```bash
# Clone repository
git clone https://github.com/Subham130695/personal-blog.git

# Create virtual environment
python3 -m venv myenv
source myenv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create database directory
mkdir -p ~/personal-blog/instance
chmod 755 ~/personal-blog/instance
```

---

## 📋 **Essential Settings**

### **Virtual Environment Path**
```
/home/yourusername/personal-blog/myenv
```

### **WSGI File Content**
```python
import sys
import os

project_home = '/home/yourusername/personal-blog'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-secret-key-here'

from app import app as application

if __name__ == "__main__":
    application.run()
```

---

## 🎯 **Your App URL**
```
https://yourusername.pythonanywhere.com
```

## 🔑 **Admin Login**
- **Username**: `admin`
- **Password**: `admin123`

---

## ✅ **Success Indicators**
- Green "Running" status in Web tab
- Website loads without errors
- Admin login works
- Blog posts can be created

---

## 🆘 **Quick Fixes**

### **App won't load?**
- Check error logs in Web tab
- Verify WSGI file configuration
- Make sure virtual environment is set

### **Import errors?**
- Install missing packages: `pip install package-name`
- Verify virtual environment is activated

### **Database errors?**
- Create instance directory: `mkdir -p ~/personal-blog/instance`
- Set permissions: `chmod 755 ~/personal-blog/instance`

---

**🚀 Your Flask blog will be live in 5 minutes!** 