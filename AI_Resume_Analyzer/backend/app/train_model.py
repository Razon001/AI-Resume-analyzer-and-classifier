import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# -------------------------------
# Sample training resumes
# -------------------------------

train_texts = [
    # AI/ML Engineer
    "Python TensorFlow PyTorch Machine Learning Deep Learning AI",
    "Worked on ML models using Scikit-Learn, Pandas, NumPy, Neural Networks",
    "AI Engineer with experience in NLP, Computer Vision, TensorFlow, Keras",
    "Deep Learning models, data preprocessing, model deployment with Flask",
    "ML Engineer, Python, PyTorch, supervised and unsupervised learning",

    # Web Developer
    "Frontend development with HTML, CSS, JavaScript, React",
    "Created responsive websites using React, Bootstrap, and Tailwind CSS",
    "Web developer, frontend design, JavaScript, UI/UX optimization",
    "Developed dynamic web pages using HTML5, CSS3, JavaScript",
    "React.js, JavaScript, HTML, CSS, website development, frontend engineer",

    # FullStack Developer
    "FullStack Developer with Node.js, Django, React, REST APIs, MongoDB",
    "Worked on backend and frontend, Node.js, Express, React, MySQL",
    "Developed full stack applications, React frontend, Python backend",
    "JavaScript, React, Django, REST API, SQL, full stack engineer",
    "Experienced in full stack development using MERN stack and Django",

    # DevOps/Cloud Engineer
    "AWS, Docker, Kubernetes, Cloud Infrastructure, CI/CD pipelines",
    "DevOps Engineer with experience in Jenkins, Docker, AWS, Terraform",
    "Cloud engineer, AWS cloud, Docker containers, Kubernetes orchestration",
    "Set up CI/CD pipelines, cloud deployment using AWS and Azure",
    "Managed cloud infrastructure with Docker, Kubernetes, Terraform",

    # Software Engineer
    "Software engineer experienced in C++, Java, backend algorithms",
    "Developed software modules in Java, C++, object-oriented programming",
    "Backend software development, data structures, algorithms, Java",
    "Implemented desktop applications using C++ and Python",
    "Experienced in software engineering, testing, and development",

    # Data Scientist
    "Data analysis using Python, Pandas, NumPy, Matplotlib, Seaborn",
    "Data Scientist, machine learning models, feature engineering, Python",
    "Analyzed large datasets, created predictive models using Python",
    "Worked on data cleaning, visualization, and statistical modeling",
    "Python, data analytics, SQL, machine learning, predictive modeling"
]

train_labels = [
    # Corresponding labels
    "AI/ML Engineer", "AI/ML Engineer", "AI/ML Engineer", "AI/ML Engineer", "AI/ML Engineer",
    "Web Developer", "Web Developer", "Web Developer", "Web Developer", "Web Developer",
    "FullStack Developer", "FullStack Developer", "FullStack Developer", "FullStack Developer", "FullStack Developer",
    "DevOps/Cloud Engineer", "DevOps/Cloud Engineer", "DevOps/Cloud Engineer", "DevOps/Cloud Engineer", "DevOps/Cloud Engineer",
    "Software Engineer", "Software Engineer", "Software Engineer", "Software Engineer", "Software Engineer",
    "Data Scientist", "Data Scientist", "Data Scientist", "Data Scientist", "Data Scientist"
]

# -------------------------------
# Train TF-IDF vectorizer
# -------------------------------
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(train_texts)

# -------------------------------
# Train Logistic Regression Classifier
# -------------------------------
clf = LogisticRegression(max_iter=1000)
clf.fit(X, train_labels)

# -------------------------------
# Save model & vectorizer
# -------------------------------
joblib.dump(clf, "resume_clf.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Training complete! Files saved as 'resume_clf.pkl' and 'tfidf_vectorizer.pkl'.")
