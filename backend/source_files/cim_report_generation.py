from pydantic import BaseModel
from openai import OpenAI
import os
import dotenv
from pathlib import Path
dotenv.load_dotenv()


async def cim_generate_report(prompt_1_and_2, prompt_3, prompt_4, file, client, model, send_status_update, title_file):
    await send_status_update("Searching document for information ...")

    file_content = await file.read()
    current_dir = Path(__file__).parent.parent 
    output_dir = current_dir / "output_files"
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
    
    temp_pdf = output_dir / f"{title_file}.pdf"
    with open(temp_pdf, "wb") as f:
        f.write(file_content)

    assistant = client.beta.assistants.create(
        name="Private Equity Analyst",
        instructions="You are an expert private equity analyst. Answer questions about the CIM report, according to the prompt. Use the attached file as your knowledge base.",
        model=model,
        tools=[{"type": "file_search"}],
    )

    message_file = client.files.create(
        file=open(temp_pdf, "rb"),
        purpose="assistants"
    )

    await send_status_update("First and second prompts sent ...")

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": prompt_1_and_2,
                "attachments": [{ "file_id": message_file.id, "tools": [{"type": "file_search"}] }],
            }
        ]
    )



    run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    report_part_1 = messages[0].content[0].text.value

    await send_status_update("Third prompt sent ...")

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt_3,
    )
    run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    report_part_2 = messages[0].content[0].text.value

    await send_status_update("Fourth prompt sent ...")

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt_4,
    )
    run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant.id)
    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    report_part_3 = messages[0].content[0].text.value

    await send_status_update("Report generated successfully")

    full_report = f"{report_part_1}\n\n{report_part_2}\n\n{report_part_3}"

    output_file = output_dir / "cim_report.md"
    with open(output_file, "w") as f:
        f.write(full_report)

    os.remove(temp_pdf)
    client.files.delete(message_file.id)
    client.beta.assistants.delete(assistant.id)

    return full_report
