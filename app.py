"""
CareerLens - AI Powered Resume Analyzer & Skill Gap Finder
Main Flask Application

Author: Anurag Kushwaha
College: Jagan College of Arts, Science and Commerce, Kanpur
"""

from datetime import datetime
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

# Import our custom modules
from utils.resume_parser import extract_text_from_pdf, get_word_count
from utils.skill_matcher import extract_skills, compare_skills
from utils.ai_analyzer import analyze_resume_with_ai

# Create Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max file size

@app.context_processor
def inject_year():
    return {'year': datetime.now().year}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ==================================================
# ROUTES
# ==================================================

@app.route('/')
def home():
    """Homepage - shows upload form"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded resume and show results"""

    # Get uploaded file and job role
    file = request.files.get('resume')
    job_role = request.form.get('job_role', '').strip()

    # ============================
    # VALIDATIONS
    # ============================
    if not file:
        return render_template('error.html',
                               error="No file uploaded. Please go back and try again.")

    filename = secure_filename(file.filename or "")

    if not filename.lower().endswith('.pdf'):
        return render_template('error.html',
                               error="Only PDF files are allowed. Please upload a PDF resume.")

    if not job_role:
        return render_template('error.html',
                               error="Please enter a job role you are targeting.")

    # ============================
    # SAVE FILE
    # ============================
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    print("\n" + "="*60)
    print(f"[NEW REQUEST] File: {filename} | Job: {job_role}")
    print("="*60)

    # ============================
    # STEP 1: Extract text from PDF
    # ============================
    print("\n[STEP 1/4] Extracting text from PDF...")
    resume_text = extract_text_from_pdf(filepath)

    if resume_text.startswith("ERROR"):
        return render_template('error.html',
                               error=f"Could not read your PDF: {resume_text}")

    word_count = get_word_count(resume_text)

    # ============================
    # STEP 2: Find skills in resume
    # ============================
    print("\n[STEP 2/4] Finding skills in resume...")
    resume_skills = extract_skills(resume_text)

    # ============================
    # STEP 3: Compare with job requirements
    # ============================
    print("\n[STEP 3/4] Comparing skills with job requirements...")
    skill_analysis = compare_skills(resume_skills, job_role)

    # ============================
    # STEP 4: AI Analysis
    # ============================
    print("\n[STEP 4/4] Running AI analysis...")
    ai_result = analyze_resume_with_ai(resume_text, job_role)

    print("\n[COMPLETE] Analysis finished successfully!")
    print("="*60 + "\n")

    # Render results page
    return render_template('result.html',
                           filename=filename,
                           job_role=job_role,
                           resume_text=resume_text,
                           word_count=word_count,
                           resume_skills=resume_skills,
                           analysis=skill_analysis,
                           ai=ai_result)


@app.errorhandler(413)
def too_large(e):
    return render_template('error.html',
                           error="File is too large. Maximum size is 10 MB.")


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html',
                           error="Page not found.")


# ==================================================
# RUN APP
# ==================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("CareerLens - AI Resume Analyzer")
    print("="*60)
    print("Server starting...")
    print("Open: http://127.0.0.1:5000")
    print("Stop: Press Control + C")
    print("="*60 + "\n")

    app.run(debug=True, port=5000)
