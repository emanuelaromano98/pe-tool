from pydantic import BaseModel
import os
import json


async def generate_report(topic, client, model, send_status_update):
    class ReportGeneration(BaseModel):
        report: str
        sources: list[str]

    prompts = open("backend/output_files/output_prompts.txt", "r").readlines()
    reports = []
    for prompt in prompts:
        prompt = prompt.strip()
        if prompt and prompt[0].isdigit():
            i = 0
            while i < len(prompt) and (prompt[i].isdigit() or prompt[i] in '. '):
                i += 1
            prompt = "Question: " + prompt[i:].strip()
        await send_status_update(f"Generating for prompt: {prompt.split(':')[1].strip()}")
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Report Generation GPT. Generate a report on the given prompt. Remember the focus is on the {topic}."},
                {"role": "user", "content": "Generate a report on the following prompt: " + prompt},
            ],
            response_format=ReportGeneration,
        )

        report_generation = completion.choices[0].message.parsed
        reports.append({
            "topic": topic,
            "prompt": prompt,
            "report": report_generation.report,
            "sources": report_generation.sources
        })

    existing_reports = []
    if os.path.exists("backend/output_files/reports.json"):
        with open("backend/output_files/reports.json", "r") as f:
            try:
                existing_reports = json.load(f)
            except json.JSONDecodeError:
                existing_reports = []

    all_reports = existing_reports + reports

    with open("backend/output_files/reports.json", "w") as f:
        json.dump(all_reports, f, indent=4)

