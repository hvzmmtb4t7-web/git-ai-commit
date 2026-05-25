# git-ai-commit

> One command. Perfect commit messages. Powered by AI.

Generate conventional commit messages from your `git diff` using any OpenAI-compatible API (DeepSeek, GPT, Claude, local models).

## Install

```bash
# Clone & use
git clone https://github.com/hvzmmtb4t7-web/git-ai-commit.git
cd git-ai-commit

# Or just copy git_ai_commit.py to your PATH
cp git_ai_commit.py /usr/local/bin/git-ai-commit
chmod +x /usr/local/bin/git-ai-commit
```

**Zero dependencies** — only Python 3.7+ stdlib.

## Quick Start

```bash
# Set your API key (pick one)
export AI_COMMIT_API_KEY="sk-xxx"
export AI_COMMIT_BASE_URL="https://api.deepseek.com/v1"  # or api.openai.com, etc.
export AI_COMMIT_MODEL="deepseek-chat"                    # or gpt-4o, claude-3-5-sonnet, etc.

# Stage your changes
git add .

# Generate & commit
python git_ai_commit.py -y
```

## Usage

```bash
# Generate message for staged changes (default)
python git_ai_commit.py

# Preview only, don't commit
python git_ai_commit.py -d

# Use unstaged changes
python git_ai_commit.py -a

# Auto-commit without prompt
python git_ai_commit.py -y

# Amend last commit message
python git_ai_commit.py --amend

# Override model/API per command
python git_ai_commit.py -k "sk-xxx" -u "https://api.deepseek.com/v1" -m "deepseek-chat"
```

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `AI_COMMIT_API_KEY` | API key | (required) |
| `AI_COMMIT_BASE_URL` | API base URL | `https://api.deepseek.com/v1` |
| `AI_COMMIT_MODEL` | Model name | `deepseek-chat` |

Also supports `OPENAI_API_KEY` and `DEEPSEEK_API_KEY` as fallbacks.

## Supported APIs

Any OpenAI-compatible API works:

- **DeepSeek** — `https://api.deepseek.com/v1` (default, cheapest)
- **OpenAI** — `https://api.openai.com/v1`
- **Claude** (via proxy) — any OpenAI-compatible endpoint
- **Local models** — Ollama, vLLM, LM Studio, etc.

## Output Format

Generates [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(auth): add OAuth2 login support

- Implement Google and GitHub OAuth providers
- Add token refresh logic
- Update user session handling
```

## Why?

- **Fast** — one command instead of typing for 30 seconds
- **Consistent** — always follows conventional commits format
- **Private** — your code stays between you and your API
- **Flexible** — works with any OpenAI-compatible API
- **Zero deps** — just Python stdlib, no pip install needed

## License

MIT
