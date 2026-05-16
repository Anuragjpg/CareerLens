# 🎯 CareerLens

AI-Powered Resume Analyzer & Skill Gap Finder for Students & Freshers

## 📌 Overview

CareerLens is a smart web application that helps students analyze their resumes, identify missing skills, and become job-ready faster using AI.

Users can upload a PDF resume and enter their target job role (e.g., Data Analyst, Web Developer). The system then analyzes the resume and provides:

- ✅ Resume Score
- ✅ ATS Compatibility Score
- ✅ Skill Match Percentage
- ✅ Missing Skills Analysis
- ✅ Personalized Suggestions
- ✅ Learning Roadmap with Free Resources

---

## 🚀 Features

### 📄 Resume Upload
Upload resume in PDF format.

### 🤖 AI Resume Analysis
Uses Claude AI to analyze:
- Resume quality
- ATS friendliness
- Strengths & weaknesses
- Improvement suggestions

### 🎯 Skill Gap Finder
Compares resume skills with industry-required skills for target job roles.

### 🗺️ Learning Roadmap
Provides free learning resources and skill priorities.

### 📊 Clean Dashboard
Displays all results in a modern UI.

---

## 🛠️ Tech Stack

- 🐍 **Python** — Core backend, data processing, and app logic
- 🌐 **Flask** — Lightweight web server, routing, and templating
- 🎨 **HTML / CSS** — Clean responsive UI and styling
- 📄 **pdfplumber** — Reliable PDF resume parsing and text extraction
- 🤖 **Gemini AI** — AI-driven resume scoring, suggestions, and insights
- 💻 **JavaScript** — Interactive frontend updates and smooth UX

---

## 🚀 Installation

1. Create and activate a virtual environment.

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Gemini API key.

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the app.

```powershell
python app.py
```

5. Open the app in your browser.

```text
http://127.0.0.1:5000
```

### Notes

- Uploads must be PDF files.
- Maximum upload size is 10 MB.
- AI analysis needs a valid Gemini API key.
- Skill matching still works if the API key is missing.

---

## 📂 Project Structure

```bash
CareerLens/
├── uploads/
├── templates/
│   ├── index.html
│   ├── result.html
│   └── error.html
├── static/
│   └── style.css
├── utils/
│   ├── resume_parser.py
│   ├── skill_matcher.py
│   └── ai_analyzer.py
├── app.py
├── requirements.txt
└── .env

