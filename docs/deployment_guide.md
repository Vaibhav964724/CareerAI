# Optional Production Deployment Guide: CareerAI

This guide explains how to deploy **CareerAI** to cloud hosting platforms if you wish to host it online after local demonstration.

> [!NOTE]
> Local development using SQLite is fully functional and recommended for your college project viva demonstration. Deploying to the cloud is optional.

---

## 1. Hosting Architecture Overview

In a production cloud deployment:
- **Frontend**: Hosted on modern static hosting platforms like **Vercel**, **Netlify**, or **Cloudflare Pages**.
- **Backend API**: Hosted as a containerized service on platforms like **Render**, **Railway**, **Fly.io**, or **AWS ECS/App Runner**.
- **Persistent Database**: Managed **PostgreSQL** instance on **Supabase**, **Neon**, **Render Postgres**, or **AWS RDS**.

---

## 2. Important Database Consideration: SQLite vs. PostgreSQL

- **Local SQLite Storage**: Local SQLite files (`careerai.db`) are stored on the local filesystem. On ephemeral serverless or container hosting platforms (such as Render Free Tier or Heroku), disk storage is reset on each restart or deploy.
- **Production PostgreSQL**: To persist student data permanently in the cloud, set the `DATABASE_URL` environment variable to a managed PostgreSQL connection string:
  ```text
  DATABASE_URL=postgresql://user:password@hostname:5432/careerai_db
  ```
  FastAPI and SQLAlchemy will automatically connect to PostgreSQL without changing application logic.

---

## 3. Backend Deployment (Example: Render or Railway)

### Using Render Web Service
1. Push your code to GitHub.
2. In the Render Dashboard, click **New** → **Web Service**.
3. Connect your GitHub repository.
4. Set:
   - **Root Directory**: `CareerAI/backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Configure Environment Variables in Render:
   - `DATABASE_URL`: Your managed PostgreSQL URL.
   - `ANTHROPIC_API_KEY`: (Optional) Your Claude API key if enabling LLM mode.
   - `CORS_ORIGINS`: JSON list of allowed origins, e.g. `["https://your-frontend.vercel.app"]`.
   - `AGENT_MAX_ITERATIONS`: `5`

---

## 4. Frontend Deployment (Example: Vercel)

### Using Vercel
1. In the Vercel Dashboard, click **Add New** → **Project**.
2. Select your repository.
3. Configure the project settings:
   - **Root Directory**: `CareerAI/frontend`
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Set Environment Variables:
   - `VITE_API_URL`: `https://your-backend-api.onrender.com`
5. In `frontend/vite.config.js` or API client, configure the API target to route requests to your deployed backend URL.

---

## 5. Production CORS & Security Checklist

1. **Explicit Allowed Origins**: In production, do not allow all origins `*` with credentials. Set `CORS_ORIGINS` strictly to your production frontend domain.
2. **Never Commit API Keys**: Keep `ANTHROPIC_API_KEY` stored exclusively in cloud environment secret variables.
3. **Database SSL**: Ensure your PostgreSQL connection string enforces SSL mode (`?sslmode=require`).
