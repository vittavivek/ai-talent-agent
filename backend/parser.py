import os
import re
import json
import asyncio
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SKILLS = {
    "python", "javascript", "java", "c#", "c++", "sql", "html", "css",
    "react", "node", "django", "flask", "fastapi", "docker", "kubernetes",
    "aws", "azure", "gcp", "machine learning", "ml", "data science",
    "nlp", "pytorch", "tensorflow", "pandas", "numpy", "git", "rest",
    "graphql", "devops", "linux", "bash", "api", "cloud", "automation",
    "swift", "kotlin", "typescript", "scala", "spark", "hadoop"
}

SKILL_PATTERN = re.compile(r"\b([A-Za-z#+]+(?:\s+[A-Za-z#+]+)?)\b")


def normalize_skill(token):
    token = token.strip().lower()
    if token == "ml":
        return "machine learning"
    if token == "rest":
        return "api"
    return token


def extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.S)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    return None


def extract_skills(text):
    text = text.lower()
    skills = set()

    for skill in DEFAULT_SKILLS:
        if skill in text:
            skills.add(skill)

    if not skills:
        for token in SKILL_PATTERN.findall(text):
            normalized = normalize_skill(token)
            if normalized in DEFAULT_SKILLS:
                skills.add(normalized)

    return sorted(skills)


def extract_experience(text):
    match = re.search(r"(\d+)\+?\s*years?", text, re.I)
    if match:
        return match.group(0)
    return "Unknown"


def extract_role(text):
    match = re.search(r"(senior|lead|principal|staff|junior|entry[- ]level|manager|engineer|developer|analyst|scientist)[^\n\r]*", text, re.I)
    if match:
        return match.group(0).strip()
    return "Unknown"


# Try to use LLM, fallback if fails
async def safe_parse(prompt):
    try:
        from google.genai import Client
        client = Client(api_key=os.getenv("GEMINI_API_KEY"))

        res = await client.models.generate_content_async(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return res.text
    except Exception as e:
        print("LLM failed, fallback used:", e)
        return None


async def parse_jd(jd):
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

    result = await safe_parse(prompt)

    if result:
        parsed = extract_json(result)
        if parsed and isinstance(parsed, dict):
            skills = parsed.get("skills") or []
            if isinstance(skills, str):
                skills = [skills]
            skills = [normalize_skill(s) for s in skills if isinstance(s, str)]
            skills = sorted(set(skills + extract_skills(jd)))
            return {
                "skills": skills,
                "role": parsed.get("role", "Unknown"),
                "experience": parsed.get("experience", "Unknown"),
                "raw_text": jd
            }

    return {
        "skills": extract_skills(jd),
        "role": extract_role(jd),
        "experience": extract_experience(jd),
        "raw_text": jd
    }


async def parse_resume(text):
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

    result = await safe_parse(prompt)

    if result:
        parsed = extract_json(result)
        if parsed and isinstance(parsed, dict):
            skills = parsed.get("skills") or []
            if isinstance(skills, str):
                skills = [skills]
            skills = [normalize_skill(s) for s in skills if isinstance(s, str)]
            skills = sorted(set(skills + extract_skills(text)))
            return {
                "skills": skills,
                "experience": parsed.get("experience", "Unknown"),
                "projects": parsed.get("projects", []),
                "raw_text": text
            }

    return {
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "projects": [],
        "raw_text": text
    }