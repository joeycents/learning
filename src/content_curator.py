"""
Content Curator - Uses AI to curate learning resources
"""
import anthropic
import json
import os
from typing import Dict, Optional


class ContentCurator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the content curator with Anthropic API key."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def curate_learning_bundle(
        self,
        user_prompt: str,
        learning_focus: str = "game development",
        config: Dict = None
    ) -> Dict:
        """
        Curate a learning bundle based on user's description of what they worked on.

        Args:
            user_prompt: Description of what the user worked on/wants to learn
            learning_focus: Primary learning focus (e.g., "game development")
            config: Configuration dictionary

        Returns a dictionary with:
        - youtube_video: YouTube video recommendation
        - article: Article recommendation
        - exercise: Coding exercise
        """
        config = config or {}

        # Build the prompt for Claude
        prompt = self._build_curation_prompt(user_prompt, learning_focus, config)

        try:
            # Call Claude API with extended thinking for better research
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=16000,
                thinking={
                    "type": "enabled",
                    "budget_tokens": 10000
                },
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse the response (skip thinking blocks, get the text)
            response_text = ""
            for block in message.content:
                if block.type == "text":
                    response_text = block.text
                    break

            bundle = self._parse_response(response_text)

            return bundle

        except Exception as e:
            print(f"Error in content curation: {e}")
            return self._get_fallback_bundle(str(e))

    def _build_curation_prompt(
        self,
        user_prompt: str,
        learning_focus: str,
        config: Dict
    ) -> str:
        """Build the prompt for Claude to curate content."""

        prompt = f"""You are a learning curator specializing in {learning_focus}. Your task is to create a personalized daily learning bundle.

## What the user worked on / wants to learn:

{user_prompt}

## Task

Create a learning bundle with the following components:

1. **YouTube Video**: Search the web to find a REAL, high-quality YouTube video (10-30 minutes).
   - First search for articles/pages that mention or link to relevant videos
   - Extract the ACTUAL YouTube URL from those sources (copy it exactly as it appears)
   - Verify the URL format is correct (youtube.com/watch?v=VIDEO_ID)
   - Also provide the channel's main URL as a fallback

2. **Article**: Search the web to find a REAL, high-quality article or tutorial.
   - Search for articles on the topic from reputable sources
   - Copy the EXACT URL from the search results (do not modify or construct URLs)
   - Also provide the source's main website URL as a fallback

3. **Coding Exercise**: Create an original, practical exercise that takes only 15 minutes to complete.
   - Focus on ONE specific skill or concept
   - Make it simple and achievable for beginners
   - Should be a focused practice exercise, not a full project

## CRITICAL REQUIREMENTS FOR URLs

- **Search first, extract URLs second** - Find pages that reference the content, then copy URLs exactly
- **Copy URLs character-by-character** - Do not paraphrase, modify, or construct URLs
- **Verify URL format** - Check that URLs start with https:// and look valid
- **Provide fallback URLs** - Include channel homepage and source homepage as backup options
- Focus on {learning_focus}
- YouTube: reputable channels (Sebastian Lague, Brackeys, Code Monkey, Catlike Coding, GDC, etc.)
- Articles: quality sources (Unity docs, Unreal docs, gamedeveloper.com, official documentation)

## Output Format

Respond ONLY with valid JSON in this exact format:

{{
  "youtube_video": {{
    "title": "Exact video title as it appears",
    "url": "https://youtube.com/watch?v=EXACT_VIDEO_ID",
    "channel": "Exact channel name",
    "channel_url": "https://youtube.com/@channelname or channel homepage",
    "duration": "MM:SS",
    "why_relevant": "Why this specific video helps (1-2 sentences)"
  }},
  "article": {{
    "title": "Exact article title as it appears",
    "url": "https://exact-url-from-search.com/path",
    "source": "Website name",
    "source_url": "https://website-homepage.com",
    "estimated_read_time": "X minutes",
    "why_relevant": "Why this specific article is helpful (1-2 sentences)"
  }},
  "exercise": {{
    "title": "Exercise Title",
    "description": "Clear description of ONE specific thing to practice",
    "difficulty": "beginner",
    "estimated_time": "15 minutes",
    "learning_objectives": ["one focused objective", "related sub-skill"],
    "starter_code": "// Brief starter code if helpful",
    "hints": ["hint 1", "hint 2", "hint 3"],
    "bonus_challenges": ["optional extension 1", "optional extension 2"]
  }},
  "daily_insight": "A brief, motivating insight (1-2 sentences)"
}}

CRITICAL: When searching, look for pages that LIST or REFERENCE videos/articles about this topic, then COPY the exact URLs you find. Do not construct or guess URLs. Output ONLY the JSON, no other text."""

        return prompt

    def _parse_response(self, response_text: str) -> Dict:
        """Parse Claude's JSON response."""
        try:
            # Try to extract JSON from the response
            # Handle cases where Claude might add markdown code blocks
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            bundle = json.loads(response_text)
            return bundle

        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {e}")
            print(f"Response text: {response_text[:500]}")
            return self._get_fallback_bundle("Failed to parse AI response")

    def _get_fallback_bundle(self, error_msg: str = "") -> Dict:
        """Return a fallback bundle if AI curation fails."""
        return {
            "youtube_video": {
                "title": "Game Development Tutorial",
                "url": "https://www.youtube.com/results?search_query=game+development+tutorial",
                "channel": "Various",
                "duration": "Varies",
                "why_relevant": "Fallback recommendation - AI curation unavailable"
            },
            "article": {
                "title": "Game Development Resources",
                "url": "https://www.gamedeveloper.com/",
                "source": "Game Developer",
                "estimated_read_time": "Varies",
                "why_relevant": "Fallback recommendation - AI curation unavailable"
            },
            "exercise": {
                "title": "Practice Your Recent Code",
                "description": "Review and refactor the code you wrote yesterday. Focus on improving code quality, adding comments, and writing tests.",
                "difficulty": "intermediate",
                "estimated_time": "30 minutes",
                "learning_objectives": [
                    "Code review skills",
                    "Refactoring techniques",
                    "Testing best practices"
                ],
                "starter_code": "// Review your recent commits",
                "hints": [
                    "Look for repeated code patterns",
                    "Check for edge cases",
                    "Add meaningful variable names"
                ],
                "bonus_challenges": [
                    "Write unit tests for your functions",
                    "Add documentation"
                ]
            },
            "daily_insight": f"AI curation temporarily unavailable. Continue your game development journey by reviewing your recent work! {error_msg}",
            "error": error_msg
        }
