# Market Research Report Generator

This application is an AI-powered market research report generator that creates detailed reports based on specified industries and topics.

## Features
- Generates comprehensive market research reports using OpenAI
- Filters and processes reports for relevance
- Outputs results in multiple formats (JSON, Markdown, Jupyter Notebook)
- Handles multiple topics per industry
- Includes similarity-based content filtering

## Setup

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:

```bash
OPENAI_API_KEY=<your_openai_api_key>
```

## Usage

```bash
python main.py
```

## Output

The application will generate a report in the following formats:
- `reports.json`: JSON file containing all reports
- `report.ipynb`: Jupyter Notebook file with detailed report
- `report.md`: Markdown file with report content



