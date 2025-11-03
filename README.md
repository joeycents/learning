# 🎮 Daily Game Dev Learning Bundle

An intelligent system that analyzes your daily game development work and sends you a personalized learning bundle every day. Each bundle includes a curated YouTube video, article, and coding exercise tailored to what you've been working on.

## ✨ Features

- **Smart Code Analysis**: Analyzes your git commits to understand what you've been working on
- **AI-Powered Curation**: Uses Claude AI to find relevant YouTube videos, articles, and generate custom coding exercises
- **Beautiful Emails**: Sends professionally designed HTML emails with all your learning resources
- **Highly Configurable**: Customize learning topics, difficulty levels, and preferences
- **Automated Scheduling**: Set it up once and get daily learning bundles automatically

## 📋 What You'll Get Daily

Each morning, you'll receive an email containing:

1. **🎥 YouTube Video**: A 10-30 minute tutorial related to your recent work
2. **📚 Article**: An in-depth article or tutorial to deepen your understanding
3. **💻 Coding Exercise**: A custom exercise with starter code, hints, and bonus challenges
4. **💡 Daily Insight**: A personalized reflection connecting your work to your learning

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git repository (for code analysis)
- Anthropic API key (for Claude AI)
- Email account with SMTP access (Gmail recommended)

### Installation

1. **Clone or navigate to your project directory**:
   ```bash
   cd /path/to/your/game/project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your credentials:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   EMAIL_FROM=your-email@gmail.com
   EMAIL_PASSWORD=your_app_specific_password
   EMAIL_TO=your-email@gmail.com
   ```

   **For Gmail users**: You'll need to create an App Password:
   - Go to your Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use that password in your `.env` file

4. **Configure your preferences** (optional):
   Edit `config.yaml` to customize your learning topics, difficulty level, and other settings.

### Usage

#### Test your setup:
```bash
# Test email connection
python daily_bundle.py --test-email

# Generate bundle without sending (dry run)
python daily_bundle.py --dry-run
```

#### Send your first learning bundle:
```bash
python daily_bundle.py
```

This will:
1. Analyze your git commits from yesterday
2. Use AI to curate relevant learning content
3. Send a beautiful email to your inbox

## ⚙️ Configuration

Edit `config.yaml` to customize your experience:

```yaml
# Your primary learning focus
learning_focus: "game development"

# Topics of interest
topics:
  - "Unity game engine"
  - "game physics"
  - "game AI"
  - "3D graphics"
  - "shader programming"

# How many days back to analyze
days_to_analyze: 1

# Content preferences
content:
  youtube:
    preferred_duration: "10-30 minutes"
  article:
    preferred_length: "medium"
  exercise:
    difficulty: "intermediate"
    include_solution_hints: true
```

## 🤖 Automation

### Set up daily automation with cron:

1. Open your crontab:
   ```bash
   crontab -e
   ```

2. Add a daily job (example: run at 9 AM every day):
   ```bash
   0 9 * * * cd /home/user/learning && /usr/bin/python3 daily_bundle.py
   ```

3. Or use the full path to your Python virtual environment:
   ```bash
   0 9 * * * cd /home/user/learning && /home/user/learning/venv/bin/python daily_bundle.py
   ```

### Alternative: GitHub Actions

Create `.github/workflows/daily-bundle.yml`:

```yaml
name: Daily Learning Bundle

on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM UTC daily
  workflow_dispatch:

jobs:
  send-bundle:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - name: Send Daily Bundle
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
          EMAIL_PASSWORD: ${{ secrets.EMAIL_PASSWORD }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
        run: python daily_bundle.py
```

## 📂 Project Structure

```
learning/
├── daily_bundle.py          # Main orchestrator script
├── config.yaml              # User configuration
├── .env                     # Environment variables (not in git)
├── .env.example             # Example environment file
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── src/
│   ├── git_analyzer.py     # Analyzes git commits
│   ├── content_curator.py  # AI-powered content curation
│   └── email_sender.py     # Email sending logic
└── templates/
    └── email_template.html # Beautiful HTML email template
```

## 🎨 Customizing the Email Template

The email template is in `templates/email_template.html`. It uses Jinja2 templating and includes:

- Responsive design
- Beautiful gradients and styling
- Mobile-friendly layout
- Fallback plain text version

Feel free to customize colors, fonts, and layout to match your preferences!

## 🔧 Troubleshooting

### Email not sending

1. **Gmail users**: Make sure you're using an App Password, not your regular password
2. **Check SMTP settings**: Verify your SMTP server and port in `.env`
3. **Test connection**: Run `python daily_bundle.py --test-email`

### No content being generated

1. **API key**: Verify your Anthropic API key is correct
2. **Git commits**: Make sure you have recent commits (run `git log` to check)
3. **Dry run**: Test with `python daily_bundle.py --dry-run` to see what's being generated

### Bundle not relevant to your work

1. **Update config**: Adjust topics in `config.yaml`
2. **Commit messages**: Write descriptive commit messages for better analysis
3. **Days to analyze**: Increase `days_to_analyze` in config.yaml

## 💡 Tips for Best Results

1. **Write meaningful commit messages**: The AI uses these to understand your work
2. **Commit regularly**: More commits = better understanding of your progress
3. **Update config.yaml**: Keep your learning topics aligned with current goals
4. **Review and adjust**: Fine-tune preferences based on the content you receive

## 🤝 Contributing

This is a personal learning tool, but feel free to:
- Fork and customize for your needs
- Add new features (e.g., Discord notifications, Slack integration)
- Improve the AI prompts for better content curation
- Enhance the email template design

## 📝 License

MIT License - Feel free to use and modify for your personal learning journey!

## 🙏 Acknowledgments

- Built with [Claude AI](https://www.anthropic.com/) for intelligent content curation
- Email template inspired by modern web design principles
- Created to support continuous learning in game development

---

**Happy Learning! 🚀** Keep building, keep coding, keep growing!
