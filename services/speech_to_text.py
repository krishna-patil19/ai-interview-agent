from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(audio_path, language_code):
    """
    audio_path: path to wav file (string)
    language_code: 'hi' or 'kn'
    """

    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            file=audio_file,                 # ✅ correct type
            model="gpt-4o-transcribe",
            language=language_code
        )

    return response.text
