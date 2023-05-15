import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import shutil
import json

ITEMS_JSON = "items.json"

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
    
    try:
        with open(file.filename, 'rb') as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()

    except Exception as e:
        return str(e)
    
    image_name = sha256 + 'jpg'

    fname = file.filename
    upload_dir = open(os.path.join("images", fname),'wb+')
    shutil.copy(fname, 'images/' + image_name)
    upload_dir.close()

    added_item = {'name': name, 'category': category, 'image_filename': image_name}
    
    try:
        with open(ITEMS_JSON, 'r') as f:
            read_data = json.load(f)
    except Exception as e:
        return str(e)
    
    read_data["items"].append(added_item)

    try:   
     with open(ITEMS_JSON, 'w') as f:
            json.dump(read_data, f)
    
    except Exception as e:
        return str(e)
    
    logger.info(f"Receive item: {name}")
    return {"message": f"item received: {name}, {category}, {image_name}"}
    

@app.get("/items")
def get_items():
    try:
        with open(ITEMS_JSON, 'r') as f:
            read_data = json.load(f)
        return read_data
    
    except Exception as e:
        return str(e)

@app.get("/items/{item_id}")
def read_item(item_id: int):
    try:
        with open(ITEMS_JSON, 'r') as f:
            read_data = json.load(f)
        return read_data["items"][item_id-1]
    
    except Exception as e:
        return str(e)


@app.get("/image/{image_filename}")
async def get_image(image_filename):
   
    image = images / image_filename

    if not image_filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)
