import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import shutil
import json
import sqlite3

ITEMS_JSON = "items.json"
ITEMS_DB = '/home/kurita/mercari-build-training-2023/db/mercari.sqlite3'

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
def add_item(id: int = Form(...), name: str = Form(...), category: str = Form(...), file: UploadFile = File(...)):
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

    conn = sqlite3.connect(ITEMS_DB)
    cur = conn.cursor()
    cur.execute('SELECT * FROM items')
    sql = 'INSERT INTO items values(' + str(id) + ', "' + name  + '", "' + category + '", "' + image_name + '")'
    cur.execute(sql)
    conn.commit()
    conn.close()
    
    logger.info(f"Receive item: {name}")
    return {"message": f"item received: {id}, {name}, {category}, {image_name}"}

#step4-1
# @app.get("/items")
# def get_items():
#     conn = sqlite3.connect(dbname)
#     cur = conn.cursor()
#     cur.execute('SELECT * FROM items')
#     sql_items = {"items": []}
#     for row in cur:
#         sql_items["items"].append(json.dumps(row))
#     conn.close()  
#     return sql_items

#step4-3
@app.get("/items")
def get_items():
    conn = sqlite3.connect(ITEMS_DB)
    cur = conn.cursor()
    cur.execute('SELECT * FROM items2 INNER JOIN category ON items2.category_id = category.id')

    sql_items = {"items": []}
    for row in cur:
        sql_items["items"].append(json.dumps(row))
    conn.close()
    
    return sql_items


@app.get("/search")
def item_search(keyword: str = ''):
    
    conn = sqlite3.connect(ITEMS_DB)
    cur = conn.cursor()
    cur.execute('SELECT * FROM items WHERE name = "'+ keyword + '"')
    sql_items = {"items": []}
    for row in cur:
        sql_items["items"].append(json.dumps(row))
    conn.close()
    
    return sql_items


@app.get("/items/{item_id}")
def read_item(item_id: int):
    with open(ITEMS_JSON, 'r') as f:
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
