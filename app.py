from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from loader import BenchmarkLoader
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SciWorkFlow Benchmark")

app.mount("/static", StaticFiles(directory="static"), name="static")

loader = BenchmarkLoader()

# Lazy load Grok only when needed
def get_llm():
    from langchain_xai import ChatXAI
    from langchain_core.messages import HumanMessage
    key = os.getenv("XAI_API_KEY")
    if not key:
        return None
    return ChatXAI(model="grok-3", api_key=key, temperature=0.7)

@app.get("/")
async def home():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SciWorkFlow Benchmark</title>
        <style>
            body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #f8fafc; color: #1e2937; padding: 40px; margin: 0; text-align: center; }}
            .logo {{ max-width: 340px; margin: 0 auto 25px auto; display: block; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}
            h1 {{ color: #1e40af; margin: 0; font-size: 2.8em; }}
            .subtitle {{ color: #64748b; font-size: 1.35em; margin-top: 8px; }}
            .task {{ background: white; padding: 28px; margin: 25px auto; max-width: 820px; border-radius: 20px; border: 1px solid #e2e8f0; text-align: left; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }}
            button {{ background: linear-gradient(90deg, #1e40af, #3b82f6); color: white; padding: 14px 36px; border: none; border-radius: 50px; cursor: pointer; font-weight: 600; }}
            button:hover {{ background: linear-gradient(90deg, #1e3a8a, #2563eb); }}
        </style>
    </head>
    <body>
        <img src="/static/logo.png" alt="SciWorkFlow" class="logo">
        <h1>SciWorkFlow Benchmark</h1>
        <p class="subtitle">High-Quality AI Research Challenges</p>
    """

    for task in loader.tasks:
        html += f"""
        <div class="task">
            <strong style="font-size:1.3em;">{task['title']}</strong><br>
            <small style="color:#64748b;">Difficulty: {task['difficulty'].upper()} • Category: {task['category']}</small><br><br>
            <button onclick="alert('Selected: {task['title']}')">Run This Task</button>
        </div>
        """
    
    html += "</body></html>"
    return HTMLResponse(html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
