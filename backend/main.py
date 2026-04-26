from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

# old parser (keep temporarily for /rank)
from ai_simulation import parse_jd as old_parse_jd

# new modules
from parser import parse_jd, parse_resume
from resume_reader import read_resume
from semantic_matcher import compute_similarity
from interest_agent import compute_interest

# ✅ app
app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- OLD API (for existing frontend) ----------

class JDInput(BaseModel):
    jd: str


with open("candidates.json") as f:
    candidates = json.load(f)


def match_score(jd_skills, candidate):
    overlap = len(set(jd_skills) & set(candidate["skills"]))
    return round((overlap / max(len(jd_skills), 1)) * 100, 2)


@app.post("/rank")
def rank(data: JDInput):
    jd_data = old_parse_jd(data.jd)

    results = []

    for c in candidates:
        matched = list(set(jd_data["skills"]) & set(c["skills"]))
        match = match_score(jd_data["skills"], c)

        reply = "Interested in this role"
        interest = 70
        final = round(0.7 * match + 0.3 * interest, 2)

        results.append({
            "name": c["name"],
            "match_score": match,
            "interest_score": interest,
            "final_score": final,
            "matched_skills": matched,
            "reply": reply,
            "reason": f"Matched skills: {matched}"
        })

    results.sort(key=lambda x: x["final_score"], reverse=True)

    return {
        "parsed_jd": jd_data,
        "ranked_candidates": results
    }


# ---------- NEW API (AI PIPELINE) ----------

@app.post("/process")
async def process(jd: str = Form(...), resumes: list[UploadFile] = File(...)):

    results = []

    # parse JD
    jd_data = parse_jd(jd)
    jd_skills = jd_data.get("skills", [])

    for file in resumes:
        resume_text = read_resume(file.file)
        resume_data = parse_resume(resume_text)

        resume_skills = resume_data.get("skills", [])

        # ✅ semantic match
        similarity = compute_similarity(jd, resume_text)
        match_score = round(float(similarity) * 100, 2)

        # ✅ matched skills (FIXED)
        matched_skills = list(set(jd_skills) & set(resume_skills))

        # ✅ interest scoring
        interest_score, reply, _ = compute_interest(resume_data, jd_data)

        # ✅ final score
        final_score = round(0.7 * match_score + 0.3 * interest_score, 2)

        results.append({
            "name": file.filename,
            "match_score": match_score,
            "interest_score": interest_score,
            "final_score": final_score,
            "reply": reply,
            "matched_skills": matched_skills,
            "reason": f"Matched skills: {matched_skills}"
        })

    # ✅ ranking
    results.sort(key=lambda x: x["final_score"], reverse=True)

    return {
        "ranked_candidates": results
    }