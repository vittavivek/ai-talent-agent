def compute_interest(resume_data, jd_data):

    skills = resume_data.get("skills", [])
    jd_skills = jd_data.get("skills", [])

    matched = set(skills) & set(jd_skills)

    score = 40 + (len(matched) * 15) + (len(skills) * 2)
    score = min(score, 95)

    # dynamic reply
    if score > 80:
        reply = "Highly interested and actively looking"
    elif score > 65:
        reply = "Open to opportunities in this domain"
    elif score > 50:
        reply = "Somewhat interested depending on role"
    else:
        reply = "Not actively looking right now"

    return score, reply, matched