import subprocess
from pathlib import Path
from typing import Optional


from core.sdk_manager import SDKManager




class APKBuilder:
    """بیلد پروژه اندروید و تولید فایل APK"""

    def __init__(self, sdk_manager: SDKManager):
        self.sdk_manager = sdk_manager

    def build(self, project_path: Path, release: bool = False) -> Optional[Path]:
        """
        بیلد پروژه و برگرداندن مسیر فایل APK
        """
        project_path = Path(project_path)

        if not project_path.exists():
            print(f"[red]مسیر پروژه وجود ندارد: {project_path}[/red]")
            return None

        # اطمینان از آماده بودن SDK
        if not self.sdk_manager.is_sdk_ready():
            print("[yellow]SDK آماده نیست. در حال آماده‌سازی...[/yellow]")
            if not self.sdk_manager.setup_sdk():
                return None

        # پیدا کردن gradlew
        gradlew = self._find_gradlew(project_path)
        if not gradlew:
            print("[red]فایل gradlew در پروژه پیدا نشد.[/red]")
            print("پروژه باید یک پروژه استاندارد Gradle اندروید باشد.")
            return None

        # دستور بیلد
        task = "assembleRelease" if release else "assembleDebug"
        cmd = [str(gradlew), task, "--no-daemon"]

        print(f"\n[bold cyan]در حال بیلد پروژه ({task})...[/bold cyan]")
        print(f"مسیر: {project_path}\n")

        env = self.sdk_manager.get_env()

        try:
            result = subprocess.run(
                cmd,
                cwd=str(project_path),
                env=env,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print("[bold red]بیلد ناموفق بود:[/bold red]")
                print(result.stderr[-2000:] if result.stderr else result.stdout[-2000:])
                return None

            # پیدا کردن فایل APK
            apk_path = self._find_apk(project_path, release)
            if apk_path:
                print(f"\n[bold green]✓ APK با موفقیت ساخته شد:[/bold green]")
                print(f"[cyan]{apk_path}[/cyan]")
                return apk_path
            else:
                print("[yellow]بیلد موفق بود اما فایل APK پیدا نشد.[/yellow]")
                return None

        except Exception as e:
            print(f"[bold red]خطا در اجرای بیلد: {e}[/bold red]")
            return None

    def _find_gradlew(self, project_path: Path) -> Optional[Path]:
        """پیدا کردن gradlew یا gradlew.bat"""
        candidates = [
            project_path / "gradlew",
            project_path / "gradlew.bat",
        ]
        for c in candidates:
            if c.exists():
                # در لینوکس/مک باید اجرایی باشد
                if c.name == "gradlew":
                    c.chmod(0o755)
                return c
        return None

    def _find_apk(self, project_path: Path, release: bool) -> Optional[Path]:
        """جستجو برای فایل APK ساخته شده"""
        build_dir = project_path / "app" / "build" / "outputs" / "apk"
        if not build_dir.exists():
            # بعضی پروژه‌ها ساختار متفاوتی دارند
            build_dir = project_path / "build" / "outputs" / "apk"

        if not build_dir.exists():
            return None

        pattern = "**/release/*.apk" if release else "**/debug/*.apk"
        apks = list(build_dir.glob(pattern))

        if not apks:
            # هر APKی که پیدا شد
            apks = list(build_dir.rglob("*.apk"))

        if apks:
            # جدیدترین فایل
            return max(apks, key=lambda p: p.stat().st_mtime)
        return None
