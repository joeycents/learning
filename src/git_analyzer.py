"""
Git Analyzer - Analyzes recent commits and code changes
"""
import git
from datetime import datetime, timedelta
from typing import List, Dict
import os


class GitAnalyzer:
    def __init__(self, repo_path: str = "."):
        """Initialize the Git analyzer with a repository path."""
        try:
            self.repo = git.Repo(repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Not a valid git repository: {repo_path}")

    def get_recent_commits(self, days: int = 1) -> List[git.Commit]:
        """Get commits from the last N days."""
        since_date = datetime.now() - timedelta(days=days)
        commits = []

        try:
            for commit in self.repo.iter_commits(since=since_date):
                commits.append(commit)
        except git.GitCommandError:
            # Handle case where there are no commits yet
            pass

        return commits

    def analyze_commits(self, days: int = 1) -> Dict:
        """Analyze recent commits and extract meaningful information."""
        commits = self.get_recent_commits(days)

        if not commits:
            return {
                "has_changes": False,
                "commit_count": 0,
                "files_changed": [],
                "commit_messages": [],
                "code_snippets": [],
                "summary": "No recent commits found."
            }

        files_changed = set()
        commit_messages = []
        code_snippets = []

        for commit in commits:
            commit_messages.append({
                "message": commit.message.strip(),
                "author": commit.author.name,
                "date": commit.committed_datetime.strftime("%Y-%m-%d %H:%M:%S")
            })

            # Get files changed in this commit
            try:
                for diff in commit.diff(commit.parents[0] if commit.parents else None):
                    if diff.a_path:
                        files_changed.add(diff.a_path)
                    if diff.b_path:
                        files_changed.add(diff.b_path)

                    # Extract code snippets from diffs
                    if diff.diff:
                        try:
                            diff_text = diff.diff.decode('utf-8', errors='ignore')
                            # Get the changed lines (additions)
                            changed_lines = [
                                line[1:] for line in diff_text.split('\n')
                                if line.startswith('+') and not line.startswith('+++')
                            ]
                            if changed_lines:
                                code_snippets.append({
                                    "file": diff.b_path or diff.a_path,
                                    "changes": changed_lines[:20]  # Limit to 20 lines
                                })
                        except Exception:
                            pass
            except Exception:
                # Handle commits with no parents (initial commit)
                pass

        return {
            "has_changes": True,
            "commit_count": len(commits),
            "files_changed": list(files_changed),
            "commit_messages": commit_messages,
            "code_snippets": code_snippets[:5],  # Limit to 5 snippets
            "summary": self._generate_summary(commit_messages, files_changed)
        }

    def _generate_summary(self, commit_messages: List[Dict], files_changed: set) -> str:
        """Generate a human-readable summary of the changes."""
        if not commit_messages:
            return "No changes detected."

        summary_parts = []
        summary_parts.append(f"You made {len(commit_messages)} commit(s) recently.")

        if files_changed:
            summary_parts.append(f"Modified {len(files_changed)} file(s).")

        # Include first commit message if available
        if commit_messages:
            first_msg = commit_messages[0]["message"].split('\n')[0]  # First line only
            summary_parts.append(f"Latest change: {first_msg}")

        return " ".join(summary_parts)

    def get_project_context(self) -> Dict:
        """Get overall project context by scanning file types and structure."""
        context = {
            "languages": set(),
            "frameworks": set(),
            "file_types": set()
        }

        # Walk through the repository
        for root, dirs, files in os.walk(self.repo.working_dir):
            # Skip .git directory and other hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for file in files:
                if file.startswith('.'):
                    continue

                ext = os.path.splitext(file)[1].lower()
                if ext:
                    context["file_types"].add(ext)

                # Detect languages
                lang_map = {
                    '.py': 'Python',
                    '.js': 'JavaScript',
                    '.ts': 'TypeScript',
                    '.cs': 'C#',
                    '.cpp': 'C++',
                    '.c': 'C',
                    '.java': 'Java',
                    '.rs': 'Rust',
                    '.go': 'Go',
                    '.rb': 'Ruby',
                    '.shader': 'Shader',
                    '.glsl': 'GLSL',
                    '.hlsl': 'HLSL'
                }
                if ext in lang_map:
                    context["languages"].add(lang_map[ext])

                # Detect frameworks/engines
                if file.lower() in ['package.json', 'yarn.lock']:
                    context["frameworks"].add('Node.js')
                elif file.lower() == 'requirements.txt':
                    context["frameworks"].add('Python')
                elif file.lower() in ['unity', 'unityengine']:
                    context["frameworks"].add('Unity')
                elif file.lower() == 'cargo.toml':
                    context["frameworks"].add('Rust')

        # Convert sets to lists for JSON serialization
        context["languages"] = list(context["languages"])
        context["frameworks"] = list(context["frameworks"])
        context["file_types"] = list(context["file_types"])

        return context
