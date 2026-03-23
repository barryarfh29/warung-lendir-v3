from flask import Flask, render_template, jsonify
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

app = Flask(__name__, template_folder='../templates')

# KONFIGURASI DATABASE
MONGO_URL = "mongodb+srv://Nadira31:Nadira31@cluster0.4rqcy61.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client.warung_lendir_db

@app.route('/')
def index():
    # Menampilkan HTML dasar saja agar web tidak crash saat loading
    return render_template('index.html')

@app.route('/api/data')
async def get_data():
    try:
        # Mencari data di collection settings dengan id config
        config = await db.settings.find_one({"id": "config"})
        if config:
            # BERSIHKAN URL dari karakter aneh jika ada
            url = str(config.get("preview_url", "")).replace("`", "").strip()
            return jsonify({
                "preview_url": url,
                "harga_vip": config.get("harga_vip", "0"),
                "nama_paket": config.get("nama_paket", "WARUNG LENDIR")
            })
        return jsonify({"error": "Data tidak ditemukan"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Wajib ada agar Vercel mengenali Flask
def handler(app, event, context):
    return app(event, context)