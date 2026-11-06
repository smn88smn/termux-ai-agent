import os
import subprocess
import sys

print("🤖 سیستم چند ایجنتی (Multi-Agent) ترموکس با قابلیت گیت فعال شد...")
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
        code_content = """# بازی نمونه پایتونی
import random
def play():
    print("🎮 بازی ایجنت اجرا شد و آماده نبرد است!")
if __name__ == "__main__":
    play()
"""
    else:
        code_content = f'''# اسکریپت پروژه برای: {task_description}
def main():
    print("🚀 پروژه با موفقیت توسط ایجنت آپدیت شد.")
    print("هدف: {task_description}")
if __name__ == "__main__":
    main()
'''
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(code_content)
    print(f"📁 فایل {file_name} ذخیره شد.")
    return file_name

def git_agent(commit_message):
    """ایجنت گیت و گیت‌هاب: فایل‌ها را کامیت و به گیت‌هاب ارسال می‌کند"""
    print("\n📦 [ایجنت گیت]: در حال بررسی وضعیت مخزن و ثبت تغییرات...")
    
    # بررسی اینکه آیا گیت مقداردهی شده یا نه
    if not os.path.exists(".git"):
        run_command("git init")
    
    # افزودن فایل‌ها، کامیت و پوش کردن
    run_command("git add .")
    
    # کامیت کردن تغییرات
    commit_cmd = f'git commit -m "Auto-Agent update: {commit_message}"'
    success, _ = run_command(commit_cmd)
    
    if success:
        print("🎉 تغییرات با موفقیت در گیت ثبت (Commit) شدند!")
        print("💡 نکته: اگر ریپوی ریموت متصل باشد، می‌توانی با دستور git push اون رو بفرستی روی گیت‌هاب.")
    else:
        print("ℹ️ تغییر جدیدی برای کامیت وجود نداشت یا مخزن نیاز به تنظیم دارد.")

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
        print("\n🧪 [ایجنت تست و عیب‌یاب]: در حال اجرای کد...")
        success, _ = run_command(f"python {created_file}")
        
        if success:
            print("🎉 تست با موفقیت پاس شد!")
            # ۳. ایجنت گیت وارد عمل میشه
            git_agent(user_input)
        else:
            print("⚠️ مشکلی در اجرا بود.")

if __name__ == "__main__":
    main()

