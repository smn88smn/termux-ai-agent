import os
import subprocess
import sys

print("🤖 سیستم چند ایجنتی (Multi-Agent) ترموکس با ساختار پاکسازی‌شده فعال شد...")
print("--------------------------------------------------")

def run_command(command):
    print(f"⚙️ در حال اجرای دستور: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"❌ خطا در اجرا:\n{stderr}")
        return False, stderr
    else:
        print(f"✅ خروجی موفق:\n{stdout}")
        return True, stdout

def coder_agent(task_description):
    print(f"\n👨‍💻 [ایجنت برنامه‌نویس]: در حال ساخت ساختار پروژه برای: '{task_description}'")
    
    os.makedirs("app_source", exist_ok=True)
    file_name = os.path.join("app_source", "main.py")
    
    lower_task = task_description.lower()
    if "ماشین حساب" in lower_task or "calculator" in lower_task:
        code_content = '''# ماشین حساب پایتونی برای اندروید
def main():
    print("🧮 ماشین حساب موبایلی فعال شد!")
    a = 20
    b = 10
    print(f"جمع: {a + b}")
    print(f"تفریق: {a - b}")
    print(f"ضرب: {a * b}")
    print(f"تقسیم: {a / b}")

if __name__ == "__main__":
    main()
'''
    elif "بازی" in lower_task or "game" in lower_task:
        code_content = """# بازی ساده پایتونی
import random

def main():
    print("🎮 بازی موبایلی ایجنت اجرا شد!")
    print(f"عدد شانس: {random.randint(1, 100)}")

if __name__ == "__main__":
    main()
"""
    else:
        code_content = f'''# فایل اصلی پروژه
def main():
    print("🚀 اپلیکیشن شما اجرا شد.")
    print("هدف: {task_description}")

if __name__ == "__main__":
    main()
'''

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(code_content)
        
    build_spec = os.path.join("app_source", "buildozer.spec")
    if not os.path.exists(build_spec):
        with open(build_spec, "w", encoding="utf-8") as f:
            f.write("""[app]
title = MyAgentApp
package.name = myagentapp
package.domain = org.test
source.include_exts = py
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
""")

    # تنظیمات کاملاً استاندارد گیت‌هاب اکشنز برای بیلد
    workflow_dir = os.path.join(".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    workflow_file = os.path.join(workflow_dir, "build_apk.yml")
    
    workflow_content = """name: Build Android APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Build with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        with:
          workdir: app_source
          command: buildozer android debug

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: app-release-debug
          path: app_source/bin/*.apk
"""
    with open(workflow_file, "w", encoding="utf-8") as f:
        f.write(workflow_content)

    print(f"📁 ساختار پروژه در پوشه app_source آماده شد.")
    return "app_source"

def git_agent(commit_message):
    print("\n📦 [ایجنت گیت]: در حال ارسال به گیت‌هاب...")
    
    run_command("git add .")
    success, _ = run_command(f'git commit -m "Update build for: {commit_message}"')
    
    if success:
        run_command("git pull origin main --rebase")
        push_success, _ = run_command("git push origin main")
        if push_success:
            print("🚀 کدها با موفقیت پوش شدند!")
        else:
            print("⚠️ خطا در پوش کردن.")
    else:
        print("ℹ️ تغییر جدیدی نبود.")

def main():
    while True:
        user_input = input("\n💬 دستورت رو به ایجنت بگو (یا برای خروج 'exit' رو بزن): ")
        if user_input.lower() == 'exit':
            print("👋 خدانگهدار داداش!")
            break
        if not user_input.strip():
            continue
            
        print(f"\n🧠 [مدیر پروژه]: دستور دریافت شد -> '{user_input}'")
        target_dir = coder_agent(user_input)
        
        print("\n🧪 [ایجنت تست و عیب‌یاب]: بررسی سینتکس...")
        success, _ = run_command(f"python -m py_compile {target_dir}/main.py")
        
        if success:
            print("🎉 تست سینتکس موفق بود!")
            git_agent(user_input)
        else:
            print("⚠️ خطا در کد.")

if __name__ == "__main__":
    main()

