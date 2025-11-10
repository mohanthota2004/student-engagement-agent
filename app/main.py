from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os
from app.agents.langchain_agent import analyze_engagement

app = FastAPI()

# Create data directory if not exists
os.makedirs("data", exist_ok=True)
DATA_FILE = "data/engagement_results.csv"

# ---------- HTML Template ----------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Engagement Analyzer</title>
    <style>
        body {{ font-family: Arial; background-color: #f9f9f9; padding: 40px; }}
        .container {{ max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        textarea {{ width: 100%; height: 120px; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }}
        button {{ padding: 10px 20px; background-color: #0078D7; color: white; border: none; border-radius: 5px; cursor: pointer; }}
        button:hover {{ background-color: #005fa3; }}
        .result {{ margin-top: 20px; background: #f1f1f1; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h2>🧠 Student Engagement Analyzer</h2>
        <form method="post" action="/">
            <textarea name="student_text" placeholder="Enter a student's message..."></textarea><br><br>
            <button type="submit">Analyze Engagement</button>
        </form>

        {result_html}

        <p style="margin-top: 20px;">
            <a href="/dashboard">📊 View Dashboard</a>
        </p>
    </div>
</body>
</html>
"""

# ---------- Routes ----------

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE.format(result_html="")

@app.post("/", response_class=HTMLResponse)
async def analyze(student_text: str = Form(...)):
    result = analyze_engagement(student_text)

    # Save to CSV
    df_new = pd.DataFrame([{
        "text": student_text,
        "engagement_level": result["engagement_level"],
        "reasons": ", ".join(result["reasons"]),
        "suggestion": result["suggestion"]
    }])

    if os.path.exists(DATA_FILE):
        df_old = pd.read_csv(DATA_FILE)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.to_csv(DATA_FILE, index=False)

    # Display Result Nicely
    result_html = f"""
    <div class="result">
        <h3>Result:</h3>
        <p><b>Engagement Level:</b> {result['engagement_level']}</p>
        <p><b>Reasons:</b> {', '.join(result['reasons'])}</p>
        <p><b>Suggestion:</b> {result['suggestion']}</p>
    </div>
    """

    return HTML_TEMPLATE.format(result_html=result_html)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    if not os.path.exists(DATA_FILE):
        return "<h3>No engagement data yet!</h3>"

    df = pd.read_csv(DATA_FILE)
    summary = df["engagement_level"].value_counts().to_dict()

    html = "<h2>📊 Engagement Summary</h2><ul>"
    for level, count in summary.items():
        html += f"<li><b>{level}</b>: {count}</li>"
    html += "</ul><a href='/'>⬅ Back</a>"

    return HTMLResponse(content=html)

