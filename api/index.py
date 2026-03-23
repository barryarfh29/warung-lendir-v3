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
        # Mencari data dengan id: config
        config = await db.settings.find_one({"id": "config"})
        
        # Jika data ditemukan di MongoDB
        if config:
            data_web = {
                "harga_vip": config.get("harga_vip", "0"),
                "preview_url": config.get("preview_url", "https://via.placeholder.com/400"),
                "nama_paket": config.get("nama_paket", "Paket Belum Diatur")
            }
        else:
            # Jika database masih kosong
            data_web = {
                "harga_vip": "0",
                "preview_url": "https://via.placeholder.com/400",
                "nama_paket": "Gunakan Bot Admin untuk Set Data"
            }
            
        # PENTING: Perhatikan penulisan {"request": request, "data": data_web}
        return templates.TemplateResponse("index.html", {"request": request, "data": data_web})
    
    except Exception as e:
        return f"Error Koneksi Database: {str(e)}"