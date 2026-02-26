# 🚀 Deploy Your IKMS RAG System

## Option 1: Render (Easiest, Free, Recommended)

### Step 1: Push to GitHub
```bash
# If you haven't already, initialize git
git init
git add .
git commit -m "Initial commit - IKMS RAG system"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/ikms-rag.git
git push -u origin main
```

### Step 2: Deploy to Render
1. Go to https://render.com and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render auto-detects the `render.yaml` config
5. Click **"Apply"** - it will automatically:
   - Install dependencies
   - Start your FastAPI server
   - Give you a public URL like: `https://ikms-rag-demo.onrender.com`

### Step 3: Access Your App
Your app will be live at: `https://YOUR-APP-NAME.onrender.com/static/index.html`

**Note:** Free tier sleeps after 15 minutes of inactivity. First request takes ~30 seconds to wake up.

---

## Option 2: Railway (Also Easy, Free)

### Deploy to Railway
1. Go to https://railway.app and sign up
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repository
4. Railway auto-configures using `Procfile`
5. Set environment variables:
   - `DEMO_MODE=true`
   - `LOG_LEVEL=INFO`
6. Get your public URL: `https://YOUR-APP.railway.app`

---

## Option 3: Fly.io (More Advanced)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Create app
fly launch --name ikms-rag-demo

# Set secrets
fly secrets set DEMO_MODE=true

# Deploy
fly deploy
```

Your app: `https://ikms-rag-demo.fly.dev`

---

## 🔑 Environment Variables for Production

If you want to use **real API keys** in production:

### On Render/Railway:
1. Go to your app dashboard
2. Add environment variables:
   - `DEMO_MODE=false` (disable demo mode)
   - `OPENAI_API_KEY=sk-your-real-key`
   - `PINECONE_API_KEY=pcsk-your-real-key`
   - `PINECONE_INDEX=your-index-name`
   - `PINECONE_ENV=your-environment`

---

## 📦 What Gets Deployed

- ✅ FastAPI backend (all endpoints)
- ✅ Static frontend (HTML/CSS/JS)
- ✅ Demo mode enabled (works without API keys)
- ✅ Mock data for search/Q&A
- ✅ PDF upload simulation

---

## 🧪 Test Your Deployment

Once deployed, test these URLs:

```bash
# Health check
https://YOUR-APP.onrender.com/health

# API docs
https://YOUR-APP.onrender.com/docs

# Web UI
https://YOUR-APP.onrender.com/static/index.html
```

---

## 🛠️ Troubleshooting

### Port Issues
Most platforms set `$PORT` automatically. Our `render.yaml` and `Procfile` handle this.

### Frontend Not Loading
Make sure your app serves static files from `backend/static/`. This is already configured in `main.py`.

### API Errors
Check logs in your platform dashboard. Common issues:
- Missing environment variables
- Python version mismatch (we use 3.11+)
- Module import errors (check requirements.txt)

---

## 💡 Next Steps

1. **Custom Domain**: Add your own domain in platform settings
2. **Production Mode**: Set `DEMO_MODE=false` and add real API keys
3. **Scale Up**: Upgrade to paid tier for:
   - No cold starts
   - More compute power
   - Custom resources

---

## 📊 Platform Comparison

| Platform  | Free Tier | Cold Starts | Custom Domain | Ease |
|-----------|-----------|-------------|---------------|------|
| Render    | 750h/mo   | Yes (~30s)  | ✅            | ⭐⭐⭐⭐⭐ |
| Railway   | $5 credit | Yes         | ✅            | ⭐⭐⭐⭐ |
| Fly.io    | 3 apps    | Minimal     | ✅            | ⭐⭐⭐ |
| Heroku    | Deprecated| N/A         | N/A           | ❌ |

**Recommendation:** Start with **Render** - easiest setup, reliable free tier.
