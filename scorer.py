def calculate_score(resume, jd_skills, similarity_score, weights):

    if len(jd_skills) == 0:
        skill_match = 0
    else:
        skill_match = len(set(resume["skills"]) & set(jd_skills)) / len(jd_skills)

    final_score = (
        skill_match * weights["skills"] +
        similarity_score * weights["similarity"]
    )

    return round(final_score, 3)