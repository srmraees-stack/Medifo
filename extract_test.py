import google.generativeai as genai
import os
import json
import PIL.Image
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

PROMPT = """Extract the following from this discharge document into ONLY valid JSON, no other text, no markdown:
{
  "diagnosis": "",
  "discharge_medications": [
    {"name": "", "dose": "", "frequency": "", "duration": "", "route": ""}
  ],
  "diet_restrictions": [""],
  "follow_up": {"doctor": "", "date": "", "reason": ""},
  "warning_signs": [""]
}

Important rules:
- Only include DISCHARGE medications (what the patient takes home), NOT medicines given during the hospital stay.
- If a field is not present in the document, use an empty string or empty array.
- Do NOT invent or guess any information that isn't explicitly written."""

def extract(image_path):
    img = PIL.Image.open(image_path)
    response = model.generate_content(
        [PROMPT, img],
        generation_config={"response_mime_type": "application/json"}
    )
    return response.text

if __name__ == "__main__":
    path = "test_documents/mock1_pneumonia.jpg"
    result = extract(path)
    print("RAW OUTPUT:\n", result)
    print("\nPARSED:\n", json.dumps(json.loads(result), indent=2))