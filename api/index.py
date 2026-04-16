from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>IELTS AI Grader</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-6">
        <h1 class="text-3xl font-bold mb-4 text-center text-teal-600">IELTS AI 评分</h1>
        <p class="text-gray-600 mb-6 text-center">输入作文，获取AI评分（基于DeepSeek）</p>
        
        <textarea id="essay" rows="12" class="w-full p-4 border rounded-lg mb-4" placeholder="在此输入雅思作文（至少250词）..."></textarea>
        
        <button onclick="grade()" class="w-full bg-teal-500 text-white py-3 rounded-lg font-bold hover:bg-teal-600">
            提交评分
        </button>
        
        <div id="result" class="mt-6 p-4 bg-gray-50 rounded-lg hidden">
            <div class="text-center text-3xl font-bold text-teal-600 mb-2" id="score"></div>
            <div id="details" class="text-sm text-gray-700"></div>
        </div>
    </div>

    <script>
        async function grade() {
            const essay = document.getElementById('essay').value;
            if (essay.trim().split(/\\s+/).length < 250) {
                alert('需要至少250词');
                return;
            }
            
            const btn = document.querySelector('button');
            btn.textContent = '评分中...';
            btn.disabled = true;
            
            try {
                const res = await fetch('/api/grade_writing', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        essay: essay,
                        task_type: 'task2',
                        prompt: 'test',
                        target_band: 7.0
                    })
                });
                
                const data = await res.json();
                document.getElementById('result').classList.remove('hidden');
                document.getElementById('score').textContent = '总分: ' + data.overall_band;
                document.getElementById('details').innerHTML = 
                    'TR: ' + data.breakdown.TR.score + '<br>' +
                    'CC: ' + data.breakdown.CC.score + '<br>' +
                    'LR: ' + data.breakdown.LR.score + '<br>' +
                    'GRA: ' + data.breakdown.GRA.score;
            } catch(e) {
                alert('错误: ' + e.message);
            }
            
            btn.textContent = '提交评分';
            btn.disabled = false;
        }
    </script>
</body>
</html>
    """
    return html

class WritingRequest(BaseModel):
    essay: str
    task_type: Literal["task1", "task2"]
    prompt: str
    target_band: float = 7.0

@app.post("/api/grade_writing")
async def grade_writing(data: WritingRequest):
    word_count = len(data.essay.split())
    target = 150 if data.task_type == "task1" else 250
    
    if word_count < target:
        return {"error": f"字数不足，需要至少{target}词", "word_count": word_count}
    
    # 如果没设置DeepSeek API，返回模拟数据
    if not os.getenv("DEEPSEEK_API_KEY"):
        return {
            "overall_band": 6.5,
            "breakdown": {
                "TR": {"score": 6.5, "comments": "Good"},
                "CC": {"score": 6.5, "comments": "Good"},
                "LR": {"score": 6.0, "comments": "Ok"},
                "GRA": {"score": 6.5, "comments": "Good"}
            },
            "detailed_feedback": {
                "weaknesses": ["Add more complex sentences", "Use academic vocabulary"]
            },
            "word_count": word_count,
            "mode": "demo"
        }
    
    # 有API Key时调用DeepSeek
    import openai, json
    try:
        client = openai.OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": '你是雅思考官。输出JSON: {"overall_band": float, "breakdown": {"TR":{"score":float,"comments":"str"}, "CC":{}, "LR":{}, "GRA":{}}, "detailed_feedback": {"weaknesses":[]}}'},
                {"role": "user", "content": f"评分这篇{data.task_type}作文：{data.essay}"}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        result = json.loads(response.choices[0
