from services.openai_client import get_chat_completion


def evaluate_interview(conversation, job_context):
    """
    Evaluation report in ENGLISH.
    Must clearly state if the candidate is a Good Fit or Not a Good Fit.
    """

    messages = [
        {
            "role": "system",
            "content": (
                "You are an HR evaluator.\n"
                "Evaluate the candidate for a housekeeping role.\n\n"
                "Respond ONLY in English using this structure:\n\n"
                "1. Overall Verdict (Good Fit / Not a Good Fit)\n"
                "2. Reasoning (bullet points)\n"
                "3. Strengths\n"
                "4. Concerns or Gaps\n"
                "5. Final Recommendation (Hire / Consider / Reject)\n"
            )
        },
        {
            "role": "system",
            "content": f"Job Description:\n{job_context}"
        }
    ]

    # Add full conversation transcript
    for msg in conversation:
        messages.append({
            "role": "user",
            "content": f"{msg['role'].upper()}: {msg['content']}"
        })

    return get_chat_completion(messages, temperature=0.3)
