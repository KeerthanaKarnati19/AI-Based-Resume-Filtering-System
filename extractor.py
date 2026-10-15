import spacy
import re

nlp = spacy.load("en_core_web_sm")


def load_skills():
    with open("data/skills.txt", "r") as f:
        return [s.strip().lower() for s in f.readlines()]


skills_db = load_skills()


def extract_email(text):
    match = re.findall(r'\S+@\S+', text)
    return match[0] if match else "N/A"


def extract_phone(text):
    match = re.findall(r'\d{10}', text)
    return match[0] if match else "N/A"


def extract_name(text):
    doc = nlp(text[:1000])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Unknown"


def extract_skills(text):
    text = text.lower()
    return list(set([skill for skill in skills_db if skill in text]))


def extract_features(text):
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "text": text
    }