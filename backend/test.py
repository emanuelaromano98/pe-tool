import asyncio
import websockets
import requests

request = requests.post("http://34.60.164.32:8000/generate-theme-report", json={
    "theme": "AI",
    "countries": ["US", "CA", "GB"],
    "from_year": 2020,
    "to_year": 2026,
    "api_key": "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"
})

print(request.json())