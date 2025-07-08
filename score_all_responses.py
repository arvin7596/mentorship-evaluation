import json
import subprocess
import re
import time

# File paths
INPUT_JSON = "evaluation.json"
OUTPUT_JSON = "evaluation_scored.json"

# Descriptions of each criterion
criteria_descriptions = {
    "relevance": "How well the response addresses the question.",
    "clarity": "How clearly and understandably the response is written.",
    "actionability": "Whether the advice includes specific, actionable steps.",
    "empathy_tone": "Whether the tone is supportive, encouraging, and empathetic.",
    "depth_expertise": "How much expertise and insight the response demonstrates.",
    "personalization": "Whether the advice feels tailored to the mentee's situation.",
    "bias_fairness": "Whether the response is unbiased, inclusive, and fair."
}

# Combine descriptions into readable format
criteria_text = "\n".join([f"{k}: {v}" for k, v in criteria_descriptions.items()])

# Load dataset
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# Loop over each question/response
for question in data:
    print(f"🔍 Evaluating: {question['question_id']}")

    for response in question["responses"]:
        print(f"  🧠 Scoring response from {response['responder_id']}...")

        # Skip if already scored
        if response["evaluation"]["relevance"] is not None:
            print("    ✅ Already scored. Skipping.")
            continue

        # Create the prompt
        prompt = f"""
Evaluate the following mentorship response based on the 7 criteria below.
Score each from 1 (poor) to 5 (excellent).
Return only a JSON object like this:
{{"relevance": 4, "clarity": 5, ..., "bias_fairness": 4}}

Criteria descriptions:
{criteria_text}

Response:
\"\"\"{response['response_text']}\"\"\"
"""

        # Run Mistral
        try:
            result = subprocess.run(
                ["./build/bin/llama-cli", "-m", "models/mistral.gguf", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=450
            )
            output = result.stdout.strip()

            # Extract last valid JSON
            matches = re.findall(r'{.*?}', output, re.DOTALL)
            if matches:
                json_text = matches[-1]
                try:
                    scores = json.loads(json_text)
                    response["evaluation"] = scores
                    response["evaluation_total"] = sum(scores.values())
                    print("    ✅ Scored.")
                except Exception as parse_error:
                    print("    ❌ JSON Parse Error. Skipping.")
                    print(json_text)
            else:
                print("    ❌ No JSON found in output.")

        except subprocess.TimeoutExpired:
            print("    ❌ Timeout. Skipping.")
        except Exception as e:
            print(f"    ❌ Error: {e}")

        # Optional: slow down between calls
        time.sleep(1)

# Save the updated file
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✅ All evaluations completed. Saved to 'evaluation_scored.json'.")