#!/usr/bin/env python3
"""
MF AI — Mini Fire AI
نسخه سبک و سازگار با Termux (بدون وابستگی سنگین)
"""

import os
from core.agent import MFAIAgent

def print_banner():
    print("""
╔══════════════════════════════════════╗
║           MF AI — Mini Fire AI       ║
║      از ایده تا APK  |  کاملاً رایگان ║
╚══════════════════════════════════════╝
""")

def print_help():
    print("""
دستورات اصلی:
  /new <نام>          ساخت پروژه جدید
  /open <نام>         باز کردن پروژه موجود
  /list               لیست پروژه‌ها
  /build              بیلد Debug
  /build-release      بیلد Release
  /sdk                نصب/بررسی SDK
  /status             وضعیت
  /help               راهنما
  /exit یا /quit      خروج

هر چیز دیگری را به عنوان پیام به AI بفرست.
""")

def main():
    # مدل پیش‌فرض
    if not os.getenv("OLLAMA_MODEL"):
        os.environ["OLLAMA_MODEL"] = "phi3:mini"

    print_banner()
    print("برای راهنما تایپ کن: /help\n")

    agent = MFAIAgent()
    agent.show_status()

    while True:
        try:
            user_input = input("\nتو: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("/exit", "/quit", "exit", "quit"):
                print("\nخداحافظ. بازی بساز و بدرخش.")
                break

            if user_input.lower() in ("/help", "help"):
                print_help()
                continue

            if user_input.lower() == "/status":
                agent.show_status()
                continue

            if user_input.lower() == "/list":
                print(agent.list_projects())
                continue

            if user_input.lower().startswith("/new "):
                name = user_input[5:].strip()
                if name:
                    print(agent.create_project(name))
                else:
                    print("نام پروژه را بنویس.")
                continue

            if user_input.lower().startswith("/open "):
                name = user_input[6:].strip()
                if name:
                    print(agent.set_project(name))
                else:
                    print("نام پروژه را بنویس.")
                continue

            if user_input.lower() == "/sdk":
                print(agent.setup_android_sdk())
                continue

            if user_input.lower() == "/build":
                print(agent.build_current_project(release=False))
                continue

            if user_input.lower() == "/build-release":
                print(agent.build_current_project(release=True))
                continue

            # پیام عادی به AI
            print("\nMF AI:")
            response = agent.chat(user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\nخروج...")
            break
        except Exception as e:
            print(f"خطای غیرمنتظره: {e}")

if __name__ == "__main__":
    main()
