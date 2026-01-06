from services.openai_client import get_chat_completion


def evaluate_interview(conversation, job_context):
    """
    Evaluates the interview based on:
    - Candidate responses in the conversation
    - Job description / JD content
    Returns a structured recruiter-style evaluation in English.
    """

    # Extract only candidate answers
    candidate_answers = [
        msg["content"]
        for msg in conversation
        if msg["role"] == "user"
    ]

    conversation_text = "\n".join(candidate_answers)

    system_prompt = """
You are a professional HR recruiter evaluating a housekeeping candidate.

Your task:
1. Carefully analyze the Job Description.
2. Analyze the candidate's interview answers.
3. Judge alignment between the two.

IMPORTANT RULES:
- Do NOT assume skills that are not explicitly stated.
- If answers are short or vague, treat that as a weakness.
- If the candidate barely answered questions, mark NOT A GOOD FIT.
- Be strict but fair.
- Output must be ONLY in English.
- Use simple, clear language (non-technical).

Return the evaluation in EXACTLY the following format:

### Candidate Evaluation Report

**Strengths**
- Bullet points

**Weaknesses**
- Bullet points

**Concerns / Risks**
- Bullet points (if any)

**Overall Fit Assessment**
GOOD FIT / NOT A GOOD FIT

**Reasoning**
2–4 sentences clearly explaining WHY this verdict was given.
"""

    user_prompt = f"""
JOB DESCRIPTION:
{job_context}

CANDIDATE INTERVIEW ANSWERS:
{conversation_text}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    evaluation = get_chat_completion(
        messages=messages,
        temperature=0.3  # low temp = more stable verdicts
    )

    return evaluation
