# CareerLens

AI-powered resume analyzer and skill gap finder built with Flask and Gemini.

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the app.

```powershell
python app.py
```

Open `http://127.0.0.1:5000`.

## Notes

- Uploads must be PDF files.
- Maximum upload size is 10 MB.
- AI analysis needs a valid Gemini API key.
- Skill matching still works if the API key is missing.
