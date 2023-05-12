import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import shutil
import json

filename = "items.json"


app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.DEBUG
images = pathlib.Path(__file__).parent.resolve() / "images"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:3000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello, world!"}





@app.post("/items")
def add_item(name: str = Form(...), category: str = Form(...), file: UploadFile = File(...)):
    with open(file.filename, 'rb') as f:
        sha256 = hashlib.sha256(f.read()).hexdigest()

    fname = file.filename
    upload_dir = open(os.path.join("images", fname),'wb+')
    shutil.copy(fname, 'images/' + sha256 + '.jpg')
    upload_dir.close()
    
    item_tsuika = {'name': name, 'category': category, 'image_filename': sha256 + '.jpg'}
    with open(filename, 'r') as f:
        read_data = json.load(f)

    
    read_data["items"].append(item_tsuika)
   
    
    with open(filename, 'w') as f:
        json.dump(read_data, f)
    
    
    logger.info(f"Receive item: {name}")
    return {"message": f"item received: {name}, {category}, {sha256 + '.jpg'}"}

@app.get("/items")
def root():
    with open(filename, 'r') as f:
        read_data = json.load(f)
    return read_data

@app.get("/items/{item_id}")
def read_item(item_id: int):
    with open(filename, 'r') as f:
        read_data = json.load(f)
    return read_data["items"][item_id-1]
    

@app.get("/image/{image_filename}")
async def get_image(image_filename):
   
    image = images / image_filename

    if not image_filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
