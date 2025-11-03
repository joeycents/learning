# Quick Start Guide

Get your Daily Learning Bundle system running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip3 install -r requirements.txt
```

## Step 2: Configure Credentials

Run the interactive setup wizard:

```bash
python3 setup.py
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
python3 daily_bundle.py --test-email
```

## Step 4: Generate Your First Bundle!

Try one of these methods:

**Interactive mode** (will prompt you):
```bash
python3 daily_bundle.py
```

**With a prompt**:
```bash
python3 daily_bundle.py --prompt "Worked on Unity character physics today"
```

**Preview first** (doesn't send email):
```bash
python3 daily_bundle.py --dry-run --prompt "Learning shader programming"
```

Check your email inbox!

## Usage Tips

**Save daily notes to a file**:
```bash
echo "Today I worked on Unity physics and character controllers" > today.txt
python3 daily_bundle.py --prompt-file today.txt
```

**Weekly summaries**:
```bash
python3 daily_bundle.py --prompt "This week I learned about Unity's new input system, shader graphs, and scriptable objects"
```

## Troubleshooting

**Email not working?**
- Gmail users: Use an App Password, not your regular password
- Run `python3 daily_bundle.py --test-email` to diagnose

**No prompt provided error?**
- In interactive mode, press Ctrl+D (Mac/Linux) or Ctrl+Z (Windows) when done
- Or use `--prompt` flag instead

**Need help?**
- Read the full [README.md](README.md)
- Check your `config.yaml` settings

## What's Next?

- Try different prompts to see what kind of content you get
- Edit `config.yaml` to adjust difficulty and preferences
- Make it part of your daily learning routine!

---

**Pro Tip**: The more specific your prompt ("Struggled with Unity Rigidbody constraints today"), the better the AI can find relevant resources!
