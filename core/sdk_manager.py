import platform
import subprocess
import zipfile
import os
from pathlib import Path
from typing import Optional



from core.downloader import Downloader
from config.settings import SDK_DIR, CMDLINE_TOOLS_DIR, ANDROID_API_LEVEL, BUILD_TOOLS_VERSION




class SDKManager:
    """
    مدیریت نصب و استفاده از Android Command-line Tools + SDK
    همه چیز با اینترنت و فضای کاربر انجام می‌شود.
    """

    # لینک‌های رسمی گوگل
    CMDLINE_TOOLS_URLS = {
        "Windows": "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip",
        "Linux": "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip",
        "Darwin": "https://dl.google.com/android/repository/commandlinetools-mac-11076708_latest.zip",
    }

    def __init__(self):
        self.system = platform.system()
        # در Termux معمولاً Linux + aarch64 هستیم
        if self.system not in self.CMDLINE_TOOLS_URLS:
            self.system = "Linux"
        self.downloader = Downloader()
        self.sdk_dir = SDK_DIR
        self.cmdline_tools_dir = CMDLINE_TOOLS_DIR
        self.sdkmanager_path: Optional[Path] = None

    def is_sdk_ready(self) -> bool:
        """بررسی اینکه آیا SDK آماده استفاده است یا نه"""
        sdkmanager = self._find_sdkmanager()
        if not sdkmanager:
            return False

        # چک کردن وجود platform و build-tools
        platform_dir = self.sdk_dir / "platforms" / f"android-{ANDROID_API_LEVEL}"
        build_tools_dir = self.sdk_dir / "build-tools" / BUILD_TOOLS_VERSION
        return platform_dir.exists() and build_tools_dir.exists()

    def _find_sdkmanager(self) -> Optional[Path]:
        """پیدا کردن مسیر sdkmanager"""
        possible_paths = [
            self.cmdline_tools_dir / "bin" / "sdkmanager",
            self.cmdline_tools_dir / "latest" / "bin" / "sdkmanager",
            self.sdk_dir / "cmdline-tools" / "latest" / "bin" / "sdkmanager",
            self.sdk_dir / "tools" / "bin" / "sdkmanager",
        ]

        for path in possible_paths:
            if path.exists():
                self.sdkmanager_path = path
                return path
        return None

    def setup_sdk(self, force: bool = False) -> bool:
        """
        نصب کامل SDK در صورت نیاز.
        از کاربر اجازه می‌گیرد.
        """
        if self.is_sdk_ready() and not force:
            print("[green]✓ Android SDK آماده است.[/green]")
            return True

        print("\n[bold yellow]Android SDK پیدا نشد یا ناقص است.[/bold yellow]")
        print("برای ساخت APK نیاز به نصب Command-line Tools و SDK داریم.")
        print(f"مسیر نصب: [cyan]{self.sdk_dir}[/cyan]")
        print("حجم تقریبی: حدود ۴۰۰ تا ۸۰۰ مگابایت (بسته به پکیج‌ها)")
        print("تمام ترافیک و فضای دیسک از سیستم خودت استفاده می‌شود.\n")

        if not True:
            print("[red]نصب لغو شد.[/red]")
            return False

        try:
            self._install_cmdline_tools()
            self._install_required_packages()
            print("\n[bold green]✓ Android SDK با موفقیت نصب و آماده شد.[/bold green]")
            return True
        except Exception as e:
            print(f"[bold red]خطا در نصب SDK: {e}[/bold red]")
            return False

    def _install_cmdline_tools(self):
        """دانلود و نصب Command-line Tools"""
        if self.system not in self.CMDLINE_TOOLS_URLS:
            raise RuntimeError(f"سیستم‌عامل پشتیبانی نمی‌شود: {self.system}")

        url = self.CMDLINE_TOOLS_URLS[self.system]
        zip_path = self.cmdline_tools_dir / "cmdline-tools.zip"

        print("\n[cyan]در حال دانلود Command-line Tools...[/cyan]")
        self.downloader.download(url, zip_path)

        print("[cyan]در حال استخراج...[/cyan]")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.cmdline_tools_dir)

        # ساختار استاندارد گوگل: cmdline-tools/latest/bin/...
        extracted = list(self.cmdline_tools_dir.glob("*"))
        for item in extracted:
            if item.is_dir() and item.name.startswith("cmdline-tools"):
                target = self.cmdline_tools_dir / "latest"
                if target.exists():
                    import shutil
                    shutil.rmtree(target)
                item.rename(target)
                break

        zip_path.unlink(missing_ok=True)
        self._find_sdkmanager()

        if not self.sdkmanager_path:
            raise RuntimeError("sdkmanager بعد از نصب پیدا نشد")

        print("[green]✓ Command-line Tools نصب شد.[/green]")

    def _install_required_packages(self):
        """نصب پکیج‌های ضروری با sdkmanager"""
        if not self.sdkmanager_path:
            raise RuntimeError("sdkmanager در دسترس نیست")

        packages = [
            f"platforms;android-{ANDROID_API_LEVEL}",
            f"build-tools;{BUILD_TOOLS_VERSION}",
            "platform-tools",
        ]

        print("\n[cyan]در حال نصب پکیج‌های SDK...[/cyan]")
        print("این مرحله ممکن است چند دقیقه طول بکشد و لایسنس‌ها را باید بپذیری.\n")

        # تنظیم ANDROID_HOME
        env = os.environ.copy()
        env["ANDROID_HOME"] = str(self.sdk_dir)
        env["ANDROID_SDK_ROOT"] = str(self.sdk_dir)

        # پذیرش لایسنس‌ها
        licenses_cmd = [
            str(self.sdkmanager_path),
            f"--sdk_root={self.sdk_dir}",
            "--licenses"
        ]

        print("[yellow]لایسنس‌های گوگل را باید بپذیری (با تایپ y)[/yellow]")
        subprocess.run(licenses_cmd, env=env)

        # نصب پکیج‌ها
        install_cmd = [
            str(self.sdkmanager_path),
            f"--sdk_root={self.sdk_dir}",
            *packages
        ]

        result = subprocess.run(install_cmd, env=env, capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stderr)
            raise RuntimeError("نصب پکیج‌های SDK ناموفق بود")

        print("[green]✓ پکیج‌های ضروری نصب شدند.[/green]")

    def get_sdk_path(self) -> Path:
        return self.sdk_dir

    def get_env(self) -> dict:
        """محیط لازم برای بیلد Gradle"""
        env = os.environ.copy()
        env["ANDROID_HOME"] = str(self.sdk_dir)
        env["ANDROID_SDK_ROOT"] = str(self.sdk_dir)
        return env
