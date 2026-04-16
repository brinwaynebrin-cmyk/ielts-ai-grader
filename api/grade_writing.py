from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Literal
import os

app = FastAPI()

# 前端页面（直接内嵌，省去文件路径问题）
@app.get("/", response_class=HTMLResponse)
def frontend():
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IELTS AI Grader</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-8">
    <div class="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-6">
        <h1 class="text-2xl font-bold mb-4 text-center">雅思写作 AI 评分</h1>
        
        <div class="mb-4">
            <label class="block text-sm font-medium mb-2">题目：</label>
            <input id="prompt" type="text" class="w-full p-2 border rounded" 
                value="Some people think that the best way to reduce crime is to give longer prison sentences. Discuss both views." />
        </div>
        
        <div class="mb-4">
            <label class="block text-sm font-medium mb-2">作文（Task 2）：</label>
            <textarea id="essay" rows="10" class="w-full p-2 border rounded" 
                placeholder="在此输入你的作文...至少250词"></textarea>
        </div>
        
        <button onclick="submitEssay()" class="w-full bg-teal-500 text-white py-2 rounded hover:bg-teal-600">
            提交评分
        </button>
        
        <div id="result" class="mt-6 hidden">
            <div class="text-center text-4xl font-bold text-teal-600 mb-2" id="score"></div>
            <div id="feedback" class="text-sm text-gray-600"></div>
        </div>
    </div>

    <script>
        const API_BASE = "https://ielts-ai-grader.vercel.app";
        
        async function submitEssay() {
            const essay = document.getElementById('essay').value;
            const prompt = document.getElementById('prompt').value;
            
            if (essay.split(/\\s+/).length < 250) {
                alert('字数不足250词');
                return;
            }
            
            document.querySelector('button').textContent = '评分中...';
            
            try {
                const res = await fetch(`${API_BASE}/api/grade_writing`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({essay, task_type: 'task2', prompt, target_band: 7.0})
                });
                
                const data = await res.json();
                document.getElementById('score').textContent = data.overall_band;
                document.getElementById('feedback').innerHTML = 
                    `<strong>TR:</strong> ${data.breakdown.TR.score} | 
                     <strong>CC:</strong> ${data.breakdown.CC.score} | 
                     <strong>LR:</strong> ${data.breakdown.LR.score} | 
                     <strong>GRA:</strong> ${data.breakdown.GRA.score}<br>
                     ${data.detailed_feedback.weaknesses.map(w => `• ${w}`).join('<br>')}`;
                document.getElementById('result').classList.remove('hidden');
                
            } catch(e) {
                alert('评分失败，请重试');
            }
            
            document.querySelector('button').textContent = '提交评分';
        }
    </script>
</body>
</html>"""

# API 路由保持不变
class WritingRequest(BaseModel):
    essay: str
    task_type: Literal["task1", "task2"]
    prompt: str
    target_band: float = 7.0

@app.post("/api/grade_writing")
async def grade_writing(data: WritingRequest):
    import openai
    import json
    
    # 模拟数据模式（测试用，确认流程走通）
    return {
        "overall_band": 6.5,
        "breakdown": {
            "TR": {"score": 6.5, "comments": "Task response adequate"},
            "CC": {"score": 6.5, "comments": "Good cohesion"},
            "LR": {"score": 6.0, "comments": "Vocabulary range acceptable"},
            "GRA": {"score": 6.5, "comments": "Grammar generally accurate"}
        },
        "detailed_feedback": {
            "strengths": ["Clear structure", "Good topic sentences"],
            "weaknesses": ["Need more complex sentences", "Expand vocabulary for band 7"],
            "vocabulary_suggestions": []
        },
        "word_count": len(data.essay.split()),
        "provider": "test_mode",
        "cost_usd": 0
    }

from mangum import Mangum
handler = Mangum(app)
