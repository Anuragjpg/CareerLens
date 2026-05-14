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

| Technology | Purpose |
|------------|---------|
| Python | Backend logic |
| Flask | Web framework |
| HTML/CSS | Frontend |
| pdfplumber | PDF text extraction |
| Claude AI API | AI analysis |
| JavaScript | Frontend interactions |

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