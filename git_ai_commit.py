#!/usr/bin/env python3
"""git-ai-commit: Generate commit messages from git diffs using AI."""

import argparse
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error

__version__ = "1.0.0"

SYSTEM_PROMPT = """You are a commit message generator. Given a git diff, produce a concise commit message.

Rules:
- Use conventional commits format: type(scope): description
- Types: feat, fix, docs, style, refactor, perf, test, chore, build, ci
- Subject line max 72 characters
- Use imperative mood ("add" not "added")
- No period at end of subject
- If complex, add a blank line then body (max 76 chars per line)
- Output ONLY the commit message, nothing else"""

def get_git_diff(staged=True):
    """Get git diff output."""
    cmd = ["git", "diff", "--cached"] if staged else ["git", "diff"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def get_git_diff_stat(staged=True):
    """Get git diff --stat for a summary view."""
    cmd = ["git", "diff", "--cached", "--stat"] if staged else ["git", "diff", "--stat"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def get_new_files():
    """Get newly added files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=A"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def call_api(prompt, api_key=None, base_url=None, model=None):
    """Call OpenAI-compatible API."""
    api_key = api_key or os.environ.get("AI_COMMIT_API_KEY") or os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY", "")
    base_url = base_url or os.environ.get("AI_COMMIT_BASE_URL", "https://api.deepseek.com/v1")
    model = model or os.environ.get("AI_COMMIT_MODEL", "deepseek-chat")

    base_url = base_url.rstrip("/")
    url = f"{base_url}/chat/completions"

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 300
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data["choices"][0]["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"API Error {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def build_prompt(diff, stat, new_files):
    """Build the prompt for the API."""
    parts = ["Generate a commit message for the following changes.\n"]

    if new_files:
        parts.append(f"New files added:\n{new_files}\n")

    if stat:
        parts.append(f"Change summary:\n{stat}\n")

    # Truncate diff if too long (keep first 4000 chars)
    if len(diff) > 4000:
        diff = diff[:4000] + "\n... (diff truncated)"

    parts.append(f"Full diff:\n{diff}")
    return "\n".join(parts)

def main():
    parser = argparse.ArgumentParser(
        prog="git-ai-commit",
        description="Generate AI-powered commit messages from git diffs"
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-a", "--all", action="store_true", help="Use unstaged changes (default: staged)")
    parser.add_argument("-m", "--model", help="AI model name (default: deepseek-chat)")
    parser.add_argument("-k", "--api-key", help="API key (or set AI_COMMIT_API_KEY env)")
    parser.add_argument("-u", "--base-url", help="API base URL (or set AI_COMMIT_BASE_URL env)")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto-commit with generated message")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Print message only, don't commit")
    parser.add_argument("--amend", action="store_true", help="Amend the last commit message")

    args = parser.parse_args()

    # Check if in a git repo
    try:
        subprocess.run(["git", "rev-parse", "--git-dir"],
                       capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: Not a git repository", file=sys.stderr)
        sys.exit(1)

    staged = not args.all
    diff = get_git_diff(staged)
    stat = get_git_diff_stat(staged)
    new_files = get_new_files()

    if not diff.strip():
        if staged:
            print("No staged changes. Use -a for unstaged changes, or stage files first with: git add <files>")
        else:
            print("No changes detected.")
        sys.exit(1)

    print("Analyzing changes...", file=sys.stderr)
    prompt = build_prompt(diff, stat, new_files)
    message = call_api(prompt, api_key=args.api_key, base_url=args.base_url, model=args.model)

    if args.dry_run:
        print(message)
        sys.exit(0)

    print(f"\nGenerated commit message:\n")
    print(f"  {message}\n")

    if args.yes:
        do_commit = True
    else:
        try:
            answer = input("Use this message? (Y/n/edit): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            sys.exit(0)

        if answer == "n":
            print("Cancelled.")
            sys.exit(0)
        elif answer == "edit":
            print("Enter your commit message (Ctrl+D to finish):")
            lines = []
            try:
                while True:
                    lines.append(input())
            except EOFError:
                pass
            message = "\n".join(lines).strip()
            if not message:
                print("Empty message. Cancelled.")
                sys.exit(1)
        do_commit = True

    if do_commit:
        if args.amend:
            subprocess.run(["git", "commit", "--amend", "-m", message], check=True)
        else:
            subprocess.run(["git", "commit", "-m", message], check=True)
        print("Committed!")

if __name__ == "__main__":
    main()
