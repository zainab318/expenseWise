# 🚀 ExpenseWise Deployment Guide

Complete guide to deploy ExpenseWise to free hosting platforms.

## 🎯 **Quick Deploy Options**

### **🥇 Railway (Recommended)**
**Best for**: Full-stack apps with databases
- **Free tier**: $5 credit monthly
- **Auto-deploy**: GitHub integration
- **Zero config**: Just connect your repo!

#### **Steps:**
1. **Fork Repository**
   - Go to [GitHub](https://github.com)
   - Fork this repository to your account

2. **Deploy to Railway**
   - Go to [Railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "Deploy from GitHub"
   - Select your forked repository
   - Railway auto-detects and deploys!

3. **Access Your App**
   - Railway provides a public URL
   - Your app is live worldwide! 🌍

---

### **🥈 Render**
**Best for**: Reliable production hosting
- **Free tier**: 750 hours/month
- **Auto-deploy**: GitHub integration
- **Always-on**: With paid plans

#### **Steps:**
1. **Connect GitHub**
   - Go to [Render.com](https://render.com)
   - Sign up with GitHub
   - Click "New Web Service"

2. **Configure Service**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Environment**: Python 3

3. **Deploy**
   - Click "Create Web Service"
   - Render builds and deploys automatically!

---

### **🥉 Heroku**
**Best for**: Learning and prototypes
- **Free tier**: Limited hours, sleep after inactivity
- **Git-based**: Easy deployment
- **Classic platform**: Well-documented

#### **Steps:**
1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Deploy**
   ```bash
   heroku login
   heroku create your-expensewise-app
   git push heroku main
   heroku open
   ```

---

## 🛠️ **Local Development Setup**

### **Prerequisites**
- Python 3.9 or higher
- pip (Python package manager)
- Git (for version control)

### **Installation**
```bash
# Clone the repository
git clone https://github.com/yourusername/expensewise.git
cd expensewise

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run_streamlit.py
```

### **Access Locally**
Open your browser and go to: `http://localhost:8501`

---

## 📁 **File Structure**

```
expensewise/
├── streamlit_app.py          # Main application
├── database.py               # Database management
├── auth.py                   # Authentication
├── ai_processor.py          # AI processing
├── requirements.txt          # Dependencies
├── railway.json             # Railway config
├── render.yaml              # Render config
├── Procfile                 # Heroku config
├── runtime.txt              # Python version
├── setup.sh                 # Setup script
├── run_streamlit.py         # App runner
└── README.md                # Documentation
```

---

## 🔧 **Configuration Files**

### **Railway (railway.json)**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0",
    "healthcheckPath": "/_stcore/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### **Render (render.yaml)**
```yaml
services:
  - type: web
    name: expensewise
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
    healthCheckPath: /_stcore/health
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

### **Heroku (Procfile)**
```
web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
```

---

## 🎨 **Customization**

### **Branding**
- Update app name in `streamlit_app.py`
- Change colors in CSS variables
- Modify logo and icons

### **Features**
- Add new pages in navigation
- Extend AI processing capabilities
- Add new analytics charts
- Integrate with external APIs

### **Database**
- Switch from SQLite to PostgreSQL
- Add data backup strategies
- Implement data migration

---

## 🔒 **Security Considerations**

### **Production Deployment**
- Use environment variables for secrets
- Enable HTTPS/SSL
- Set up proper authentication
- Implement rate limiting
- Add data encryption

### **Environment Variables**
```bash
# Database
DATABASE_URL=your_database_url

# Authentication
SECRET_KEY=your_secret_key

# API Keys
OPENAI_API_KEY=your_openai_key
```

---

## 📊 **Monitoring & Analytics**

### **Health Checks**
- Railway: Automatic health monitoring
- Render: Built-in health checks
- Heroku: Custom health check endpoints

### **Logs**
- Railway: View logs in dashboard
- Render: Access logs in service panel
- Heroku: `heroku logs --tail`

### **Performance**
- Monitor response times
- Track user engagement
- Analyze usage patterns

---

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Port Configuration**
   ```bash
   # Make sure to use $PORT environment variable
   streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Database Issues**
   ```bash
   # Database is created automatically on first run
   # Check file permissions if issues occur
   ```

3. **Dependencies**
   ```bash
   # Make sure all dependencies are in requirements.txt
   pip install -r requirements.txt
   ```

4. **Memory Issues**
   ```bash
   # For large datasets, consider upgrading hosting plan
   # Or implement data pagination
   ```

### **Debug Mode**
```bash
# Run with debug information
streamlit run streamlit_app.py --logger.level=debug
```

---

## 📈 **Scaling**

### **Free Tier Limits**
- **Railway**: $5 credit monthly
- **Render**: 750 hours/month
- **Heroku**: Limited hours, sleep after inactivity

### **Upgrade Options**
- **Railway Pro**: $5/month for more resources
- **Render Standard**: $7/month for always-on
- **Heroku Hobby**: $7/month for always-on

### **Performance Optimization**
- Implement caching
- Optimize database queries
- Use CDN for static assets
- Add load balancing

---

## 🎯 **Next Steps**

1. **Deploy to your chosen platform**
2. **Customize the application**
3. **Add your own features**
4. **Share with your team**
5. **Scale as needed**

---

## 🆘 **Support**

- **Documentation**: Check README files
- **Issues**: GitHub Issues
- **Community**: GitHub Discussions
- **Email**: Support contact

---

**🚀 Your ExpenseWise app is ready to deploy! Choose your platform and get started!**
