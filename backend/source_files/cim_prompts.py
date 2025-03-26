prompt_1 = """
Doc Analysis
You are a managing partner and an investment professional at Warren Equity Partners, a low- to mid-market private equity firm. Your task is to do a thorough Analysis and a deep dive analysis into the attached Confidential Investment Memo (CIM) document and then provide accurate answers to questions provided. But before we dive into the analysis, here are the Analysis Guidelines to ensure clarity and consistency:

Accurately Reference Page Numbers 
    - For every fact, data point, or statement included in the memo, you must verify and confirm the exact page number in the CIM where the information is found. 
        - Use the format: ‘(Page X, CIM)’ 
        - If the information spans multiple pages, use: ‘(Pages X–Y,CIM)’ 
        - If no page number is visible or the data is not explicitly stated in the CIM, note: ‘This information is not explicitly stated in the CIM.’ 
        - Ensure that no placeholders (X) remain and that all data points reference specific, confirmed pages from the CIM. Double-check accuracy before applying changes.

Prohibit Illustrative Examples 
    - Never infer, estimate, or extrapolate page numbers. If the data or insight is not directly stated or confirmed in the CIM, do not include it in the memo. 
    - All page references must align exactly with the CIM document. 

Validate All Facts 
    - Revisit and manually verify page references to ensure they are 100% accurate before including them in the output. 

Incorporate External Validation 
    - Independently verify and cross-check key claims using reliable external sources (e.g., industry benchmarks, market research reports, government databases) to validate or challenge the claims in the CIM. Examples include:
        - Industry Benchmarks: PitchBook, S&P Capital IQ, FactSet, Preqin for EV/EBITDA multiples and M&A trends.
        - Market Trends: IBISWorld, Frost & Sullivan, or Statista for market size and growth rates.
        - Regulatory Standards: OSHA, EPA, and local government databases for environmental and compliance risks.
        - Legal and Litigation Data: PACER and LexisNexis for lawsuit history or regulatory violations.
    - Explicitly cite external sources using the following format: ‘According to [Source Name], [specific data or insight].’ Include full citations for transparency. 

Analysis & Insights: Compare and contrast the CIM’s claims with external findings. Identify discrepancies, risks, or areas where additional due diligence is required.

Accuracy & Double-Checking: 
    - Verify all financial, operational, and market data against independent sources. 
    - Ensure all metrics, trends, and benchmarks are factually supported and sourced.   

Sequential Prompt: CIM Source Differentiation and Critical Analysis Framework
To ensure clarity, transparency, and analytical rigor, all outputs must clearly distinguish between information sourced from the CIM and independent analysis.  Apply the following structured approach in every response:
	
    1.	CIM References: When citing the CIM, explicitly state “The CIM states…” and reference the specific source. Do not paraphrase without attribution. Double check for accuracy.
	2.	Contextual Critical Assessment: If the CIM-provided information contains claims, projections, assumptions, or subjective insights, provide a concise yet thorough evaluation of its credibility, potential biases, and limitations. Highlight inconsistencies or gaps and explicitly introduce independent critiques with “WEP.ai analysis…” to ensure transparency. Double check for accuracy.
        - No critical assessment is needed for objective, factual data such as founding date, headquarters location, or other verifiable details, unless there is reason to question their accuracy or relevance.
        - Apply critical assessment selectively where analysis adds value, such as for financial projections, strategic positioning, or qualitative statements.
	3.	Independent Analysis: Clearly label all proprietary insights, assessments, and conclusions as “WEP.ai analysis” to distinguish them from CIM-derived content. Independent analysis should go beyond summarization, offering original evaluation, contextual insights, and strategic interpretation. Double check for accuracy.

Maintain a precise, objective, and structured approach to enhance analytical integrity and clarity.
"""

prompt_2 = """Please provide the following key details about the company:"""

points = {
    "fh": "1.	Founding & Headquarters – When was the company founded, and where is it headquartered?",
    "bo": "2.	Business Overview – Describe what the company does in one concise sentence.",
    "cb": "3.	Customer Base – Define who their customers are in one concise sentence.",
    "vp": "4.	Value Proposition – Summarize the company’s unique value proposition in one concise sentence.",
    "cc": "5.	Customer Concentration – Describe the company's customer concentration in one concise sentence.",
    "gb": "6.	Geographic Breakdown – Describe the geographic breakdown of the company in one concise sentence.",
    "ka": "7.	Key Assets – Outline the company’s key assets in one concise sentence.",
    "eo": "8.	Employee Overview – Provide a brief description of the company’s workforce.",
    "fb": "9.	Financial Breakdown – Include revenue by service, end market, and customer."}




def generate_cim_prompt_part_1_and_2(analysis_types):
    prompt = prompt_1
    if "all" in analysis_types:
        for key in points.keys():
            prompt += "\n" + points[key] + "\n"
    else:
        for key in points.keys():
            if key in analysis_types:
                prompt += "\n" + points[key] + "\n"
    return prompt


prompt_3 = """
I'm the managing partner at Warren Equity Partners with deep expertise in due diligence, I'm evaluating this company for potential investment as a platform. My goal is to systematically assess the company’s differentiation and scalability to determine its potential for long-term growth and competitive advantage. Before we begin the analysis, I will provide the necessary sequential prompts.

Prompt Step 1: Core Differentiation & Market Position
- Title this section, 'Core Differentiation & Market Position'.
- Objective: Assess the company’s unique strengths and long-term competitive advantage.
- Key Questions:
    - What are the key differentiators compared to competitors?
    - Is differentiation based on technology, customer relationships, regulatory advantages, operational excellence, or pricing power?
    - How defensible are these differentiators, and what risks could erode them?
    - What barriers to entry exist for new competitors?
    - Does the company have proprietary IP, exclusive partnerships, or unique capabilities that create a lasting advantage?
- Risk Mitigation Strategies:
    - How can differentiation be reinforced or expanded to sustain long-term value?
    - Are there any emerging competitors, regulatory shifts, or technology changes that could impact defensibility?
    - What contingency plans exist if key differentiators weaken?
- For each independent analysis, label it as 'WEP.ai analysis'.

Prompt Step 2: Market Scalability & Addressable Market Expansion
- Title this section, 'Market Scalability & Addressable Market Expansion'.
- Objective: Evaluate the growth potential of the company in its market.
- Key Questions:
    - What is the Total Addressable Market (TAM), and how much is realistically accessible?
    - Does the company have a clear strategy for market share expansion (geographic, customer segments, product diversification)?
    - How scalable is the business model, cost structure, and operations?
    - What constraints (e.g., supply chain, regulatory, capital intensity) could hinder growth?
    - How well does the company leverage technology and automation to scale efficiently?
- Risk Mitigation Strategy:
    - What alternative expansion paths exist if the primary growth strategy fails?
    - How resilient is the company’s growth plan to macroeconomic downturns or industry shifts?
    - Are there contingency plans for scalability challenges, such as talent acquisition or production constraints?
- For each independent analysis, label it as 'WEP.ai analysis'.

Prompt Step 3: Competitive Landscape & Defensibility
- Title this section, 'Competitive Landscape & Defensibility'.
- Objective: Understand the competitive forces shaping the company’s position.
- Key Questions:
    - Who are the primary competitors, and how does this company differentiate itself?
    - Are there signs of pricing pressure or industry commoditization?
    - How strong is customer loyalty and retention?
    - Does the company benefit from high switching costs, network effects, or other defensibility factors?
- Risk Mitigation Strategy:
    - What strategic defenses can be built to maintain a competitive edge?
    - If pricing pressure increases, how can the company preserve margins and value proposition?
    - Are there acquisition or partnership opportunities to strengthen market positioning?
- For each independent analysis, label it as 'WEP.ai analysis'.

Prompt Step 4: Financial & Operational Scalability
- Title this section, 'Financial & Operational Scalability'.
- Objective: Assess financial sustainability and operational risks.
- Key Questions:
    - How do unit economics evolve with scale?
    - Are margins improving, stable, or declining as the company grows?
    - What is the CapEx vs. OpEx intensity of scaling the business?
    - Are there hidden risks or operational bottlenecks that could limit growth?
    - How does the working capital cycle change with expansion?
- Risk Mitigation Strategy:
    - What financial adjustments or operational efficiencies can enhance scalability?
    - Are there early warning signs of margin compression or capital inefficiencies?
    - How can the company improve capital deployment to maximize return on investment?
- For each independent analysis, label it as 'WEP.ai analysis'.
"""

def generate_cim_prompt_part_3():
    return prompt_3


prompt_4 = """
Title this section, 'Key Risks & Mitigation Strategy'.
- Objective: Identify key risks and propose targeted mitigation strategies.
- Key Risks to Assess:
    - Regulatory Risks: How could tariffs, compliance shifts, or industry regulations impact operations?
    - Macroeconomic Risks: Are there interest rate, inflation, or geopolitical factors that could affect the business?
    - Competitive Risks: Could new entrants or shifting customer preferences erode market share?
    - Operational Risks: Are there supply chain vulnerabilities, talent shortages, or execution challenges?
    - Financial Risks:
        - What assumptions in financial projections need further validation?
        - Revenue Predictability & Contractual Stability: Evaluate the proportion of upfront vs. recurring revenue, customer concentration risks, and pricing elasticity.
        - Management’s Forward Projections & Validation: Analyze the reasonableness of revenue growth forecasts, margin expansion expectations, and new market expansion risks.
- Risk Mitigation Strategy:
    - What proactive strategies can be implemented to reduce exposure?
    - Are there insurance, hedging, or strategic diversification tactics that would protect the business?
    - What contingency planning exists for worst-case scenarios?
- For each independent analysis, label it as 'WEP.ai analysis'.
"""

def generate_cim_prompt_part_4():
    return prompt_4