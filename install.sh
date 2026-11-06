#!/data/data/com.termux/files/usr/bin/bash

echo "=========================================="
echo "   MF AI — Mini Fire AI  |  نصب‌کننده"
echo "=========================================="
echo ""

# بررسی Termux
if [ -z "$PREFIX" ]; then
    echo "❌ این اسکریپت فقط داخل Termux کار می‌کند."
    exit 1
fi

echo "→ به‌روزرسانی پکیج‌ها..."
pkg update -y

echo ""
echo "→ نصب وابستگی‌های سیستمی..."
pkg install -y python git wget curl openjdk-17 unzip which

echo ""
echo "→ نصب / ارتقای pip و کتابخانه‌ها..."
pip install --upgrade pip
pip install ollama requests rich pydantic python-dotenv tqdm aiohttp aiofiles

echo ""
echo "→ بررسی Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "در حال نصب Ollama..."
    pkg install -y ollama || {
        echo "⚠️  نصب Ollama از طریق pkg ممکن نشد."
        echo "بعداً دستی نصب کن: pkg install ollama"
    }
fi

echo ""
echo "→ آماده‌سازی پوشه‌ها..."
mkdir -p "$HOME/.mf-ai/android-sdk"
mkdir -p "$HOME/.mf-ai/projects"
mkdir -p "$HOME/.mf-ai/cmdline-tools"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.mf-ai/app"

echo "→ کپی فایل‌ها به $INSTALL_DIR ..."
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/" 2>/dev/null || true

echo "→ ساخت دستور mfai ..."
cat > "$PREFIX/bin/mfai" << 'INNER'
#!/data/data/com.termux/files/usr/bin/bash
cd "$HOME/.mf-ai/app"
python main.py "$@"
INNER
chmod +x "$PREFIX/bin/mfai"
chmod +x "$INSTALL_DIR/main.py" 2>/dev/null || true

echo ""
echo "=========================================="
echo "✅ نصب MF AI تمام شد!"
echo ""
echo "مراحل بعدی:"
echo "1. مدل را دانلود کن:"
echo "     ollama pull qwen2.5-coder:7b"
echo ""
echo "2. (اختیاری) Ollama را در پس‌زمینه اجرا کن:"
echo "     ollama serve &"
echo ""
echo "3. برنامه را اجرا کن:"
echo "     mfai"
echo "=========================================="
