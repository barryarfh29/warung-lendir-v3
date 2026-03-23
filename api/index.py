from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Pastikan MONGO_URL sudah ada di Environment Variables Vercel
MONGO_URL = os.environ.get("MONGO_URL")
client = AsyncIOMotorClient(MONGO_URL)
db = client.warung_lendir_db

@app.get("/")
async def home(request: Request):
    try:
        # 1. Ambil data dari MongoDB
        config = await db.settings.find_one({"id": "config"})
        
        # 2. Siapkan data (pastikan tidak ada ID MongoDB yang terbawa)
        if config:
            web_info = {
                "harga": config.get("harga_vip", "0"),
                "foto": config.get("preview_url", "https://via.placeholder.com/400"),
                "nama": config.get("nama_paket", "Paket Belum Diatur")
            }
        else:
            web_info = {
                "harga": "0",
                "foto": "https://via.placeholder.com/400",
                "nama": "Gunakan Bot Admin untuk Set Data"
            }
            
        # 3. Kirim ke HTML dengan format context yang paling aman
        return templates.TemplateResponse(
            name="index.html",
            context={"request": request, "data": web_info}
        )
    
    except Exception as e:
        # Jika error, tampilkan pesan error yang jelas
        return f"Koneksi Database Bermasalah: {str(e)}"