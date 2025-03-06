import json
import nbformat as nbf
import os


reports = json.load(open("backend/output_files/reports.json", "r"))

def generate_markdown(topics, reports):

    if os.path.exists("backend/output_files/report.md"):
        os.remove("backend/output_files/report.md")

    if isinstance(reports, str):
        reports = json.loads(reports)

    for topic in topics:
        markdown_content = f"# {topic}\n\n"

        for report in reports:
            if report['topic'] == topic:
                markdown_content += f"## {report['prompt'].strip()}\n\n"
                markdown_content += f"{report['report']}\n\n"
                if report['sources']:
                    markdown_content += "### Sources\n"
                    for index, source in enumerate(report['sources']):
                        if source.startswith("-"):
                            markdown_content += f"{source}\n"
                        elif source.startswith(f"{index + 1}."):
                            markdown_content += f"{source}\n"
                        else:
                            markdown_content += f"- {source}\n"
                    markdown_content += "\n"

        with open("backend/output_files/report.md", "a") as f:
            f.write("\n" + markdown_content)


generate_markdown(["Market Size and Dynamics"], reports)