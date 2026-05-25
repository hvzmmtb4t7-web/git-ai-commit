# git-ai-commit

> One command. Perfect commit messages. Powered by AI.

Generate conventional commit messages from your `git diff` using any OpenAI-compatible API (DeepSeek, GPT, Claude, local models).

> **一行命令，AI 帮你写 commit message。**
>
> 从 `git diff` 自动生成规范的 commit message，支持 DeepSeek、GPT、Claude 或任何 OpenAI 兼容 API。零依赖，Python 3.7+ 标准库即可运行。

## Install / 安装

```bash
# Clone & use / 克隆使用
git clone https://github.com/hvzmmtb4t7-web/git-ai-commit.git
cd git-ai-commit

# Or just copy git_ai_commit.py to your PATH / 或者直接复制到 PATH
cp git_ai_commit.py /usr/local/bin/git-ai-commit
chmod +x /usr/local/bin/git-ai-commit
```

**Zero dependencies** — only Python 3.7+ stdlib.

**零依赖** — 只需 Python 3.7+ 标准库。

## Quick Start / 快速开始

```bash
# Set your API key / 设置 API Key
export AI_COMMIT_API_KEY="sk-xxx"
export AI_COMMIT_BASE_URL="https://api.deepseek.com/v1"  # or api.openai.com, etc.
export AI_COMMIT_MODEL="deepseek-chat"                    # or gpt-4o, claude-3-5-sonnet, etc.

# Stage your changes / 暂存你的修改
git add .

# Generate & commit / 生成并提交
python git_ai_commit.py -y
```

## Usage / 用法

```bash
# Generate message for staged changes (default) / 为暂存区的修改生成 message（默认）
python git_ai_commit.py

# Preview only, don't commit / 仅预览，不提交
python git_ai_commit.py -d

# Use unstaged changes / 使用未暂存的修改
python git_ai_commit.py -a

# Auto-commit without prompt / 自动提交，不询问
python git_ai_commit.py -y

# Amend last commit message / 修改上一次的 commit message
python git_ai_commit.py --amend

# Override model/API per command / 单次命令覆盖模型/API
python git_ai_commit.py -k "sk-xxx" -u "https://api.deepseek.com/v1" -m "deepseek-chat"
```

## Environment Variables / 环境变量

| Variable | Description / 说明 | Default / 默认值 |
|---|---|---|
| `AI_COMMIT_API_KEY` | API key / API 密钥 | (required) |
| `AI_COMMIT_BASE_URL` | API base URL / API 地址 | `https://api.deepseek.com/v1` |
| `AI_COMMIT_MODEL` | Model name / 模型名称 | `deepseek-chat` |

Also supports `OPENAI_API_KEY` and `DEEPSEEK_API_KEY` as fallbacks.

也支持 `OPENAI_API_KEY` 和 `DEEPSEEK_API_KEY` 作为备选。

## Supported APIs / 支持的 API

Any OpenAI-compatible API works / 任何 OpenAI 兼容 API 均可使用：

- **DeepSeek** — `https://api.deepseek.com/v1` (default, cheapest / 默认，最便宜)
- **OpenAI** — `https://api.openai.com/v1`
- **Claude** (via proxy) — any OpenAI-compatible endpoint
- **Local models / 本地模型** — Ollama, vLLM, LM Studio, etc.

## Output Format / 输出格式

Generates [Conventional Commits](https://www.conventionalcommits.org/) / 生成规范化的 commit message：

```
feat(auth): add OAuth2 login support

- Implement Google and GitHub OAuth providers
- Add token refresh logic
- Update user session handling
```

## Why? / 为什么用这个？

| Feature / 特性 | Description / 说明 |
|---|---|
| **Fast / 快** | One command instead of typing for 30 seconds / 一条命令搞定，不用手写30秒 |
| **Consistent / 统一** | Always follows conventional commits format / 始终遵循规范格式 |
| **Private / 私密** | Your code stays between you and your API / 代码只在你和 API 之间传输 |
| **Flexible / 灵活** | Works with any OpenAI-compatible API / 兼容所有 OpenAI 格式 API |
| **Zero deps / 零依赖** | Just Python stdlib, no pip install / 只用标准库，无需 pip install |

## License

MIT
