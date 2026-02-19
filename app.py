from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
from downloader import download_video

app = FastAPI()

templates = Jinja2Templates(directory="templates")

DOWNLOAD_FOLDER = "downloads"

# Ensure downloads folder exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download")
def download(request: Request, url: str = Form(...)):
    try:
        file_path = download_video(url)

        return FileResponse(
            path=file_path,
            filename=os.path.basename(file_path),
            media_type="application/octet-stream"
        )

    except Exception as e:
        return {"error": str(e)}
