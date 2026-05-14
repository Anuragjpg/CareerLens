"""
Skill Matcher Module
Extracts skills from resume and compares with job requirements.
"""

# ==================================================
# JOB SKILLS DATABASE
# Skills required for each job role
# ==================================================

JOB_SKILLS = {
    "data analyst": [
        "python", "sql", "excel", "power bi", "tableau",
        "statistics", "pandas", "numpy", "data cleaning",
        "data visualization", "matplotlib"
    ],
    "web developer": [
        "html", "css", "javascript", "react", "node.js",
        "git", "responsive design", "bootstrap", "api",
        "mongodb", "express"
    ],
    "frontend developer": [
        "html", "css", "javascript", "react", "vue",
        "tailwind", "git", "responsive design", "typescript",
        "bootstrap"
    ],
    "backend developer": [
        "python", "node.js", "java", "sql", "mongodb",
        "api", "django", "flask", "express", "git"
    ],
    "full stack developer": [
        "html", "css", "javascript", "react", "node.js",
        "sql", "mongodb", "git", "api", "python"
    ],
    "data scientist": [
        "python", "machine learning", "statistics", "pandas",
        "numpy", "scikit-learn", "tensorflow", "sql",
        "deep learning", "data visualization"
    ],
    "python developer": [
        "python", "django", "flask", "sql", "api",
        "git", "oop", "data structures", "html", "css"
    ],
    "android developer": [
        "java", "kotlin", "android studio", "xml",
        "firebase", "git", "api", "sqlite", "material design"
    ],
    "devops engineer": [
        "linux", "docker", "kubernetes", "aws", "git",
        "jenkins", "terraform", "bash", "python", "ci/cd"
    ],
    "software engineer": [
        "python", "java", "data structures", "algorithms",
        "sql", "git", "api", "oop", "system design", "linux"
    ],
    "machine learning engineer": [
        "python", "machine learning", "deep learning", "tensorflow",
        "pytorch", "scikit-learn", "pandas", "numpy", "statistics",
        "sql"
    ],
}


# ==================================================
# ALL SKILLS DATABASE
# Used to find skills in resume text
# ==================================================

ALL_SKILLS = [
    # Programming Languages
    "python", "java", "c++", "c", "c#", "javascript", "typescript",
    "kotlin", "swift", "go", "rust", "php", "ruby", "r", "matlab",

    # Web Frontend
    "html", "css", "react", "vue", "angular", "svelte", "next.js",
    "bootstrap", "tailwind", "sass", "material design",

    # Web Backend
    "node.js", "express", "django", "flask", "fastapi", "spring boot",
    "laravel", "asp.net",

    # Databases
    "sql", "mysql", "mongodb", "postgresql", "sqlite", "firebase",
    "redis", "oracle",

    # DevOps & Cloud
    "git", "github", "gitlab", "docker", "kubernetes", "aws", "azure",
    "gcp", "linux", "bash", "powershell", "jenkins", "terraform",
    "ansible", "ci/cd",

    # Data Tools
    "excel", "power bi", "tableau", "looker", "google sheets",

    # Data Science
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "keras",
    "statistics", "probability", "data cleaning", "data visualization",

    # General
    "api", "rest api", "graphql", "responsive design",
    "oop", "data structures", "algorithms", "system design",
    "agile", "scrum",

    # Mobile
    "android studio", "xcode", "react native", "flutter",

    # Other
    "xml", "json", "yaml", "sas", "spss",

    # Soft Skills
    "communication", "teamwork", "leadership", "problem solving"
]


# ==================================================
# FUNCTIONS
# ==================================================

def extract_skills(resume_text):
    """
    Find all skills mentioned in resume text.

    Args:
        resume_text (str): Full resume text

    Returns:
        list: Sorted list of unique skills found
    """
    if not resume_text:
        return []

    resume_lower = resume_text.lower()
    found_skills = []

    for skill in ALL_SKILLS:
        if skill in resume_lower:
            found_skills.append(skill.title())

    # Remove duplicates and sort
    found_skills = sorted(list(set(found_skills)))

    print(f"[SKILLS] Found {len(found_skills)} skills in resume")
    return found_skills


def get_required_skills(job_role):
    """
    Get list of required skills for a job role.

    Args:
        job_role (str): Job title (e.g., "Data Analyst")

    Returns:
        list: Required skills, or empty list if job not found
    """
    job_lower = job_role.lower().strip()

    # Exact match
    if job_lower in JOB_SKILLS:
        return JOB_SKILLS[job_lower]

    # Partial match
    for role, skills in JOB_SKILLS.items():
        if job_lower in role or role in job_lower:
            return skills

    return []


def compare_skills(resume_skills, job_role):
    """
    Compare resume skills with job requirements.

    Args:
        resume_skills (list): Skills found in resume
        job_role (str): Target job role

    Returns:
        dict: Analysis with matched, missing, and percentage
    """
    required = get_required_skills(job_role)

    if not required:
        return {
            "job_found": False,
            "matched": [],
            "missing": [],
            "match_percentage": 0,
            "matched_count": 0,
            "missing_count": 0,
            "total_required": 0,
            "message": f"Job role '{job_role}' not in our database. Try: Data Analyst, Web Developer, Python Developer, Frontend Developer, Backend Developer, Data Scientist, Full Stack Developer, Android Developer, DevOps Engineer, Software Engineer, or Machine Learning Engineer."
        }

    # Convert to lowercase for comparison
    resume_lower = [s.lower() for s in resume_skills]

    matched = [s.title() for s in required if s.lower() in resume_lower]
    missing = [s.title() for s in required if s.lower() not in resume_lower]

    total = len(required)
    match_count = len(matched)
    match_percentage = round((match_count / total) * 100) if total > 0 else 0

    print(f"[MATCH] {match_count}/{total} skills matched ({match_percentage}%)")

    return {
        "job_found": True,
        "matched": matched,
        "missing": missing,
        "match_percentage": match_percentage,
        "matched_count": match_count,
        "missing_count": len(missing),
        "total_required": total,
        "message": ""
    }