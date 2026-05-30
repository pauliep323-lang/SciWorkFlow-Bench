from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
from loader import BenchmarkLoader

app = FastAPI(title="SciWorkFlow Benchmark")

loader = BenchmarkLoader()

@app.get("/")
async def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SciWorkFlow Benchmark</title>
        <style>
            body { font-family: Arial; background: #f8fafc; color: #1e2937; padding: 40px; text-align: center; }
            h1 { color: #1e40af; }
            .task { background: white; padding: 20px; margin: 20px auto; max-width: 700px; border-radius: 12px; border: 1px solid #ddd; }
        </style>
    </head>
    <body>
        <h1>SciWorkFlow Benchmark</h1>
        <p>10 Tasks Loaded</p>
    """
    for task in loader.tasks:
        html += f"""
        <div class="task">
            <strong>{task['title']}</strong><br>
            <small>Difficulty: {task['difficulty']} | Category: {task['category']}</small>
        </div>
        """
    html += "</body></html>"
    return HTMLResponse(html)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
