from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


def print_banner():
    banner = """
╔══════════════════════════════════════╗
║           MF AI — Mini Fire AI       ║
║      از ایده تا APK  |  کاملاً رایگان ║
╚══════════════════════════════════════╝
"""
    console.print(banner, style="bold cyan")


def print_help():
    help_text = """
**دستورات اصلی:**

- `/new <نام>`          ساخت پروژه جدید
- `/open <نام>`         باز کردن پروژه موجود
- `/list`               لیست پروژه‌ها
- `/build`              بیلد Debug و ساخت APK
- `/build-release`      بیلد Release
- `/sdk`                نصب/بررسی Android SDK
- `/status`             وضعیت فعلی
- `/help`               راهنما
- `/exit` یا `/quit`    خروج

هر چیز دیگری را به عنوان پیام به AI بفرست.
"""
    console.print(Markdown(help_text))


def get_user_input() -> str:
    return Prompt.ask("\n[bold cyan]تو[/bold cyan]")
