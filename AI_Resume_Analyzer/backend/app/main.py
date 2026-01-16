from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import re
import joblib

# -----------------------
# Initialize FastAPI
# -----------------------
app = FastAPI(title="AI Resume Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# Load ML model & vectorizer
# -----------------------
clf = joblib.load("app/resume_clf.pkl")
vectorizer = joblib.load("app/tfidf_vectorizer.pkl")

# -----------------------
# Helper functions
# -----------------------
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_basic_info(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    name = lines[0] if lines else "Unknown"
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0) if email_match else None
    phone_match = re.search(r'\+?\d[\d\s-]{7,}\d', text)
    phone = phone_match.group(0) if phone_match else None
    return {"name": name, "email": email, "phone": phone}

def extract_skills(text, skills_list=None):
    if not skills_list:
        skills_list = ["Python", "Java", "C++", "Django", "React", "TensorFlow", "PyTorch", "SQL"]
    found = []
    for skill in skills_list:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found.append(skill)
    return found

def estimate_experience(text):
    work_lines = []
    for line in text.split("\n"):
        if re.search(r'(experience|worked|role|job|internship|position|employment)', line, re.IGNORECASE):
            work_lines.append(line)
    text_work = "\n".join(work_lines)
    years = re.findall(r'(\d{4})\s*[-to]+\s*(\d{4})', text_work)
    total_years = 0
    for start, end in years:
        try:
            total_years += int(end) - int(start)
        except:
            continue
    return total_years

def experience_level(years):
    if years <= 2:
        return "Junior"
    elif years <= 5:
        return "Mid"
    else:
        return "Senior"

def extract_education(text):
    education_keywords = ["university", "college", "institute", "school", "academy"]
    degree_keywords = ["bsc", "msc", "phd", "mba", "bachelor", "master", "high school", "ssc", "hsc", "diploma"]
    exclude_keywords = ["project", "team leader", "internship", "experience", "worked", "position", "role",
                        "job", "employment", "training", "certification", "workshop", "course", "organized by", "seminar"]

    seen_institutions = set()
    edu_structured = []

    for line in text.split("\n"):
        line_lower = line.lower()
        if any(exk in line_lower for exk in exclude_keywords):
            continue
        if not any(k in line_lower for k in education_keywords + degree_keywords):
            continue

        # Find all institutions in line
        institutions = re.findall(r'([A-Za-z\s]+(?:university|college|institute|school|academy))', line, re.IGNORECASE)

        for inst in institutions:
            words = inst.strip().split()
            inst_clean = " ".join(dict.fromkeys(words))  # remove repeated words

            if inst_clean.lower() in seen_institutions:
                continue
            seen_institutions.add(inst_clean.lower())

            # Degree
            degree_found = ""
            for deg in degree_keywords:
                if deg in line_lower:
                    degree_found = deg.upper() if len(deg) <= 4 else deg.title()
                    break

            # Year
            year_match = re.search(r'(\d{4})\s*[-to]+\s*(\d{4})', line)
            year = f"{year_match.group(1)}-{year_match.group(2)}" if year_match else ""

            edu_structured.append({
                "institution": inst_clean,
                "degree": degree_found,
                "year": year
            })

    return edu_structured if edu_structured else []

# -----------------------
# /analyze endpoint
# -----------------------
@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(None), raw_text: str = Form(None)):
    if file:
        temp_path = "temp_resume.pdf"
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)
        text = extract_text_from_pdf(temp_path)
    elif raw_text:
        text = raw_text
    else:
        return {"error": "No file or text provided"}

    basic_info = extract_basic_info(text)
    skills = extract_skills(text)
    experience_years = estimate_experience(text)
    exp_level = experience_level(experience_years)
    education = extract_education(text)

    # ML Classification
    text_vec = vectorizer.transform([text])
    pred_label = clf.predict(text_vec)[0]
    pred_prob = clf.predict_proba(text_vec).max()

    return {
        "name": basic_info["name"],
        "email": basic_info["email"],
        "phone": basic_info["phone"],
        "skills": skills,
        "experience_years": experience_years,
        "experience_level": exp_level,
        "classification": pred_label,
        "confidence": round(float(pred_prob), 2),
        "education": education
    }

# -----------------------
# Root
# -----------------------
@app.get("/")
def root():
    return {"status": "API is running"}
