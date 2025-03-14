# Market Research Report Generator

This application is an AI-powered platform for generating market research reports and analyzing Confidential Information Memorandums (CIMs). It leverages OpenAI's models to create detailed analyses based on user specifications.

## Features

### Theme-Based Market Research
- Search and analyze market themes with specific geographic focus (US, UK, EU)
- Set custom time periods for analysis
- Generate comprehensive market research reports using various OpenAI models
- Download reports in multiple formats (HTML, PDF, Markdown, Text)

### CIM Summary Analysis
- Upload and analyze Confidential Information Memorandums (PDFs)
- Select specific analysis types:
  - Founding & Headquarters
  - Business Overview
  - Customer Base
  - Value Proposition
  - Customer Concentration
  - Geographic Breakdown
  - Key Assets
  - Employee Overview
  - Financial Breakdown
- Advanced filtering options:
  - Multiple embedding models (MiniLM, T5 Base, ALBERT, MPNet-QA)
  - Adjustable similarity thresholds for content relevance
- Download processed reports in multiple formats (HTML, PDF, Markdown, Text)

## Setup

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage Backend

```bash
cd backend
python main.py
```

## Usage Frontend

```bash
cd frontend
npm start
```


## Output

The application will generate reports in the following formats:
- HTML: Interactive web-based reports
- PDF: Formatted documents for sharing
- Markdown: Text-based format with formatting
- Text: Plain text version of the reports