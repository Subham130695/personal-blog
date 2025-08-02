# Deployment Guide for Personal Blog

This guide will help you deploy your Flask blog application to various platforms.

## ⚠️ Important Note About Netlify

**Netlify is designed for static websites only.** Your Flask application is a dynamic web application that requires a Python server to run. Therefore, Netlify cannot host your Flask application directly.

## Recommended Deployment Options

### Option 1: Render (Recommended - Free)

Render is a modern platform that supports Python applications and offers a free tier.

#### Steps to Deploy on Render:

1. **Create a Render Account**
   - Go to [render.com](https://render.com)
   - Sign up for a free account

2. **Connect Your Repository**
   - Click "New +" and select "Web Service"
   - Connect your GitHub/GitLab account
   - Select your blog repository

3. **Configure the Service**
   - **Name**: `personal-blog` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

4. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - Your app will be available at `https://your-app-name.onrender.com`

### Option 2: Railway

Railway is another excellent platform for Python applications.

#### Steps to Deploy on Railway:

1. **Create a Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up for a free account

2. **Deploy Your App**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your blog repository
   - Railway will automatically detect it's a Python app

3. **Configure Environment**
   - Railway will automatically install dependencies from `requirements.txt`
   - The app will be deployed and available at a Railway-provided URL

### Option 3: Heroku

Heroku is a well-established platform, though it now requires a credit card for the free tier.

#### Steps to Deploy on Heroku:

1. **Create a Heroku Account**
   - Go to [heroku.com](https://heroku.com)
   - Sign up for an account (credit card required)

2. **Install Heroku CLI**
   - Download and install from [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

3. **Deploy via CLI**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create a new Heroku app
   heroku create your-blog-app-name
   
   # Add your files to git (if not already done)
   git add .
   git commit -m "Deploy to Heroku"
   
   # Deploy to Heroku
   git push heroku main
   ```

## Files Created for Deployment

The following files have been created to support deployment:

- `render.yaml` - Configuration for Render deployment
- `gunicorn.conf.py` - Gunicorn server configuration
- `Procfile` - Required for Heroku deployment
- `runtime.txt` - Specifies Python version
- `requirements.txt` - Updated with Gunicorn dependency

## Environment Variables

For production deployment, you may want to set these environment variables:

- `SECRET_KEY` - A secure secret key for Flask
- `DATABASE_URL` - Database connection string (if using external database)

## Database Considerations

- The current setup uses SQLite, which works fine for small to medium applications
- For production, consider using PostgreSQL or MySQL
- Render and Railway provide managed databases

## Custom Domain

After deployment, you can:
1. Purchase a domain from a registrar (GoDaddy, Namecheap, etc.)
2. Configure DNS settings to point to your deployed application
3. Set up SSL certificates (usually automatic on modern platforms)

## Monitoring and Maintenance

- Most platforms provide built-in monitoring
- Set up logging to track application performance
- Regularly update dependencies for security

## Support

If you encounter issues during deployment:
1. Check the platform's documentation
2. Review the deployment logs
3. Ensure all required files are present in your repository

## Next Steps

1. Choose your preferred deployment platform
2. Follow the platform-specific steps above
3. Test your deployed application thoroughly
4. Update your documentation with the live URL
5. Consider setting up a custom domain

---

**Note**: All deployment platforms mentioned above offer free tiers suitable for personal projects and certificate submissions. 