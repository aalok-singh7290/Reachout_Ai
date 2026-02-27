# 🚀 ReachOut AI — Complete Deployment Tutorial

> Deploy your AI Resume + Cold Email platform in under 30 minutes.
> **Frontend** (React) → Vercel | **Backend** (Python/Streamlit) → Streamlit Cloud

---

## 📁 Final Project Structure

Before you start, your project folder should look like this:

```
reachout-ai/
├── 📄 vercel.json                  ← Vercel config (provided)
├── 📄 package.json                 ← Node dependencies (provided)
├── 📄 vite.config.js               ← Vite bundler config (provided)
├── 📄 index.html                   ← HTML entry point (provided)
├── 📄 requirements.txt             ← Python dependencies (provided)
├── 📄 .gitignore                   ← Git ignore rules (provided)
├── 📄 .env.example                 ← Env variable template (provided)
├── 📄 ai_email_gtm_reachout.py     ← Your Python email backend
├── src/
│   ├── 📄 main.jsx                 ← React entry point (provided)
│   └── 📄 App.jsx                  ← Your main React component
└── .streamlit/
    └── 📄 secrets.toml.example     ← Streamlit secrets template
```

---

## ✅ Prerequisites — Install These First

Open your terminal and check if these are installed:

```bash
node --version    # Need v18 or higher
npm --version     # Comes with Node
git --version     # Need any recent version
python --version  # Need 3.9 or higher
```

### Install Missing Tools

**Node.js** (includes npm): Download from https://nodejs.org — choose "LTS" version

**Git**: Download from https://git-scm.com/downloads

**Python**: Download from https://python.org/downloads

---

## PART 1 — Set Up Your Project Locally

### Step 1.1 — Create Project Folder

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux):

```bash
# Create and enter your project folder
mkdir reachout-ai
cd reachout-ai
```

### Step 1.2 — Copy All Files Into the Folder

Place these files into `reachout-ai/` exactly as shown in the structure above:

- `vercel.json` (downloaded from Claude)
- `package.json` (downloaded from Claude)
- `vite.config.js` (downloaded from Claude)
- `index.html` (downloaded from Claude)
- `requirements.txt` (downloaded from Claude)
- `.gitignore` (downloaded from Claude)
- `.env.example` (downloaded from Claude)
- `ai_email_gtm_reachout.py` (your existing Python file)

Then create the `src/` folder and put your React component inside it:

```bash
mkdir src
# Copy main.jsx into src/
# Copy your App.jsx (ai_resume_outreach.jsx renamed) into src/
```

**Rename your React file:**
```bash
# Mac/Linux:
cp ai_resume_outreach.jsx src/App.jsx

# Windows:
copy ai_resume_outreach.jsx src\App.jsx
```

### Step 1.3 — Create the Streamlit Secrets Folder

```bash
# Mac/Linux:
mkdir .streamlit

# Windows:
mkdir .streamlit
```

### Step 1.4 — Set Up Environment Variables

```bash
# Mac/Linux:
cp .env.example .env

# Windows:
copy .env.example .env
```

Now open `.env` in any text editor (Notepad, VS Code, etc.) and fill in your API keys:

```
VITE_ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
EXA_API_KEY=xxxxxxxxxxxxxxxx
```

**Where to get API keys:**
- **Anthropic** (Claude): https://console.anthropic.com → API Keys
- **OpenAI**: https://platform.openai.com/api-keys
- **Exa**: https://exa.ai/dashboard → API Keys

### Step 1.5 — Install Node Dependencies

```bash
npm install
```

You should see a `node_modules/` folder appear. This is normal.

### Step 1.6 — Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 1.7 — Test Locally

**Test the React frontend:**
```bash
npm run dev
```
Open http://localhost:3000 in your browser. You should see the ReachOut AI interface.

**Test the Python backend:**
```bash
streamlit run ai_email_gtm_reachout.py
```
Open http://localhost:8501 in your browser. You should see the email outreach interface.

Press `Ctrl+C` to stop each server when done testing.

---

## PART 2 — Push to GitHub

Vercel and Streamlit Cloud both deploy directly from GitHub.

### Step 2.1 — Create a GitHub Account

Go to https://github.com and sign up (free).

### Step 2.2 — Create a New Repository

1. Click the **+** button in the top-right corner → **New repository**
2. Name it: `reachout-ai`
3. Set it to **Private** (recommended — your API keys logic lives here)
4. Do NOT check "Add a README" or "Add .gitignore" (you already have these)
5. Click **Create repository**

### Step 2.3 — Push Your Code

GitHub will show you commands. Run these in your terminal inside the `reachout-ai/` folder:

```bash
# Initialize git
git init

# Add all files (your .gitignore will automatically exclude .env and node_modules)
git add .

# Create your first commit
git commit -m "Initial commit: ReachOut AI platform"

# Connect to GitHub (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/reachout-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Verify:** Refresh your GitHub repository page — you should see all your files there. Make sure `.env` is NOT listed (the .gitignore should have excluded it).

---

## PART 3 — Deploy React Frontend to Vercel

### Step 3.1 — Create a Vercel Account

Go to https://vercel.com and click **Sign Up** → choose **Continue with GitHub**. This links Vercel to your GitHub account.

### Step 3.2 — Import Your Project

1. On your Vercel dashboard, click **Add New** → **Project**
2. Find `reachout-ai` in the list and click **Import**
3. Vercel will auto-detect it as a Vite project

### Step 3.3 — Configure Environment Variables

Before clicking Deploy, scroll down to **Environment Variables** and add:

| Name | Value |
|------|-------|
| `VITE_ANTHROPIC_API_KEY` | Your Anthropic API key |

Click **Add** after each one.

### Step 3.4 — Deploy

Click the **Deploy** button. Vercel will:
1. Install your npm packages
2. Run `npm run build`
3. Deploy to a live URL like `reachout-ai.vercel.app`

This takes about 60–90 seconds.

### Step 3.5 — Visit Your Live Site

Click the URL Vercel shows you. Your React app is live! 🎉

**Every time you push to GitHub, Vercel auto-redeploys.** No manual steps needed.

### Optional: Add a Custom Domain

1. In Vercel dashboard → your project → **Settings** → **Domains**
2. Add your domain (e.g., `reachoutai.com`)
3. Follow the DNS instructions Vercel provides

---

## PART 4 — Deploy Python Backend to Streamlit Cloud

### Step 4.1 — Create a Streamlit Account

Go to https://share.streamlit.io and click **Sign up** → **Continue with GitHub**.

### Step 4.2 — Create a New App

1. Click **New app**
2. Choose your repository: `YOUR_USERNAME/reachout-ai`
3. Branch: `main`
4. Main file path: `ai_email_gtm_reachout.py`
5. App URL: choose something like `reachout-emails` (gives you `reachout-emails.streamlit.app`)

### Step 4.3 — Add Secret API Keys

Before deploying, click **Advanced settings** → **Secrets**

Paste this (with your real keys):

```toml
OPENAI_API_KEY = "sk-your-openai-key-here"
EXA_API_KEY = "your-exa-key-here"
```

### Step 4.4 — Deploy

Click **Deploy!**

Streamlit will install your Python dependencies from `requirements.txt` and launch the app. Takes 2–4 minutes on first deploy.

Your Python email sender is now live at `https://reachout-emails.streamlit.app` 🎉

---

## PART 5 — Connecting Frontend ↔ Backend

The React app generates email content using Claude AI. To send those emails through your Python Gmail backend:

### Option A — Use Both Separately (Easiest)
- Use the **React app** (Vercel) to build profile, enhance resume, and draft emails
- Copy the generated email text
- Paste into the **Streamlit app** (Streamlit Cloud) to actually send via Gmail

### Option B — Pass Emails Directly (Advanced)

In your `App.jsx`, when emails are generated, post them to your Streamlit backend:

```javascript
// In your sendEmail function, add:
const sendViaBackend = async (email) => {
  const response = await fetch('https://YOUR-APP.streamlit.app/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      to: email.company.email,
      subject: email.subject,
      body: email.body
    })
  });
};
```

---

## PART 6 — Updating Your App After Changes

When you make changes to your code:

```bash
# Save your changes, then:
git add .
git commit -m "Update: describe what you changed"
git push
```

**Vercel** auto-redeploys the React app within 60 seconds.
**Streamlit Cloud** auto-redeploys the Python app within 2–3 minutes.

---

## 🔧 Troubleshooting

### "npm run dev" shows errors
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
npm run dev
```

### Vercel build fails
Check the build log in Vercel dashboard. Most common fix:
- Make sure `src/App.jsx` exists (not `src/App.js`)
- Make sure `src/main.jsx` exists
- Check that `package.json` has the correct build script

### Streamlit app crashes with "ModuleNotFoundError"
Add the missing package to `requirements.txt`, commit, and push. Streamlit will reinstall.

### API key not working on Vercel
- Vercel env vars prefixed with `VITE_` are available in the browser
- Non-`VITE_` vars are server-side only
- Go to Vercel → Project → Settings → Environment Variables to update

### Claude API returns errors
Make sure your Anthropic account has credits at https://console.anthropic.com/billing

---

## 💰 Cost Summary

| Service | Free Tier | Paid |
|---------|-----------|------|
| Vercel | 100GB bandwidth/mo, unlimited projects | $20/mo Pro |
| Streamlit Cloud | 1 app, sleeps after inactivity | $0 (community) |
| Anthropic Claude | Pay per token | ~$0.003/resume enhance |
| OpenAI | Pay per token | ~$0.002/email |
| Exa Search | 1000 searches/mo free | $0–$50/mo |

**Estimated cost for 100 cold emails: < $1**

---

## ✅ Deployment Checklist

- [ ] Node.js v18+ installed
- [ ] Python 3.9+ installed
- [ ] Git installed
- [ ] All files placed in correct folders
- [ ] `.env` created with real API keys
- [ ] `npm install` completed without errors
- [ ] `npm run dev` works locally at localhost:3000
- [ ] `streamlit run` works locally at localhost:8501
- [ ] GitHub repository created (private)
- [ ] Code pushed to GitHub (`git push`)
- [ ] Vercel account created with GitHub login
- [ ] Project imported in Vercel
- [ ] `VITE_ANTHROPIC_API_KEY` added in Vercel env vars
- [ ] Vercel deployment successful
- [ ] Streamlit Cloud account created
- [ ] App created pointing to `ai_email_gtm_reachout.py`
- [ ] `OPENAI_API_KEY` and `EXA_API_KEY` added in Streamlit secrets
- [ ] Streamlit deployment successful
- [ ] Both live URLs tested and working

---

*Made with ReachOut AI — Built on Vercel + Streamlit Cloud*
