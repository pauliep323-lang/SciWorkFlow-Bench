from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="SciWorkflow Benchmark")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/benchmarks', response_class=HTMLResponse)
def robotics_benchmarks():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Robotics Horizon Benchmarks - SciWorkflow</title>
        <style>
            body { 
                font-family: system-ui, sans-serif; 
                background: #0a0f1c; 
                color: #e0f0ff; 
                padding: 30px; 
                line-height: 1.6; 
            }
            .logo { 
                display: block; 
                margin: 0 auto 20px; 
                max-width: 220px; 
            }
            h1 { 
                color: #00d4ff; 
                text-align: center; 
            }
            .card { 
                background: #0f1629; 
                border: 1px solid #1e4d7a; 
                border-radius: 12px; 
                padding: 22px; 
                margin: 20px 0; 
            }
            button { 
                padding: 14px; 
                margin: 6px 4px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                font-weight: bold; 
                width: 48%; 
            }
            .ask-btn { background: #00b8d4; color: #000; }
            .test-btn { background: #00c853; color: #000; }
            .response { 
                margin-top: 12px; 
                padding: 15px; 
                background: #1a2338; 
                border-radius: 8px; 
                white-space: pre-wrap; 
            }
        </style>
    </head>
    <body>
        <img src="/static/logo.png" class="logo" alt="SciWorkflow">
        <h1>Robotics Horizon Benchmarks</h1>
        <p style="text-align:center; color:#88aaff;">Long-Horizon Agentic Challenges</p>
    """

    for i in range(1, 16):
        html += f'''
        <div class="card">
            <strong>{i}. Benchmark {i}</strong><br><br>
            <button class="ask-btn" onclick="askGrok({i})">Ask Grok →</button>
            <button class="test-btn" onclick="alert('Test Yourself - Coming Soon!')">Test Yourself</button>
            <div id="resp{i}" class="response" style="display:none;"></div>
        </div>
        '''

    html += """
        <script>
        async function askGrok(id) {
            const div = document.getElementById('resp' + id);
            div.style.display = 'block';
            div.textContent = 'Thinking...';
            try {
                const res = await fetch('/ask-grok', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({benchmark: 'Benchmark ' + id})
                });
                const data = await res.json();
                div.innerHTML = '<strong>Grok Report:</strong><br>' + data.response;
            } catch(e) {
                div.textContent = 'Error connecting to Grok.';
            }
        }
        </script>
    </body>
    </html>
    """
    return html


@app.post('/ask-grok')
async def ask_grok(data: dict):
    try:
        from langchain_xai import ChatXAI
        from langchain_core.messages import HumanMessage

        llm = ChatXAI(
            model="grok-3-beta",
            xai_api_key="xai-f3Gcr70xbyQwwIaF70EJb6itKjhofZUZ2oLFumrlRPntSyX616wIcIWgjokKb3b0GXfT6syCx8C6qYN7"
        )
        
        response = llm.invoke([HumanMessage(content=f"Explain this robotics horizon benchmark in detail and give current research status: {data['benchmark']}")])
        return {"response": response.content}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
