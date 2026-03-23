import os
import telebot
import cloudinary
import cloudinary.uploader
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# --- KONFIGURASI ---
TOKEN = "8618695271:AAEEi_0zZKuDNPMmn0CKlKxfJIasz684Nmk"
ADMIN_ID = 5894622820
MONGO_URL = "mongodb+srv://Nadira31:Nadira31@cluster0.4rqcy61.mongodb.net/?appName=Cluster0"

# --- CLOUDINARY ---
cloudinary.config(
    cloud_name="dtrsnjeuf", 
    api_key="511323976984432", 
    api_secret="Txo-wOe6VCkYAeZBtC8EbFMghsM"
)

# --- INIT ---
bot = telebot.TeleBot(TOKEN, threaded=False)
client = AsyncIOMotorClient(MONGO_URL)
db = client.warung_lendir_db
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id == ADMIN_ID:
        bot.reply_to(message, "✅ **BOT ADMIN SIAP!**\n\nKirim foto dengan caption `/setfoto` untuk update gambar website secara otomatis.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.from_user.id == ADMIN_ID and message.caption == "/setfoto":
        status = bot.reply_to(message, "⏳ **Sedang memproses...**")
        
        try:
            # Download Foto
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded = bot.download_file(file_info.file_path)
            
            with open("img_update.jpg", "wb") as f:
                f.write(downloaded)
                
            # Upload ke Cloudinary
            res = cloudinary.uploader.upload("img_update.jpg")
            # BERSIHKAN URL (Hapus spasi atau karakter aneh)
            clean_url = res["secure_url"].strip()
            
            # UPDATE MONGODB (Pastikan ID: "config" dan field: "preview_url")
            async def update_db():
                await db.settings.update_one(
                    {"id": "config"}, 
                    {"$set": {"preview_url": clean_url}}, 
                    upsert=True
                )
            loop.run_until_complete(update_db())
            
            # Kirim balasan tanpa tanda petik miring agar tidak ada %60
            bot.edit_message_text(
                f"✅ **BERHASIL!**\n\nFoto web telah diperbarui.\nLink Aktif:\n{clean_url}", 
                message.chat.id, 
                status.message_id
            )
            print(f"DEBUG: URL Berhasil disimpan -> {clean_url}")
            
        except Exception as e:
            bot.edit_message_text(f"❌ **GAGAL:** {str(e)}", message.chat.id, status.message_id)
        finally:
            if os.path.exists("img_update.jpg"):
                os.remove("img_update.jpg")

print("--- BOT ADMIN RUNNING (CLEAN VERSION) ---")
bot.remove_webhook()
bot.polling(non_stop=True)