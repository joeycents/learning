"""
Email Sender - Sends beautiful HTML emails
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from datetime import datetime
from typing import Dict, Optional
import os


class EmailSender:
    def __init__(
        self,
        smtp_server: Optional[str] = None,
        smtp_port: Optional[int] = None,
        email_from: Optional[str] = None,
        email_password: Optional[str] = None
    ):
        """Initialize the email sender with SMTP credentials."""
        self.smtp_server = smtp_server or os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.email_from = email_from or os.getenv("EMAIL_FROM")
        self.email_password = email_password or os.getenv("EMAIL_PASSWORD")

        if not self.email_from or not self.email_password:
            raise ValueError("Email credentials not provided. Set EMAIL_FROM and EMAIL_PASSWORD environment variables.")

    def send_learning_bundle(
        self,
        bundle: Dict,
        email_to: str,
        subject: str = "🎮 Daily Game Dev Learning Bundle",
        template_path: str = "templates/email_template.html"
    ) -> bool:
        """
        Send a learning bundle email.

        Args:
            bundle: The curated learning bundle dictionary
            email_to: Recipient email address
            subject: Email subject line
            template_path: Path to the HTML template

        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Read the HTML template
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()

            # Render the template with bundle data
            html_content = self._render_template(template_content, bundle)

            # Create the email message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.email_from
            message["To"] = email_to

            # Create plain text version as fallback
            text_content = self._create_text_version(bundle)

            # Attach both versions
            part1 = MIMEText(text_content, "plain")
            part2 = MIMEText(html_content, "html")
            message.attach(part1)
            message.attach(part2)

            # Send the email
            return self._send_email(message, email_to)

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def _render_template(self, template_content: str, bundle: Dict) -> str:
        """Render the Jinja2 template with bundle data."""
        template = Template(template_content)

        # Prepare template variables
        template_vars = {
            "date": datetime.now().strftime("%B %d, %Y"),
            "youtube_video": bundle.get("youtube_video", {}),
            "article": bundle.get("article", {}),
            "exercise": bundle.get("exercise", {}),
            "daily_insight": bundle.get("daily_insight", "Keep learning and building!")
        }

        return template.render(**template_vars)

    def _create_text_version(self, bundle: Dict) -> str:
        """Create a plain text version of the email."""
        text_parts = []
        text_parts.append("🎮 DAILY GAME DEV LEARNING BUNDLE")
        text_parts.append("=" * 50)
        text_parts.append("")

        # Daily insight
        if "daily_insight" in bundle:
            text_parts.append(f"💡 Today's Insight: {bundle['daily_insight']}")
            text_parts.append("")

        # YouTube video
        if "youtube_video" in bundle:
            video = bundle["youtube_video"]
            text_parts.append("🎥 WATCH & LEARN")
            text_parts.append("-" * 50)
            text_parts.append(f"Title: {video.get('title', 'N/A')}")
            text_parts.append(f"Channel: {video.get('channel', 'N/A')}")
            text_parts.append(f"Duration: {video.get('duration', 'N/A')}")
            text_parts.append(f"Why: {video.get('why_relevant', 'N/A')}")
            text_parts.append(f"Watch: {video.get('url', 'N/A')}")
            text_parts.append("")

        # Article
        if "article" in bundle:
            article = bundle["article"]
            text_parts.append("📚 READ & UNDERSTAND")
            text_parts.append("-" * 50)
            text_parts.append(f"Title: {article.get('title', 'N/A')}")
            text_parts.append(f"Source: {article.get('source', 'N/A')}")
            text_parts.append(f"Read time: {article.get('estimated_read_time', 'N/A')}")
            text_parts.append(f"Why: {article.get('why_relevant', 'N/A')}")
            text_parts.append(f"Read: {article.get('url', 'N/A')}")
            text_parts.append("")

        # Exercise
        if "exercise" in bundle:
            exercise = bundle["exercise"]
            text_parts.append("💻 CODE & PRACTICE")
            text_parts.append("-" * 50)
            text_parts.append(f"Title: {exercise.get('title', 'N/A')}")
            text_parts.append(f"Difficulty: {exercise.get('difficulty', 'N/A')}")
            text_parts.append(f"Time: {exercise.get('estimated_time', 'N/A')}")
            text_parts.append(f"\nDescription: {exercise.get('description', 'N/A')}")

            if exercise.get('learning_objectives'):
                text_parts.append("\nLearning Objectives:")
                for obj in exercise['learning_objectives']:
                    text_parts.append(f"  - {obj}")

            if exercise.get('hints'):
                text_parts.append("\nHints:")
                for hint in exercise['hints']:
                    text_parts.append(f"  - {hint}")

        text_parts.append("")
        text_parts.append("🚀 Keep building, keep learning!")

        return '\n'.join(text_parts)

    def _send_email(self, message: MIMEMultipart, email_to: str) -> bool:
        """Send the email via SMTP."""
        try:
            # Create SMTP session
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.email_from, self.email_password)
                server.send_message(message)

            print(f"✅ Email sent successfully to {email_to}")
            return True

        except smtplib.SMTPAuthenticationError:
            print("❌ SMTP Authentication failed. Check your email and password.")
            print("   For Gmail, you need to use an App Password: https://support.google.com/accounts/answer/185833")
            return False

        except smtplib.SMTPException as e:
            print(f"❌ SMTP error occurred: {e}")
            return False

        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False

    def test_connection(self) -> bool:
        """Test the SMTP connection without sending an email."""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.email_from, self.email_password)

            print("✅ SMTP connection test successful!")
            return True

        except Exception as e:
            print(f"❌ SMTP connection test failed: {e}")
            return False
