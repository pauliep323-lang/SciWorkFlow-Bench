from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="SciWorkflow Benchmark")

@app.get("/")
def home():
    return {"message": "SciWorkflow is running. Go to /benchmarks for robotics page."}

@app.get("/benchmarks", response_class=HTMLResponse)
def robotics_benchmarks():
    benchmarks = [
        "1. Autonomous Navigation in Dynamic Environments",
        "2. Human-Robot Collaboration Safety Systems",
        "3. Multi-Robot Coordination & Swarming",
        "4. Dexterous Manipulation & Fine Motor Skills",
        "5. Long-Duration Autonomous Operation",
        "6. Real-time Environmental Adaptation",
        "7. Ethical Decision Making Frameworks",
        "8. Energy-Efficient Locomotion & Power Management",
        "9. Advanced Computer Vision & Object Recognition",
        "10. Natural Language Understanding & Instruction Following",
        "11. Self-Repair & Maintenance Capabilities",
        "12. Human Emotion & Intent Recognition",
        "13. Secure Multi-Agent Communication Protocols",
        "14. Learning from Demonstration & Few-Shot Adaptation",
        "15. Integration with Real-World Infrastructure"
    ]
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Robotics Horizon Benchmarks</title>
        <style>
            body { font-family: Arial, sans-serif; background: #0a0a0a; color: #ddd; padding: 40px; }
            h1 { color: #f2a65a; }
            .card { background: #1f1f1f; padding: 20px; margin: 15px 0; border-radius: 12px; border-left: 5px solid #f2a65a; }
        </style>
    </head>
    <body>
        <h1>🚀 Robotics Horizon Benchmarks</h1>
        <p>15 key long-horizon challenges</p>
    """
    for i, b in enumerate(benchmarks, 1):
        html += f'<div class="card"><strong>{i}.</strong> {b}</div>'
    html += "</body></html>"
    return html

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
