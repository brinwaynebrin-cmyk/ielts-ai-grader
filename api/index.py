from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal
import os

# 必须是顶级变量（不能缩进）
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>IELTS AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-6">
        <h1 class="text-3xl font-bold mb-4 text-center text-teal-600">雅思 AI 评分</h1>
        <textarea id="essay" rows="10" class="w-full p-4 border rounded-lg mb-4" placeholder="输入作文（250词）"></textarea>
        <button onclick="grade()" class="w-full bg-teal-500 text-white py-3 rounded-lg font-bold">提交评分</button>
        <div id="result" class="mt-4 p-4 bg-gray-50 rounded-lg hidden">
            <div class="text-center text-3xl font-bold text-teal-600" id="score"></div>
        </div>
    </div>
    <script>
        async function grade() {
            const essay = document.getElementById('essay').value;
            const res = await fetch('/api/grade_writing', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({essay: essay, task_type: 'task2', prompt: 'test', target_band: 7.0})
            });
            const data = await res.json();
            document.getElementById('result').classList.remove('hidden');
            document.getElementById('score').textContent = '总分: ' + data.overall_band;
        }
    </script>
</body>
</html>"""

class WritingRequest(BaseModel):
    essay: str
    task_type: Literal["task1", "task2"]
    prompt: str
    target_band: float = 7.0

@app.post("/api/grade_writing")
async def grade_writing(data: WritingRequest):
    if not os.getenv("DEEPSEEK_API_KEY"):
        return {
            "overall_band": 6.5,
            "breakdown": {
                "TR": {"score": 6.5, "comments": "Good"},
                "CC": {"score": 6.5, "comments": "Good"},
                "LR": {"score": 6.0, "comments": "Ok"},
                "GRA": {"score": 6.5, "comments": "Good"}
            },
            "detailed_feedback": {"weaknesses": ["Add complex sentences"]},
            "word_count": len(data.essay.split())
        }
    return {"overall_band": 6.0, "error": "Demo mode"}

# 必须是顶级变量（不能缩进，不能放在if里）
from mangum import Mangum
handler = Mangum(app)
