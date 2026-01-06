from services.openai_client import get_chat_completion


def get_interviewer_response(conversation, job_context, language):
    if language == "Kannada":
        language_instruction = (
            "Speak ONLY in simple, spoken Kannada. "
            "Use natural everyday Kannada suitable for a housekeeping interview."
        )
    else:
        language_instruction = (
            "Speak ONLY in simple, spoken Hindi. "
            "Use natural everyday Hindi suitable for a housekeeping interview."
        )

    system_prompt = f"""
You are an AI interviewer hiring for a housekeeping role.

Rules:
- {language_instruction}
- Be polite and professional
- Ask ONE question at a time
- Do NOT repeat questions
- Keep responses short (2–3 lines)

Job Description:
{job_context}
"""

    messages = [{"role": "system", "content": system_prompt}]

    for msg in conversation:
        messages.append({
            "role": "assistant" if msg["role"] == "interviewer" else "user",
            "content": msg["content"]
        })

    return get_chat_completion(messages, temperature=0.6)
