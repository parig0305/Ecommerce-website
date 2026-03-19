Deployment guide

This repository contains a Django app ready for Docker and common PaaS deployment.

Steps to put it live (summary):

1. Push this repo to GitHub (create a new repo and push).
2. On a hosting provider (Render, Railway, DigitalOcean App Platform):
   - Create a new web service and connect your GitHub repo.
   - Use the `Dockerfile` (recommended) or the Python environment.
   - Add required environment variables (see `.env.example`).
   - For Render, add `RENDER_SERVICE_ID` and set `RENDER_API_KEY` as a repo secret if using the deploy workflow.
     - Create a new web service and connect your GitHub repo.
     - Use the `Dockerfile` (recommended) or the Python environment.
     - Add required environment variables (see `.env.example`).
     - For Render, add `RENDER_SERVICE_ID` and set `RENDER_API_KEY` as a repo secret if using the deploy workflow.

   Render-specific steps (quick)
   -----------------------------
   1. Sign in to https://render.com and create a new Web Service → "Connect a repository" → choose `kishuu1/Ecommerce-website`.
   2. Build & Runtime:
      - Environment: "Docker"
      - Branch: `main`
      - Start command: leave blank (Dockerfile CMD will be used). The Dockerfile binds Gunicorn to `$PORT`.
   3. Environment variables: add the values from your local `.env` (do NOT commit `.env`):
      - `SECRET_KEY`, `DEBUG` (False), `ALLOWED_HOSTS` (your domain),
      - `DATABASE_URL` or `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT`,
      - `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_UPI_ID`.
   4. (Optional) Create a managed Postgres on Render: Dashboard → New → Database → follow prompts. Copy the `DATABASE_URL` into the Web Service env vars.
   5. Deploy: click "Create Web Service" — Render will build and deploy. Monitor logs for errors.

   Run migrations & collectstatic on Render
   --------------------------------------
   After the first deploy, open your service on Render and use the "Shell" (or "New Job") to run one-off commands:

   ```
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

   If you use a managed Postgres service on Render, make sure the Web Service has the `DATABASE_URL` secret set to the database's connection string.

   If you prefer I can walk through each Render screen while you do the clicks, or I can provide exact env values and commands to run locally before pushing. 
3. Alternatively, use Docker Compose on a VPS: `docker-compose up -d --build`.

Important env vars (example):

- SECRET_KEY
- DEBUG=False
- ALLOWED_HOSTS=yourdomain.com
- DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT
- RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET

If you want, I can:
- Create the repository on your GitHub and push the code (you must provide a Personal Access Token with repo access), or
- Walk you through connecting this repo to Render/Railway and configuring secrets.
