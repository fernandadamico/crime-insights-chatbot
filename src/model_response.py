import together

def load_prompt_template(path="assets/prompt_template.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def construct_prompt(question, parsed_input, crime_count, summary_text, template_path="assets/prompt_template.txt"):
    template = load_prompt_template(template_path)
    # Use .get() to avoid KeyError if key is missing
    prompt = template.format(
        question=question,
        intent=parsed_input.get('intent', ''),
        dates=parsed_input.get('dates', ''),
        years=parsed_input.get('years', ''),
        crime_types=parsed_input.get('crime_types', ''),
        community_areas=parsed_input.get('community_areas', ''),
        crime_count=crime_count,
        summary=summary_text
    )
    return prompt

def ask_question_with_together(prompt):
    response = together.Completion.create(
        model="mistralai/Mistral-7B-Instruct-v0.1",
        prompt=prompt,
        temperature=0,
        max_tokens=512,
    )
    
    return response.choices[0].text.strip()
