# AI Resume Analyzer + Classifier

AI Resume Analyzer is a full-stack application that extracts key information from resumes, classifies the job role, and estimates experience level. Users can upload PDF resumes or paste raw text directly. The system is built with FastAPI for the backend and React for the frontend. It includes a trained ML model for classification and uses TF-IDF for text vectorization.

Features include extracting Name, Email, Phone, Skills, Education, estimating experience level (Junior / Mid / Senior), and classifying resumes into categories: Software Engineer, AI/ML Engineer, Data Scientist, Web Developer, DevOps/Cloud Engineer, FullStack Developer. The frontend is simple, colorful, and displays results with confidence scores.

Project structure:

AI_Resume_Analyzer/

├─ backend/

│   ├─ app/

│   │   ├─ __init__.py

│   │   ├─ main.py

│   │   ├─ resume_clf.pkl

│   │   └─ tfidf_vectorizer.pkl

│   └─ requirements.txt

├─ frontend/

│   ├─ public/

│   ├─ src/

│   │   ├─ App.js

│   │   └─ App.css

│   └─ package.json

└─ README.md


Backend Setup:

1. Navigate to backend folder: `cd backend`
2. Create and activate virtual environment (Python 3.12): `python -m venv venv` then `.\venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Start FastAPI server: `uvicorn app.main:app --reload`
5. Backend will run at http://127.0.0.1:8000

Frontend Setup:

1. Navigate to frontend folder: `cd frontend`
2. Install dependencies: `npm install`
3. Start React app: `npm start`
4. Frontend will run at http://localhost:3000

Usage:

1. Open the frontend in a browser
2. Upload a PDF resume or paste raw text
3. Click "Analyze Resume"
4. View extracted information including name, email, phone, skills, education, experience, experience level, classification, and confidence

Notes:

- Ensure the backend is running before using the frontend
- Education duplicates are removed automatically in the output
- Classification uses the trained model `resume_clf.pkl`
- Raw text input is optional; PDF upload works fully
- The system is designed to be simple for demonstration purposes
- For improved classification results, retrain the model with more resumes

ScreenShots:
<img width="1920" height="910" alt="image" src="https://github.com/user-attachments/assets/f2dee1cb-c79c-48a0-8697-2e3b8acd0bc7" />



LIVE LINK:

 https://ai-resume-analyzer-and-classifier.vercel.app/
