import json
import pandas as pd

# Load the evaluated JSON
with open("evaluation_scored.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare a list to store flattened results
rows = []

# Loop through each question and its responses
for q in data:
    question_id = q["question_id"]
    question_text = q["question_text"]

    for response in q["responses"]:
        row = {
            "question_id": question_id,
            "question_text": question_text,
            "responder_id": response["responder_id"],
            "response_text": response["response_text"],
            "relevance": response["evaluation"].get("relevance"),
            "clarity": response["evaluation"].get("clarity"),
            "actionability": response["evaluation"].get("actionability"),
            "empathy_tone": response["evaluation"].get("empathy_tone"),
            "depth_expertise": response["evaluation"].get("depth_expertise"),
            "personalization": response["evaluation"].get("personalization"),
            "bias_fairness": response["evaluation"].get("bias_fairness"),
            "evaluation_total": response.get("evaluation_total")
        }
        rows.append(row)

# Create a DataFrame and export to Excel
df = pd.DataFrame(rows)
df.to_excel("evaluated_responses.xlsx", index=False)

print("✅ Done: Exported to 'evaluated_responses.xlsx'")