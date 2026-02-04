from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import csv
from datetime import datetime
import os

TOKEN = os.getenv("TOKEN")

MENU = ReplyKeyboardMarkup(
    [
        ["➕ Tambah Pengeluaran"],
        ["📊 Hari Ini", "📅 Bulanan"],
        ["❌ Hapus Terakhir"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "Halo 👋\nPilih menu pengeluaran:",
        reply_markup=MENU
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "➕ Tambah Pengeluaran":
        context.user_data["step"] = "jumlah"
        await update.message.reply_text("Masukkan jumlah pengeluaran:")

    elif context.user_data.get("step") == "jumlah":
        if not text.isdigit():
            await update.message.reply_text("❌ Masukkan angka saja")
            return
        context.user_data["jumlah"] = text
        context.user_data["step"] = "keterangan"
        await update.message.reply_text("Masukkan keterangan:")

    elif context.user_data.get("step") == "keterangan":
        jumlah = context.user_data.get("jumlah")
        keterangan = text
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open("pengeluaran.csv", "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([tanggal, jumlah, keterangan])
        context.user_data.clear()
        await update.message.reply_text("✅ Pengeluaran tersimpan", reply_markup=MENU)

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

app.run_polling()

