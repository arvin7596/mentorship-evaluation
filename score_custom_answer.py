import subprocess
import json
import re

model_path = "./models/mistral.gguf"
llama_bin = "./build/bin/llama-cli" 

question = "12.What are the job prospects and average salary ranges in different software engineering domains (e.g., AI, web, embedded systems)?"

custom_response = """
The salary range depends on many factors, like which level you are applying for (junior, midlevel, senior, or even manager), and job details can affect that. if it is a complicated position and requires special skills, that would be higher in salary. The best place to find out is LinkedIn job posts or Indeed, but generally, I believe AI ranges in salaries is more than others. """

prompt = f"""
You are an AI trained to evaluate mentorship responses based on seven criteria.

Here is the question the response is answering:
"{question}"

Score the following mentorship response from 1 (poor) to 5 (excellent) on each of these:

1. Relevance: Does it address the question directly?
2. Clarity: Is it clear and well-structured?
3. Actionability: Does it provide concrete, useful advice?
4. Empathy_Tone: Is the tone understanding, respectful, and encouraging?
5. Depth_Expertise: Does it reflect deep or practical knowledge?
6. Personalization: Is it tailored to a junior software engineer's context?
7. Bias_Fairness: Is the response inclusive and fair?

Return only a valid JSON object like:
{{"relevance": 4, "clarity": 5, ..., "bias_fairness": 4}}

Mentorship Response:
\"\"\"{custom_response.strip()}\"\"\"
"""

print("🧠 Evaluating with Mistral...")

try:
    result = subprocess.run(
        [llama_bin, "-m", model_path, "-p", prompt],
        capture_output=True,
        text=True,
        timeout=450
    )

    output = result.stdout.strip()
    print("🧠 Raw Output:\n", output)

    # Extract all JSON-like strings
    json_matches = re.findall(r"\{[^{}]*\}", output)
    if json_matches:
        # Pick the last one (usually the actual scores)
        json_str = json_matches[-1]
        scores = json.loads(json_str)
        total = sum(scores.values())
        scores["total_score"] = total
        print("\n✅ Final Evaluation:\n", json.dumps(scores, indent=2))
    else:
        print("❌ No valid JSON found in model output.")

except subprocess.TimeoutExpired:
    print("⏱️ Mistral evaluation timed out.")
except Exception as e:
    print("❌ Error:", e)
