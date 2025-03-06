import subprocess
import os
from pathlib import Path
from typing import Optional
from weasyprint import HTML

def convert_markdown_to_html(input_file: str, output_file: Optional[str] = None) -> str:
    # Check if input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # If output file is not specified, create one based on input file name
    if output_file is None:
        input_path = Path(input_file)
        output_file = str(input_path.with_suffix('.html'))
    
    try:
        # Run pandoc command to convert the file
        subprocess.run([
            'pandoc',
            input_file,
            '-f', 'markdown',
            '-t', 'html',
            '-o', output_file,
            '--standalone',  
            '--metadata', 'title=Market Research Report'
        ], check=True)
        
        return output_file
    
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(
            e.returncode,
            e.cmd,
            f"Failed to convert {input_file} to HTML: {e.output if e.output else ''}"
        )

def convert_html_to_pdf(html_file: str, output_pdf: str) -> bool:
    try:
        if not os.path.exists(html_file):
            print(f"HTML file not found: {html_file}")
            return False
            
        HTML(html_file).write_pdf(output_pdf)
        print(f"Successfully converted {html_file} to {output_pdf}")
        return True
    except Exception as e:
        print(f"Failed to convert {html_file} to PDF: {str(e)}")
        return False

def convert_markdown_to_all_formats(markdown_path: str) -> tuple[bool, bool]:
    try:
        # Define output paths
        html_path = str(Path(markdown_path).with_suffix('.html'))
        pdf_path = str(Path(markdown_path).with_suffix('.pdf'))
        
        # Convert markdown to HTML
        convert_markdown_to_html(markdown_path, html_path)
        
        # Convert HTML to PDF
        pdf_success = convert_html_to_pdf(html_path, pdf_path)
        
        return True, pdf_success
        
    except Exception as e:
        print(f"Error in conversion chain: {str(e)}")
        return False, False

if __name__ == "__main__":
    markdown_path = "backend/output_files/report.md"
    html_success, pdf_success = convert_markdown_to_all_formats(markdown_path)
    
    if html_success and pdf_success:
        print("All conversions completed successfully")
    else:
        print("Some conversions failed")


