# 🚀 Deployment Guide — Vercel

This guide will help you deploy the **MoodFlow** app to Vercel and set up your repository.

## 1. Prepare Your Repository
Since you want to push to your own repository, follow these steps in your terminal:

```bash
# Initialize git (if not already done)
git init

# Add all files (the .gitignore will automatically exclude your .env and venv)
git add .

# Commit your changes
git commit -m "chore: prepare for vercel deployment"

# Connect to your GitHub/GitLab repo (replace with your URL)
git remote add origin <your-repo-url>
git push -u origin main
```

## 2. Deploy to Vercel
1. Go to [Vercel](https://vercel.com) and log in.
2. Click **Add New** > **Project**.
3. Import your new repository.
4. **Environment Variables**: This is the most important step. In the Vercel dashboard, add the following variables:
   - `SUPABASE_URL`: (Your Supabase URL)
   - `SUPABASE_KEY`: (Your Supabase Anon/Public Key)
   - `SECRET_KEY`: (Your JWT Secret Key)
5. Click **Deploy**.

## 3. Why Vercel?
- **Python Support**: Vercel natively supports FastAPI via serverless functions.
- **Speed**: Your static frontend is served through a Global CDN.
- **Easy Updates**: Every time you push to your repository, Vercel will automatically redeploy the latest version.

## 4. Troubleshooting
- If you see a "Module Not Found" error, ensure `backend/requirements.txt` contains all the necessary packages (I've already updated it for you).
- Ensure your Supabase RLS policies are active on the newly created tables.
