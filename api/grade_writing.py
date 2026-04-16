from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal
import openai
import json
import os
import hashlib
import time

app = FastAPI()

# DeepSeek API配置（从环境变量读取）
CLIENTS = {
    "deepseek": openai.OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        base_url="https://api.deepseek.com/v1"
    ),
    "openai": openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "")
    )
}

CACHE = {}

# 完整学习网站HTML（内嵌，避免文件路径问题）
HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IELTS Zenith | 雅思自主学习空间</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=Space+Grotesk:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary: #2D3436;
            --accent: #00B894;
            --accent-warm: #E17055;
            --paper: #FAFAFA;
            --ink: #2D3436;
        }
        
        body {
            font-family: 'Space Grotesk', sans-serif;
            background-color: #F7F5F3;
            background-image: 
                radial-gradient(at 0% 0%, rgba(0,184,148,0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(225,112,85,0.08) 0px, transparent 50%);
            color: var(--ink);
            overflow-x: hidden;
        }
        
        .serif {
            font-family: 'Playfair Display', serif;
        }
        
        .glass {
            background: rgba(255, 255, 255, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        .hover-lift {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .hover-lift:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px -15px rgba(0,0,0,0.1);
        }
        
        .section-hidden { display: none; }
        
        .loader {
            border: 3px solid #f3f3f3;
            border-radius: 50%;
            border-top: 3px solid var(--accent);
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-slide-in { animation: slideIn 0.6s ease-out forwards; }
    </style>
</head>
<body class="antialiased">

    <!-- API配置 -->
    <script>
        const API_BASE = window.location.origin + "/api";
    </script>

    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 glass border-b border-gray-200/50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center space-x-3 cursor-pointer" onclick="showSection('dashboard')">
                    <div class="w-8 h-8 bg-gradient-to-br from-teal-400 to-teal-600 rounded-lg flex items-center justify-center text-white font-bold text-lg">Z</div>
                    <span class="serif text-xl font-bold text-gray-800 tracking-tight">Zenith IELTS</span>
                </div>
                
                <div class="hidden md:flex space-x-1">
                    <button onclick="showSection('dashboard')" class="px-4 py-2 rounded-full text-sm font-medium transition-all hover:bg-gray-100 text-gray-700">仪表盘</button>
                    <button onclick="showSection('writing')" class="px-4 py-2 rounded-full text-sm font-medium transition-all hover:bg-gray-100 text-gray-700">写作</button>
                    <button onclick="showSection('vocabulary')" class="px-4 py-2 rounded-full text-sm font-medium transition-all hover:bg-gray-100 text-gray-700">词汇</button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="pt-20 pb-12 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">

        <!-- DASHBOARD SECTION -->
        <section id="dashboard" class="section animate-slide-in">
            <div class="mb-8">
                <h1 class="serif text-4xl md:text-5xl font-bold text-gray-900 mb-2">欢迎回来，学习者</h1>
                <p class="text-gray-600 text-lg">今天是雅思冲刺的第 <span class="font-semibold text-teal-600">1</span> 天，保持节奏。</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div class="glass rounded-2xl p-6 hover-lift border border-white/50">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-sm font-medium text-gray-500">总学习时长</span>
                        <div class="p-2 bg-teal-50 rounded-lg">
                            <svg class="w-5 h-5 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        </div>
                    </div>
                    <div class="text-3xl font-bold text-gray-900">0<span class="text-lg text-gray-500 font-normal">小时</span></div>
                    <div class="mt-2 text-sm text-teal-600">开始你的学习之旅</div>
                </div>

                <div class="glass rounded-2xl p-6 hover-lift border border-white/50">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-sm font-medium text-gray-500">模考均分</span>
                        <div class="p-2 bg-blue-50 rounded-lg">
                            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
                        </div>
                    </div>
                    <div class="text-3xl font-bold text-gray-900">-<span class="text-lg text-gray-500 font-normal">分</span></div>
                    <div class="mt-2 text-sm text-blue-600">完成一次写作评分</div>
                </div>

                <div class="glass rounded-2xl p-6 hover-lift border border-white/50 cursor-pointer" onclick="showSection('writing')">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-sm font-medium text-gray-500">AI写作评分</span>
                        <div class="p-2 bg-orange-50 rounded-lg">
                            <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                        </div>
                    </div>
                    <div class="text-lg font-bold text-gray-900">点击开始</div>
                    <div class="mt-2 text-sm text-orange-600">基于DeepSeek AI</div>
                </div>

                <div class="glass rounded-2xl p-6 hover-lift border border-white/50 cursor-pointer" onclick="showSection('vocabulary')">
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-sm font-medium text-gray-500">词汇库</span>
                        <div class="p-2 bg-purple-50 rounded-lg">
                            <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"/></svg>
                        </div>
                    </div>
                    <div class="text-lg font-bold text-gray-900">开始学习</div>
                    <div class="mt-2 text-sm text-purple-600">AWL词汇表</div>
                </div>
            </div>

            <div class="glass rounded-2xl p-6 border border-white/50 bg-gradient-to-br from-teal-50/50 to-transparent">
                <h3 class="font-bold text-gray-900 mb-2">🚀 快速开始</h3>
                <p class="text-gray-600 mb-4">你是第一次使用，建议先尝试AI写作评分功能，体验雅思作文智能批改。</p>
                <button onclick="showSection('writing')" class="px-6 py-3 bg-teal-500 text-white rounded-xl hover:bg-teal-600 transition-all">
                    立即体验写作评分 →
                </button>
            </div>
        </section>

        <!-- WRITING SECTION -->
        <section id="writing" class="section section-hidden">
            <div class="mb-8">
                <h2 class="serif text-4xl font-bold text-gray-900 mb-2">AI写作精批</h2>
                <p class="text-gray-600">基于DeepSeek/GPT-4，按官方四项标准评分 • 约¥0.02/篇</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-5 gap-6">
                <div class="lg:col-span-3 space-y-6">
                    <div class="glass rounded-2xl p-6 border border-white/50">
                        <div class="flex items-center justify-between mb-4">
                            <span id="taskBadge" class="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-xs font-semibold">Task 2</span>
                            <div class="flex space-x-2">
                                <button onclick="switchTask('task1')" class="text-xs px-3 py-1 rounded-full border hover:bg-gray-50">Task 1</button>
                                <button onclick="switchTask('task2')" class="text-xs px-3 py-1 rounded-full bg-gray-900 text-white">Task 2</button>
                            </div>
                        </div>
                        
                        <div id="promptBox" class="p-4 bg-gradient-to-br from-teal-50 to-orange-50 rounded-xl border border-teal-100 mb-4">
                            <p class="text-gray-800 font-medium leading-relaxed">
                                Some people think that the best way to reduce crime is to give longer prison sentences. Others believe there are better ways to reduce crime. Discuss both views and give your opinion.
                            </p>
                        </div>

                        <div class="mb-4 flex items-center justify-between">
                            <span class="text-sm text-gray-500">字数：<span id="wordCount" class="font-bold text-gray-900">0</span></span>
                            <span class="text-sm text-gray-500">目标：<span id="targetWord">250</span>词</span>
                        </div>

                        <textarea id="essayInput" 
                            class="w-full h-64 p-4 border border-gray-300 rounded-xl bg-white/80 resize-none focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all"
                            placeholder="在此输入你的作文...至少250词"
                            oninput="updateWordCount()"></textarea>

                        <div class="mt-4 flex justify-between items-center">
                            <div class="text-xs text-gray-400">AI评分约需5秒</div>
                            <button onclick="submitEssay()" id="submitBtn" class="px-8 py-3 bg-gray-900 text-white rounded-full hover:bg-gray-800 transition-all flex items-center space-x-2">
                                <span id="btnText">提交AI评分</span>
                                <div id="btnLoader" class="loader hidden" style="width: 16px; height: 16px; border-width: 2px;"></div>
                            </button>
                        </div>
                    </div>

                    <!-- Result Area -->
                    <div id="resultArea" class="hidden glass rounded-2xl p-6 border border-white/50">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="serif text-2xl font-bold">AI评分报告</h3>
                            <div class="text-4xl font-bold text-teal-600" id="overallScore">-</div>
                        </div>
                        
                        <div class="grid grid-cols-2 gap-4 mb-6">
                            <div class="p-4 bg-gray-50 rounded-xl">
                                <div class="flex justify-between mb-2">
                                    <span class="font-bold text-sm">TR (任务回应)</span>
                                    <span class="text-teal-600 font-bold" id="trScore">-</span>
                                </div>
                                <p class="text-xs text-gray-600" id="trComment">-</p>
                            </div>
                            <div class="p-4 bg-gray-50 rounded-xl">
                                <div class="flex justify-between mb-2">
                                    <span class="font-bold text-sm">CC (连贯衔接)</span>
                                    <span class="text-teal-600 font-bold" id="ccScore">-</span>
                                </div>
                                <p class="text-xs text-gray-600" id="ccComment">-</p>
                            </div>
                            <div class="p-4 bg-gray-50 rounded-xl">
                                <div class="flex justify-between mb-2">
                                    <span class="font-bold text-sm">LR (词汇资源)</span>
                                    <span class="text-teal-600 font-bold" id="lrScore">-</span>
                                </div>
                                <p class="text-xs text-gray-600" id="lrComment">-</p>
                            </div>
                            <div class="p-4 bg-gray-50 rounded-xl">
                                <div class="flex justify-between mb-2">
                                    <span class="font-bold text-sm">GRA (语法)</span>
                                    <span class="text-teal-600 font-bold" id="graScore">-</span>
                                </div>
                                <p class="text-xs text-gray-600" id="graComment">-</p>
                            </div>
                        </div>

                        <div class="bg-gray-900 text-white rounded-xl p-4">
                            <h4 class="font-bold mb-2">改进建议</h4>
                            <ul id="suggestions" class="text-sm space-y-1"></ul>
                        </div>
                    </div>
                </div>

                <div class="lg:col-span-2">
                    <div class="glass rounded-2xl p-6 border border-white/50">
                        <h4 class="font-bold text-gray-900 mb-4">评分标准说明</h4>
                        <div class="space-y-3 text-sm text-gray-600">
                            <div>
                                <strong class="text-gray-900">TR (Task Response):</strong> 扣题程度、论点发展
                            </div>
                            <div>
                                <strong class="text-gray-900">CC (Coherence):</strong> 逻辑连贯、段落结构
                            </div>
                            <div>
                                <strong class="text-gray-900">LR (Lexical):</strong> 词汇多样性、学术表达
                            </div>
                            <div>
                                <strong class="text-gray-900">GRA (Grammar):</strong> 句式复杂度、语法准确性
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- VOCABULARY SECTION -->
        <section id="vocabulary" class="section section-hidden">
            <div class="mb-8">
                <h2 class="serif text-4xl font-bold text-gray-900 mb-2">词汇库</h2>
                <p class="text-gray-600">Academic Word List 学术词汇</p>
            </div>

            <div class="max-w-2xl mx-auto">
                <div class="glass rounded-2xl p-8 border border-white/50 text-center cursor-pointer hover:shadow-lg transition-all" onclick="flipCard()">
                    <div id="cardFront">
                        <div class="text-sm text-teal-600 mb-4">Academic Word List</div>
                        <h3 class="serif text-5xl font-bold text-gray-900 mb-4">ambiguous</h3>
                        <div class="text-gray-400">点击查看释义</div>
                    </div>
                    <div id="cardBack" class="hidden">
                        <div class="text-2xl font-medium mb-4">模棱两可的；含糊不清的</div>
                        <div class="text-gray-600 italic mb-4">"The instructions were ambiguous."</div>
                        <div class="flex justify-center space-x-4">
                            <button onclick="event.stopPropagation(); nextWord()" class="px-6 py-2 bg-teal-500 text-white rounded-full">认识</button>
                            <button onclick="event.stopPropagation(); nextWord()" class="px-6 py-2 bg-red-500 text-white rounded-full">不认识</button>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <script>
        let currentTask = 'task2';
        const words = ['ambiguous', 'controversial', 'empirical', 'hypothesis', 'significant'];
        let currentWord = 0;

        function showSection(id) {
            document.querySelectorAll('.section').forEach(s => {
                s.classList.add('section-hidden');
                s.classList.remove('animate-slide-in');
            });
            const target = document.getElementById(id);
            target.classList.remove('section-hidden');
            target.classList.add('animate-slide-in');
        }

        function switchTask(task) {
            currentTask = task;
            const prompt = task === 'task1' 
                ? "The graph shows internet access in three countries (1998-2008). Summarize the information."
                : "Some people think that the best way to reduce crime is to give longer prison sentences...";
            document.getElementById('promptBox').innerHTML = `<p class="text-gray-800 font-medium">${prompt}</p>`;
            document.getElementById('taskBadge').textContent = task === 'task1' ? 'Task 1' : 'Task 2';
            document.getElementById('targetWord').textContent = task === 'task1' ? '150' : '250';
        }

        function updateWordCount() {
            const text = document.getElementById('essayInput').value;
            const count = text.trim() ? text.trim().split(/\\s+/).length : 0;
            document.getElementById('wordCount').textContent = count;
            const target = currentTask === 'task1' ? 150 : 250;
            if (count >= target) {
                document.getElementById('wordCount').classList.add('text-teal-600');
            } else {
                document.getElementById('wordCount').classList.remove('text-teal-600');
            }
        }

        async function submitEssay() {
            const essay = document.getElementById('essayInput').value;
            const wordCount = essay.trim() ? essay.trim().split(/\\s+/).length : 0;
            const target = currentTask === 'task1' ? 150 : 250;
            
            if (wordCount < target) {
                alert(`字数不足，需要至少 ${target} 词`);
                return;
            }

            const btn = document.getElementById('submitBtn');
            const btnText = document.getElementById('btnText');
            const loader = document.getElementById('btnLoader');
            
            btn.disabled = true;
            btnText.textContent = 'AI评分中...';
            loader.classList.remove('hidden');

            try {
                const response = await fetch(`${API_BASE}/grade_writing`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        essay: essay,
                        task_type: currentTask,
                        prompt: document.getElementById('promptBox').innerText,
                        target_band: 7.0
                    })
                });
                
                const result = await response.json();
                displayResult(result);
                
            } catch (error) {
                alert('评分服务暂时繁忙，请稍后重试');
            } finally {
                btn.disabled = false;
                btnText.textContent = '提交AI评分';
                loader.classList.add('hidden');
            }
        }

        function displayResult(data) {
            document.getElementById('resultArea').classList.remove('hidden');
            document.getElementById('overallScore').textContent = data.overall_band;
            document.getElementById('trScore').textContent = data.breakdown.TR.score;
            document.getElementById('trComment').textContent = data.breakdown.TR.comments;
            document.getElementById('ccScore').textContent = data.breakdown.CC.score;
            document.getElementById('ccComment').textContent = data.breakdown.CC.comments;
            document.getElementById('lrScore').textContent = data.breakdown.LR.score;
            document.getElementById('lrComment').textContent = data.breakdown.LR.comments;
            document.getElementById('graScore').textContent = data.breakdown.GRA.score;
            document.getElementById('graComment').textContent = data.breakdown.GRA.comments;
            
            const suggestions = document.getElementById('suggestions');
            suggestions.innerHTML = '';
            data.detailed_feedback.weaknesses.forEach(w => {
                suggestions.innerHTML += `<li>• ${w}</li>`;
            });
        }

        function flipCard() {
            const front = document.getElementById('cardFront');
            const back = document.getElementById('cardBack');
            if (front.classList.contains('hidden')) {
                front.classList.remove('hidden');
                back.classList.add('hidden');
            } else {
                front.classList.add('hidden');
                back.classList.remove('hidden');
            }
        }

        function nextWord() {
            currentWord = (currentWord + 1) % words.length;
            document.querySelector('#cardFront h3').textContent = words[currentWord];
            document.getElementById('cardFront').classList.remove('hidden');
            document.getElementById('cardBack').classList.add('hidden');
        }
    </script>
</body>
</html>"""

# 首页路由 - 直接返回完整学习网站
@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_CONTENT

@app.get("/api")
def api_root():
    return {"status": "ok", "api": "IELTS AI Grader"}

# 数据模型
class WritingRequest(BaseModel):
    essay: str
    task_type: Literal["task1", "task2"]
    prompt: str
    target_band: float = 7.0

def get_cache_key(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

# AI评分路由
@app.post("/api/grade_writing")
async def grade_writing(data: WritingRequest):
    start_time = time.time()
    
    # 字数检查
    word_count = len(data.essay.split())
    min_words = 150 if data.task_type == "task1" else 250
    
    if word_count < min_words:
        raise HTTPException(status_code=400, detail=f"字数不足，需要至少{min_words}词")

    # 如果环境变量没设置，返回模拟数据（避免报错）
    if not os.getenv("DEEPSEEK_API_KEY"):
        return {
            "overall_band": 6.5,
            "breakdown": {
                "TR": {"score": 6.5, "comments": "Task response adequate, covers both views"},
                "CC": {"score": 6.5, "comments": "Clear paragraphing, good cohesion"},
                "LR": {"score": 6.0, "comments": "Adequate vocabulary, some repetition"},
                "GRA": {"score": 6.5, "comments": "Mix of simple and complex sentences"}
            },
            "detailed_feedback": {
                "strengths": ["Clear structure", "Both views discussed"],
                "weaknesses": ["Use more academic vocabulary", "Add more specific examples", "Vary sentence structures for band 7"],
                "vocabulary_suggestions": []
            },
            "word_count": word_count,
            "provider": "demo_mode",
            "processing_time": round(time.time() - start_time, 2),
            "cost_usd": 0
        }

    # 调用DeepSeek
    system_prompt = """你是资深雅思考官，按官方四项标准评分。
输出JSON格式：
{
  "overall_band": float,
  "breakdown": {
    "TR": {"score": float, "comments": "string"},
    "CC": {"score": float, "comments": "string"},
    "LR": {"score": float, "comments": "string"},
    "GRA": {"score": float, "comments": "string"}
  },
  "detailed_feedback": {
    "strengths": ["string"],
    "weaknesses": ["string"]
  }
}"""

    user_prompt = f"""题目：{data.prompt}
作文（{word_count}词）：{data.essay}
请评分并给出提升到{data.target_band}分的建议。"""

    try:
        client = CLIENTS["deepseek"]
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=2000
        )
        
        result = json.loads(response.choices[0].message.content)
        result["word_count"] = word_count
        result["processing_time"] = round(time.time() - start_time, 2)
        result["provider"] = "deepseek"
        result["cost_usd"] = round(response.usage.total_tokens * 0.000001, 5)
        return result
        
    except Exception as e:
        return {
            "overall_band": 6.0,
            "breakdown": {
                "TR": {"score": 6.0, "comments": f"Error: {str(e)[:50]}"},
                "CC": {"score": 6.0, "comments": "Service temporarily unavailable"},
                "LR": {"score": 6.0, "comments": "Using fallback mode"},
                "GRA": {"score": 6.0, "comments": "Please try again later"}
            },
            "detailed_feedback": {
                "strengths": ["Essay submitted"],
                "weaknesses": ["AI service error, using default score"]
            },
            "word_count": word_count,
            "error": str(e)
        }

# Vercel handler
from mangum import Mangum
handler = Mangum(app)
