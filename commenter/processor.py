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

def add_comments_to_file(file_path: Path) -> str:
    code = file_path.read_text(encoding="utf-8")
    lang = detect_language(file_path)

    prompt = f"""You are a senior developer. Add clear, concise inline comments to the following {lang} code.
Explain what each section, function, and important line does.
Return ONLY the commented code, no explanations outside the code.

```{file_path.suffix.strip(".")}
{code}
```"""

    response = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

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
    return response["message"]["content"]