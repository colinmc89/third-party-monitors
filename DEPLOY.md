# Deployment Guide

## Step 1: Push to GitHub

### Option A: Using GitHub CLI (if installed)
```bash
gh repo create third-party-monitors --public --source=. --remote=origin --push
```

### Option B: Manual GitHub Setup
1. Go to https://github.com/new
2. Create a new repository named `third-party-monitors` (or any name you prefer)
3. **Don't** initialize with README, .gitignore, or license (we already have these)
4. Run these commands:

```bash
cd /Users/colinmcd/Downloads/third_party_monitors
git remote add origin https://github.com/YOUR_USERNAME/third-party-monitors.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Step 2: Deploy to Render (Free & Easy)

1. Go to https://render.com and sign up/login (free account)
2. Click "New +" → "Web Service"
3. Connect your GitHub account and select the `third-party-monitors` repository
4. Configure:
   - **Name**: `third-party-monitors` (or any name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free
5. Click "Create Web Service"
6. Wait 2-3 minutes for deployment
7. Your app will be live at: `https://third-party-monitors.onrender.com` (or similar)

## Step 3: Share the URL

Once deployed, Render will give you a URL like:
- `https://third-party-monitors-XXXX.onrender.com`

Share this URL with your CEO!

## Alternative: Railway (Also Free)

1. Go to https://railway.app and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python and deploys
5. Get your URL from the project dashboard

