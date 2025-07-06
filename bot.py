import os
import json
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv

# Load env vars
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
DOMAIN = os.getenv("DOMAIN")

FILES_DIR = "./files/"
os.makedirs(FILES_DIR, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ دسترسی غیرمجاز")
        return
    await update.message.reply_text("✅ خوش اومدی! فایل رو بفرست.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ دسترسی غیرمجاز")
        return

    # پشتیبانی از document, video, photo
    file = update.message.document or \
           update.message.video or \
           (update.message.photo[-1] if update.message.photo else None)

    if not file:
        await update.message.reply_text("📁 فایل معتبر بفرست")
        return

    tg_file = await file.get_file()
    filename = f"{file.file_unique_id}_{getattr(file, 'file_name', 'file')}"
    filepath = os.path.join(FILES_DIR, filename)
    await tg_file.download_to_drive(filepath)

    expire_time = datetime.utcnow() + timedelta(hours=24)

    db = {}
    if os.path.exists("db.json"):
        with open("db.json", "r") as f:
            db = json.load(f)

    db[filename] = {"expire_time": expire_time.isoformat()}

    with open("db.json", "w") as f:
        json.dump(db, f)

    link = f"{DOMAIN}/download/{filename}"
    await update.message.reply_text(
        f"✅ فایل ذخیره شد.\n📥 لینک دانلود:\n{link}\n⏳ معتبر تا ۲۴ ساعت."
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.Document | filters.Video | filters.PHOTO,
            handle_file
        )
    )

    print("Bot is running...")
    app.run_polling()
