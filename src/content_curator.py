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

1. **YouTube Video**: Search the web to find a REAL, high-quality YouTube video (10-30 minutes) that teaches concepts related to what the user described. You MUST provide an actual, real video URL.

2. **Article**: Search the web to find a REAL, high-quality article or tutorial. You MUST provide an actual, real article URL from a reputable source (official docs, well-known blogs, tutorials).

3. **Coding Exercise**: Create an original, practical coding exercise that reinforces the concepts. Make it challenging but achievable in 30-60 minutes.

## CRITICAL REQUIREMENTS

- **Use web search to find REAL resources** - Do NOT make up URLs or links
- **Verify the content exists** - Only recommend resources you can confirm are real
- Focus on {learning_focus}
- YouTube videos should be from reputable channels (Sebastian Lague, Brackeys, Code Monkey, GDC, etc.)
- Articles should be from quality sources (Unity docs, Unreal docs, gamedeveloper.com, etc.)
- Exercise should be original and practical

## Output Format

Respond ONLY with valid JSON in this exact format:

{{
  "youtube_video": {{
    "title": "Exact video title",
    "url": "https://youtube.com/watch?v=REAL_VIDEO_ID",
    "channel": "Exact channel name",
    "duration": "MM:SS",
    "why_relevant": "Why this specific video helps with what they're learning"
  }},
  "article": {{
    "title": "Exact article title",
    "url": "https://actual-real-url.com/article",
    "source": "Website name",
    "estimated_read_time": "X minutes",
    "why_relevant": "Why this specific article is helpful"
  }},
  "exercise": {{
    "title": "Exercise Title",
    "description": "Clear, detailed description of what to build/implement",
    "difficulty": "beginner|intermediate|advanced",
    "estimated_time": "X minutes",
    "learning_objectives": ["objective 1", "objective 2", "objective 3"],
    "starter_code": "// Helpful starter code if applicable",
    "hints": ["hint 1", "hint 2", "hint 3"],
    "bonus_challenges": ["bonus 1", "bonus 2"]
  }},
  "daily_insight": "A brief, motivating insight connecting their work to today's learning (2-3 sentences)"
}}

IMPORTANT: Use your web search capability to find real, verified URLs. Output ONLY the JSON, no other text."""

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
