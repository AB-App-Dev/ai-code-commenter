import ollama
from pathlib import Path

MODEL = "deepseek-coder:6.7b"

SUPPORTED_EXTENSIONS = {".tsx", ".ts", ".jsx", ".js"}

def detect_language(file_path: Path) -> str:
    ext = file_path.suffix
    return {
        ".tsx": "TypeScript React (TSX)",
        ".ts": "TypeScript",
        ".jsx": "JavaScript React (JSX)",
        ".js": "JavaScript",
    }.get(ext, "JavaScript")

def check_ollama():
    try:
        ollama.list()
    except Exception:
        raise RuntimeError("❌ Ollama is not running. Start it with: ollama serve")

def strip_code_fences(result: str) -> str:
    lines = result.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.startswith("```"):
            start = i + 1
            break
    end = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "```":
            end = i
            break
    return "\n".join(lines[start:end])

def add_comments_to_file(file_path: Path) -> str:
    code = file_path.read_text(encoding="utf-8")
    lang = detect_language(file_path)

    prompt = f"""You are a senior developer. Add clear, concise comments to the following {lang} code.
Rules:
- Place comments on their OWN LINE above the code they describe, never at the end of a line
- Use // for single line comments
- Use /* */ for multi-line comments
- Do not modify the code itself, only add comments
- Return ONLY the commented code, no explanations outside the code

```{file_path.suffix.strip(".")}
{code}
```"""

    response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])

    result = response.get("message", {}).get("content", None)
    if not result:
        raise ValueError(f"Model returned empty response for {file_path.name}")

    return strip_code_fences(result)

def summarize_file(file_path: Path, commented_code: str) -> str:
    lang = detect_language(file_path)

    prompt = f"""Given this commented {lang} file named '{file_path.name}', 
write a short markdown summary explaining:
- What this file/component does
- Key props, state, or exports
- Any important logic or side effects

Code:
{commented_code}"""

    response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])

    result = response.get("message", {}).get("content", None)
    if not result:
        raise ValueError(f"Model returned empty summary for {file_path.name}")

    return result