from source_files.theme_report_generation import theme_generate_report
from source_files.file_converter import convert_markdown_to_all_formats
from dotenv import load_dotenv
import os
from openai import OpenAI
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, HTTPException, Form, File
from pydantic import BaseModel
import glob
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from source_files.theme_prompts import generate_prompt_1, generate_prompt_2
import time
import asyncio
from pathlib import Path
from source_files.cim_prompts import generate_cim_prompt_part_1_and_2, generate_cim_prompt_part_3, generate_cim_prompt_part_4
from source_files.cim_report_generation import cim_generate_report
from fastapi import UploadFile
from PyPDF2 import PdfReader
import json
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
        # Send a ready message
        await websocket.send_text("WebSocket connected and ready")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        print(f"Sending message: {message}")
        if not self.active_connections:
            print("No active connections!")
            return
            
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
                # Add a small delay to ensure message processing
                await asyncio.sleep(0.1)
            except WebSocketDisconnect:
                disconnected.append(connection)
            except Exception as e:
                print(f"Error sending message: {e}")
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
    print(f"Sending message: {message}")
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

@app.post("/generate-theme-report")
async def generate_theme_report(request: ThemeRequest):
    clear_output_files("output_files/*")    
    
    prompts = [generate_prompt_1(request.theme, request.countries, request.from_year, request.to_year), generate_prompt_2()]
    client = OpenAI(api_key=request.api_key)
    model = request.model
    await theme_generate_report(prompts, client, model, send_status_update)
    
    # Wait a moment for WebSocket to be ready
    if not manager.active_connections:
        await asyncio.sleep(0.5)  # Give frontend time to connect
        
    await send_status_update("Starting report generation...")
    
    try:
        with open("output_files/theme_report.md", "r") as f:
            report = f.read()
        if not report:
            await send_status_update("No reports generated")
            return {"message": "No reports generated"}
    except FileNotFoundError:
        await send_status_update("No reports generated")
        return {"message": "No reports generated"}
            
    markdown_path = "output_files/theme_report.md"
    html_success, pdf_success, txt_success = convert_markdown_to_all_formats(markdown_path)
    
    if not html_success:
        await send_status_update("Warning: HTML conversion failed")
    if not pdf_success:
        await send_status_update("Warning: PDF conversion failed")
    if not txt_success:
        await send_status_update("Warning: TXT conversion failed")

    await send_status_update("Successfully converted report to all formats.")

    return {"message": "Report generated successfully"}

@app.post("/generate-cim-report")
async def generate_cim_report(
    model: str = Form(...),
    filtering_model: str = Form(...),
    threshold: float = Form(...),
    api_key: str = Form(...),
    file: UploadFile = File(...),
    analysis_type: str = Form(...),
    title_file: str = Form(...)
):
    analysis_types = json.loads(analysis_type)
    clear_output_files("output_files/*")    
    
    # First update
    await send_status_update("Starting report generation...")
    
    prompt_1_and_2 = generate_cim_prompt_part_1_and_2(analysis_types)
    prompt_3 = generate_cim_prompt_part_3()
    prompt_4 = generate_cim_prompt_part_4()
    client = OpenAI(api_key=api_key)
    
    try:
        await cim_generate_report(prompt_1_and_2, prompt_3, prompt_4, file, client, model, send_status_update, title_file)
        
        # Processing the report only if generation was successful
        markdown_path = "output_files/cim_report.md"
        html_success, pdf_success, txt_success = convert_markdown_to_all_formats(markdown_path)
        
        if not html_success:
            await send_status_update("Warning: HTML conversion failed")
        if not pdf_success:
            await send_status_update("Warning: PDF conversion failed")
        if not txt_success:
            await send_status_update("Warning: TXT conversion failed")

        await send_status_update("Successfully converted report to all formats.")
        return {"message": "Report generated successfully"}
    except Exception as e:
        await send_status_update(f"Error generating report: {str(e)}")
        return {"message": f"Error: {str(e)}"}

async def handle_pdf_file(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

@app.get("/download-theme-report")
async def download_theme_report(format: str):

    backend_dir = Path(__file__).parent / "output_files"
    print(backend_dir)
    
    file_mapping = {
        "html": (backend_dir / "theme_report.html", "text/html"),
        "pdf": (backend_dir / "theme_report.pdf", "application/pdf"),
        "markdown": (backend_dir / "theme_report.md", "text/markdown"),
        "txt": (backend_dir / "theme_report.txt", "text/plain")
    }
    
    if format not in file_mapping:
        raise HTTPException(status_code=400, detail="Invalid format specified")
    
    file_path, content_type = file_mapping[format]
    
    try:
        if format == "pdf":
            # Make sure to set proper headers for PDF
            return FileResponse(
                path=file_path,
                media_type="application/pdf",
                filename=f"theme_report.pdf",
                headers={"Content-Disposition": "attachment"}
            )
        return FileResponse(
            path=file_path,
            media_type=content_type,
            filename=f"theme_report.{format}"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Report file in {format} format not found")
    

@app.get("/download-cim-report")
async def download_cim_report(format: str):

    backend_dir = Path(__file__).parent / "output_files"
    print(backend_dir)
    
    file_mapping = {
        "html": (backend_dir / "cim_report.html", "text/html"),
        "pdf": (backend_dir / "cim_report.pdf", "application/pdf"),
        "markdown": (backend_dir / "cim_report.md", "text/markdown"),
        "txt": (backend_dir / "cim_report.txt", "text/plain")
    }
    
    if format not in file_mapping:
        raise HTTPException(status_code=400, detail="Invalid format specified")
    
    file_path, content_type = file_mapping[format]
    
    try:
        return FileResponse(
            path=file_path,
            media_type=content_type,
            filename=f"cim_report.{format}"
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Report file in {format} format not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
