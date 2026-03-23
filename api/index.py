from flask import Flask, render_template, jsonify
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

app = Flask(__name__, template_folder='../templates')

# KONEKSI MONGO
MONGO_URL = "mongodb+srv://Nadira31:Nadira31@cluster0.4rqcy61.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client.warung_lendir_db

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/data')
async def get_data():
    try:
        # Mencari data yang diupdate Bot Admin
        config = await db.settings.find_one({"id": "config"})
        if config:
            return jsonify({
                "preview_url": config.get("preview_url", ""),
                "harga_vip": config.get("harga_vip", "0"),
                "nama_paket": config.get("nama_paket", "WARUNG LENDIR")
            })
        return jsonify({"error": "Data config tidak ditemukan di MongoDB"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Wajib untuk Vercel
def handler(app, event, context):
    return app(event, context)