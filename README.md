# 🤖 ai-code-commenter

A CLI tool that uses a **local AI model** (via [Ollama](https://ollama.com)) to automatically add inline comments to your code and generate a `DOCS.md` documentation file.

No API keys. No cloud. Runs 100% locally and for free.

---

## ✨ Features

- 📝 Adds inline comments to `.ts`, `.tsx`, `.js`, `.jsx` files
- 📄 Generates a `DOCS.md` with a summary of each file
- 💾 Optional `--backup` flag to save originals before overwriting
- 👁 `--dry-run` mode to preview without changing anything
- 🔀 Swap AI models on the fly with `--model`
- 🔍 Auto-detects file language (TypeScript, JavaScript, React)
- ✅ Friendly error if Ollama isn't running

---

## 🧱 Tech Stack

| Tool | Purpose |
|---|---|
| [Python](https://python.org) | Core language |
| [Ollama](https://ollama.com) | Local LLM runner |
| [deepseek-coder](https://ollama.com/library/deepseek-coder) | Default AI model |
| [Typer](https://typer.tiangolo.com) | CLI framework |
| [Rich](https://rich.readthedocs.io) | Terminal formatting |

---

## ⚙️ Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running
- [pipx](https://pipx.pypa.io)

---

## ⚙️ Installation

**1. Install and start Ollama**

Download from [ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull deepseek-coder:6.7b
```

**2. Install the CLI tool**

```bash
cd ai-code-commenter
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

**3. Add the alias so `comment-code` works from anywhere**

```bash
echo 'alias comment-code="/path/to/ai-code-commenter/venv/bin/comment-code"' >> ~/.zshrc
source ~/.zshrc
```

> Replace `/path/to/` with your actual project path. For example:
> `/Users/user/Documents/htdocs/AI/ai-code-commenter/venv/bin/comment-code`

---

### ⚠️ Command not found after opening a new terminal?

If you get `zsh: command not found: comment-code` in a new terminal session, the alias needs to be reloaded. Fix it with:

```bash
source ~/.zshrc
```

To verify the alias is saved correctly:
```bash
cat ~/.zshrc
```

You should see a line like:
```bash
alias comment-code="/path/to/ai-code-commenter/venv/bin/comment-code"
```

If it's missing, re-run the `echo` command from Step 3 above. Once saved in `.zshrc` it will persist across all terminal sessions automatically.

---

## 🚀 Usage

### Single File

To add comments to a single file:

```bash
# Dry run first (no files modified)
comment-code src/App.tsx --dry-run

# Run for real with backup
comment-code src/App.tsx --backup
```

---

### All Files in a Project

The easiest way is to run from **inside your project folder**:

```bash
cd my-react-app
```

**Step 1 — Dry run first (no files are modified)**
```bash
comment-code . --dry-run
```

**Step 2 — Run for real with backup and generate docs**
```bash
comment-code . --backup --output DOCS.md
```

That's it! This will:
- 💾 Back up all original files before overwriting
- 📝 Add inline comments to all `.ts`, `.tsx`, `.js`, `.jsx` files
- 📄 Generate a `DOCS.md` in your project folder

---

### Running from outside the project folder

```bash
# Single file
comment-code ./my-react-app/src/App.tsx --dry-run
comment-code ./my-react-app/src/App.tsx --backup

# All files
comment-code ./my-react-app --dry-run
comment-code ./my-react-app --backup --output ./my-react-app/DOCS.md
```

---

## 🚀 All options

| Flag | Short | Default | Description |
|---|---:|---|---|
| `--output` | `-o` | `DOCS.md` | Output documentation filename |
| `--backup` | `-b` | `false` | Save original files before overwriting |
| `--dry-run` |  | `false` | Run without writing any files |
| `--model` | `-m` | `deepseek-coder:6.7b` | Ollama model to use |

---

## 🚀 Example Output

**Before (Button.tsx)**

```tsx
export const Button = ({ label, onClick, disabled }) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};
```

**After (Button.tsx)**

```tsx
// Button component — renders a clickable button with optional disabled state
export const Button = ({ label, onClick, disabled }) => {
  return (
    // Attach the onClick handler and pass the disabled prop to the native button
    <button onClick={onClick} disabled={disabled}>
      {/* Render the button label passed as a prop */}
      {label}
    </button>
  );
};
```

**Generated `DOCS.md` entry:**

```md
## `Button.tsx`

A simple reusable Button component that accepts a label string, an onClick
handler, and an optional disabled boolean. Renders a native HTML button
element styled and controlled via props.
```

---

## 🚀 Project Structure

```text
ai-code-commenter/
├── commenter/
│   ├── __init__.py
│   ├── cli.py          # CLI entry point and flags
│   ├── processor.py    # File reading, AI calls, language detection
│   └── docs_writer.py  # Markdown documentation generator
├── pyproject.toml
└── README.md
```

---

## 🚀 Supported Models

Any model available in Ollama works. Recommended for code:

| Model | Size | Command |
|---|---:|---|
| `deepseek-coder:6.7b` | ~4GB | `ollama pull deepseek-coder:6.7b` |
| `codellama:7b` | ~4GB | `ollama pull codellama:7b` |
| `qwen2.5-coder:7b` | ~4GB | `ollama pull qwen2.5-coder:7b` |

---

## 🚀 Why I Built This

When working on AI-assisted projects, generated code can be hard to understand at a glance.
This tool solves that by automatically annotating code with human-readable comments and
producing a documentation file — making codebases easier to onboard into and maintain.

Built as a portfolio project to demonstrate:

- Python CLI development
- Local LLM integration
- Developer tooling and UX thinking

---

## 🚀 License

MIT
