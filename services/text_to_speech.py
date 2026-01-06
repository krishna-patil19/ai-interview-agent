import os
import tempfile
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 🔥 THIS IS REQUIRED

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not loaded")

client = OpenAI(api_key=api_key)

def speak_text(text: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        audio_path = f.name

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    response.stream_to_file(audio_path)
    return audio_path
