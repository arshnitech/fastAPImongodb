from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os

app = FastAPI()

# Static files (keep for CSS/JS only)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# 🔐 MongoDB Connection
MONGO_URL = "mongodb+srv://azureuser:F#nterzma1@yamazakimongodbcluster2.global.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"

client = AsyncIOMotorClient(MONGO_URL)
db = client.ecommerceDB
collection = db.products


# 🏠 Home Page – Fetch Products From MongoDB
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    products = []

    async for item in collection.find():
        item["_id"] = str(item["_id"])
        products.append(item)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products
    })


@app.get("/cart", response_class=HTMLResponse)
async def cart(request: Request):
    return templates.TemplateResponse("cart.html", {
        "request": request
    })
