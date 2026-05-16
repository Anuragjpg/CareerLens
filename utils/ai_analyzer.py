import os
import json
import time
import sys
from dotenv import load_dotenv
from utils.skill_matcher import compare_skills, extract_skills

# Load environment variables from .env file
load_dotenv()

# Attempt to import Gemini AI client
try:
    from google import genai
    from google.genai import types
    GEMINI_IMPORT_ERROR = False
except ModuleNotFoundError as e:
    genai = None
    types = None
    GEMINI_IMPORT_ERROR = True
    print(f"[WARNING] Gemini AI client not available: {e}")

# Initialize Gemini client
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[WARNING] GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key) if api_key and not GEMINI_IMPORT_ERROR else None

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
]

RETRYABLE_ERROR_MARKERS = (
    "503",
    "UNAVAILABLE",
    "RESOURCE_EXHAUSTED",
    "429",
    "high demand",
    "rate limit",
)


def is_retryable_ai_error(error):
    """Return True for temporary Gemini capacity/quota errors."""
    error_text = str(error).lower()
    return any(marker in error_text for marker in RETRYABLE_ERROR_MARKERS)


def clamp_number(value, minimum, maximum, default):
    """Convert AI numbers safely so the UI never breaks on odd responses."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return max(minimum, min(maximum, round(number)))


def normalize_list(value, fallback):
    """Keep the response shape predictable for templates."""
    if isinstance(value, list):
        cleaned = [str(item).strip() for item in value if str(item).strip()]
        return cleaned or fallback
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return fallback


def normalize_roadmap(value):
    """Normalize roadmap entries returned by the AI."""
    if not isinstance(value, list):
        return []

    roadmap = []
    for item in value[:6]:
        if not isinstance(item, dict):
            continue
        roadmap.append({
            "skill": str(item.get("skill") or "Core skill").strip(),
            "priority": str(item.get("priority") or "Medium").strip().title(),
            "resource": str(item.get("resource") or "freeCodeCamp / YouTube free course").strip(),
            "duration": str(item.get("duration") or "2 weeks").strip(),
            "why": str(item.get("why") or "Important for the target role.").strip(),
        })
    return roadmap


def build_local_analysis(resume_text, job_role, reason):
    """
    Return a useful non-AI analysis when the Gemini API is unavailable.
    This keeps the report page working instead of showing an empty AI block.
    """
    resume_skills = extract_skills(resume_text)
    skill_analysis = compare_skills(resume_skills, job_role)
    match = skill_analysis.get("match_percentage", 0)
    word_count = len(resume_text.split()) if resume_text else 0

    resume_score = 3
    if word_count >= 250:
        resume_score += 1
    if word_count >= 450:
        resume_score += 1
    if resume_skills:
        resume_score += 1
    if match >= 50:
        resume_score += 1
    if match >= 75:
        resume_score += 1

    ats_score = min(95, max(20, match + (20 if word_count >= 300 else 8)))
    missing = skill_analysis.get("missing", [])[:5]
    roadmap = []

    for index, skill in enumerate(missing):
        roadmap.append({
            "skill": skill,
            "priority": "High" if index < 2 else "Medium",
            "resource": f"Search freeCodeCamp, Kaggle, or YouTube for a free {skill} course",
            "duration": "1-2 weeks",
            "why": f"{skill} appears in the target role requirements but was not found in your resume.",
        })

    return {
        "ai_error": False,
        "fallback": True,
        "notice": f"Gemini could not be reached, so CareerLens generated a local analysis. Reason: {reason}",
        "resume_score": resume_score,
        "ats_score": ats_score,
        "summary": "Local analysis completed from resume length, detected skills, and role skill match.",
        "strengths": [
            f"Found {len(resume_skills)} skill(s) in the resume.",
            f"Matched {skill_analysis.get('matched_count', 0)} required skill(s) for {job_role}.",
            "The resume text could be parsed successfully from the PDF.",
        ],
        "weaknesses": [
            f"Missing {skill_analysis.get('missing_count', 0)} role skill(s)." if skill_analysis.get("job_found") else "Target role is not in the local skill database.",
            "AI-specific writing feedback was unavailable during this run.",
            "Add measurable achievements, links, and project impact where possible.",
        ],
        "suggestions": [
            "Add a clear summary tailored to the target role.",
            "Include measurable project outcomes such as speed, accuracy, users, or time saved.",
            "Group technical skills by category so recruiters can scan them quickly.",
            "Add GitHub, LinkedIn, and live project links if available.",
            "Use keywords from the target job description naturally in project bullets.",
        ],
        "roadmap": roadmap,
    }


def extract_json_from_text(text):
    """Attempt to extract the first JSON object from noisy AI output."""
    start = text.find('{')
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False

    for index, char in enumerate(text[start:], start=start):
        if escape:
            escape = False
            continue
        if char == '\\':
            escape = True
            continue
        if char == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return text[start:index + 1]

    return None


def analyze_resume_with_ai(resume_text, job_role):
    """
    Send resume to Gemini AI and get detailed analysis.

    Args:
        resume_text (str): Full resume text
        job_role (str): Target job role

    Returns:
        dict: AI analysis with scores, feedback, and roadmap
    """

    # Check if AI client is available and configured
    if not client:
        if GEMINI_IMPORT_ERROR:
            return build_local_analysis(
                resume_text,
                job_role,
                f"Gemini package is missing in this Python environment ({sys.executable}). Run the app with the project virtualenv."
            )

        return build_local_analysis(
            resume_text,
            job_role,
            "GEMINI_API_KEY is not configured in .env."
        )

    # Keep prompt size predictable so Gemini has enough room to finish valid JSON.
    resume_excerpt = resume_text[:12000]

    # Create the prompt
    prompt = f"""You are an expert resume reviewer and career advisor for freshers and students in India.

Analyze this resume for the job role: "{job_role}"

RESUME TEXT:
{resume_excerpt}

You MUST return ONLY valid JSON. No markdown, no extra text before or after.

Return this exact JSON structure:
{{
    "resume_score": <number from 1 to 10>,
    "ats_score": <number from 0 to 100>,
    "summary": "<one short line about resume quality>",
    "strengths": [
        "specific strength 1",
        "specific strength 2",
        "specific strength 3"
    ],
    "weaknesses": [
        "specific weakness 1",
        "specific weakness 2",
        "specific weakness 3"
    ],
    "suggestions": [
        "actionable suggestion 1",
        "actionable suggestion 2",
        "actionable suggestion 3",
        "actionable suggestion 4",
        "actionable suggestion 5"
    ],
    "roadmap": [
        {{
            "skill": "skill name",
            "priority": "High",
            "resource": "free course name and platform",
            "duration": "X weeks",
            "why": "why this matters for this role"
        }},
        {{
            "skill": "skill name",
            "priority": "Medium",
            "resource": "free course",
            "duration": "X weeks",
            "why": "reason"
        }}
    ]
}}

RULES:
1. Score honestly (most fresher resumes score 4-7)
2. ATS score checks: keywords, formatting, sections, contact info
3. Suggestions must be SPECIFIC (not "improve your resume")
4. Roadmap should have 3-6 items, ordered by priority (High first)
5. Recommend ONLY FREE resources (Coursera audit, Kaggle, YouTube, freeCodeCamp, Khan Academy)
6. Keep every string under 140 characters
7. Return ONLY JSON, no other text"""

    try:
        print("[AI] Sending resume to Gemini AI...")

        response = None
        last_error = None

        for model in GEMINI_MODELS:
            for attempt in range(2):
                try:
                    print(f"[AI] Trying {model} (attempt {attempt + 1}/2)...")
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            temperature=0.2,
                            max_output_tokens=6000,
                        ),
                    )
                    print(f"[AI] Response received from {model}")
                    last_error = None
                    break
                except Exception as e:
                    last_error = e
                    print(f"[AI WARNING] {model} failed: {str(e)}")

                    if not is_retryable_ai_error(e):
                        raise

                    time.sleep(2 + attempt)

            if response:
                break

        if not response:
            raise last_error or RuntimeError("No response from Gemini API.")

        # Get response text
        response_text = response.text or ""
        print(f"[AI] Got response: {len(response_text)} characters")

        # Clean response (remove markdown if AI added it)
        clean_text = response_text.strip()

        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:]

        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]

        clean_text = clean_text.strip()

        # Parse JSON
        try:
            result = json.loads(clean_text)
        except json.JSONDecodeError:
            fallback = extract_json_from_text(clean_text)
            if fallback:
                print("[AI] Attempting fallback JSON extraction from noisy response...")
                result = json.loads(fallback)
            else:
                raise

        result = {
            "resume_score": clamp_number(result.get("resume_score"), 1, 10, 5),
            "ats_score": clamp_number(result.get("ats_score"), 0, 100, 50),
            "summary": str(result.get("summary") or "AI analysis completed.").strip(),
            "strengths": normalize_list(result.get("strengths"), ["Resume text was parsed successfully."]),
            "weaknesses": normalize_list(result.get("weaknesses"), ["Add more role-specific detail where possible."]),
            "suggestions": normalize_list(result.get("suggestions"), ["Tailor the resume to the target role."]),
            "roadmap": normalize_roadmap(result.get("roadmap")),
            "ai_error": False,
            "fallback": False,
        }

        print("[AI] Analysis successful!")
        return result

    except json.JSONDecodeError as e:
        print(f"[AI ERROR] Invalid JSON: {e}")
        return build_local_analysis(
            resume_text,
            job_role,
            "AI returned invalid JSON. Please try again later for full AI feedback."
        )

    except Exception as e:
        print(f"[AI ERROR] {str(e)}")
        return build_local_analysis(resume_text, job_role, f"AI service error: {str(e)}")
