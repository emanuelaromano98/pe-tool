import subprocess
import os
from pathlib import Path
from typing import Optional
from weasyprint import HTML

def convert_markdown_to_html(input_file: str, output_file: Optional[str] = None) -> str:
    backend_dir = Path(__file__).parent.parent / "output_files"
    
    input_file = str(backend_dir / Path(input_file).name)
    
    if output_file is None:
        output_file = str(backend_dir / Path(input_file).with_suffix('.html').name)

    print(f"Converting Markdown to HTML:\n- Input: {input_file}\n- Output: {output_file}")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    try:
        subprocess.run([
            'pandoc', input_file, '-f', 'markdown', '-t', 'html', '-o', output_file,
            '--standalone', '--metadata', 'title=Market Research Report'
        ], check=True)
        
        return output_file
    
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to convert {input_file} to HTML: {e}")

def convert_markdown_to_txt(input_file: str, output_file: Optional[str] = None) -> str:
    backend_dir = Path(__file__).parent.parent / "output_files"
    
    input_file = str(backend_dir / Path(input_file).name)
    
    if output_file is None:
        output_file = str(backend_dir / Path(input_file).with_suffix('.txt').name)

    print(f"Converting Markdown to TXT:\n- Input: {input_file}\n- Output: {output_file}")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    try:
        subprocess.run([
            'pandoc', input_file, '-f', 'markdown', '-t', 'plain', '-o', output_file,
            '--standalone', '--metadata', 'title=Market Research Report'
        ], check=True)
        
        return output_file
    
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to convert {input_file} to TXT: {e}")

def convert_html_to_pdf(html_file: str, output_pdf: str) -> bool:
    backend_dir = Path(__file__).parent.parent / "output_files"
    
    html_file = str(backend_dir / Path(html_file).name)
    output_pdf = str(backend_dir / Path(output_pdf).name)

    print(f"Converting HTML to PDF:\n- Input: {html_file}\n- Output: {output_pdf}")

    if not os.path.exists(html_file):
        print(f"HTML file not found: {html_file}")
        return False
    
    try:
        HTML(html_file).write_pdf(output_pdf)
        return True
    except Exception as e:
        print(f"Failed to convert {html_file} to PDF: {e}")
        return False

def convert_markdown_to_all_formats(markdown_path: str):
    backend_dir = Path(__file__).parent.parent / "output_files"
    
    markdown_file = str(backend_dir / Path(markdown_path).name)
    html_path = str(Path(markdown_file).with_suffix('.html'))
    pdf_path = str(Path(markdown_file).with_suffix('.pdf'))
    txt_path = str(Path(markdown_file).with_suffix('.txt'))

    try:
        # Convert markdown to HTML
        html_success = convert_markdown_to_html(markdown_file, html_path)

        # Convert HTML to PDF
        pdf_success = convert_html_to_pdf(html_path, pdf_path)

        # Convert markdown to TXT
        txt_success = convert_markdown_to_txt(markdown_file, txt_path)

        return html_success, pdf_success, txt_success
    
    except Exception as e:
        print(f"Error in conversion chain: {e}")
        return None, None, None

if __name__ == "__main__":
    markdown_path = "report.md"
    html_success, pdf_success, txt_success = convert_markdown_to_all_formats(markdown_path)

    print("Conversion Results:")
    print(f"- HTML: {'Success' if html_success else 'Failed'}")
    print(f"- PDF: {'Success' if pdf_success else 'Failed'}")
    print(f"- TXT: {'Success' if txt_success else 'Failed'}")
