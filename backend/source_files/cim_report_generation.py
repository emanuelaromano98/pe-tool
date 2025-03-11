from pydantic import BaseModel
from openai import OpenAI
import os
import dotenv
from pathlib import Path
dotenv.load_dotenv()

async def cim_generate_report(prompt, file, client, model, send_status_update):
    await send_status_update("Searching document for information...")

    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "file_id": file.id,
                    },
                    {
                        "type": "input_text",
                        "text": prompt,
                    },
                ]
            }
        ]
    )

    report_generation = response.choices[0].message.content
    current_dir = Path(__file__).parent.parent 
    output_dir = current_dir / "output_files"
    
    # Create output directory if it doesn't exist
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write the file using proper path joining
    output_file = output_dir / "cim_report.md"
    with open(output_file, "w") as f:
        f.write(report_generation)
    
    return report_generation
