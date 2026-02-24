Deployment guide

This repository contains a Django app ready for Docker and common PaaS deployment.

Steps to put it live (summary):

1. Push this repo to GitHub (create a new repo and push).
2. On a hosting provider (Render, Railway, DigitalOcean App Platform):
   - Create a new web service and connect your GitHub repo.
   - Use the `Dockerfile` (recommended) or the Python environment.
   - Add required environment variables (see `.env.example`).
   - For Render, add `RENDER_SERVICE_ID` and set `RENDER_API_KEY` as a repo secret if using the deploy workflow.
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
