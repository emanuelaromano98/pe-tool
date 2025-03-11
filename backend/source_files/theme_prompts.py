prompt_1 = """
You are a managing partner and an investment professional at Warren Equity Partners, a low- to mid-market private equity firm. Your task is to research and do a deep dive into {theme} in {countries} as a potential new investment theme and sub-sector, and to identify suitable acquisition target companies to invest in. Provide the following headings in the order that they appear: 
   
   - a thorough analysis of the sub-sector; 
   - a detailed Market Overview, theme background, and description of it; 
   - Market Size and/or Total Addressable Market (TAM) and its CAGR in {countries} for {from_year}-{to_year} from reputable and reliable sources; 
   - full list of Services and Products in this new investment theme;
   - overall Industry Trends; 
   - Key Growth Drivers; 
   - a complete description and listing of its Value Chain;
   - a full list for each of Products and Services Offering in this theme; 
   - a comprehensive list of End Markets;
   - a complete analysis of the competitive landscape, alongside a ranking of how fragmented it is (one of three options: low, medium or high), a minimum of 3-5 Market Leaders and their respective Market Share; 
   - an overview of Emerging Technologies and Regulatory and Policy Considerations that could materially impact the industry as well as an analysis of what types of investment opportunities may arise as a result;
   - a description of Valuation Benchmarks and M&A trends in this theme; 
   - a list of Notable Deal Activity and comparable transactions in the last 5 years, presented as a table with the following column headings of Date of the Deal (month and year), Acquirer, Target, and Deal Value. Be sure to list the most recent deal first in chronological order;
   - and a table with a comprehensive list of potential targets for acquisition and roll-up (so to build a platform) in {countries} with revenues or enterprise value of less than $500 mm. Make sure these potential targets are private companies (including family owned) - exclude public companies, those owned by other private equity companies, or subsidiaries of large companies. Present this table with column headings of Name of the Company, its Headquarter location (city and state), its home website address, a short one-sentence Description of what it does, most recent Annual Revenues (if estimated, designate "est"), Number of Employees (if you can't find it, state "N/A"), what Business Sub-Segments it covers, and End-Markets it serves. 

For your research, please make sure your output is correct, double-check your sources and use reliable sources only, and ensure accuracy and reliability (do not make up company names). Thank you. 
"""

prompt_2 = """
summarize your entire output with the following categories and word limits for each category: 

- Description (maximum of 50 words)
- Investment Opportunity & Thesis (maximum of 65 words), for which you will provide a concise rationale on why this theme is a good fit for Warren Equity Partners, how it meshes with its investment mandate and other sectors it invests in, and potential for above-average risk-adjusted returns. Be precise and do not state generalities. 
- Market Size, TAM & CAGR, including Services and Products (maximum of 130 words)
- Industry Trends (maximum of 50 words)
- Key Growth Drivers (maximum of 30 words)
- Value Chain (maximum of 60 words)
- Product/Services Offering (separate summary list for Products and then Services - maximum of 65 words)
- End Markets (maximum of 25 words)
- Competitive Landscape, specially how fragmented the industry is (low, medium or high) in general and how fragmented each of the main components are (low, medium or high) (maximum of 20 words)
- Top 5 Market Leaders and their individual Market Share expressed in percentage as well as a short description of how their market share has changed over the last 3-5 years (maximum of 35 words)

Also provide a table for Notable Deal Activity (list most recent deals first) as well as a table for Potential Acquisition Targets. Do you state the word limits in your output next to each category; only include the category title (example: Description, Market Size, etc.). Thank you. 
"""


def generate_prompt_1(theme, countries, from_year, to_year):
    if len(countries) == 1:
        countries = countries[0]
    elif len(countries) == 2:
        countries = " and ".join(countries)
    else:
        countries = ", ".join(countries[:-1]) + " and " + countries[-1]
    prompt = prompt_1.format(theme=theme, countries=countries, from_year=from_year, to_year=to_year)
    return prompt


def generate_prompt_2():
    return prompt_2