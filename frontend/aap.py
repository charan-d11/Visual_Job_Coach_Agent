"""
app.py (Streamlit Frontend)
---------------------------
Voice-first career assistant UI for the Visual Job Coach Agent.
Talks directly to the FastAPI backend at http://localhost:8000.
"""

import io
import base64
import requests
import streamlit as st

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Visual Job Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000"

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    color: #e0e0f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Cards */
.vjc-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
    transition: transform 0.2s, box-shadow 0.2s;
}
.vjc-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(99,102,241,0.2);
}

/* Job cards */
.job-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1));
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}
.job-title { font-size: 1.1rem; font-weight: 600; color: #a5b4fc; }
.job-company { font-size: 0.9rem; color: #c4b5fd; margin: 0.2rem 0; }
.job-detail { font-size: 0.85rem; color: #9ca3af; }
.badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-right: 6px;
}
.badge-remote { background: rgba(16,185,129,0.2); color: #6ee7b7; border: 1px solid #10b981; }
.badge-fulltime { background: rgba(99,102,241,0.2); color: #a5b4fc; border: 1px solid #6366f1; }
.badge-access { background: rgba(245,158,11,0.2); color: #fcd34d; border: 1px solid #f59e0b; }

/* Chat bubbles */
.chat-user {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 18px 18px 4px 18px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 0 0.5rem 20%;
    color: white;
    font-size: 0.95rem;
}
.chat-bot {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px 18px 18px 4px;
    padding: 0.8rem 1.2rem;
    margin: 0.5rem 20% 0.5rem 0;
    color: #e0e0f0;
    font-size: 0.95rem;
}
.chat-agent-label {
    font-size: 0.7rem;
    color: #6366f1;
    font-weight: 600;
    margin-bottom: 2px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
}

/* Headings */
h1, h2, h3 { color: #e0e0f0 !important; }
h1 { font-size: 2rem !important; font-weight: 700 !important; }

/* Inputs */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #e0e0f0 !important;
    border-radius: 10px !important;
}

/* Metric */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem;
}

/* Status dot */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}
.dot-green { background: #10b981; box-shadow: 0 0 6px #10b981; }
.dot-red { background: #ef4444; }

/* Audio player */
audio { width: 100%; margin-top: 0.5rem; }

/* Tips box */
.tip-box {
    background: rgba(16,185,129,0.1);
    border-left: 3px solid #10b981;
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.9rem;
    color: #6ee7b7;
}

/* Strength/improvement boxes */
.strength-box {
    background: rgba(99,102,241,0.1);
    border-left: 3px solid #6366f1;
    border-radius: 0 8px 8px 0;
    padding: 0.5rem 0.8rem;
    margin: 0.3rem 0;
    font-size: 0.88rem;
    color: #a5b4fc;
}
.improve-box {
    background: rgba(245,158,11,0.1);
    border-left: 3px solid #f59e0b;
    border-radius: 0 8px 8px 0;
    padding: 0.5rem 0.8rem;
    margin: 0.3rem 0;
    font-size: 0.88rem;
    color: #fcd34d;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "tts_audio" not in st.session_state:
    st.session_state.tts_audio = None
if "job_results" not in st.session_state:
    st.session_state.job_results = None
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None


# ── Helpers ───────────────────────────────────────────────────────────────────
def check_api_health() -> bool:
    try:
        r = requests.get(f"{API_BASE}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def send_chat(message: str) -> dict | None:
    try:
        payload = {"message": message, "session_id": st.session_state.session_id}
        r = requests.post(f"{API_BASE}/api/chat", json=payload, timeout=30)
        if r.status_code == 200:
            data = r.json()
            st.session_state.session_id = data.get("session_id")
            return data
        return {"reply": f"Error {r.status_code}: {r.text[:200]}", "agent_used": None}
    except requests.exceptions.ConnectionError:
        return {"reply": "❌ Cannot connect to the backend. Is the server running? (`python run.py`)", "agent_used": None}
    except Exception as e:
        return {"reply": f"Request failed: {e}", "agent_used": None}


def search_jobs_api(role: str, location: str, remote_only: bool) -> dict | None:
    try:
        payload = {"role": role, "location": location, "remote_only": remote_only, "limit": 6}
        r = requests.post(f"{API_BASE}/api/jobs/search", json=payload, timeout=15)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def get_questions_api(role: str) -> dict | None:
    try:
        r = requests.get(f"{API_BASE}/api/interview/questions/{role}", timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def get_feedback_api(role: str, question: str, answer: str) -> dict | None:
    try:
        payload = {"role": role, "question": question, "answer": answer}
        r = requests.post(f"{API_BASE}/api/interview/feedback", json=payload, timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def format_resume_api(section: str, content: str) -> dict | None:
    try:
        payload = {"section_name": section, "content": content}
        r = requests.post(f"{API_BASE}/api/resume/format", json=payload, timeout=10)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def get_tts_audio(text: str) -> bytes | None:
    try:
        payload = {"text": text, "lang": "en", "slow": False}
        r = requests.post(f"{API_BASE}/api/voice/speak", json=payload, timeout=15)
        return r.content if r.status_code == 200 else None
    except Exception:
        return None


def audio_player_html(audio_bytes: bytes) -> str:
    b64 = base64.b64encode(audio_bytes).decode()
    return f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎯 Visual Job Coach")
    st.markdown("*Voice-first career assistant for visually impaired job seekers*")
    st.divider()

    api_ok = check_api_health()
    status_color = "dot-green" if api_ok else "dot-red"
    status_text = "API Online" if api_ok else "API Offline — run `python run.py`"
    st.markdown(
        f'<span class="status-dot {status_color}"></span> **{status_text}**',
        unsafe_allow_html=True,
    )
    st.divider()

    page = st.radio(
        "Navigate",
        ["💬 Chat Assistant", "🔍 Job Search", "📝 Resume Builder", "🎤 Interview Prep", "🔊 Voice Tools"],
        label_visibility="collapsed",
    )
    st.divider()

    if st.session_state.session_id:
        st.caption(f"Session: `{st.session_state.session_id[:8]}…`")
        if st.button("🗑 Clear Session"):
            st.session_state.chat_history = []
            st.session_state.session_id = None
            st.rerun()

    st.divider()
    st.markdown("**Quick Commands (in chat):**")
    st.caption("• *Find me a remote data entry job*")
    st.caption("• *Help me write my resume summary*")
    st.caption("• *Practice interview questions for customer service*")
    st.caption("• *Create a 7-day job hunt plan*")


# ── Pages ─────────────────────────────────────────────────────────────────────

# ── 1. Chat Assistant ─────────────────────────────────────────────────────────
if page == "💬 Chat Assistant":
    st.markdown("# 💬 Chat with Your Job Coach")
    st.markdown("Ask anything about jobs, resume, interviews, or career planning.")

    # Chat history display
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            agent_label = msg.get("agent", "")
            label_html = f'<div class="chat-agent-label">🤖 {agent_label}</div>' if agent_label else ""
            st.markdown(
                f'{label_html}<div class="chat-bot">{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
            # TTS button for last bot message
            if msg == st.session_state.chat_history[-1]:
                if st.button("🔊 Listen to response", key="tts_last"):
                    audio = get_tts_audio(msg["content"])
                    if audio:
                        st.markdown(audio_player_html(audio), unsafe_allow_html=True)
                    else:
                        st.warning("TTS unavailable. Start the backend with `python run.py`.")

    st.divider()

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Your message",
                placeholder="e.g. Find me a remote data entry job in New York",
                label_visibility="collapsed",
            )
        with col2:
            submitted = st.form_submit_button("Send →", use_container_width=True)

    if submitted and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Your coach is thinking…"):
            response = send_chat(user_input)
        if response:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response.get("reply", "No response"),
                "agent": response.get("agent_used", ""),
            })
        st.rerun()

    if not st.session_state.chat_history:
        st.markdown("""
        <div class="vjc-card">
        <h3>👋 Welcome to Visual Job Coach!</h3>
        <p>I'm your AI-powered career assistant, designed to be fully accessible and voice-friendly. Here's what I can help with:</p>
        <ul>
        <li>🔍 <strong>Job Search</strong> — find openings that suit you</li>
        <li>📝 <strong>Resume Building</strong> — craft a professional resume section by section</li>
        <li>🎤 <strong>Interview Prep</strong> — practice questions and get feedback</li>
        <li>🗓 <strong>Career Planning</strong> — build a step-by-step job hunt plan</li>
        </ul>
        <p>Just type a message below to get started!</p>
        </div>
        """, unsafe_allow_html=True)


# ── 2. Job Search ─────────────────────────────────────────────────────────────
elif page == "🔍 Job Search":
    st.markdown("# 🔍 Job Search")
    st.markdown("Search for accessible job opportunities tailored to your needs.")

    with st.form("job_search_form"):
        col1, col2 = st.columns(2)
        with col1:
            role = st.text_input("Job Role / Title", placeholder="e.g. Data Entry Specialist", value="data entry")
        with col2:
            location = st.text_input("Location", placeholder="e.g. New York or remote", value="remote")
        remote_only = st.checkbox("Remote only", value=True)
        search_btn = st.form_submit_button("🔍 Search Jobs", use_container_width=True)

    if search_btn and role.strip():
        with st.spinner(f"Searching for {role} jobs…"):
            results = search_jobs_api(role, location, remote_only)
            st.session_state.job_results = results

    if st.session_state.job_results:
        results = st.session_state.job_results
        jobs = results.get("jobs", [])
        source = results.get("source", "mock")

        st.markdown(f"### Found **{len(jobs)}** jobs")
        if source == "mock":
            st.caption("📌 Showing example jobs. Add a RapidAPI JSearch key for real results.")

        for job in jobs:
            remote_badge = '<span class="badge badge-remote">🌐 Remote</span>' if job.get("remote") else ""
            access_badge = (
                f'<span class="badge badge-access">♿ {job.get("accessibility_note", "")[:40]}</span>'
                if job.get("accessibility_note") else ""
            )
            salary = f'💰 {job["salary"]}' if job.get("salary") else ""
            url = job.get("url", "#")

            st.markdown(f"""
            <div class="job-card">
                <div class="job-title">{job['title']}</div>
                <div class="job-company">🏢 {job['company']}</div>
                <div class="job-detail">📍 {job['location']} &nbsp; {salary}</div>
                <div style="margin-top:8px">{remote_badge} {access_badge}</div>
                <div style="margin-top:10px; font-size:0.85rem; color:#9ca3af;">
                    {job.get('description', '')[:200]}…
                </div>
                <div style="margin-top:10px">
                    <a href="{url}" target="_blank" style="color:#a5b4fc; font-size:0.85rem;">
                        🔗 Apply Now
                    </a>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # TTS read-aloud
        if st.button("🔊 Read job titles aloud"):
            titles = ", ".join(f"{j['title']} at {j['company']}" for j in jobs)
            summary = f"I found {len(jobs)} jobs for {role}. {titles}."
            audio = get_tts_audio(summary)
            if audio:
                st.markdown(audio_player_html(audio), unsafe_allow_html=True)


# ── 3. Resume Builder ─────────────────────────────────────────────────────────
elif page == "📝 Resume Builder":
    st.markdown("# 📝 Resume Builder")
    st.markdown("Build your resume section by section with AI guidance.")

    sections = [
        "Professional Summary", "Work Experience", "Education",
        "Skills", "Certifications", "Volunteer Work", "Projects", "Languages",
    ]

    col1, col2 = st.columns([1, 2])
    with col1:
        section = st.selectbox("Choose a Section", sections)
    with col2:
        content = st.text_area(
            f"Your {section}",
            height=150,
            placeholder=f"Enter your {section.lower()} details here…",
        )

    if st.button("✨ Format this Section", use_container_width=True):
        if not content.strip():
            st.warning("Please enter some content first.")
        else:
            with st.spinner("Formatting…"):
                result = format_resume_api(section, content)
            if result:
                st.markdown("#### ✅ Formatted Section")
                st.markdown(f"""
                <div class="vjc-card">
                    <pre style="white-space:pre-wrap; font-family:'Inter',sans-serif; color:#e0e0f0;">
{result['formatted_text']}</pre>
                    <small style="color:#9ca3af;">Word count: {result['word_count']}</small>
                </div>
                """, unsafe_allow_html=True)

                if result.get("tips"):
                    st.markdown("#### 💡 Tips for this Section")
                    for tip in result["tips"]:
                        st.markdown(f'<div class="tip-box">💡 {tip}</div>', unsafe_allow_html=True)

                if st.button("🔊 Read formatted section aloud"):
                    audio = get_tts_audio(result["formatted_text"])
                    if audio:
                        st.markdown(audio_player_html(audio), unsafe_allow_html=True)
            else:
                st.error("Could not format section. Is the backend running?")

    st.divider()
    st.markdown("#### 💬 Or ask the Resume Agent")
    with st.form("resume_chat_form", clear_on_submit=True):
        resume_msg = st.text_input(
            "Ask for resume help",
            placeholder="e.g. How do I describe a gap in employment?",
            label_visibility="visible",
        )
        if st.form_submit_button("Ask →"):
            if resume_msg.strip():
                with st.spinner("Thinking…"):
                    response = send_chat(f"Resume question: {resume_msg}")
                if response:
                    st.markdown(f'<div class="chat-bot">{response["reply"]}</div>', unsafe_allow_html=True)


# ── 4. Interview Prep ─────────────────────────────────────────────────────────
elif page == "🎤 Interview Prep":
    st.markdown("# 🎤 Interview Preparation")
    st.markdown("Practice interview questions and get instant feedback.")

    tab1, tab2 = st.tabs(["📋 Practice Questions", "🔍 Answer Feedback"])

    with tab1:
        role_q = st.text_input("Target Role", placeholder="e.g. Customer Service Representative", value="customer service")
        if st.button("Get Questions", use_container_width=True):
            with st.spinner("Loading questions…"):
                result = get_questions_api(role_q)
                st.session_state.interview_questions = result

        if st.session_state.interview_questions:
            qdata = st.session_state.interview_questions
            st.markdown(f"### {qdata['count']} Questions for **{qdata['role']}**")

            for i, q in enumerate(qdata["questions"], 1):
                st.markdown(f"""
                <div class="vjc-card">
                    <strong style="color:#a5b4fc;">Q{i}.</strong> {q}
                </div>
                """, unsafe_allow_html=True)

            for tip in qdata.get("tips", []):
                st.markdown(f'<div class="tip-box">💡 {tip}</div>', unsafe_allow_html=True)

            if st.button("🔊 Read all questions aloud"):
                all_q = " ".join(f"Question {i}: {q}" for i, q in enumerate(qdata["questions"], 1))
                audio = get_tts_audio(all_q)
                if audio:
                    st.markdown(audio_player_html(audio), unsafe_allow_html=True)

    with tab2:
        st.markdown("#### Practice & Get Feedback")
        fb_role = st.text_input("Role", value="customer service", key="fb_role")
        fb_question = st.selectbox(
            "Select a question",
            [
                "Tell me about yourself and your professional background.",
                "What are your greatest strengths?",
                "Describe a challenge you faced and how you overcame it.",
                "Why do you want to work for this company?",
                "Where do you see yourself in five years?",
            ],
        )
        fb_answer = st.text_area(
            "Your Answer",
            height=150,
            placeholder="Type your practice answer here…",
        )

        if st.button("📊 Get Feedback", use_container_width=True):
            if not fb_answer.strip():
                st.warning("Please write an answer first.")
            else:
                with st.spinner("Analyzing your answer…"):
                    feedback = get_feedback_api(fb_role, fb_question, fb_answer)
                if feedback:
                    cols = st.columns(3)
                    cols[0].metric("Word Count", feedback["answer_length_words"])
                    cols[1].metric("STAR Method Used", "✅ Yes" if feedback["star_used"] else "❌ No")
                    cols[2].metric("Strengths Found", len(feedback["strengths"]))

                    st.markdown("#### ✅ Strengths")
                    for s in feedback["strengths"]:
                        st.markdown(f'<div class="strength-box">✅ {s}</div>', unsafe_allow_html=True)

                    st.markdown("#### 🔧 Areas to Improve")
                    for imp in feedback["improvements"]:
                        st.markdown(f'<div class="improve-box">🔧 {imp}</div>', unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="vjc-card">
                        <strong>💬 Overall Tip:</strong> {feedback["overall_tip"]}
                    </div>
                    """, unsafe_allow_html=True)

                    if st.button("🔊 Listen to feedback"):
                        feedback_text = (
                            f"Your answer had {feedback['answer_length_words']} words. "
                            f"{'You used the STAR method. ' if feedback['star_used'] else 'Try using the STAR method. '}"
                            f"Strengths: {'. '.join(feedback['strengths'])}. "
                            f"Areas to improve: {'. '.join(feedback['improvements'])}. "
                            f"{feedback['overall_tip']}"
                        )
                        audio = get_tts_audio(feedback_text)
                        if audio:
                            st.markdown(audio_player_html(audio), unsafe_allow_html=True)


# ── 5. Voice Tools ────────────────────────────────────────────────────────────
elif page == "🔊 Voice Tools":
    st.markdown("# 🔊 Voice Tools")
    st.markdown("Text-to-speech and speech-to-text tools for accessibility.")

    # Check voice service status
    try:
        r = requests.get(f"{API_BASE}/api/voice/status", timeout=5)
        if r.status_code == 200:
            vstat = r.json()
            col1, col2 = st.columns(2)
            tts_ok = vstat["text_to_speech"]["available"]
            stt_ok = vstat["speech_to_text"]["available"]
            with col1:
                icon = "✅" if tts_ok else "❌"
                st.metric("Text-to-Speech (TTS)", f"{icon} {'Available' if tts_ok else 'Unavailable'}")
            with col2:
                icon = "✅" if stt_ok else "❌"
                st.metric("Speech-to-Text (STT)", f"{icon} {'Available' if stt_ok else 'Unavailable'}")
    except Exception:
        st.warning("Could not check voice service status. Is the backend running?")

    st.divider()

    tab_tts, tab_stt = st.tabs(["🔊 Text → Speech", "🎙️ Audio → Text"])

    with tab_tts:
        st.markdown("#### Convert any text to audio")
        tts_text = st.text_area(
            "Enter text to speak",
            height=120,
            placeholder="e.g. Hello! I am your Visual Job Coach. How can I help you today?",
        )
        col1, col2 = st.columns(2)
        with col1:
            tts_lang = st.selectbox("Language", ["en", "es", "fr", "de", "hi", "ar"], index=0)
        with col2:
            tts_slow = st.checkbox("Speak slowly (clearer)")

        if st.button("🔊 Generate Audio", use_container_width=True):
            if tts_text.strip():
                with st.spinner("Generating audio…"):
                    try:
                        payload = {"text": tts_text, "lang": tts_lang, "slow": tts_slow}
                        r = requests.post(f"{API_BASE}/api/voice/speak", json=payload, timeout=15)
                        if r.status_code == 200:
                            st.session_state.tts_audio = r.content
                            st.success("Audio generated!")
                        else:
                            st.error(f"TTS failed: {r.text[:200]}")
                    except Exception as e:
                        st.error(f"Request failed: {e}")
            else:
                st.warning("Enter some text first.")

        if st.session_state.tts_audio:
            st.markdown("#### 🎵 Your Audio")
            st.markdown(audio_player_html(st.session_state.tts_audio), unsafe_allow_html=True)
            st.download_button(
                "⬇️ Download MP3",
                data=st.session_state.tts_audio,
                file_name="speech.mp3",
                mime="audio/mpeg",
            )

    with tab_stt:
        st.markdown("#### Upload audio to transcribe")
        st.info("Upload a WAV or MP3 file to convert to text. Maximum size: 10 MB.")
        audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "flac", "ogg"])
        if audio_file and st.button("🎙️ Transcribe", use_container_width=True):
            with st.spinner("Transcribing audio…"):
                try:
                    files = {"audio": (audio_file.name, audio_file.read(), audio_file.type)}
                    r = requests.post(f"{API_BASE}/api/voice/transcribe", files=files, timeout=30)
                    if r.status_code == 200:
                        result = r.json()
                        if result["success"]:
                            st.markdown("#### 📝 Transcription")
                            st.markdown(f"""
                            <div class="vjc-card">
                                {result['text']}
                                <br><small style="color:#9ca3af;">Word count: {result['word_count']}</small>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(f"Transcription failed: {result.get('error', 'Unknown error')}")
                    else:
                        st.error(f"Server error: {r.status_code}")
                except Exception as e:
                    st.error(f"Request failed: {e}")
