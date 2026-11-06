import os
import subprocess
import sys

print("🤖 سیستم چند ایجنتی (Multi-Agent) ترموکس با قابلیت ساخت APK در گیت‌هاب فعال شد...")
print("--------------------------------------------------")

def run_command(command):
    """تابع اجرایی برای دستورات گیت و سیستمی"""
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
    """ایجنت برنامه‌نویس: فایل‌های کامل پروژه، بیلدوزر و گیت‌هاب اکشنز را می‌سازد"""
    print(f"\n👨‍💻 [ایجنت برنامه‌نویس]: در حال ساخت ساختار کامل پروژه برای: '{task_description}'")
    
    # ۱. ساخت پوشه اصلی پروژه
    os.makedirs("app_source", exist_ok=True)
    file_name = os.path.join("app_source", "main.py")
    
    lower_task = task_description.lower()
    if "ماشین حساب" in lower_task or "calculator" in lower_task:
        code_content = '''# ماشین حساب پیشرفته پایتونی برای اندروید
def main():
    print("🧮 ماشین حساب موبایلی فعال شد!")
    num1 = 10
    num2 = 5
    print(f"جمع {num1} و {num2} برابر است با: {num1 + num2}")
    print(f"تفریق: {num1 - num2}")
    print(f"ضرب: {num1 * num2}")
    print(f"تقسیم: {num1 / num2}")

if __name__ == "__main__":
    main()
'''
    elif "بازی" in lower_task or "game" in lower_task:
        code_content = """# کدهای بازی پایتونی برای اندروید
import random

def main():
    print("🎮 بازی موبایلی ایجنت اجرا شد!")
    number = random.randint(1, 10)
    print(f"عدد شانس اندروید: {number}")

if __name__ == "__main__":
    main()
"""
    else:
        code_content = f'''# فایل اصلی پروژه برای: {task_description}
def main():
    print("🚀 اپلیکیشن اندروید شما با موفقیت اجرا شد.")
    print("هدف پروژه: {task_description}")

if __name__ == "__main__":
    main()
'''

    with open(file_name, "w", encoding="utf-8") as f:
        f.write(code_content)
        
    # ۲. ساخت فایل تنظیمات Buildozer
    build_spec = os.path.join("app_source", "buildozer.spec")
    if not os.path.exists(build_spec):
        with open(build_spec, "w", encoding="utf-8") as f:
            f.write("""[app]
title = AgentApp
package.name = agentapp
package.domain = org.agent
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
""")

    # ۳. ساخت فایل GitHub Actions (.github/workflows/build.yml) برای اینکه گیت‌هاب خودکار APK بسازه
    workflow_dir = os.path.join(".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    workflow_file = os.path.join(workflow_dir, "build_apk.yml")
    
    workflow_content = """name: Build Android APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Build with Buildozer
        uses: ArtemSBulgakov/buildozer-action@v1
        id: buildozer
        with:
          workdir: app_source
          command: buildozer android debug

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v3
        with:
          name: package
          path: app_source/bin/*.apk
"""
    with open(workflow_file, "w", encoding="utf-8") as f:
        f.write(workflow_content)

    print(f"📁 فایل‌های پروژه، Buildozer و GitHub Actions با موفقیت ساخته شدند.")
    return "app_source"

def git_agent(commit_message):
    """ایجنت گیت: کامیت و ارسال خودکار فایل‌ها به گیت‌هاب"""
    print("\n📦 [ایجنت گیت]: در حال ارسال ساختار کامل به گیت‌هاب...")
    
    run_command("git add .")
    success, _ = run_command(f'git commit -m "Auto-agent build for: {commit_message}"')
    
    if success:
        print("🔄 دریافت آخرین تغییرات از گیت‌هاب (Pull)...")
        run_command("git pull origin main --rebase")
        
        push_success, _ = run_command("git push origin main")
        if push_success:
            print("🚀 پروژه با موفقیت روی گیت‌هاب نشست! گیت‌هاب اکشنز الان باید شروع به ساخت APK کند.")
        else:
            print("⚠️ خطا در ارسال به گیت‌هاب.")
    else:
        print("ℹ️ تغییر جدیدی برای ثبت وجود نداشت.")

def main():
    while True:
        user_input = input("\n💬 دستورت رو به ایجنت بگو (یا برای خروج 'exit' رو بزن): ")
        if user_input.lower() == 'exit':
            print("👋 خدانگهدار داداش!")
            break
        if not user_input.strip():
            continue
            
        print(f"\n🧠 [مدیر پروژه]: دستور دریافت شد -> '{user_input}'")
        
        # ۱. برنامه‌نویس فایل‌ها رو می‌سازه
        target_dir = coder_agent(user_input)
        
        # ۲. ایجنت تست و عیب‌یاب (چک کردن سلامت سینتکس بدون قفل شدن روی input)
        print("\n🧪 [ایجنت تست و عیب‌یاب]: در حال بررسی صحت کدهای پایتون...")
        success, _ = run_command(f"python -m py_compile {target_dir}/main.py")
        
        if success:
            print("🎉 تست سینتکس با موفقیت پاس شد!")
            # ۳. ایجنت گیت کل پکیج (کد + بیلدوزر + گیت‌هاب اکشنز) رو می‌فرسته گیت‌هاب
            git_agent(user_input)
        else:
            print("⚠️ خطا در کدهای تولید شده.")

if __name__ == "__main__":
    main()

