import typer
import shutil
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.progress import track
from .processor import (
    add_comments_to_file,
    summarize_file,
    check_ollama,
    SUPPORTED_EXTENSIONS,
)
from .docs_writer import write_docs

app = typer.Typer(help="AI-powered code commenter and documentation generator.")
console = Console()

def collect_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix in SUPPORTED_EXTENSIONS else []
    return [f for f in target.rglob("*") if f.suffix in SUPPORTED_EXTENSIONS]

def backup_file(file_path: Path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".backup_{timestamp}{file_path.suffix}")
    shutil.copy2(file_path, backup_path)
    return backup_path

@app.command()
def run(
    path: str = typer.Argument(..., help="Path to a folder or single file"),
    output: str = typer.Option("DOCS.md", "--output", "-o", help="Output documentation file"),
    backup: bool = typer.Option(False, "--backup", "-b", help="Backup original files before overwriting"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without writing any files"),
    model: str = typer.Option("deepseek-coder:6.7b", "--model", "-m", help="Ollama model to use"),
):
    """
    Add AI-generated comments to .ts/.tsx/.js/.jsx files and generate a DOCS.md.
    """

    # 1. Check Ollama is running
    console.print("🔍 Checking Ollama...", end=" ")
    try:
        check_ollama()
        console.print("[green]OK[/green]")
    except RuntimeError as e:
        console.print(f"\n[red]{e}[/red]")
        raise typer.Exit(code=1)

    # 2. Collect files
    target = Path(path)
    if not target.exists():
        console.print(f"[red]Path not found: {path}[/red]")
        raise typer.Exit(code=1)

    files = collect_files(target)
    if not files:
        console.print(f"[red]No supported files found. Supported: {SUPPORTED_EXTENSIONS}[/red]")
        raise typer.Exit(code=1)

    console.print(f"📁 Found [bold]{len(files)}[/bold] file(s) to process\n")

    # 3. Process each file
    summaries = {}
    for file in track(files, description="Processing..."):
        console.print(f"\n  📄 [bold]{file.name}[/bold] [dim]({file.suffix})[/dim]")

        try:
            commented = add_comments_to_file(file)
            summaries[file.name] = summarize_file(file, commented)

            if not dry_run:
                if backup:
                    backup_path = backup_file(file)
                    console.print(f"     💾 Backed up → [dim]{backup_path.name}[/dim]")
                file.write_text(commented, encoding="utf-8")
                console.print(f"     ✅ Comments written")
            else:
                console.print(f"     👁  Dry run — skipped writing")

        except Exception as e:
            console.print(f"     [red]❌ Failed: {e}[/red]")
            continue

    # 4. Write docs
    if not dry_run and summaries:
        docs_path = Path(output)
        write_docs(summaries, docs_path)
        console.print(f"\n📝 Documentation written to [bold]{docs_path}[/bold]")

    console.print("\n[green]✅ Done![/green]")

def main():
    app()