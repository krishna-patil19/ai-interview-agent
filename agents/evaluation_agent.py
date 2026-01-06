from services.openai_client import get_chat_completion


def evaluate_interview(conversation, job_context):
    """
    Strict evaluation based on:
    1. What the candidate actually said (conversation)
    2. How well it matches the Job Description (resource)

    Output: English only
    """

    # Extract only candidate responses
    candidate_answers = [
        msg["content"].strip()
        for msg in conversation
        if msg["role"] == "candidate"
    ]

    # If candidate barely spoke → reject immediately
    if len(candidate_answers) < 3:
        return """
### ❌ Overall Verdict: NOT A GOOD FIT

**Reason:**
- The interview conversation was too short.
- The candidate did not provide enough information to evaluate against the job requirements.

**JD Match Analysis:**
- No evidence of required skills or experience mentioned.

**Final Recommendation:**
❌ Reject — insufficient interview data.
"""

    combined_answers = " ".join(candidate_answers)

    system_prompt = """
You are a strict HR evaluator.

IMPORTANT RULES:
- Evaluate ONLY based on the interview conversation and the Job Description
- Do NOT assume skills or experience
- Do NOT be polite or optimistic
- If candidate answers do NOT clearly match JD requirements, mark NOT A GOOD FIT
- Respond ONLY in English

Your task:
1. Extract key requirements from the Job Description
2. Extract key skills/experience from the candidate's answers
3. Compare them explicitly
4. Decide fit ONLY if there is clear overlap

Evaluation Criteria:
- Relevant experience mentioned by candidate
- Duties handled match JD responsibilities
- Availability/work expectations align with JD
- Communication clarity
- Willingness/attitude

If any major JD requirement is missing from the candidate answers,
the verdict MUST be NOT A GOOD FIT.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": f"Job Description:\n{job_context}"},
        {
            "role": "user",
            "content": f"""
Interview Transcript (source of truth):
{conversation}

Candidate Answers:
{combined_answers}

Evaluate STRICTLY based on JD alignment.
"""
        }
    ]

    return get_chat_completion(messages, temperature=0.1)
