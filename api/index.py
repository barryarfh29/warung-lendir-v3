from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Koneksi ke MongoDB (Gunakan link koneksi kamu)
MONGO_URL = "mongodb+srv://Nadira31:Nadira31@cluster0.4rqcy61.mongodb.net/?appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client.warung_lendir_db # Nama database kamu

@app.get("/")
async def home(request: Request):
    # Ambil data dari koleksi 'settings' dengan ID 'config'
    config = await db.settings.find_one({"id": "config"})
    
    # Ambil data, jika tidak ada pakai default
    data_web = {
        "harga_vip": config.get("harga_vip", "50.000") if config else "50.000",
        "preview_url": config.get("preview_url", "https://via.placeholder.com/400") if config else "https://via.placeholder.com/400",
        "nama_paket": config.get("nama_paket", "VIP MONTHLY") if config else "VIP MONTHLY"
    }

    return templates.TemplateResponse("index.html", {
        "request": request,
        "data": data_web
    })
