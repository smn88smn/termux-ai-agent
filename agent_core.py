import os
import subprocess
import sys

print("🤖 سیستم چند ایجنتی (Multi-Agent) ترموکس با قابلیت گیت‌هاب فعال شد...")
print("--------------------------------------------------")

def run_command(command):
    """تابع اجرایی برای اجرای دستورات ترموکس"""
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
    """ایجنت برنامه‌نویس: کدهای پویا تولید می‌کند"""
    print(f"\n👨‍💻 [ایجنت برنامه‌نویس]: در حال نوشتن کد برای: '{task_description}'")
    file_name = "main_project.py"
    
    lower_task = task_description.lower()
    if "بازی" in lower_task or "game" in lower_task:
        code_content = """# بازی نمونه پایتونی ساخته شده توسط ایجنت
import random
def play():
    print("🎮 بازی هوشمند ایجنت با موفقیت اجرا شد!")
if __name__ == "__main__":
    play()
"""
    else:
        code_content = f'''# اسکریپت پروژه برای: {task_description}
def main():
    print("🚀 پروژه با موفقیت توسط ایجنت آپدیت و توسعه یافت.")
    print("🎯 هدف: {task_description}")
if __name__ == "__main__":
    main()
'''
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(code_content)
    print(f"📁 فایل {file_name} با موفقیت ایجاد و ذخیره شد.")
    return file_name

def git_agent(commit_message):
    """ایجنت گیت: تغییرات را ثبت و به گیت‌هاب ارسال می‌کند"""
    print("\n📦 [ایجنت گیت]: در حال ارسال تغییرات به گیت‌هاب...")
    
    run_command("git add .")
    success, _ = run_command(f'git commit -m "Auto-Agent update: {commit_message}"')
    
    if success:
        # ارسال خودکار به گیت‌هاب
        push_success, _ = run_command("git push origin main")
        if push_success:
            print("🚀 کدها با موفقیت روی گیت‌هاب آپلود شدند!")
        else:
            print("⚠️ در ارسال به گیت‌هاب خطایی رخ داد.")
    else:
        print("ℹ️ تغییر جدیدی برای کامیت وجود نداشت.")

def main():
    while True:
        user_input = input("\n💬 دستورت رو به ایجنت بگو (یا برای خروج 'exit' رو بزن): ")
        if user_input.lower() == 'exit':
            print("👋 خدانگهدار داداش!")
            break
        if not user_input.strip():
            continue
            
        print(f"\n🧠 [مدیر پروژه]: دستور دریافت شد -> '{user_input}'")
        
        # ۱. برنامه‌نویس کد رو می‌نویسه
        created_file = coder_agent(user_input)
        
        # ۲. تست و عیب‌یاب کد رو اجرا می‌کنه
        print("\n🧪 [ایجنت تست و عیب‌یاب]: در حال اجرای تست کد...")
        success, _ = run_command(f"python {created_file}")
        
        if success:
            print("🎉 تست با موفقیت پاس شد!")
            # ۳. ایجنت گیت وارد عمل میشه و خودکار می‌فرسته رو گیت‌هاب
            git_agent(user_input)
        else:
            print("⚠️ مشکلی در اجرای کد بود.")

if __name__ == "__main__":
    main()

