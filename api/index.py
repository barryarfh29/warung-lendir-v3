from flask import Flask, render_template, jsonify
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

app = Flask(__name__, template_folder='../templates')

# --- KONEKSI DATABASE ---
# Pastikan URL ini benar dan tidak ada spasi
MONGO_URL = "mongodb+srv://Nadira31:Nadira31@cluster0.4rqcy61.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client.warung_lendir_db

async def get_config_data():
    try:
        # Mencari data dengan id "config" sesuai yang disimpan bot admin kamu
        doc = await db.settings.find_one({"id": "config"})
        return doc
    except Exception as e:
        print(f"Error Database: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
async def get_data():
    try:
        config = await get_config_data()
        if config:
            # Bersihkan URL dari karakter aneh (seperti backtick atau %60)
            raw_url = str(config.get("preview_url", ""))
            clean_url = raw_url.replace("`", "").strip()
            
            return jsonify({
                "preview_url": clean_url,
                "harga_vip": config.get("harga_vip", "0"),
                "nama_paket": config.get("nama_paket", "WARUNG LENDIR")
            })
        return jsonify({"error": "Data config tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Standar Vercel Serverless
def handler(event, context):
    return app(event, context)