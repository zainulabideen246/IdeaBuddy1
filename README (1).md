# IdeaBuddy — AI Idea Simplifier

IdeaBuddy is a beginner-friendly Streamlit app. A user describes a goal, problem, or interest, and Gemini suggests one practical idea with simple steps.

## Features
- Generates one focused idea from user input
- Considers time, budget, interests, and skill level
- Beginner-friendly steps, tools, a first action, and a progress check
- Downloadable JSON plan
- Gemini API key stored in Streamlit Secrets

## Run locally
1. Install Python 3.10+.
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml` with:
   ```toml
   GEMINI_API_KEY = "paste-your-api-key-here"
   ```
4. Run `streamlit run app.py`.

Never commit or share your API key.

## GitHub website upload (no Git commands)
1. Create a repository at https://github.com.
2. Use **Add file → Create new file** to add `app.py`, paste its contents, and commit.
3. Repeat for `README.md` and `requirements.txt`.
4. Do not upload secrets.

## Deploy on Streamlit Community Cloud
1. Visit https://share.streamlit.io/ and sign in with GitHub.
2. Create an app from your repository; set main file to `app.py`.
3. In app settings / Secrets, add:
   ```toml
   GEMINI_API_KEY = "paste-your-api-key-here"
   ```
4. Deploy. Streamlit Cloud installs requirements from `requirements.txt`.

## Notes
- Sidebar model defaults to `gemini-3.8-flash`; use a model available to your API key.
- AI suggestions may be imperfect; verify details.
- Python syntax was checked. A live Gemini call requires your key, model access, and quota.
