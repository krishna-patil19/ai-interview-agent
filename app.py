import streamlit as st
import tempfile

from agents.conversation_agent import get_interviewer_response
from agents.evaluation_agent import evaluate_interview
from services.file_parser import parse_sales_resource
from services.speech_to_text import transcribe_audio
from services.text_to_speech import speak_text

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="AI Interview Agent (Voice)", layout="wide")
st.title("AI Interview Agent (Voice)")

# ---------------- HELPER ----------------
def get_welcome_text(language):
    if language == "Kannada":
        return "ನಮಸ್ಕಾರ! ನಿಮ್ಮನ್ನು ಸಂದರ್ಶನಕ್ಕೆ ಸ್ವಾಗತಿಸುತ್ತೇವೆ. ಮೊದಲು ನಿಮ್ಮ ಹೆಸರನ್ನು ಹೇಳಿ."
    else:
        return "नमस्ते! आपका स्वागत है। सबसे पहले कृपया अपना नाम बताइए।"

def get_stt_language_code(language):
    return "kn" if language == "Kannada" else "hi"

# ---------------- SESSION STATE ----------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "job_context" not in st.session_state:
    st.session_state.job_context = ""

if "language" not in st.session_state:
    st.session_state.language = "Hindi"

if "started" not in st.session_state:
    st.session_state.started = False

if "ended" not in st.session_state:
    st.session_state.ended = False

if "last_audio_size" not in st.session_state:
    st.session_state.last_audio_size = 0

if "pending_audio" not in st.session_state:
    st.session_state.pending_audio = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("Interview Setup")

    st.session_state.language = st.selectbox(
        "Conversation Language",
        ["Hindi", "Kannada"]
    )

    uploaded_file = st.file_uploader(
        "Upload Job Description (PDF / TXT)",
        type=["pdf", "txt"]
    )

    if uploaded_file:
        st.session_state.job_context = parse_sales_resource(uploaded_file)
        st.success("Job description loaded")

# ---------------- AI WELCOMES FIRST ----------------
if (
    not st.session_state.started
    and st.session_state.job_context
):
    welcome_text = get_welcome_text(st.session_state.language)

    st.session_state.conversation.append({
        "role": "interviewer",
        "content": welcome_text
    })

    st.session_state.pending_audio = speak_text(welcome_text)
    st.session_state.started = True
    st.rerun()

# ---------------- SHOW CONVERSATION ----------------
st.subheader("💬 Interview Conversation")

for msg in st.session_state.conversation:
    if msg["role"] == "interviewer":
        st.markdown(f" **इंटरव्यूअर:** {msg['content']}")
    else:
        st.markdown(f" **उम्मीदवार:** {msg['content']}")

# ---------------- PLAY AI AUDIO ----------------
if st.session_state.pending_audio:
    st.audio(st.session_state.pending_audio, autoplay=True)
    st.session_state.pending_audio = None

# ---------------- CANDIDATE SPEAKS ----------------
if st.session_state.started and not st.session_state.ended:
    st.subheader("🎙️ बोलिए (उम्मीदवार)")

    audio = st.audio_input("Speak")

    if audio:
        size = len(audio.getbuffer())
        if size != st.session_state.last_audio_size:
            st.session_state.last_audio_size = size

            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio.getbuffer())
                audio_path = f.name

            # ✅ FIX: pass language code explicitly
            user_text = transcribe_audio(
                audio_path,
                language_code=get_stt_language_code(st.session_state.language)
            )

            st.session_state.conversation.append({
                "role": "candidate",
                "content": user_text
            })

            reply_text = get_interviewer_response(
                st.session_state.conversation,
                st.session_state.job_context,
                st.session_state.language
            )

            st.session_state.conversation.append({
                "role": "interviewer",
                "content": reply_text
            })

            st.session_state.pending_audio = speak_text(reply_text)
            st.rerun()

# ---------------- END INTERVIEW ----------------
st.markdown("---")

if not st.session_state.ended:
    if st.button("🔴 End Interview"):
        st.session_state.ended = True
        st.success("Interview ended. You can now evaluate.")

# ---------------- EVALUATION ----------------
if st.session_state.ended:
    st.subheader("📊 Evaluation Report (English)")

    if st.button("Generate Evaluation"):
        with st.spinner("Evaluating candidate..."):
            report = evaluate_interview(
                st.session_state.conversation,
                st.session_state.job_context
            )

        st.markdown(report)
