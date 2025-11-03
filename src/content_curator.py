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
        git_analysis: Dict,
        learning_focus: str = "game development",
        config: Dict = None
    ) -> Dict:
        """
        Curate a learning bundle based on git analysis.

        Returns a dictionary with:
        - youtube_video: YouTube video recommendation
        - article: Article recommendation
        - exercise: Coding exercise
        """
        config = config or {}

        # Build the prompt for Claude
        prompt = self._build_curation_prompt(git_analysis, learning_focus, config)

        try:
            # Call Claude API
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Parse the response
            response_text = message.content[0].text
            bundle = self._parse_response(response_text)

            return bundle

        except Exception as e:
            return self._get_fallback_bundle(str(e))

    def _build_curation_prompt(
        self,
        git_analysis: Dict,
        learning_focus: str,
        config: Dict
    ) -> str:
        """Build the prompt for Claude to curate content."""

        prompt = f"""You are a learning curator specializing in {learning_focus}. Your task is to create a personalized daily learning bundle based on recent coding work.

## Recent Work Analysis

{self._format_git_analysis(git_analysis)}

## Task

Create a learning bundle with the following components:

1. **YouTube Video**: Find a relevant YouTube video (10-30 minutes) that teaches a concept related to the code changes above. The video should deepen understanding of what was worked on.

2. **Article**: Recommend a high-quality article or tutorial that provides detailed knowledge about the topics in the code.

3. **Coding Exercise**: Create an original coding exercise that reinforces the concepts from the recent work. The exercise should be practical and directly applicable to game development.

## Requirements

- Focus on {learning_focus}
- Make recommendations highly relevant to the actual code changes
- YouTube video should be from a reputable channel
- Article should be from a quality source (official docs, well-known blogs, tutorials)
- Exercise should be challenging but achievable in 30-60 minutes
- Exercise should include: description, starter code (if needed), and hints

## Output Format

Respond ONLY with valid JSON in this exact format:

{{
  "youtube_video": {{
    "title": "Video Title",
    "url": "https://youtube.com/watch?v=...",
    "channel": "Channel Name",
    "duration": "15:30",
    "why_relevant": "Explanation of why this video is relevant to the recent work"
  }},
  "article": {{
    "title": "Article Title",
    "url": "https://...",
    "source": "Website/Blog Name",
    "estimated_read_time": "10 minutes",
    "why_relevant": "Explanation of relevance"
  }},
  "exercise": {{
    "title": "Exercise Title",
    "description": "Detailed description of what to build/implement",
    "difficulty": "intermediate",
    "estimated_time": "45 minutes",
    "learning_objectives": ["objective 1", "objective 2"],
    "starter_code": "// Optional starter code here",
    "hints": ["hint 1", "hint 2", "hint 3"],
    "bonus_challenges": ["bonus 1", "bonus 2"]
  }},
  "daily_insight": "A brief motivational insight connecting yesterday's work to today's learning (2-3 sentences)"
}}

Remember: Output ONLY the JSON, no other text."""

        return prompt

    def _format_git_analysis(self, git_analysis: Dict) -> str:
        """Format git analysis for the prompt."""
        if not git_analysis.get("has_changes"):
            return "No recent code changes detected. Please provide general game development learning content."

        formatted = []
        formatted.append(f"**Summary**: {git_analysis.get('summary', 'N/A')}")
        formatted.append(f"**Commits**: {git_analysis.get('commit_count', 0)}")

        if git_analysis.get("commit_messages"):
            formatted.append("\n**Recent Commit Messages**:")
            for msg in git_analysis["commit_messages"][:3]:  # Top 3 commits
                formatted.append(f"- {msg['message']}")

        if git_analysis.get("files_changed"):
            formatted.append(f"\n**Files Modified**: {', '.join(git_analysis['files_changed'][:10])}")

        if git_analysis.get("code_snippets"):
            formatted.append("\n**Sample Code Changes**:")
            for snippet in git_analysis["code_snippets"][:2]:  # Top 2 snippets
                formatted.append(f"\nFile: {snippet['file']}")
                formatted.append("```")
                formatted.append('\n'.join(snippet['changes'][:10]))
                formatted.append("```")

        return '\n'.join(formatted)

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
