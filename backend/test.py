import requests
import os
import dotenv

dotenv.load_dotenv()

response = requests.post("http://localhost:8000/generate-report", json={
    "model": "gpt-4o-mini",
    "theme": "AI",
    "industry": "Technology",
    "countries": ["United States", "Canada"],
    "from_year": "2020",
    "to_year": "2024",
    "api_key": os.getenv("OPENAI_API_KEY")
})

print(response.json())