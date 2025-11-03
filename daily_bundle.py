#!/usr/bin/env python3
"""
Daily Learning Bundle - Main orchestrator script
Analyzes your recent code changes and sends a personalized learning bundle
"""
import os
import sys
import yaml
import argparse
from pathlib import Path
from typing import Dict
from dotenv import load_dotenv

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from git_analyzer import GitAnalyzer
from content_curator import ContentCurator
from email_sender import EmailSender


class DailyBundleOrchestrator:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the orchestrator with configuration."""
        # Load environment variables
        load_dotenv()

        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        # Initialize components
        self.git_analyzer = GitAnalyzer()
        self.content_curator = ContentCurator()
        self.email_sender = EmailSender()

    def run(self, dry_run: bool = False, test_email: bool = False) -> bool:
        """
        Run the daily learning bundle workflow.

        Args:
            dry_run: If True, generates bundle but doesn't send email
            test_email: If True, only tests email connection

        Returns:
            bool: True if successful, False otherwise
        """
        print("🎮 Daily Learning Bundle Generator")
        print("=" * 50)
        print()

        # Test email connection if requested
        if test_email:
            print("Testing email connection...")
            return self.email_sender.test_connection()

        # Step 1: Analyze git commits
        print("📊 Analyzing recent code changes...")
        days = self.config.get("days_to_analyze", 1)
        git_analysis = self.git_analyzer.analyze_commits(days=days)

        if git_analysis["has_changes"]:
            print(f"✓ Found {git_analysis['commit_count']} commit(s)")
            print(f"✓ {len(git_analysis['files_changed'])} file(s) changed")
        else:
            print("ℹ️  No recent commits found")

        print()

        # Step 2: Curate learning content
        print("🤖 Curating personalized learning content with AI...")
        learning_focus = self.config.get("learning_focus", "game development")

        try:
            bundle = self.content_curator.curate_learning_bundle(
                git_analysis=git_analysis,
                learning_focus=learning_focus,
                config=self.config
            )
            print("✓ Content curated successfully")
        except Exception as e:
            print(f"❌ Error curating content: {e}")
            return False

        print()

        # Display bundle summary
        self._display_bundle_summary(bundle)

        # Step 3: Send email (unless dry run)
        if dry_run:
            print("\n🔍 DRY RUN - Email not sent")
            print("To send the email, run without --dry-run flag")
            return True

        print("\n📧 Sending email...")
        email_to = os.getenv("EMAIL_TO")
        if not email_to:
            print("❌ EMAIL_TO not set in environment variables")
            return False

        subject_prefix = self.config.get("email", {}).get("subject_prefix", "🎮 Daily Game Dev Learning Bundle")
        subject = f"{subject_prefix} - {self._get_date()}"

        success = self.email_sender.send_learning_bundle(
            bundle=bundle,
            email_to=email_to,
            subject=subject
        )

        if success:
            print("\n✅ Learning bundle sent successfully!")
            print(f"📬 Check your inbox at {email_to}")
        else:
            print("\n❌ Failed to send email")

        return success

    def _display_bundle_summary(self, bundle: Dict):
        """Display a summary of the curated bundle."""
        print("📦 Learning Bundle Summary")
        print("-" * 50)

        if "daily_insight" in bundle:
            print(f"\n💡 Insight: {bundle['daily_insight'][:100]}...")

        if "youtube_video" in bundle:
            video = bundle["youtube_video"]
            print(f"\n🎥 Video: {video.get('title', 'N/A')}")
            print(f"   Channel: {video.get('channel', 'N/A')}")
            print(f"   URL: {video.get('url', 'N/A')[:60]}...")

        if "article" in bundle:
            article = bundle["article"]
            print(f"\n📚 Article: {article.get('title', 'N/A')}")
            print(f"   Source: {article.get('source', 'N/A')}")
            print(f"   URL: {article.get('url', 'N/A')[:60]}...")

        if "exercise" in bundle:
            exercise = bundle["exercise"]
            print(f"\n💻 Exercise: {exercise.get('title', 'N/A')}")
            print(f"   Difficulty: {exercise.get('difficulty', 'N/A')}")
            print(f"   Time: {exercise.get('estimated_time', 'N/A')}")

    def _get_date(self) -> str:
        """Get formatted date string."""
        from datetime import datetime
        return datetime.now().strftime("%B %d, %Y")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate and send a daily learning bundle based on your recent code changes"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate bundle but don't send email"
    )
    parser.add_argument(
        "--test-email",
        action="store_true",
        help="Test email connection without generating bundle"
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)"
    )

    args = parser.parse_args()

    try:
        orchestrator = DailyBundleOrchestrator(config_path=args.config)
        success = orchestrator.run(dry_run=args.dry_run, test_email=args.test_email)
        sys.exit(0 if success else 1)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("  1. Created a .env file with your credentials (see .env.example)")
        print("  2. config.yaml exists in the current directory")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
