import json
import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="IdeaBuddy | AI Idea Simplifier", page_icon="💡", layout="wide")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #f8f7ff 0%, #eef2ff 55%, #f8fbff 100%); }
[data-testid="stSidebar"] { background: #111827; }
[data-testid="stSidebar"] * { color: #f3f4f6 !important; }
.hero { padding: 2rem 2.2rem; border-radius: 24px; color: white;
background: linear-gradient(120deg, #7c3aed, #4f46e5 60%, #0ea5e9); box-shadow: 0 12px 32px rgba(79,70,229,.18); }
.hero h1 { color: white; font-size: 2.35rem; margin: 0; }
.hero p { color: #f0eaff; margin: .65rem 0 0; font-size: 1.05rem; }
div[data-testid="stMetric"] { background: white; border: 1px solid #e6eaf2; padding: 1rem; border-radius: 16px; }
div[data-testid="stExpander"] { border-radius: 14px; border: 1px solid #e5eaf3; background: white; }
</style>
""", unsafe_allow_html=True)

def get_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.getenv("GEMINI_API_KEY", "")

def make_prompt(user_input, interests, available_time, budget, skill_level, language):
    return f"""
You are IdeaBuddy, a friendly idea coach. Suggest ONE simple, practical, original-feeling idea based on the user's input.
Do not claim it is globally unique. Make it easy for a beginner.
User problem or goal: {user_input}
Interests: {interests or "Not specified"}
Available time: {available_time}
Budget: {budget}
Skill level: {skill_level}
Language: {language}

Return ONLY valid JSON:
{{
 "idea_name":"short name",
 "tagline":"one sentence",
 "problem":"problem addressed",
 "solution":"plain-language idea description",
 "difficulty":"Beginner|Easy Intermediate",
 "estimated_time":"realistic estimate",
 "budget_note":"budget-aware explanation",
 "tools":[{{"name":"tool","purpose":"why needed","cost":"free or estimated cost"}}],
 "steps":[{{"step":1,"title":"action title","description":"clear action"}}],
 "first_action":"tiny thing to do today",
 "success_check":"how to check if working",
 "possible_upgrade":"optional improvement"
}}
Use 4-7 actionable steps, prefer low-cost resources, don't promise income or success, and avoid unsafe, illegal, age-restricted, or deceptive activities.
"""

def parse_json(text):
    text=text.strip()
    if text.startswith("```"):
        text=text.split("\n",1)[-1]
        if text.endswith("```"): text=text[:-3]
    return json.loads(text.strip())

def generate_idea(prompt, api_key, model):
    client=genai.Client(api_key=api_key)
    response=client.models.generate_content(
        model=model, contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.7),
    )
    if not response.text: raise ValueError("Gemini returned an empty response.")
    return parse_json(response.text)

st.markdown("""
<div class="hero">
<h1>💡 IdeaBuddy</h1>
<p>Turn a problem, interest, or goal into one simple idea you can actually start.</p>
</div>
""", unsafe_allow_html=True)
st.write("Share what you're thinking about. IdeaBuddy will give you one practical idea and a clear starter plan.")
st.caption("AI suggestions are for brainstorming. Check details and adapt the idea to your situation.")

with st.sidebar:
    st.markdown("## Your idea inputs")
    user_input=st.text_area("What do you want help with?", placeholder="Example: I want a simple project idea that helps students organize homework.", height=125)
    interests=st.text_input("Your interests (optional)", placeholder="Example: AI, design, study, cars")
    available_time=st.selectbox("Time you can spend", ["A few hours","1–2 days","A week","A few weeks"])
    budget=st.selectbox("Budget", ["Free / no budget","Very low budget","Some budget"])
    skill_level=st.selectbox("Your skill level", ["Beginner","Intermediate","Advanced"])
    language=st.selectbox("Response language", ["Simple English","English"])
    model=st.text_input("Gemini model", value="gemini-3.8-flash", help="Choose a model available to your Gemini API key.")
    create_button=st.button("✨ Generate my idea", type="primary", use_container_width=True)

st.markdown("### Simple. Practical. Beginner-friendly.")
c1,c2,c3=st.columns(3)
with c1:
    st.markdown("**💭 One focused idea**"); st.caption("No overwhelming list of concepts.")
with c2:
    st.markdown("**🪜 Clear starter steps**"); st.caption("Understand what to do first.")
with c3:
    st.markdown("**🧰 Simple resources**"); st.caption("Tools matched to your budget and skills.")

if create_button:
    if not user_input.strip():
        st.warning("Please describe a problem, interest, or goal first.")
    elif not get_api_key():
        st.error("Gemini API key not found. Add GEMINI_API_KEY to Streamlit Secrets or your local environment.")
    else:
        prompt=make_prompt(user_input.strip(), interests.strip(), available_time, budget, skill_level, language)
        with st.spinner("IdeaBuddy is thinking of a practical idea…"):
            try:
                result=generate_idea(prompt, get_api_key(), model.strip())
                st.session_state["ideabuddy_result"]=result
                st.session_state["ideabuddy_input"]=user_input.strip()
            except json.JSONDecodeError:
                st.error("The AI response was not valid JSON. Please try again.")
            except Exception as exc:
                st.error(f"Could not generate your idea: {exc}")
                st.caption("Check your API key, model availability, internet connection, and API quota.")

if "ideabuddy_result" in st.session_state:
    result=st.session_state["ideabuddy_result"]
    st.divider()
    st.markdown(f"## 💡 {result.get('idea_name','Your idea')}")
    st.markdown(f"*{result.get('tagline','')}*")
    st.write(result.get("solution",""))
    metrics=st.columns(3)
    metrics[0].metric("Difficulty", result.get("difficulty","—"))
    metrics[1].metric("Estimated time", result.get("estimated_time","—"))
    metrics[2].metric("Budget", result.get("budget_note","—"))
    with st.expander("🎯 What problem does it solve?", expanded=True):
        st.write(result.get("problem",""))
    tools_list=result.get("tools",[])
    if tools_list:
        st.markdown("### 🧰 Tools / resources")
        for tool in tools_list:
            st.markdown(f"- **{tool.get('name','Tool')}** — {tool.get('purpose','')} *(Cost: {tool.get('cost','Not specified')})*")
    steps=result.get("steps",[])
    if steps:
        st.markdown("### 🪜 Your starter plan")
        for item in steps:
            st.markdown(f"**Step {item.get('step','?')}: {item.get('title','Action')}**")
            st.write(item.get("description",""))
    if result.get("first_action"): st.success(f"**Start today:** {result['first_action']}")
    if result.get("success_check"): st.info(f"**How to check progress:** {result['success_check']}")
    if result.get("possible_upgrade"):
        st.markdown("### 🚀 Optional future upgrade"); st.write(result["possible_upgrade"])
    st.download_button("⬇️ Download idea plan (JSON)", data=json.dumps(result,ensure_ascii=False,indent=2), file_name="my_ideabuddy_plan.json", mime="application/json")
else:
    st.info("Your idea and action plan will appear here after you generate it.")
