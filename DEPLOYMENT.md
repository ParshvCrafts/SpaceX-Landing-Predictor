# Deployment Guide for SpaceX Landing Predictor

This guide explains how to deploy the SpaceX Falcon 9 Landing Prediction web application to Render.com.

## Prerequisites

1. **GitHub Account** with this repository forked/cloned
2. **Render.com Account** (free tier works fine)

## Deployment Steps

### Step 1: Prepare Your Repository

Ensure your repository is pushed to GitHub at:
```
https://github.com/ParshvCrafts/SpaceX-Landing-Predictor.git
```

### Step 2: Create Render Web Service

1. Log into [Render.com](https://render.com)
2. Click **"New +"** button in the dashboard
3. Select **"Web Service"**

### Step 3: Connect Repository

1. Connect your GitHub account if not already connected
2. Find and select **SpaceX-Landing-Predictor** repository
3. Click **"Connect"**

### Step 4: Configure Service Settings

| Setting | Value |
|---------|-------|
| **Name** | `spacex-landing-predictor` |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Root Directory** | `webapp` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn server:app` |

### Step 5: Environment Variables (Optional)

Add these if needed:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `FLASK_ENV` | `production` |

### Step 6: Instance Type

- Select **"Free"** for the free tier
- Free tier includes 750 hours/month

### Step 7: Deploy

1. Click **"Create Web Service"**
2. Wait for the build to complete (2-5 minutes)
3. Render will:
   - Clone your repository
   - Navigate to the `webapp` directory
   - Install dependencies from `requirements.txt`
   - Start the Flask server with Gunicorn

### Step 8: Access Your Site

Once deployed, Render provides a URL like:
```
https://spacex-landing-predictor.onrender.com
```

Click to verify everything works!

## Important Configuration Notes

### Root Directory Setting

**CRITICAL**: The Root Directory must be set to `webapp` because:
- The Flask server (`server.py`) is in the `webapp` folder
- The `requirements.txt` for deployment is in `webapp`
- All static files (HTML, CSS, JS, images) are in `webapp`

### File Structure for Deployment

```
webapp/
├── server.py          # Flask application entry point
├── requirements.txt   # Python dependencies
├── Procfile          # Process file for deployment
├── render.yaml       # Render configuration
├── index.html        # Main webpage
├── styles.css        # Styles
├── app.js            # JavaScript
├── animations.js     # Animations
├── data/             # JSON data files
├── images/           # All images
└── DS_capstone_presentation.pdf
```

## Build & Start Commands

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn server:app
```

## Troubleshooting

### Build Fails

**Check the logs for:**
- Missing dependencies in `requirements.txt`
- Python version issues

**Solution:**
Ensure `requirements.txt` contains:
```
flask==3.0.0
gunicorn==21.2.0
```

### 502 Bad Gateway Error

**Possible causes:**
- Gunicorn not installed
- Server.py has syntax errors
- Wrong start command

**Solution:**
1. Check that `gunicorn` is in requirements.txt
2. Test locally: `python server.py`
3. Verify start command: `gunicorn server:app`

### Static Files Not Loading

**Possible causes:**
- Incorrect file paths
- Files not included in repository

**Solution:**
1. Check `server.py` serves static files correctly
2. Verify all files are committed to Git
3. Check browser console for 404 errors

### Health Check Failing

**The application includes a health endpoint:**
```
GET /health
```

Returns: `{"status": "healthy"}`

If health checks fail, the app may not be starting correctly.

## Local Testing Before Deployment

Test with the production server locally:

```bash
cd webapp

# Install dependencies
pip install -r requirements.txt

# Run with Gunicorn (same as production)
gunicorn server:app --bind 0.0.0.0:8080

# Or run with Flask development server
python server.py
```

Open `http://localhost:8080` and verify:
- Homepage loads correctly
- All images display
- Navigation works
- PDF download works
- No console errors

## Automatic Deployments

Render automatically redeploys when you push to the `main` branch.

To trigger a manual redeploy:
1. Go to your Render dashboard
2. Select the service
3. Click **"Manual Deploy"** → **"Deploy latest commit"**

## Custom Domain (Optional)

To use a custom domain:
1. Go to service Settings → Custom Domains
2. Add your domain
3. Configure DNS as instructed by Render
4. SSL is automatically provisioned

## Cost Considerations

**Free Tier Limitations:**
- 750 hours/month (enough for one always-on service)
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds

**For Production:**
- Consider upgrading to paid tier for better performance
- Paid tiers keep services always running

## Support

If you encounter issues:
1. Check Render's [documentation](https://render.com/docs)
2. Review the [build logs](https://dashboard.render.com) in your Render dashboard
3. Open an issue on [GitHub](https://github.com/ParshvCrafts/SpaceX-Landing-Predictor/issues)

---

**Successfully deployed?** Update the README.md with your live URL!
