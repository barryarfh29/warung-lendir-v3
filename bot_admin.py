from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
import requests
import os

# --- KONFIGURASI (PASTIKAN SUDAH BENAR) ---
API_ID = 39734936
API_HASH = "28108d534da2a925bbe59731433043e0"
BOT_TOKEN = "8618695271:AAEqiR9Y64prKoS8bQMdHh_CaUwiDrEYo94"
MONGO_URL = "mongodb+srv://Nadira31:Nadira31@cluster0.4rqcy61.mongodb.net/?appName=Cluster0"
ADMIN_ID = 5894622820  # ID Telegram kamu
# -----------------------------------------

app = Client("my_admin_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client.warung_lendir_db

# Fungsi bantu untuk upload foto ke Telegra.ph
def upload_to_telegraph(file_path):
    try:
        with open(file_path, 'rb') as f:
            response = requests.post('https://telegra.ph/upload', files={'file': ('file', f, 'image/jpg')})
            data = response.json()
            return "https://telegra.ph" + data[0]['src']
    except Exception as e:
        print(f"Error Upload: {e}")
        return None

@app.on_message(filters.command("start") & filters.user(ADMIN_ID))
async def start(client, message):
    await message.reply(
        "✅ **Bot Admin Web Aktif!**\n\n"
        "**Perintah:**\n"
        "1️⃣ `/setweb Harga|Nama` -> Contoh: `/setweb 50.000|VIP BULANAN`\n"
        "2️⃣ Kirim Foto dengan caption `/setfoto` -> Otomatis ganti foto di Web\n"
        "3️⃣ `/cekweb` -> Lihat data yang tampil di web sekarang"
    )

# FITUR: Update Harga & Nama Paket
@app.on_message(filters.command("setweb") & filters.user(ADMIN_ID))
async def set_web(client, message):
    try:
        data_input = message.text.split(" ", 1)[1]
        harga, nama = data_input.split("|")
        
        await db.settings.update_one(
            {"id": "config"}, 
            {"$set": {"harga_vip": harga, "nama_paket": nama}}, 
            upsert=True
        )
        await message.reply(f"🚀 **Web Terupdate!**\n💰 Harga: {harga}\n📦 Paket: {nama}")
    except:
        await message.reply("❌ **Format Salah!**\nContoh: `/setweb 50.000|VIP BULANAN` (Gunakan tanda | sebagai pemisah)")

# FITUR: Update Foto Preview (Kirim Foto + Caption /setfoto)
@app.on_message(filters.photo & filters.user(ADMIN_ID))
async def set_foto(client, message):
    # Cek apakah caption-nya adalah /setfoto
    if message.caption != "/setfoto":
        return

    msg = await message.reply("⏳ Sedang memproses foto...")
    
    # Download foto sementara
    path = await message.download()
    
    try:
        # Upload ke Telegra.ph
        link_baru = upload_to_telegraph(path)
        
        if link_baru:
            # Simpan ke MongoDB
            await db.settings.update_one(
                {"id": "config"}, 
                {"$set": {"preview_url": link_baru}}, 
                upsert=True
            )
            await msg.edit(f"✅ **Foto Web Terupdate!**\n🔗 Link: {link_baru}")
        else:
            await msg.edit("❌ Gagal mendapatkan link foto dari Telegra.ph")
            
    except Exception as e:
        await msg.edit(f"❌ Terjadi kesalahan: {e}")
    finally:
        # Hapus file sampah di lokal setelah upload
        if os.path.exists(path):
            os.remove(path)

# FITUR: Cek Status Web
@app.on_message(filters.command("cekweb") & filters.user(ADMIN_ID))
async def cek_web(client, message):
    config = await db.settings.find_one({"id": "config"})
    if config:
        text = (
            "📊 **Status Web Saat Ini:**\n"
            f"📦 Paket: `{config.get('nama_paket')}`\n"
            f"💰 Harga: `Rp {config.get('harga_vip')}`\n"
            f"🖼️ Preview: {config.get('preview_url')}"
        )
        await message.reply(text)
    else:
        await message.reply("📭 Database masih kosong.")

print("🚀 Bot Admin Web Berjalan...")
app.run()