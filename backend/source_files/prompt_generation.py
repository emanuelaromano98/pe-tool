from pydantic import BaseModel

def generate_prompt(industry, topic, client, model):
    class PromptGeneration(BaseModel):
        input_prompt: str
        improved_prompt: str
        output_text: str


    prompt = f"Generate a list of prompts to generate an industry report on the {industry} industry. Focus on {topic}"

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "You are a Prompt Engineer GPT. Improve the given prompt."},
            {"role": "user", "content": "Improve the following prompt: " + prompt},
        ],
        response_format=PromptGeneration,
    )

    prompt_generation = completion.choices[0].message.parsed

    with open("backend/output_files/output_prompts.txt", "w") as f:
        f.write(f"{prompt_generation.output_text}\n")