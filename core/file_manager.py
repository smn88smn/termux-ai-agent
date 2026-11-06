from pathlib import Path
from typing import Optional, Union
import shutil


class FileManager:
    """مدیریت ساخت، خواندن، نوشتن و حذف فایل‌ها"""

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def create_file(self, relative_path: str, content: str = "") -> Path:
        """ساخت فایل جدید با محتوای مشخص"""
        file_path = self.base_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return file_path

    def read_file(self, relative_path: str) -> str:
        """خواندن محتوای فایل"""
        file_path = self.base_path / relative_path
        if not file_path.exists():
            raise FileNotFoundError(f"فایل پیدا نشد: {relative_path}")
        return file_path.read_text(encoding="utf-8")

    def append_to_file(self, relative_path: str, content: str) -> Path:
        """اضافه کردن محتوا به انتهای فایل"""
        file_path = self.base_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(content)
        return file_path

    def delete_file(self, relative_path: str) -> bool:
        """حذف فایل"""
        file_path = self.base_path / relative_path
        if file_path.exists() and file_path.is_file():
            file_path.unlink()
            return True
        return False

    def create_directory(self, relative_path: str) -> Path:
        """ساخت پوشه"""
        dir_path = self.base_path / relative_path
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def list_files(self, relative_path: str = ".") -> list[str]:
        """لیست فایل‌ها و پوشه‌ها"""
        target = self.base_path / relative_path
        if not target.exists():
            return []
        return [str(p.relative_to(self.base_path)) for p in target.rglob("*")]

    def file_exists(self, relative_path: str) -> bool:
        return (self.base_path / relative_path).exists()

    def get_absolute_path(self, relative_path: str) -> Path:
        return self.base_path / relative_path
