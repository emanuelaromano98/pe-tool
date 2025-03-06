from source_files.report_generation import generate_report
from source_files.markdown_generation import generate_markdown
from source_files.prompt_generation import generate_prompt
from source_files.text_similarity_filter import filter_reports
from source_files.file_converter import convert_markdown_to_all_formats
from dotenv import load_dotenv
import os
from openai import OpenAI
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
import glob
import uvicorn
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.responses import FileResponse

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

class IndustryRequest(BaseModel):
    industry: str
    topics: list[str]
    model: str = "gpt-4o-2024-08-06"
    threshold: float = 0.85
    model_for_filtering: str = "all-MiniLM-L6-v2"
    api_key: str 

@app.post("/generate-report")
async def generate_industry_report(request: IndustryRequest):
    clear_output_files("output_files/*")
    client = OpenAI(api_key=request.api_key)
    
    await send_status_update("Starting report generation...")

    for topic in request.topics:
        await send_status_update(f"Generating prompt for {topic}...")
        generate_prompt(request.industry, topic, client, request.model)
        
        await send_status_update(f"Generating report for {topic}...")
        await generate_report(topic, client, request.model, send_status_update)

    await send_status_update("Filtering reports...")
    filter_reports(model=request.model_for_filtering, threshold=request.threshold)

    try:
        with open("backend/output_files/reports.json", "r") as f:
            reports = f.read()
        if not reports:
            await send_status_update("No reports generated")
            return {"message": "No reports generated"}
    except FileNotFoundError:
        await send_status_update("No reports generated")
        return {"message": "No reports generated"}

    await send_status_update("Generating Markdown...")
    generate_markdown(request.topics, reports)
    
    markdown_path = "backend/output_files/report.md"
    html_success, pdf_success = convert_markdown_to_all_formats(markdown_path)
    
    if not html_success:
        await send_status_update("Warning: HTML conversion failed")
    if not pdf_success:
        await send_status_update("Warning: PDF conversion failed")

    await send_status_update("Report generated successfully!")
    return {"message": "Report generated successfully"}

@app.get("/download-report")
async def download_report(format: str):
    file_mapping = {
        "html": ("backend/output_files/report.html", "text/html"),
        "pdf": ("backend/output_files/report.pdf", "application/pdf"),
        "markdown": ("backend/output_files/report.md", "text/markdown")
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