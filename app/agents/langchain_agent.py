"""
LangChain Agent for analyzing student engagement text.
Compatible with LangChain v1.0.5 and Python 3.14.
"""

import os
import json
from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


def analyze_engagement(text: str) -> Dict:
    """
    Analyze student forum text using OpenAI via LangChain.

    Returns a dictionary with:
        - engagement_level: Low / Medium / High
        - reasons: list of explanations
        - suggestion: next step or intervention
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        # 🧠 Fallback logic when no API key is set
        reasons = []
        low_keywords = ["no idea", "bored", "don't care", "boring", "not interested", "skip"]
        high_keywords = ["excited", "love", "interesting", "helpful", "thanks", "nice"]

        score = 0
        text_lower = text.lower()
        for w in low_keywords:
            if w in text_lower:
                score -= 1
                reasons.append(f"found_keyword:{w}")
        for w in high_keywords:
            if w in text_lower:
                score += 1
                reasons.append(f"found_keyword:{w}")

        if score <= -1:
            level = "Low"
            suggestion = "Try a quick interactive poll or low-stakes quiz to re-engage."
        elif score >= 1:
            level = "High"
            suggestion = "Encourage deeper reflection and peer feedback."
        else:
            level = "Medium"
            suggestion = "Offer a hint or small collaborative task."

        return {"engagement_level": level, "reasons": reasons, "suggestion": suggestion}

    # 🧩 Use LangChain with OpenAI
    prompt = ChatPromptTemplate.from_template("""
You are an educational engagement analyzer.
Analyze the student's message below and respond ONLY in JSON format like this:
{{
  "engagement_level": "Low | Medium | High",
  "reasons": ["short reason 1", "short reason 2"],
  "suggestion": "short teacher action"
}}

Message: {text}
""")

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
    chain = prompt | llm

    response = chain.invoke({"text": text})

    # LangChain returns AIMessage, so get content text
    output_text = response.content

    try:
        return json.loads(output_text)
    except Exception as e:
        return {
            "engagement_level": "Error",
            "reasons": [f"Exception: {str(e)}"],
            "suggestion": "The AI model could not process the input correctly. Please try again."
        }
