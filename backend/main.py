from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import re
import asyncio
from fastapi.staticfiles import StaticFiles

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


def normalize_skill_text(skill):
    if not isinstance(skill, str):
        return ""
    text = skill.lower().strip()
    text = re.sub(r"[^\w\s#+]", " ", text)
    text = re.sub(r"\s+", " ", text)
    if text == "ml":
        return "machine learning"
    if text == "rest":
        return "api"
    return text


def compute_matched_skills(jd_skills, resume_skills):
    jd_norm = [normalize_skill_text(s) for s in jd_skills]
    res_norm = [normalize_skill_text(s) for s in resume_skills]
    matches = set()
    for j in jd_norm:
        for r in res_norm:
            if j and r and (j == r or j in r or r in j):
                matches.add(j if len(j) <= len(r) else r)
    return sorted(matches)


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
    jd_data = await parse_jd(jd)
    jd_skills = [s.strip().lower() for s in jd_data.get("skills", []) if isinstance(s, str)]

    # Read all resume texts (sync I/O, but fast)
    resume_texts = [read_resume(file.file) for file in resumes]
    filenames = [file.filename for file in resumes]

    # Parse all resumes in parallel
    resume_data_list = await asyncio.gather(*[parse_resume(text) for text in resume_texts])

    for i, (resume_text, resume_data, filename) in enumerate(zip(resume_texts, resume_data_list, filenames)):
        resume_skills = [s.strip().lower() for s in resume_data.get("skills", []) if isinstance(s, str)]

        # ✅ semantic match
        similarity = compute_similarity(jd, resume_text)
        match_score = round(float(similarity) * 100, 2)

        # ✅ matched skills (FIXED)
        matched_skills = compute_matched_skills(jd_skills, resume_skills)

        # ✅ interest scoring
        interest_score, reply, _ = compute_interest(resume_data, jd_data)

        # ✅ final score
        final_score = round(0.7 * match_score + 0.3 * interest_score, 2)

        results.append({
            "name": filename,
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

# Mount the frontend static files at the root
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")