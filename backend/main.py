from source_files.report_generation import generate_report
from source_files.file_converter import convert_markdown_to_all_formats
from dotenv import load_dotenv
import os
from openai import OpenAI
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
import glob
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from source_files.theme_prompts import generate_prompt_1, generate_prompt_2
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except WebSocketDisconnect:
                disconnected.append(connection)
            except Exception:
                disconnected.append(connection)
        
        # Clean up disconnected connections
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

@app.websocket("/ws/status")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

async def send_status_update(message: str):
    await manager.send_message(message)

def clear_output_files(pattern):
    files = glob.glob(pattern)
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)

class ThemeRequest(BaseModel):
    theme: str
    model: str
    api_key: str 
    countries: list[str]
    from_year: str
    to_year: str

@app.post("/generate-report")
async def generate_theme_report(request: ThemeRequest):
    clear_output_files("output_files/*")    
    prompts = [generate_prompt_1(request.theme, request.countries, request.from_year, request.to_year), generate_prompt_2()]
    client = OpenAI(api_key=request.api_key)
    model = request.model
    theme = request.theme
    countries = request.countries
    from_year = request.from_year
    to_year = request.to_year
    
    await generate_report(prompts, theme, countries, from_year, to_year, client, model, send_status_update)




    try:
        with open("output_files/report.md", "r") as f:
            report = f.read()
        if not report:
            await send_status_update("No reports generated")
            return {"message": "No reports generated"}
    except FileNotFoundError:
        await send_status_update("No reports generated")
        return {"message": "No reports generated"}

    await send_status_update("Converting report to all formats...")
            
    markdown_path = "output_files/report.md"
    html_success, pdf_success, txt_success = convert_markdown_to_all_formats(markdown_path)
    
    if not html_success:
        await send_status_update("Warning: HTML conversion failed")
    if not pdf_success:
        await send_status_update("Warning: PDF conversion failed")
    if not txt_success:
        await send_status_update("Warning: TXT conversion failed")

    await send_status_update("Successfully converted report to all formats.")

    return {"message": "Report generated successfully"}


@app.get("/download-report")
async def download_report(format: str):
    file_mapping = {
        "html": ("backend/output_files/report.html", "text/html"),
        "pdf": ("backend/output_files/report.pdf", "application/pdf"),
        "markdown": ("backend/output_files/report.md", "text/markdown"),
        "txt": ("backend/output_files/report.txt", "text/plain")
    }
    
    if format not in file_mapping:
        raise HTTPException(status_code=400, detail="Invalid format specified")
    
    file_path, content_type = file_mapping[format]
    
    try:
        return FileResponse(
            path=file_path,
            media_type=content_type,
            filename=f"report.{format}"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Report file in {format} format not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
