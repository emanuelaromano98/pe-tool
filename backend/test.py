import requests

request = requests.post("http://10.128.0.3:8000/generate-theme-report", json={
    "theme": "AI",
    "countries": ["US", "CA", "GB"],
    "from_year": "2020",
    "to_year": "2026",
    "model": "gpt-4o-mini",
    "api_key": "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"
})

print(request.json())