from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Mengambil URL dari Environment Variable Vercel
MONGO_URL = os.environ.get("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client.warung_lendir_db

@app.get("/")
async def home(request: Request):
    try:
        # Mencari data konfigurasi di database
        config = await db.settings.find_one({"id": "config"})
        
        if config:
            data_web = {
                "harga_vip": config.get("harga_vip", "0"),
                "preview_url": config.get("preview_url", "https://via.placeholder.com/400"),
                "nama_paket": config.get("nama_paket", "Paket Belum Diatur")
            }
        else:
            data_web = {
                "harga_vip": "0",
                "preview_url": "https://via.placeholder.com/400",
                "nama_paket": "Gunakan Bot Admin untuk Set Data"
            }
            
        # Mengirim respon ke index.html
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "data": data_web}
        )
    
    except Exception as e:
        return f"Koneksi Database Bermasalah: {str(e)}"