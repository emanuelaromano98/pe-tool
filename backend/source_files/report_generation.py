from pydantic import BaseModel
from openai import OpenAI
import os
import dotenv
from pathlib import Path
dotenv.load_dotenv()

async def generate_report(prompts, topic, countries, from_year, to_year, client, model, send_status_update):

    await send_status_update("Deep research in progress...")

    # First prompt
    messages = [
        {"role": "system", "content": "You are a Report Generation GPT. Generate a report on the given prompt. Remember the focus is on the {topic}."},
        {"role": "user", "content": prompts[0]}
    ]

    # Get first response
    first_response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    first_response_text = first_response.choices[0].message.content

    await send_status_update("Summarizing report...")

    # Second prompt - add to conversation
    messages.extend([
        {"role": "assistant", "content": first_response_text},
        {"role": "user", "content": prompts[1]}
    ])

    # Get second response
    second_response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    report_generation = second_response.choices[0].message.content
    current_dir = Path(__file__).parent.parent 
    output_dir = current_dir / "output_files"
    
    # Create output directory if it doesn't exist
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write the file using proper path joining
    output_file = output_dir / "report.md"
    with open(output_file, "w") as f:
        f.write(report_generation)
    
    await send_status_update("Report generation complete...")

    return report_generation
