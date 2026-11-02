import os

import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException

from fastapi.staticfiles import StaticFiles

UPLOADS_FOLDER="uploads"

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB

os.makedirs(UPLOADS_FOLDER,exist_ok=True)

app=FastAPI()

app.mount("/static", StaticFiles(directory=UPLOADS_FOLDER), name="static")

@app.post("/upload")

async def upload_file(file: UploadFile = File(...)):
    # Validation:1 Check the file name
    if not file.filename:

        raise HTTPException(status_code=400, detail="file is required")
    filename=os.path.basename(file.filename)

    # validation 2:check file extention
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        raise HTTPException(status_code=400,
        detail="Invalid file type. Only JPG, JPEG, and PNG are allowed.")
    
    # validation 3:check content type
    if file.content_type!= "image/jpeg":
        raise HTTPException(status_code=400,
        detail="Invalid content type. Only JPEG and PNG are allowed.")
    
    # validation 4:check file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)  

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400, 
            detail="File size must be less than 2 MB.")

            # file handling:save the upload file
    file_path=os.path.join(UPLOADS_FOLDER,filename)
    with open(file_path,"wb") as f:
        shutil.copyfileobj(file.file,f)
    # create file url
    file_url=f"/static/{filename}"

    return {
        "message":"File uploaded successfully",
        "filename":filename,
        "file_size":file_size,
        "file_url":file_url
        }
