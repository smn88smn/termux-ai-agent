import subprocess
import os
from pathlib import Path
from typing import Optional


from config.settings import PROJECTS_DIR, SDK_DIR
from core.file_manager import FileManager
from core.downloader import Downloader
from core.sdk_manager import SDKManager
from builders.apk_builder import APKBuilder




class Tools:
    """ابزارهایی که ایجنت می‌تواند واقعاً اجرا کند"""

    def __init__(self):
        self.file_manager = FileManager(PROJECTS_DIR)
        self.downloader = Downloader()
        self.sdk_manager = SDKManager()
        self.apk_builder = APKBuilder(self.sdk_manager)
        self.current_project: Optional[str] = None

    def set_project(self, name: str) -> str:
        project_path = PROJECTS_DIR / name
        if not project_path.exists():
            return f"پروژه «{name}» وجود ندارد."
        self.current_project = name
        self.file_manager = FileManager(project_path)
        return f"پروژه «{name}» فعال شد.\nمسیر: {project_path}"

    def create_project(self, name: str) -> str:
        project_path = PROJECTS_DIR / name
        project_path.mkdir(parents=True, exist_ok=True)
        self.current_project = name
        self.file_manager = FileManager(project_path)
        return f"پروژه «{name}» ساخته شد.\nمسیر: {project_path}"

    def list_projects(self) -> str:
        projects = [p.name for p in PROJECTS_DIR.iterdir() if p.is_dir()]
        if not projects:
            return "هیچ پروژه‌ای وجود ندارد."
        result = "پروژه‌های موجود:\n"
        for p in projects:
            mark = " ← فعال" if p == self.current_project else ""
            result += f"• {p}{mark}\n"
        return result.strip()

    def create_file(self, relative_path: str, content: str = "") -> str:
        if not self.current_project:
            return "اول یک پروژه بساز یا باز کن (/new یا /open)."
        try:
            path = self.file_manager.create_file(relative_path, content)
            return f"فایل ساخته شد: {path}"
        except Exception as e:
            return f"خطا در ساخت فایل: {e}"

    def read_file(self, relative_path: str) -> str:
        if not self.current_project:
            return "اول یک پروژه فعال کن."
        try:
            content = self.file_manager.read_file(relative_path)
            return f"محتوای {relative_path}:\n\n{content}"
        except Exception as e:
            return f"خطا: {e}"

    def list_files(self, relative_path: str = ".") -> str:
        if not self.current_project:
            return "اول یک پروژه فعال کن."
        files = self.file_manager.list_files(relative_path)
        if not files:
            return "فایلی پیدا نشد."
        return "فایل‌ها:\n" + "\n".join(f"• {f}" for f in files[:50])

    def run_command(self, command: str) -> str:
        """اجرای دستور در شل Termux"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
                cwd=str(PROJECTS_DIR / self.current_project) if self.current_project else str(PROJECTS_DIR)
            )
            output = result.stdout + result.stderr
            if len(output) > 3000:
                output = output[:3000] + "\n... (خروجی کوتاه شد)"
            return output or "(خروجی خالی)"
        except subprocess.TimeoutExpired:
            return "دستور بیش از حد طول کشید (timeout)."
        except Exception as e:
            return f"خطا در اجرای دستور: {e}"

    def download_file(self, url: str, save_name: str) -> str:
        if not self.current_project:
            return "اول یک پروژه فعال کن."
        try:
            save_path = self.file_manager.get_absolute_path(save_name)
            self.downloader.download(url, save_path)
            return f"دانلود شد: {save_path}"
        except Exception as e:
            return f"خطا در دانلود: {e}"

    def setup_sdk(self) -> str:
        success = self.sdk_manager.setup_sdk()
        if success:
            return "SDK آماده است."
        return "نصب SDK ناموفق بود یا توسط کاربر لغو شد."

    def build_apk(self, release: bool = False) -> str:
        if not self.current_project:
            return "اول یک پروژه فعال کن."
        project_path = PROJECTS_DIR / self.current_project
        apk = self.apk_builder.build(project_path, release=release)
        if apk:
            return f"APK ساخته شد:\n{apk}"
        return "بیلد ناموفق بود. جزئیات در خروجی بالا آمده."
