import json
import subprocess
import re

# Load one sample response
with open("evaluation.json", "r", encoding="utf-8") as f:
    data = json.load(f)

question = data[0]["question_text"]
response_text = data[0]["responses"][0]["response_text"]

# Full criteria descriptions
criteria_descriptions = {
    "relevance": "How well the response addresses the question.",
    "clarity": "How clearly and understandably the response is written.",
    "actionability": "Whether the advice includes specific, actionable steps.",
    "empathy_tone": "Whether the tone is supportive, encouraging, and empathetic.",
    "depth_expertise": "How much expertise and insight the response demonstrates.",
    "personalization": "Whether the advice feels tailored to the mentee's situation.",
    "bias_fairness": "Whether the response is unbiased, inclusive, and fair."
}

# Build criteria block
criteria_text = "\n".join([f"{key}: {desc}" for key, desc in criteria_descriptions.items()])

# Updated prompt with definitions
prompt = f"""
Evaluate the following mentorship response based on 7 criteria. Score each from 1 (poor) to 5 (excellent).

Please return only a JSON object like this:
{{"relevance": 4, "clarity": 5, ..., "bias_fairness": 4}}

Descriptions of each criterion:
{criteria_text}

Response:
\"\"\"{response_text}\"\"\"
"""

# Run Mistral locally
try:
    result = subprocess.run(
        ["./build/bin/llama-cli", "-m", "models/mistral.gguf", "-p", prompt],
        capture_output=True,
        text=True,
        timeout=450
    )

    output = result.stdout.strip()
    print("🧠 Raw Output:\n", output)

    # Extract final JSON block
    matches = re.findall(r'{.*?}', output, re.DOTALL)
    if matches:
        json_text = matches[-1]
        try:
            scores = json.loads(json_text)
            print("\n✅ Parsed Scores:")
            print(scores)
            print("\n📊 Total Score:", sum(scores.values()))
        except Exception as parse_error:
            print("❌ JSON Parse Error:", parse_error)
            print("\n🧾 Extracted JSON text:\n", json_text)
    else:
        print("❌ No JSON object found in output.")

except Exception as e:
    print("❌ Error:", e)