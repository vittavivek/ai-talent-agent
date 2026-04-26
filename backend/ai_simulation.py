def parse_jd(jd):
    skills_db = ["Python", "React", "Node", "MongoDB", "AI", "Machine Learning", "FastAPI"]

    skills = [s for s in skills_db if s.lower() in jd.lower()]

    return {
        "skills": skills,
        "raw_text": jd
    }