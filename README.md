
# 🎯 CareerLens

**AI-Powered Resume Analyzer & Skill Gap Finder**  
*Helping students and freshers become job-ready with intelligent insights.*

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)


## 📌 Overview

CareerLens is a smart, modern web application that analyzes resumes using **Google Gemini AI**. Students and freshers can upload their resume (PDF) and enter a target job role. The system intelligently extracts information, evaluates the resume, identifies skill gaps, and generates a personalized learning roadmap with free resources.

### Key Features
- **Resume Score** (out of 10)
- **ATS Compatibility Score**
- **Skill Match Percentage**
- **Strengths & Weaknesses Analysis**
- **Actionable Improvement Suggestions**
- **Personalized Learning Roadmap**
- **Clean, Modern Dashboard UI**

---

## 🚀 Features

### 📄 Smart Resume Upload
Elegant PDF upload with validation and preview support.

### 🤖 Gemini AI Analysis
Powered by **Google Gemini AI** for:
- Resume quality scoring
- ATS optimization feedback
- Personalized suggestions
- Professional tone analysis

### 🎯 Intelligent Skill Gap Finder
Compares your skills with real industry requirements for your target job role.

### 🗺️ Personalized Learning Roadmap
Generates prioritized learning paths with **free resources** (YouTube, Coursera Audit, Kaggle, freeCodeCamp, etc.).

### 📊 Premium Dashboard
Modern, responsive, and visually rich interface with smooth animations and component-based design.

---

## 🛠️ Tech Stack

| Layer          | Technology                          | Purpose |
|----------------|-------------------------------------|-------|
| Backend        | **Python + Flask**                  | Web framework, routing, logic |
| AI Engine      | **Google Gemini AI**                | Resume scoring, feedback & roadmap |
| PDF Parsing    | **pdfplumber**                      | Accurate text extraction |
| Frontend       | **HTML5 + Jinja2 Templates**        | Component-based UI |
| Styling        | **CSS3 (modular)**                  | `main.css`, `style.css`, `components.css` |
| Interactivity  | **JavaScript**                      | `ui.js`, `swarm-background.js` |
| Architecture   | Template Inheritance (`base.html`)  | Clean, maintainable frontend |

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```powershell
git clone https://github.com/yourusername/CareerLens.git
cd CareerLens
```

### 2. Create Virtual Environment
```powershell
python -m venv venv
```

### 3. Activate Virtual Environment
```powershell
venv\Scripts\activate
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 5. Add Gemini API Key
Create a `.env` file in the root and add:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

> Get your free Gemini API key from: [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### 6. Run the Application
```powershell
python app.py
```

Open your browser and go to: **`http://127.0.0.1:5000`**

---

## 📂 Project Structure

```bash
CareerLens/
├── venv/                          # Virtual environment
├── uploads/                       # Uploaded resume PDFs
├── static/
│   ├── style.css                  # Main styles
│   ├── main.css                   # Core layout
│   ├── components.css             # Reusable components
│   ├── ui.js                      # UI interactions
│   └── swarm-background.js        # Animated background effects
├── templates/
│   ├── base.html                  # Base template (inheritance)
│   ├── nav.html                   # Navigation component
│   ├── index.html                 # Landing & upload page
│   ├── result.html                # Analysis dashboard
│   ├── error.html                 # Error page
│   ├── card.html                  # Reusable card component
│   ├── button.html                # Button component
│   └── form.html                  # Form component
├── utils/
│   ├── __init__.py
│   ├── resume_parser.py           # PDF text extraction
│   ├── skill_matcher.py           # Skill comparison logic
│   └── ai_analyzer.py             # Gemini AI integration
├── app.py                         # Main Flask application
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## 📝 Notes

- Only **PDF files** are supported (max 10MB).
- Skill matching works even without an API key.
- AI features require a valid **Gemini API key**.
- The frontend uses **template inheritance** (`base.html`) for better maintainability.
- Modern animations and glassmorphism effects are implemented via `swarm-background.js` and modular CSS.

---

## 🎓 Academic Information

**Project Title:** CareerLens — AI-Powered Resume Analyzer & Skill Gap Finder  
**Program:** Bachelor of Computer Applications (BCA)  
**College:** Jagan College of Arts, Science and Commerce, Kanpur  
**Student:** Anurag Kushwaha  
**Academic Year:** 2023–2026

---

## 👨‍💻 Author

**Anurag Kushwaha**

---

## 📜 License

This project is developed for educational purposes as part of a final year BCA project.

---

**Made with ❤️ for students who want to stand out.**
---
