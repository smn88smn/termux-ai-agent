import requests
from pathlib import Path
from typing import Optional
import hashlib


class Downloader:
    """دانلود فایل با اینترنت کاربر"""

    def __init__(self, timeout: int = 120, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MF-AI/1.0 (Mini Fire AI)"
        })

    def download(self, url: str, save_path: Path, expected_sha256: Optional[str] = None) -> Path:
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        for attempt in range(1, self.max_retries + 1):
            try:
                print(f"در حال دانلود: {url}")
                response = self.session.get(url, stream=True, timeout=self.timeout)
                response.raise_for_status()

                total_size = int(response.headers.get("content-length", 0))
                downloaded = 0

                with open(save_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                percent = (downloaded / total_size) * 100
                                print(f"\rپیشرفت: {percent:.1f}%", end="", flush=True)

                print()  # خط جدید

                if expected_sha256:
                    if not self._verify_sha256(save_path, expected_sha256):
                        save_path.unlink(missing_ok=True)
                        raise ValueError("هش فایل مطابقت ندارد")

                return save_path

            except Exception as e:
                if attempt == self.max_retries:
                    raise RuntimeError(f"دانلود ناموفق بعد از {self.max_retries} تلاش: {e}")
                print(f"تلاش {attempt} ناموفق، دوباره تلاش می‌کنم...")

        raise RuntimeError("دانلود ناموفق")

    def _verify_sha256(self, file_path: Path, expected: str) -> bool:
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest().lower() == expected.lower()

    def download_text(self, url: str) -> str:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.text
