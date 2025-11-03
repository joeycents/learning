#!/usr/bin/env python3
"""
Setup script for Daily Learning Bundle
Helps users configure the system interactively
"""
import os
import sys
from pathlib import Path


def main():
    print("🎮 Daily Learning Bundle - Setup Wizard")
    print("=" * 50)
    print()

    # Check if .env already exists
    env_path = Path(".env")
    if env_path.exists():
        response = input(".env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return

    print("Let's set up your learning bundle system!\n")

    # Collect credentials
    print("📧 Email Configuration")
    print("-" * 50)
    email_from = input("Your email address: ").strip()

    print("\nFor Gmail users:")
    print("  1. Go to https://myaccount.google.com/security")
    print("  2. Enable 2-Step Verification")
    print("  3. Generate an App Password for 'Mail'")
    print("  4. Use that app password below (not your regular password)\n")

    email_password = input("Email password (or App Password): ").strip()
    email_to = input("Send learning bundles to (press Enter for same): ").strip()
    if not email_to:
        email_to = email_from

    smtp_server = input("SMTP server (default: smtp.gmail.com): ").strip()
    if not smtp_server:
        smtp_server = "smtp.gmail.com"

    smtp_port = input("SMTP port (default: 587): ").strip()
    if not smtp_port:
        smtp_port = "587"

    print("\n🤖 Anthropic API Configuration")
    print("-" * 50)
    print("Get your API key from: https://console.anthropic.com/\n")
    anthropic_key = input("Anthropic API key: ").strip()

    # Write .env file
    env_content = f"""# API Keys
ANTHROPIC_API_KEY={anthropic_key}

# Email Configuration
SMTP_SERVER={smtp_server}
SMTP_PORT={smtp_port}
EMAIL_FROM={email_from}
EMAIL_PASSWORD={email_password}
EMAIL_TO={email_to}
"""

    with open(".env", "w") as f:
        f.write(env_content)

    print("\n✅ Configuration saved to .env")

    # Test the setup
    print("\n🧪 Would you like to test the configuration now?")
    response = input("Test email connection? (Y/n): ")

    if response.lower() != 'n':
        print("\nTesting email connection...")
        os.system("python daily_bundle.py --test-email")

    print("\n" + "=" * 50)
    print("✨ Setup complete!")
    print("\nNext steps:")
    print("  1. Edit config.yaml to customize your learning preferences")
    print("  2. Run 'python daily_bundle.py --dry-run' to test content generation")
    print("  3. Run 'python daily_bundle.py' to send your first learning bundle!")
    print("\nFor automation, see the README.md for cron/GitHub Actions setup.")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error during setup: {e}")
        sys.exit(1)
