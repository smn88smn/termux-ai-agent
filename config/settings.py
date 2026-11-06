from pathlib import Path
import os

# مسیرهای مخصوص Termux
HOME = Path(os.environ.get("HOME", Path.home()))
BASE_DIR = Path(__file__).parent.parent

# مسیرهای کاری
PROJECTS_DIR = HOME / ".mf-ai" / "projects"
SDK_DIR = HOME / ".mf-ai" / "android-sdk"
CMDLINE_TOOLS_DIR = HOME / ".mf-ai" / "cmdline-tools"
DATA_DIR = HOME / ".mf-ai"

# مدل Ollama
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# تنظیمات دانلود
DOWNLOAD_TIMEOUT = 120
MAX_RETRIES = 3

# نسخه Android SDK
ANDROID_API_LEVEL = "34"
BUILD_TOOLS_VERSION = "34.0.0"

# ایجاد پوشه‌های لازم
for d in [PROJECTS_DIR, SDK_DIR, CMDLINE_TOOLS_DIR, DATA_DIR]:
    d.mkdir(parents=True, exist_ok=True)
