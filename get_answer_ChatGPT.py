import openai


openai.api_key = "your-api-key-here"  # Replace with real key api

def get_gpt4_response(question):
    prompt = f"""You are acting as a professional career mentor for junior software engineers.
Provide a thoughtful, clear, and actionable response to the following question.
Try to be supportive, technically sound, and practical in your advice.

Mentorship Question:
"{question}"
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful and experienced mentor for software engineers."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response['choices'][0]['message']['content']

# Example usage
question = "How can I become more confident in code reviews as a junior developer?"
answer = get_gpt4_response(question)
print("GPT-4 Answer:\n", answer)
