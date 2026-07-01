"""
interview_routes.py
-------------------
FastAPI routes for interview preparation.

Endpoints:
  GET  /api/interview/questions/{role}  — get practice questions for a role
  POST /api/interview/feedback          — submit a practice answer, get AI feedback tips
"""

from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field

from app.security.input_sanitizer import sanitize_role, sanitize_text

router = APIRouter(prefix="/api/interview", tags=["Interview"])


class FeedbackRequest(BaseModel):
    role: str = Field(..., min_length=2, max_length=200, description="Target job role")
    question: str = Field(..., min_length=5, max_length=500, description="Interview question asked")
    answer: str = Field(..., min_length=10, max_length=3000, description="The user's practice answer")


class FeedbackResponse(BaseModel):
    question: str
    answer_length_words: int
    strengths: list[str]
    improvements: list[str]
    star_used: bool
    overall_tip: str


# Question bank organized by category
QUESTION_BANK: dict[str, list[str]] = {
    "general": [
        "Tell me about yourself and your professional background.",
        "What are your greatest strengths?",
        "What is your biggest weakness, and how are you working on it?",
        "Why do you want to work for this company?",
        "Where do you see yourself in five years?",
        "Describe a challenge you faced and how you overcame it.",
        "Why are you leaving your current/last job?",
        "What motivates you at work?",
    ],
    "customer service": [
        "How do you handle a difficult or angry customer?",
        "Give an example of when you went above and beyond for a customer.",
        "How do you prioritize multiple customer requests at once?",
        "Tell me about a time you solved a complex customer problem.",
    ],
    "data entry": [
        "How do you ensure accuracy when entering large amounts of data?",
        "What is your typing speed, and how do you maintain accuracy?",
        "Describe a time you caught an important data error.",
        "How do you stay focused during repetitive tasks?",
    ],
    "software developer": [
        "Describe your experience with accessible software development (WCAG, ARIA).",
        "What programming languages and frameworks are you most comfortable with?",
        "How do you approach debugging a difficult problem?",
        "Tell me about a project you're proud of and your role in it.",
    ],
    "administrative": [
        "How do you manage your time and prioritize tasks?",
        "Describe your experience with scheduling and calendar management.",
        "How do you handle confidential information?",
        "Give an example of organizing a complex project.",
    ],
}


def _get_questions_for_role(role: str) -> list[str]:
    """Find the most relevant question set for a given role."""
    role_lower = role.lower()
    for category, questions in QUESTION_BANK.items():
        if category in role_lower or any(word in role_lower for word in category.split()):
            # Return general + role-specific
            combined = QUESTION_BANK["general"][:4] + questions
            return combined[:8]
    return QUESTION_BANK["general"]


@router.get("/questions/{role}", summary="Get interview practice questions for a role")
async def get_practice_questions(
    role: str = Path(..., min_length=2, max_length=200, description="Job role to get questions for"),
) -> dict:
    """
    Return common interview questions for the given job role.
    Combines general questions with role-specific ones.
    """
    role_clean = sanitize_role(role)
    if not role_clean:
        raise HTTPException(status_code=400, detail="Role cannot be empty.")

    questions = _get_questions_for_role(role_clean)
    return {
        "role": role_clean,
        "count": len(questions),
        "questions": questions,
        "tips": [
            "Use the STAR method: Situation, Task, Action, Result.",
            "Keep answers to 1-2 minutes when speaking.",
            "Prepare 2-3 questions to ask the interviewer at the end.",
        ],
    }


@router.post("/feedback", response_model=FeedbackResponse, summary="Get feedback on a practice answer")
async def get_answer_feedback(request: FeedbackRequest) -> FeedbackResponse:
    """
    Analyze a practice interview answer and return structured feedback.

    Provides strengths, areas for improvement, and tips — without needing LLM calls
    for instant response.
    """
    question = sanitize_text(request.question, max_length=500)
    answer = sanitize_text(request.answer, max_length=3000)

    words = answer.split()
    word_count = len(words)

    # Check for STAR method keywords
    star_keywords = {
        "situation": ["situation", "when", "time", "working at", "project"],
        "task": ["task", "responsible", "role", "needed to", "had to"],
        "action": ["i did", "i took", "i created", "i built", "decided", "action"],
        "result": ["result", "outcome", "achieved", "improved", "increased", "successfully"],
    }
    answer_lower = answer.lower()
    star_components_found = sum(
        1 for keywords in star_keywords.values()
        if any(kw in answer_lower for kw in keywords)
    )
    star_used = star_components_found >= 3

    # Generate strengths based on answer analysis
    strengths = []
    if word_count >= 100:
        strengths.append("Good level of detail in your answer.")
    if star_used:
        strengths.append("You naturally used the STAR structure.")
    if "example" in answer_lower or "time" in answer_lower:
        strengths.append("You backed up your answer with a real example.")
    if "team" in answer_lower or "collaborate" in answer_lower:
        strengths.append("You highlighted teamwork, which employers value.")
    if not strengths:
        strengths.append("You gave a clear, direct response.")

    # Generate improvement suggestions
    improvements = []
    if word_count < 50:
        improvements.append("Try to expand your answer with a specific example.")
    if word_count > 400:
        improvements.append("Consider trimming your answer to under 2 minutes (about 300 words).")
    if not star_used:
        improvements.append("Try structuring your answer using the STAR method: Situation, Task, Action, Result.")
    if "result" not in answer_lower and "outcome" not in answer_lower:
        improvements.append("Always end with the positive outcome or what you learned.")
    if not improvements:
        improvements.append("Practice saying this answer out loud to improve natural flow.")

    overall_tip = (
        "Great answer — keep practicing to build confidence!"
        if star_used and word_count >= 80
        else "Keep practicing. Focus on adding a concrete result to make your answer more impactful."
    )

    return FeedbackResponse(
        question=question,
        answer_length_words=word_count,
        strengths=strengths,
        improvements=improvements,
        star_used=star_used,
        overall_tip=overall_tip,
    )
