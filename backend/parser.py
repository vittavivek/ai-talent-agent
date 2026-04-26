import os
import json
from dotenv import load_dotenv

load_dotenv()

# Try to use LLM, fallback if fails
def safe_parse(prompt):
    try:
        from google.genai import Client
        client = Client(api_key=os.getenv("GEMINI_API_KEY"))

        res = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return res.text
    except Exception as e:
        print("LLM failed, fallback used:", e)
        return None


def parse_jd(jd):
    prompt = f"""
    Extract structured data from this job description.

    Return JSON:
    {{
      "skills": [],
      "role": "",
      "experience": ""
    }}

    JD: {jd}
    """

    result = safe_parse(prompt)

    if result:
        try:
            return json.loads(result)
        except:
            pass

    # fallback
    return {
        "skills": [],
        "role": "Unknown",
        "experience": "Unknown",
        "raw_text": jd
    }


def parse_resume(text):
    prompt = f"""
    Extract structured data from this resume.

    Return JSON:
    {{
      "skills": [],
      "experience": "",
      "projects": []
    }}

    Resume: {text}
    """

    result = safe_parse(prompt)

    if result:
        try:
            return json.loads(result)
        except:
            pass
    return {
        "skills": [],
        "experience": "Unknown",
        "projects": [],
        "raw_text": text
    }