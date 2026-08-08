import os

from dotenv import load_dotenv
from groq import Groq


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# GROQ API KEY
# =====================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. "
        "Please configure your Groq API key."
    )


# =====================================================
# GROQ CLIENT
# =====================================================

client = Groq(
    api_key=GROQ_API_KEY
)


MODEL_NAME = "llama-3.3-70b-versatile"


# =====================================================
# GENERATE INTERVIEW QUESTION
# =====================================================

def generate_interview_question(
    interview_type="General",
    difficulty="Medium",
    previous_questions=None,
    previous_answers=None,
):

    if previous_questions is None:
        previous_questions = []

    if previous_answers is None:
        previous_answers = []


    history = ""

    for i, question in enumerate(previous_questions):

        history += f"\nQuestion {i + 1}: {question}"

        if i < len(previous_answers):

            history += (
                f"\nCandidate Answer: "
                f"{previous_answers[i]}"
            )


    prompt = f"""
You are a professional interviewer.

Conduct a realistic mock interview.

Interview Type:
{interview_type}

Difficulty:
{difficulty}

Previous Interview:
{history}

Generate exactly ONE interview question.

Rules:

- Ask only one question.
- Do not provide the answer.
- Do not explain the question.
- Do not number the question.
- Do not repeat previous questions.
- Keep it professional and concise.
- If previous answers exist, make the next question relevant
  to the candidate's previous answer.

Return ONLY the interview question.
"""


    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an experienced professional "
                        "interviewer."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.7,

            max_tokens=150,
        )


        question = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )


        return question


    except Exception as e:

        return f"Error generating question: {e}"


# =====================================================
# ANALYZE INTERVIEW ANSWER
# =====================================================

def analyze_answer(answer):

    prompt = f"""
You are an expert interview evaluator.

Evaluate the following candidate answer.

Candidate Answer:
{answer}

Provide:

Overall Score: /100

Confidence:
Fluency:
Clarity:
Answer Quality:

Strengths:
- 

Weaknesses:
- 

Suggestions:
- 

Keep the evaluation practical and concise.
"""


    try:

        response = client.chat.completions.create(

            model=MODEL_NAME,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert interview "
                        "performance evaluator."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.3,

            max_tokens=500,
        )


        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )


    except Exception as e:

        return f"Error analyzing answer: {e}"