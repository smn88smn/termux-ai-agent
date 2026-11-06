import requests
import json
from typing import List, Dict, Optional
from pathlib import Path

from config.settings import OLLAMA_MODEL, OLLAMA_HOST, PROJECTS_DIR
from core.tools import Tools
from prompts.system_prompt import SYSTEM_PROMPT

class MFAIAgent:
    """مغز اصلی MF AI — نسخه سبک و سازگار با Termux"""

    def __init__(self):
        self.model = OLLAMA_MODEL
        self.host = OLLAMA_HOST.rstrip("/")
        self.tools = Tools()
        self.conversation: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    def chat(self, user_message: str) -> str:
        """چت با مدل از طریق API مستقیم Ollama"""
        self.conversation.append({"role": "user", "content": user_message})

        try:
            response = requests.post(
                f"{self.host}/api/chat",
                json={
                    "model": self.model,
                    "messages": self.conversation,
                    "stream": False,
                    "options": {
                        "temperature": 0.35,
                        "num_ctx": 4096,
                    }
                },
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            assistant_message = data.get("message", {}).get("content", "پاسخی دریافت نشد.")
            self.conversation.append({"role": "assistant", "content": assistant_message})
            return assistant_message
        except requests.exceptions.ConnectionError:
            return (
                "نمی‌توانم به Ollama وصل شوم.\n"
                "این دستور را بزن:\n"
                "  ollama serve &\n"
                "بعد دوباره امتحان کن."
            )
        except Exception as e:
            return f"خطا در ارتباط با مدل:\n{e}"

    def create_project(self, name: str) -> str:
        return self.tools.create_project(name)

    def set_project(self, name: str) -> str:
        return self.tools.set_project(name)

    def list_projects(self) -> str:
        return self.tools.list_projects()

    def build_current_project(self, release: bool = False) -> str:
        return self.tools.build_apk(release=release)

    def setup_android_sdk(self) -> str:
        return self.tools.setup_sdk()

    def show_status(self):
        sdk_ready = False
        try:
            sdk_ready = self.tools.sdk_manager.is_sdk_ready()
        except:
            pass

        print("=" * 40)
        print("MF AI — Mini Fire AI")
        print(f"مدل: {self.model}")
        print(f"پروژه فعال: {self.tools.current_project or 'هیچ'}")
        print(f"SDK آماده: {'بله' if sdk_ready else 'خیر'}")
        print(f"مسیر پروژه‌ها: {PROJECTS_DIR}")
        print("=" * 40)
