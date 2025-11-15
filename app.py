import streamlit as st
from openai import OpenAI
import time

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(page_title="CareerAI 💼", page_icon="💼", layout="centered")

# ------------------------------
# DARK + SOFT NEON THEME CSS
# ------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #0A0F19;
    color: #E6E6E6;
}

/* Chat bubble container */
.user-msg, .bot-msg {
    padding: 12px 18px;
    border-radius: 18px;
    margin: 8px 0;
    max-width: 75%;
    font-size: 16px;
    line-height: 1.4;
}

/* User bubble (right side, neon purple) */
.user-msg {
    background: linear-gradient(135deg, ##544d4d, ##473d3d);
    color: white;
    margin-left: auto;
    text-align: right;
}

/* Bot bubble (left side, neon pink) */
.bot-msg {
    background: linear-gradient(135deg, ##1f1b1b, ##1a1818);
    color: white;
    margin-right: auto;
}

/* Chat input styling */
div[data-testid="stChatInputContainer"] {
    background: #0A0F19;
}

</style>
""", unsafe_allow_html=True)


# ------------------------------
# OPENAI CLIENT
# ------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# ------------------------------
# HEADER
# ------------------------------
st.markdown("""
<h1 style='text-align:center; color:#C27EFF;'>💼 CareerAI</h1>
<p style='text-align:center; color:#9B9B9B;'>
Your AI assistant for resumes, interviews, job search & LinkedIn guidance.
</p>
<hr style='border: 1px solid #1F1F1F; margin: 20px 0;'>
""", unsafe_allow_html=True)


# ------------------------------
# SESSION STATE FOR CHAT
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------
# FUNCTION: CHECK IF QUESTION IS CAREER RELATED
# ------------------------------
def is_career_question(text):
    career_keywords = [
        "job", "career", "resume", "cv", "interview",
        "linkedin", "offer", "internship", "salary",
        "cover letter", "hiring", "company", "work",
        "profession", "skill", "portfolio", "Btech", "AI",
        "ML",
    # Job Search
    "job", "jobs", "hiring", "vacancy", "recruitment", "recruiter", "apply",
    "application", "job opening", "job position", "job opportunity",
    "job hunt", "job search", "career opportunity", "internship",
    "fresher jobs", "walk-in", "job posting", "remote job", "on-site job",
    "hybrid job",

    # Resume / CV
    "resume", "cv", "curriculum vitae", "portfolio", "resume builder",
    "resume format", "resume review", "resume edit", "ats", "ats-friendly resume",
    "resume keywords", "summary statement", "experience section",
    "education section", "skills section",

    # Skills
    "skills", "hard skills", "soft skills", "technical skills",
    "communication skills", "leadership", "teamwork", "problem solving",
    "time management", "creativity", "analytical skills", "programming skills",
    "coding", "data analysis", "management skills",

    # Career Guidance
    "career", "career advice", "guidance", "suggestions", "future career",
    "career path", "career options", "career growth", "career planning",
    "career change", "switching careers", "industry trends", "job market",

    # Education / Qualifications
    "degree", "diploma", "certification", "course", "higher education",
    "college", "university", "stream", "major", "specialization",
    "training", "skill development",

    # Interview
    "interview", "interview questions", "interview preparation", "hr round",
    "technical round", "mock interview", "interview tips",
    "tell me about yourself", "strengths", "weaknesses",
    "salary expectation", "interview follow-up",

    # Work Life
    "work", "workplace", "office", "professional", "management",
    "promotion", "company", "employer", "employee", "work experience",
    "onboarding", "performance review", "appraisal",

    # Salary / Compensation
    "salary", "pay", "compensation", "package", "ctc", "stipend",
    "benefits", "payroll", "increment", "hike",

    # Career Fields / Domains
    "software", "it", "engineering", "marketing", "hr", "finance",
    "accounting", "design", "business", "ai", "data science",
    "cybersecurity", "healthcare", "teaching", "management", "operations",
    "sales"
]


    text_lower = text.lower()
    return any(word in text_lower for word in career_keywords)


# ------------------------------
# DISPLAY CHAT HISTORY
# ------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{msg['content']}</div>", unsafe_allow_html=True)


# ------------------------------
# CHAT INPUT
# ------------------------------
user_input = st.chat_input("Ask CareerAI about jobs, resumes, interviews…")


# ------------------------------
# PROCESS USER MESSAGE
# ------------------------------
if user_input:

    # 1. Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='user-msg'>{user_input}</div>", unsafe_allow_html=True)

    # 2. Loading animation
    with st.spinner("CareerAI is thinking..."):
        time.sleep(0.2)

    # 3. Greeting logic
    greetings = ["hi", "hello", "hey", "hii", "heyy"]
    if user_input.lower().strip() in greetings:
        bot_reply = "Hello! 👋 How can I help you with your career today?"

    else:
        # 4. Filter non-career questions
        if not is_career_question(user_input):
            bot_reply = (
                "I can help only with *career-related questions*, such as "
                "jobs, resumes, interviews, LinkedIn and professional growth. 😊"
            )
        else:
            # 5. Generate OpenAI response
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are CareerAI, a helpful expert in resumes, interviews, job search and LinkedIn improvement. Only answer career-related questions."},
                    {"role": "user", "content": user_input}
                ]
            )
            bot_reply = response.choices[0].message.content  # FIXED

    # 6. Show bot reply
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.markdown(f"<div class='bot-msg'>{bot_reply}</div>", unsafe_allow_html=True)
