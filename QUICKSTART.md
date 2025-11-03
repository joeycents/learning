# 🚀 Quick Start Guide

Get your Daily Learning Bundle system running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Credentials

Run the interactive setup wizard:

```bash
python setup.py
```

Or manually create a `.env` file:

```bash
cp .env.example .env
# Edit .env with your credentials
```

You'll need:
- **Anthropic API Key**: Get it from https://console.anthropic.com/
- **Email credentials**: For Gmail, use an App Password from https://myaccount.google.com/security

## Step 3: Test Your Setup

```bash
# Test email connection
python daily_bundle.py --test-email

# Generate bundle without sending (preview)
python daily_bundle.py --dry-run
```

## Step 4: Send Your First Bundle!

```bash
python daily_bundle.py
```

Check your email inbox!

## Step 5: Automate (Optional)

### Option A: Cron (Linux/Mac)

```bash
crontab -e
# Add this line to run daily at 9 AM:
0 9 * * * cd /home/user/learning && python3 daily_bundle.py
```

### Option B: GitHub Actions

1. Go to your repository Settings → Secrets
2. Add these secrets:
   - `ANTHROPIC_API_KEY`
   - `EMAIL_FROM`
   - `EMAIL_PASSWORD`
   - `EMAIL_TO`
   - `SMTP_SERVER` (optional, defaults to smtp.gmail.com)
   - `SMTP_PORT` (optional, defaults to 587)

3. The workflow in `.github/workflows/daily-learning-bundle.yml` will run automatically!

## Troubleshooting

**Email not working?**
- Gmail users: Use an App Password, not your regular password
- Run `python daily_bundle.py --test-email` to diagnose

**No content generated?**
- Check your Anthropic API key
- Make sure you have git commits (run `git log`)
- Try `python daily_bundle.py --dry-run` to see what's happening

**Need help?**
- Read the full [README.md](README.md)
- Check your `config.yaml` settings

## What's Next?

- Edit `config.yaml` to customize topics and preferences
- Write good commit messages for better content curation
- Enjoy your daily learning journey! 🎮

---

**Pro Tip**: The more descriptive your git commit messages, the better the AI can curate relevant content for you!
