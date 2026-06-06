import streamlit as st
import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="SmartPrep AI", page_icon="🧠", layout="centered")

st.markdown("""
<style>
    .question-box {
        background: #f8f7ff;
        border-left: 4px solid #7f77dd;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 12px 0;
        font-size: 16px;
        font-weight: 500;
        color: #26215c;
    }
    .feedback-box {
        background: #f0fdf4;
        border-left: 4px solid #1d9e75;
        padding: 14px 18px;
        border-radius: 8px;
        margin: 8px 0;
        font-size: 14px;
        color: #085041;
    }
</style>
""", unsafe_allow_html=True)

def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"REAL_ERROR: {str(e)}"

def generate_questions(job_desc):
    prompt = f"""
You are an expert technical interviewer. Based on the job description below, generate exactly 10 interview questions.
Mix of: 3 technical, 3 behavioral, 2 situational, 2 role-specific.
Return ONLY a numbered list like:
1. Question here
2. Question here

Job Description:
{job_desc}
"""
    raw = ask_ai(prompt)
    if "REAL_ERROR" in raw:
        return raw
    questions = []
    for line in raw.split("\n"):
        line = line.strip()
        if line and line[0].isdigit() and ". " in line:
            questions.append(line.split(". ", 1)[1].strip())
    return questions[:10]

def evaluate_answer(question, answer, job_desc):
    prompt = f"""
You are an interview coach evaluating a candidate's answer.

Job Context: {job_desc[:300]}
Question: {question}
Candidate's Answer: {answer}

Respond in this exact format:
SCORE: [number 1-10]
STRENGTH: [one sentence on what was good]
IMPROVE: [one specific suggestion]
IDEAL: [2-3 sentence model answer]
"""
    raw = ask_ai(prompt)
    result = {"score": 5, "strength": "", "improve": "", "ideal": ""}
    for line in raw.split("\n"):
        line = line.strip()
        if line.startswith("SCORE:"):
            try:
                result["score"] = int(line.replace("SCORE:", "").strip().split("/")[0])
            except:
                result["score"] = 5
        elif line.startswith("STRENGTH:"):
            result["strength"] = line.replace("STRENGTH:", "").strip()
        elif line.startswith("IMPROVE:"):
            result["improve"] = line.replace("IMPROVE:", "").strip()
        elif line.startswith("IDEAL:"):
            result["ideal"] = line.replace("IDEAL:", "").strip()
    return result

def score_color(score):
    if score >= 8: return "#16a34a"
    elif score >= 5: return "#d97706"
    else: return "#dc2626"

for key, default in {
    "stage": "home",
    "job_desc": "",
    "questions": [],
    "current_q": 0,
    "answers": [],
    "feedbacks": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# HOME
if st.session_state.stage == "home":
    st.markdown("## 🧠 SmartPrep AI")
    st.markdown("**AI-powered mock interview coach — paste a job description and start practicing!**")
    st.markdown("---")

    job_input = st.text_area(
        "📋 Paste the Job Description here",
        height=220,
        placeholder="e.g. We are looking for a Python Developer..."
    )

    if st.button("🚀 Start Interview", use_container_width=True):
        if len(job_input.strip()) < 50:
            st.error("Please paste a proper job description (at least 50 characters).")
        else:
            with st.spinner("🤖 Generating your personalised interview questions..."):
                questions = generate_questions(job_input)

            if isinstance(questions, str) and "REAL_ERROR" in questions:
                st.error(f"❌ API Error: {questions.replace('REAL_ERROR: ', '')}")
            elif isinstance(questions, list) and len(questions) >= 5:
                st.session_state.job_desc = job_input
                st.session_state.questions = questions
                st.session_state.current_q = 0
                st.session_state.answers = []
                st.session_state.feedbacks = []
                st.session_state.stage = "interview"
                st.rerun()
            else:
                st.error("Could not generate questions. Try again.")

# INTERVIEW
elif st.session_state.stage == "interview":
    total = len(st.session_state.questions)
    current = st.session_state.current_q

    st.markdown(f"#### Question {current + 1} of {total}")
    st.progress(current / total)
    st.markdown("")

    q_text = st.session_state.questions[current]
    st.markdown(f'<div class="question-box">🎯 {q_text}</div>', unsafe_allow_html=True)

    answer = st.text_area(
        "Your answer:",
        height=160,
        placeholder="Type your answer here...",
        key=f"answer_{current}"
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        submit = st.button("Submit Answer ✅", use_container_width=True)
    with col2:
        skip = st.button("Skip ⏭", use_container_width=True)

    if submit or skip:
        final_answer = answer.strip() if (submit and answer.strip()) else "(No answer given)"
        with st.spinner("🤖 Evaluating your answer..."):
            feedback = evaluate_answer(q_text, final_answer, st.session_state.job_desc)
        st.session_state.answers.append(final_answer)
        st.session_state.feedbacks.append(feedback)

        score = feedback["score"]
        color = score_color(score)
        st.markdown(f"""
        <div class="feedback-box">
            <strong>Score: <span style="color:{color}">{score}/10</span></strong><br><br>
            💪 <strong>Strength:</strong> {feedback['strength']}<br><br>
            📈 <strong>Improve:</strong> {feedback['improve']}<br><br>
            ✨ <strong>Ideal Answer:</strong> {feedback['ideal']}
        </div>
        """, unsafe_allow_html=True)

        time.sleep(1)
        if current + 1 >= total:
            st.session_state.stage = "report"
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.current_q += 1
            st.rerun()

# REPORT
elif st.session_state.stage == "report":
    questions = st.session_state.questions
    feedbacks = st.session_state.feedbacks
    answers = st.session_state.answers
    scores = [f["score"] for f in feedbacks]
    avg = round(sum(scores) / len(scores), 1) if scores else 0

    st.markdown("## 📊 Your Interview Report")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall Score", f"{avg}/10")
    col2.metric("Answered", f"{len([a for a in answers if a != '(No answer given)'])}/{len(questions)}")
    col3.metric("Top Score", f"{max(scores)}/10" if scores else "N/A")

    if avg >= 8:
        st.success("🟢 Excellent! You're interview-ready.")
    elif avg >= 6:
        st.warning("🟡 Good! A little more practice and you're set.")
    else:
        st.error("🔴 Keep practising! Review feedback below.")

    st.markdown("---")
    st.markdown("### Detailed Breakdown")

    for i, (q, a, f) in enumerate(zip(questions, answers, feedbacks)):
        with st.expander(f"Q{i+1}: {q[:70]}... — Score: {f['score']}/10"):
            st.markdown(f"**Your answer:** {a}")
            st.markdown(f"💪 **Strength:** {f['strength']}")
            st.markdown(f"📈 **Improve:** {f['improve']}")
            st.markdown(f"✨ **Ideal Answer:** {f['ideal']}")

    report_text = f"SmartPrep AI Report\n{'='*40}\nOverall Score: {avg}/10\n\n"
    for i, (q, a, f) in enumerate(zip(questions, answers, feedbacks)):
        report_text += f"Q{i+1}: {q}\nAnswer: {a}\nScore: {f['score']}/10\nStrength: {f['strength']}\nImprove: {f['improve']}\nIdeal: {f['ideal']}\n\n"

    st.download_button(
        "📥 Download Report",
        data=report_text,
        file_name="smartprep_report.txt",
        mime="text/plain",
        use_container_width=True
    )

    if st.button("🔄 Start New Interview", use_container_width=True):
        for key in ["stage", "job_desc", "questions", "current_q", "answers", "feedbacks"]:
            st.session_state[key] = "home" if key == "stage" else [] if isinstance(st.session_state[key], list) else "" if key != "current_q" else 0
        st.rerun()