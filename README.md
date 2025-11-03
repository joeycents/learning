# Daily Game Dev Learning Bundle

A minimalist AI-powered system that creates personalized learning bundles for game developers. Tell it what you're working on, and receive a curated email with a YouTube video, article, and coding exercise—all tailored to deepen your understanding.

## Features

- **Simple Prompt-Based**: Just describe what you worked on or want to learn
- **AI-Curated Content**: Claude AI searches for real, high-quality resources
- **Beautiful Minimalist Emails**: Clean black & white design, professionally formatted
- **Custom Exercises**: Original coding exercises with hints and challenges
- **Flexible Input**: Interactive mode, command-line arguments, or file-based prompts

## What You Get

Each bundle contains:

1. **YouTube Video**: A 10-30 minute tutorial from reputable channels
2. **Article**: An in-depth article or tutorial from quality sources
3. **Coding Exercise**: A custom practice exercise with learning objectives and hints
4. **Daily Insight**: A personalized reflection on why these resources matter

## Quick Start

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Set Up Credentials

```bash
python3 setup.py
```

You'll need:
- **Anthropic API Key** from https://console.anthropic.com/
- **Email credentials** (Gmail with App Password recommended)

### 3. Generate Your First Bundle

**Interactive mode** (will prompt you for input):
```bash
python3 daily_bundle.py
```

**With a prompt**:
```bash
python3 daily_bundle.py --prompt "Worked on Unity character controller physics today"
```

**Preview without sending**:
```bash
python3 daily_bundle.py --dry-run --prompt "Learning shader programming in Unity"
```

## Usage Examples

### Interactive Mode
```bash
python3 daily_bundle.py
# You'll be prompted to describe what you worked on
```

### Command Line Prompt
```bash
python3 daily_bundle.py -p "Implemented A* pathfinding for enemy AI"
```

### From a File
Create a file with your daily notes:
```bash
echo "Today I worked on:
- Implementing player movement with physics
- Adding jump mechanics
- Debugging collision detection issues" > today.txt

python3 daily_bundle.py --prompt-file today.txt
```

### Weekly Summary
```bash
echo "This week I learned about:
- Unity's new input system
- Scriptable objects for game design
- Shader graph basics" > week.txt

python3 daily_bundle.py --prompt-file week.txt
```

## Configuration

Edit `config.yaml` to customize:

```yaml
# Your primary learning focus
learning_focus: "game development"

# Content preferences
content:
  youtube:
    preferred_duration: "10-30 minutes"
  article:
    preferred_length: "medium"
  exercise:
    difficulty: "intermediate"
```

## Automation

### Save Prompts Daily

Create a simple habit of saving daily notes:

```bash
# Add to your daily workflow
echo "Today I worked on: [your notes]" >> daily_$(date +%Y%m%d).txt
python3 daily_bundle.py --prompt-file daily_$(date +%Y%m%d).txt
```

### Cron Job (Optional)

If you maintain a `today.txt` file:

```bash
crontab -e
# Add:
0 9 * * * cd /home/user/learning && python3 daily_bundle.py --prompt-file today.txt
```

## Email Template

The email template is minimalist, black & white, and professionally designed:
- Clean typography with SF Pro Display
- Clear hierarchy with numbered sections
- "Why relevant" summaries for each resource
- Mobile-responsive layout

To customize, edit `templates/email_template.html`.

## Command Reference

```bash
# Interactive mode
python3 daily_bundle.py

# With prompt
python3 daily_bundle.py --prompt "Your learning topic"
python3 daily_bundle.py -p "Your learning topic"

# From file
python3 daily_bundle.py --prompt-file myfile.txt

# Preview without sending
python3 daily_bundle.py --dry-run --prompt "Topic"

# Test email connection
python3 daily_bundle.py --test-email

# Custom config file
python3 daily_bundle.py --config custom_config.yaml
```

## Troubleshooting

**Email not sending?**
- Gmail users: Use an App Password (https://myaccount.google.com/security)
- Run `python3 daily_bundle.py --test-email` to verify connection

**Links not working?**
- The AI searches for real resources, but occasionally links may break
- Try running again or verify the URL manually

**No prompt provided?**
- In interactive mode, press Ctrl+D (Mac/Linux) or Ctrl+Z (Windows) when done typing
- Or use `--prompt` or `--prompt-file` instead

## Project Structure

```
learning/
├── daily_bundle.py              # Main script
├── config.yaml                  # Configuration
├── .env                         # Credentials (not in git)
├── requirements.txt             # Dependencies
├── src/
│   ├── content_curator.py      # AI content curation
│   └── email_sender.py         # Email delivery
└── templates/
    └── email_template.html     # Minimalist email design
```

## Tips for Best Results

1. **Be specific in your prompts**: "Worked on Unity rigidbody physics for character movement" is better than "Unity stuff"
2. **Include context**: Mention what you struggled with or want to understand better
3. **Use it regularly**: Make it part of your learning routine
4. **Review the resources**: The AI curates quality content, but you choose what to dive into

## License

MIT License - Use freely for your personal learning journey.

---

**KEEP BUILDING, KEEP LEARNING**
