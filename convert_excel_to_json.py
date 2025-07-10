import pandas as pd
import json

# Load your Excel file (update the file path if needed)
excel_path = "Survey_Human_Responses.xlsx"
df = pd.read_excel(excel_path)

# Create a list to hold structured JSON entries
response_list = []

# Loop over each row (each response)
for idx, row in df.iterrows():
    entry = {
        "response_id": f"response_{idx+1}",
        "question_id": row.get("question_id", ""),
        "question_text": row.get("question_text", ""),
        "responder_id": row.get("responder_id", ""),
        "responder_name": row.get("responder_name", ""),
        "responder_type": row.get("responder_type", ""),
        "response_text": row.get("response_text", ""),
        "criteria": {
            "relevance": None,
            "clarity": None,
            "actionability": None,
            "empathy_tone": None,
            "depth_expertise": None,
            "personalization": None,
            "bias_fairness": None
        }
    }
    response_list.append(entry)

# Save the result to a JSON file
output_path = "responses_for_evaluation.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(response_list, f, indent=2, ensure_ascii=False)

print(f"✅ JSON file created successfully: {output_path}")
