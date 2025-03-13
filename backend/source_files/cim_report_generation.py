from pydantic import BaseModel
from openai import OpenAI
import os
import dotenv
from pathlib import Path
dotenv.load_dotenv()

async def cim_generate_report(prompt, file, client, model, send_status_update, title_file):
    await send_status_update("Searching document for information...")

    # Create a temporary file to store the uploaded content
    file_content = await file.read()
    current_dir = Path(__file__).parent.parent 
    output_dir = current_dir / "output_files"
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    temp_pdf = output_dir / f"{title_file}.pdf"
    with open(temp_pdf, "wb") as f:
        f.write(file_content)

    # Create assistant
    assistant = client.beta.assistants.create(
        name="Private Equity Analyst",
        instructions="You are an expert private equity analyst. Answer questions about the CIM report, according to the prompt. Use the attached file as your knowledge base.",
        model=model,
        tools=[{"type": "file_search"}],
    )

    # Upload the file directly from the uploaded content
    message_file = client.files.create(
        file=open(temp_pdf, "rb"),
        purpose="assistants"
    )

    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": prompt,
        "attachments": [{ "file_id": message_file.id, "tools": [{"type": "file_search"}] }],
        }
    ]
    )

    run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    print("\nmessages: ", messages)
    report_generation = messages[0].content[0].text.value
    print("\nreport_generation: ", report_generation)

    # Write the output report
    output_file = output_dir / "cim_report.md"
    with open(output_file, "w") as f:
        f.write(report_generation)

    # Cleanup
    os.remove(temp_pdf)
    client.files.delete(message_file.id)
    client.beta.assistants.delete(assistant.id)

    return report_generation
