import os
import json
import time
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini client
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("[WARNING] GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key) if api_key else None

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
    error_text = str(error)
    return any(marker in error_text for marker in RETRYABLE_ERROR_MARKERS)


def analyze_resume_with_ai(resume_text, job_role):
    """
    Send resume to Gemini AI and get detailed analysis.

    Args:
        resume_text (str): Full resume text
        job_role (str): Target job role

    Returns:
        dict: AI analysis with scores, feedback, and roadmap
    """

    # Check if API client is initialized
    if not client:
        return {
            "ai_error": True,
            "error_message": "API key not configured. Please add GEMINI_API_KEY to .env file."
        }

    # Create the prompt
    prompt = f"""You are an expert resume reviewer and career advisor for freshers and students in India.

Analyze this resume for the job role: "{job_role}"

RESUME TEXT:
{resume_text}

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
6. Return ONLY JSON, no other text"""

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
                            max_output_tokens=2500,
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
        result = json.loads(clean_text)
        result["ai_error"] = False

        print("[AI] Analysis successful!")
        return result

    except json.JSONDecodeError as e:
        print(f"[AI ERROR] Invalid JSON: {e}")
        return {
            "ai_error": True,
            "error_message": "AI returned invalid format. Please try again.",
            "raw_response": response_text[:500] if 'response_text' in locals() else "No response"
        }

    except Exception as e:
        print(f"[AI ERROR] {str(e)}")
        return {
            "ai_error": True,
            "error_message": f"AI service error: {str(e)}"
        }
