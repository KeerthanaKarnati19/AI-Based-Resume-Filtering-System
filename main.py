import streamlit as st
import pandas as pd
from resume_parser import parse_resume
from extractor import extract_features, extract_skills
from similarity import compute_similarity_batch
from scorer import calculate_score

st.set_page_config(page_title="AI Resume Screener", page_icon="🚀", layout="wide")

st.title("🚀 Cognitive Resume Screening Dashboard")

# Upload
uploaded_files = st.file_uploader(
    "📂 Upload resumes (max 50)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if uploaded_files and len(uploaded_files) > 50:
    st.error("Maximum 50 resumes allowed.")
    st.stop()

# JD input
jd_text = st.text_area("📝 Enter Job Description")

# Sidebar
st.sidebar.header("⚖️ HR Weight Control")
skill_weight = st.sidebar.slider("Skills Weight", 0.0, 1.0, 0.5)
similarity_weight = st.sidebar.slider("Similarity Weight", 0.0, 1.0, 0.5)

weights = {
    "skills": skill_weight,
    "similarity": similarity_weight
}

if uploaded_files and jd_text:

    texts = []
    results = []

    jd_skills = extract_skills(jd_text)

    # Parse resumes
    for file in uploaded_files:
        if file.size > 5 * 1024 * 1024:
            st.warning(f"{file.name} too large, skipped.")
            continue
        texts.append(parse_resume(file))

    # Batch similarity
    similarity_scores = compute_similarity_batch(texts, jd_text)

    progress = st.progress(0)

    for i, file in enumerate(uploaded_files):

        features = extract_features(texts[i])
        similarity = similarity_scores[i][0]

        score = calculate_score(features, jd_skills, similarity, weights)

        results.append({
            "Name": features["name"],
            "Score": score,
            "Skills": ", ".join(features["skills"])
        })

        progress.progress((i + 1) / len(uploaded_files))

    # DataFrame
    df = pd.DataFrame(results)
    df = df.sort_values(by="Score", ascending=False)

    st.success(f"✅ Processed {len(df)} resumes")

    # Top candidate
    top = df.iloc[0]
    st.markdown("## 🏆 Top Candidate")
    st.success(f"**{top['Name']}** with score **{top['Score']}**")

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Candidate Scores")
        st.bar_chart(df.set_index("Name")["Score"])

    with col2:
        st.subheader("📋 Full Ranking")
        st.dataframe(df, use_container_width=True)

    # Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Results", csv, "results.csv", "text/csv")