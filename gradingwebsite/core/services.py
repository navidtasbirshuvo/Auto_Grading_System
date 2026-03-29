import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def grade_answer(question_text, correct_answer, student_answer, total_marks=10):
    """
    Sends the answer to the LLM API for grading.
    Returns a numeric score (float) or None if grading fails.
    """

    api_url = getattr(settings, 'LLM_API_URL', None)

    if not api_url:
        logger.error("LLM_API_URL is not configured in settings.")
        return None

    payload = {
        "question": question_text,
        "correct_answer": correct_answer,
        "student_answer": student_answer,
        "total_marks": total_marks
    }

    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()

        data = response.json()
        logger.debug(f"Grading API response: {data}")

        score = data.get("score")

        if score is None:
            logger.error(f"API returned no score. Response: {data}")
            return None

        try:
            score = float(score)
        except (TypeError, ValueError):
            logger.error(f"Invalid score format returned: {score}")
            return None

        # Ensure score is within valid bounds
        return max(0.0, min(score, float(total_marks)))

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Grading API: {e}")
        return None

    except Exception as e:
        logger.error(f"Unexpected error during grading: {e}")
        return None
