# local-code-interpreter

> A zero-dependency, zero-config skill that gives your AI agent the ability to execute Python code and shell commands **directly on your local machine**.

No AWS. No API keys. No cold starts. Just Python.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Allen091080/local-code-interpreter/releases/tag/v1.0.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-green)](https://skills.sh)

---

## Features

- ✅ Execute Python code inline or from files
- ✅ Run shell commands natively
- ✅ Full pandas / numpy / matplotlib support out of the box
- ✅ Chinese chart labels (PingFang HK on macOS, WenQuanYi on Linux)
- ✅ Works offline
- ✅ Compatible with OpenClaw / CodeBuddy / Claude Code / Cursor

## Requirements

| Tool | Version |
|------|---------|
| Python | 3.10+ |
| OS | macOS or Linux |

No extra Python packages are required at install time — the skill installs missing libraries on demand via `pip3 install`.

## Installation

```bash
npx skills add https://github.com/Allen091080/local-code-interpreter -g -y
```

Or manually copy `SKILL.md` and `scripts/` into your agent's skill directory:

```
~/.workbuddy/skills/local-code-interpreter/
~/.claude/skills/local-code-interpreter/
~/.agents/skills/local-code-interpreter/
```

## Quick Start

Once the skill is loaded, just ask your agent:

```
帮我用 pandas 分析这个 CSV 文件
画一个柱状图显示每月营收
用 Python 计算这组数据的标准差
```

The agent will automatically write and execute the code locally.

## Usage — Direct CLI

```bash
# Run a code string
python3 scripts/run.py --code "import sys; print(sys.version)"

# Run a file
python3 scripts/run.py --file /tmp/my_analysis.py

# Suppress header output
python3 scripts/run.py --code "print(42)" --no-header
```

## Example: Chart with Chinese Labels

```python
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'PingFang HK'   # macOS
months = ['1月','2月','3月','4月','5月','6月']
revenue = [12, 19, 15, 25, 22, 30]

plt.figure(figsize=(8, 4))
plt.plot(months, revenue, 'o-', color='#2196F3', linewidth=2)
plt.title('上半年营收趋势（万元）')
plt.tight_layout()
plt.savefig('/tmp/chart.png', dpi=150, bbox_inches='tight')
print('Saved: /tmp/chart.png')
```

## Repository Structure

```
local-code-interpreter/
├── SKILL.md              # Agent skill definition
├── scripts/
│   └── run.py            # Core execution script
├── README.md             # This file
├── LICENSE               # MIT License
└── .github/
    └── workflows/
        └── test.yml      # CI — smoke test on push
```

## Security Notes

- Code runs with **your user's permissions** — the same as if you ran it in a terminal.
- There is no sandboxing. Only use this skill in contexts you trust.
- Do not expose this skill to untrusted input sources.

## License

MIT © 2026
