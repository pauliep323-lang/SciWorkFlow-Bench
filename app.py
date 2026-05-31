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
    try:
        from langchain_xai import ChatXAI
        from langchain_core.messages import HumanMessage
        key = os.getenv("XAI_API_KEY")
        if not key:
            return None
        return ChatXAI(model="grok-3", api_key=key, temperature=0.7)
    except:
        return None

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
            <button onclick="openTask('{task['id']}')">Run This Task</button>
        </div>
        """
    
    html += """
    <div id="taskModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.7); z-index:1000;">
        <div style="background:white; margin:5% auto; padding:35px; width:85%; max-width:900px; border-radius:20px; max-height:90vh; overflow-y:auto;" id="modalContent">
        </div>
    </div>

    <script>
        async function openTask(taskId) {
            const res = await fetch('/task/' + taskId);
            const task = await res.json();
            
            let html = `
                <h2>${task.title}</h2>
                <p><strong>Difficulty:</strong> ${task.difficulty.toUpperCase()} | <strong>Category:</strong> ${task.category}</p>
                <p>${task.description}</p>
            `;
            if (task.hints && task.hints.length > 0) {
                html += `<p><strong>Hints:</strong></p><ul>`;
                task.hints.forEach(h => html += `<li>${h}</li>`);
                html += `</ul>`;
            }
            html += `
                <textarea id="answer" rows="12" style="width:100%; margin:20px 0; padding:15px; font-size:1.05em;" placeholder="Type your detailed answer here..."></textarea>
                <button onclick="submitAnswer('${task.id}')">Submit Answer to Grok</button>
                <button onclick="closeModal()" style="background:#64748b; margin-left:12px;">Close</button>
            `;
            document.getElementById('modalContent').innerHTML = html;
            document.getElementById('taskModal').style.display = 'block';
        }
        
        function closeModal() {
            document.getElementById('taskModal').style.display = 'none';
        }
        
        async function submitAnswer(taskId) {
            const answer = document.getElementById('answer').value.trim();
            if (!answer) {
                alert("Please write an answer.");
                return;
            }
            const res = await fetch('/grade', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({task_id: taskId, answer: answer})
            });
            const result = await res.json();
            alert(result.feedback || "Feedback received.");
        }
    </script>
    </body></html>
    """
    return HTMLResponse(html)

@app.get("/task/{task_id}")
async def get_task(task_id: str):
    for task in loader.tasks:
        if task['id'] == task_id:
            return task
    return {"error": "Task not found"}

@app.post("/grade")
async def grade_answer(data: dict):
    task = next((t for t in loader.tasks if t['id'] == data['task_id']), None)
    if not task:
        return {"feedback": "Task not found."}
    
    prompt = f"Evaluate this answer:\nTask: {task['title']}\nDescription: {task['description']}\nUser Answer: {data['answer']}\nGive honest feedback and score out of 10."
    
    llm = get_llm()
    if not llm:
        return {"feedback": "Grok grading is not available right now."}
    
    try:
        from langchain_core.messages import HumanMessage
        response = llm.invoke([HumanMessage(content=prompt)])
        return {"feedback": response.content}
    except Exception as e:
        return {"feedback": f"Grading failed: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
