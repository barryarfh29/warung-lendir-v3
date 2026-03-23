from flask import Flask, render_template, jsonify
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

app = Flask(__name__, template_folder='../templates')

# SETUP MONGO
MONGO_URL = "mongodb+srv://Nadira31:Nadira31@cluster0.4rqcy61.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client.warung_lendir_db

async def fetch_config():
    try:
        # Ambil data dari collection settings
        return await db.settings.find_one({"id": "config"})
    except:
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # Menjalankan fungsi async di dalam route Flask sync
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        config = loop.run_until_complete(fetch_config())
        if config:
            # Bersihkan URL dari karakter sampah
            raw_url = str(config.get("preview_url", ""))
            clean_url = raw_url.replace("`", "").strip()
            
            return jsonify({
                "preview_url": clean_url,
                "harga_vip": config.get("harga_vip", "0"),
                "nama_paket": config.get("nama_paket", "WARUNG LENDIR")
            })
        return jsonify({"error": "Data tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        loop.close()

# Penting: Vercel butuh objek 'app' ini di tingkat modul
# Tidak perlu handler tambahan jika vercel.json sudah benar