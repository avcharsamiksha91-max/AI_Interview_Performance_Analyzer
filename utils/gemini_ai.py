import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def evaluate_answer(question, answer):
    prompt = f"""
You are an HR interviewer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer and provide:
1. Score out of 10
2. Strengths
3. Weaknesses
4. Suggestions for improvement
"""

    response = model.generate_content(prompt)
    return response.text