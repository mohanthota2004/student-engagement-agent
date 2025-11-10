# app/agents/langchain_agent.py
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

    Always returns valid JSON output.
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # 🔹 Fallback mode when no API key is found
    if not OPENAI_API_KEY:
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

    # 🔹 LangChain + OpenAI integration
    try:
        prompt = ChatPromptTemplate.from_template("""
        You are an educational engagement analyzer.
        Analyze the student's message below and respond ONLY in JSON format like this:

        {{
            "engagement_level": "Low" | "Medium" | "High",
            "reasons": ["short list of explanations"],
            "suggestion": "actionable feedback for teacher"
        }}

        Message: {text}
        """)

        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
        chain = prompt | llm

        response = chain.invoke({"text": text})
        output_text = response.content.strip()

        # ✅ Clean and extract JSON text
        if not output_text.startswith("{"):
            start = output_text.find("{")
            end = output_text.rfind("}")
            if start != -1 and end != -1:
                output_text = output_text[start:end + 1]

        return json.loads(output_text)

    except Exception as e:
        # ✅ Always return valid JSON, even on model failure
        return {
            "engagement_level": "Error",
            "reasons": [f"Exception: {str(e)}"],
            "suggestion": "Internal server issue — please retry."
        }
