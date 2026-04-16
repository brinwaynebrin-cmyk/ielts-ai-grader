from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Literal, List, Optional
import os
import random
import json
import pathlib

app = FastAPI()

# ============ 数据文件路径处理 ============
# 获取当前文件所在目录（适配 Vercel 和本地）
CURRENT_DIR = pathlib.Path(__file__).parent
DATA_DIR = CURRENT_DIR.parent / "data"

def load_json_file(filepath: str):
    """安全加载 JSON 文件"""
    try:
        full_path = DATA_DIR / filepath
        if not full_path.exists():
            print(f"File not found: {full_path}")
            return None
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

# ============ 原有功能：写作评分 ============
class WritingRequest(BaseModel):
    essay: str
    task_type: Literal["task1", "task2"]
    prompt: str
    target_band: float = 7.0

class SpeakingRequest(BaseModel):
    transcript: str
    part: str = "2"

@app.post("/api/grade_writing")
async def grade_writing(data: WritingRequest):
    word_count = len(data.essay.split())
    min_words = 130 if data.task_type == "task1" else 220
    
    if word_count < min_words:
        return {
            "error": f"字数不足：当前{word_count}词，建议至少{min_words}词",
            "word_count": word_count,
            "overall_band": 0
        }

    # 模拟评分逻辑（实际应接入 AI）
    base_score = 6.0
    if word_count > min_words + 20: base_score = 6.5
    if word_count > min_words + 50: base_score = 7.0
    
    return {
        "overall_band": round(base_score, 1),
        "breakdown": {
            "TR": {"score": round(base_score, 1), "comments": "Task response adequate"},
            "CC": {"score": round(base_score, 1), "comments": "Logical organization"},
            "LR": {"score": round(base_score - 0.5, 1), "comments": "Good vocabulary range"},
            "GRA": {"score": round(base_score, 1), "comments": "Complex structures used"}
        },
        "detailed_feedback": {
            "weaknesses": [
                f"字数刚好达标（{word_count}词），建议写到{min_words + 50}词以上更保险",
                "可增加更多具体例子支撑论点",
                "注意使用更学术的词汇替换口语化表达"
            ]
        },
        "word_count": word_count,
        "mode": "simulated"
    }

@app.post("/api/grade_speaking")
async def grade_speaking(data: SpeakingRequest):
    word_count = len(data.transcript.split())
    if word_count < 30:
        return {"error": "回答太短，无法评分"}
    
    return {
        "overall_band": 6.5,
        "breakdown": {
            "fluency": {"score": 6.5, "comments": "Good flow, some hesitation"},
            "lexical": {"score": 6.5, "comments": "Adequate vocabulary"},
            "grammar": {"score": 6.0, "comments": "Some grammatical errors"},
            "pronunciation": {"score": 7.0, "comments": "Inferred from text clarity"}
        },
        "suggestions": [
            "使用更多连接词（however, furthermore）",
            "增加具体细节和例子",
            "避免重复用词，使用同义词替换"
        ],
        "word_count": word_count
    }

# ============ 新增：词汇 API ============

@app.get("/api/vocab/{band}")
async def get_vocabulary(
    band: str, 
    page: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None
):
    """获取分级词汇（支持9000+词汇分页加载）"""
    data = load_json_file(f"vocab/{band}.json")
    if not data:
        raise HTTPException(status_code=404, detail=f"词汇库 {band} 不存在")
    
    words = data.get("words", [])
    
    # 搜索过滤
    if search:
        search_lower = search.lower()
        words = [
            w for w in words 
            if search_lower in w["word"].lower() 
            or search_lower in w.get("meaning", "")
            or search_lower in w.get("en_meaning", "").lower()
        ]
    
    # 分页处理
    total = len(words)
    start = page * limit
    end = min(start + limit, total)
    
    return {
        "metadata": {
            "band": band,
            "total": total,
            "page": page,
            "limit": limit,
            "has_more": end < total
        },
        "words": words[start:end]
    }

@app.get("/api/vocab/search")
async def search_vocabulary(q: str = Query(..., min_length=1), limit: int = 20):
    """全局搜索所有词汇库"""
    results = []
    bands = ["academic", "band6", "band7", "band8"]
    
    for band in bands:
        data = load_json_file(f"vocab/{band}.json")
        if data:
            for word in data.get("words", []):
                if q.lower() in word["word"].lower() or q in word.get("meaning", ""):
                    results.append({**word, "source": band})
                    if len(results) >= limit:
                        break
        if len(results) >= limit:
            break
    
    return {
        "query": q,
        "total": len(results),
        "results": results
    }

@app.get("/api/game/words")
async def get_game_words(
    count: int = Query(10, ge=5, le=20),
    difficulty: str = Query("mixed", regex="^(easy|normal|hard|mixed)$")
):
    """为游戏随机抽取词汇（支持9000+词库）"""
    sources = {
        "easy": ["band6"],
        "normal": ["academic", "band7"],
        "hard": ["band8"],
        "mixed": ["academic", "band6", "band7"]
    }
    
    all_words = []
    for src in sources.get(difficulty, ["band7"]):
        data = load_json_file(f"vocab/{src}.json")
        if data:
            all_words.extend(data.get("words", []))
    
    if not all_words:
        raise HTTPException(status_code=500, detail="词汇库为空")
    
    # 随机抽取
    selected = random.sample(all_words, min(count, len(all_words)))
    
    # 生成干扰项
    game_words = []
    for word in selected:
        distractors = []
        others = [w for w in all_words if w["word"] != word["word"]]
        if len(others) >= 3:
            distractors = random.sample(others, 3)
        
        game_words.append({
            "word": word["word"],
            "phonetic": word.get("phonetic", ""),
            "meaning": word["meaning"],
            "distractors": [d["meaning"] for d in distractors]
        })
    
    return {
        "total": len(game_words),
        "difficulty": difficulty,
        "words": game_words
    }

@app.get("/api/speaking/{scenario}")
async def get_speaking_scenario(scenario: str):
    """获取口语情景化数据"""
    data = load_json_file(f"speaking/{scenario}.json")
    if not data:
        raise HTTPException(status_code=404, detail="情景不存在")
    return data

# ============ 前端页面（内嵌） ============

HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IELTS Zenith - 雅思AI学习平台</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans SC', sans-serif; background: #f5f5f0; }
        .glass { background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); }
        .nav-active { background: #0d9488; color: white; }
        .hidden-section { display: none; }
        .fade-in { animation: fadeIn 0.4s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .loading { display: inline-block; width: 20px; height: 20px; border: 3px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: white; animation: spin 1s ease-in-out infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        /* 游戏样式 */
        .falling-word {
            position: absolute;
            padding: 12px 24px;
            background: rgba(255,255,255,0.95);
            border: 2px solid #3b82f6;
            border-radius: 16px;
            color: #1e3a8a;
            font-weight: bold;
            font-size: 18px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10;
        }
        .falling-word.danger {
            border-color: #ef4444;
            animation: pulse 1s infinite;
        }
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
            50% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        }
        .shoot-btn {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            border: 2px solid #60a5fa;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
            transition: all 0.2s;
        }
        .shoot-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(59, 130, 246, 0.6); }
        .shoot-btn:active { transform: scale(0.95); }
        .shoot-btn.correct {
            background: linear-gradient(135deg, #10b981, #059669);
            border-color: #34d399;
            animation: correct-pulse 0.3s;
        }
        .shoot-btn.wrong {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            border-color: #f87171;
            animation: shake 0.5s;
        }
        @keyframes correct-pulse {
            0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            50% { box-shadow: 0 0 20px 10px rgba(16, 185, 129, 0.3); }
            100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
    </style>
</head>
<body class="antialiased text-gray-800">

    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 glass border-b border-gray-200 shadow-sm">
        <div class="max-w-6xl mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-2 cursor-pointer" onclick="showSection('dashboard')">
                    <div class="w-8 h-8 bg-teal-600 rounded-lg flex items-center justify-center text-white font-bold text-lg">Z</div>
                    <span class="text-xl font-bold text-gray-900">Zenith IELTS</span>
                </div>
                
                <div class="hidden md:flex space-x-1 text-sm">
                    <button onclick="showSection('dashboard')" id="nav-dashboard" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">仪表盘</button>
                    <button onclick="showSection('vocabulary')" id="nav-vocabulary" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">词汇库</button>
                    <button onclick="showSection('wordgame')" id="nav-wordgame" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100 text-pink-600 font-bold">🎮 游戏</button>
                    <button onclick="showSection('writing')" id="nav-writing" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">写作</button>
                    <button onclick="showSection('speaking')" id="nav-speaking" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">口语</button>
                </div>
            </div>
        </div>
    </nav>

    <main class="pt-20 pb-12 px-4 max-w-6xl mx-auto">

        <!-- DASHBOARD -->
        <section id="dashboard" class="section fade-in">
            <div class="mb-8">
                <h1 class="text-3xl font-bold text-gray-900 mb-2">雅思AI学习平台</h1>
                <p class="text-gray-600">支持9000+词汇库 | 情景化口语训练 | AI智能评分</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div class="glass rounded-2xl p-5 shadow-sm border-l-4 border-teal-500 cursor-pointer hover:shadow-md transition-all" onclick="showSection('vocabulary')">
                    <div class="text-3xl mb-2">📚</div>
                    <div class="font-bold text-gray-900">分级词汇库</div>
                    <div class="text-xs text-gray-500 mt-1">Band 6/7/8 分级学习</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm border-l-4 border-pink-500 cursor-pointer hover:shadow-md transition-all" onclick="showSection('wordgame')">
                    <div class="text-3xl mb-2">🎮</div>
                    <div class="font-bold text-gray-900">词汇守卫战</div>
                    <div class="text-xs text-gray-500 mt-1">弹幕射击背单词</div>
                    <div class="mt-2 text-xs text-pink-600">最高连击 x5</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm border-l-4 border-blue-500 cursor-pointer hover:shadow-md transition-all" onclick="showSection('writing')">
                    <div class="text-3xl mb-2">📝</div>
                    <div class="font-bold text-gray-900">AI写作精批</div>
                    <div class="text-xs text-gray-500 mt-1">Task 1 & 2 智能评分</div>
                </div>
            </div>
        </section>

        <!-- VOCABULARY SECTION -->
        <section id="vocabulary" class="section hidden-section fade-in">
            <div class="mb-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                    <h2 class="text-2xl font-bold text-gray-900">雅思分级词汇库</h2>
                    <p class="text-sm text-gray-500">共收录 9,000+ 真题高频词汇</p>
                </div>
                <div class="flex gap-2 w-full md:w-auto">
                    <div class="relative flex-1 md:w-64">
                        <input type="text" id="vocabSearch" placeholder="搜索单词、释义..." 
                            class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-full focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none text-sm"
                            onkeyup="if(event.key==='Enter') searchVocab()">
                        <svg class="w-5 h-5 text-gray-400 absolute left-3 top-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                        </svg>
                    </div>
                    <button onclick="searchVocab()" class="px-4 py-2 bg-teal-600 text-white rounded-full text-sm font-medium hover:bg-teal-700 whitespace-nowrap">搜索</button>
                </div>
            </div>

            <div class="flex flex-wrap gap-2 mb-6">
                <button onclick="loadVocab('academic')" class="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium hover:bg-purple-200 transition-all">AWL学术570词</button>
                <button onclick="loadVocab('band6')" class="px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm font-medium hover:bg-green-200 transition-all">Band 6.0-6.5</button>
                <button onclick="loadVocab('band7')" class="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium hover:bg-blue-200 transition-all">Band 7.0-7.5</button>
                <button onclick="loadVocab('band8')" class="px-4 py-2 bg-orange-100 text-orange-700 rounded-full text-sm font-medium hover:bg-orange-200 transition-all">Band 8.0+</button>
            </div>

            <div id="vocabList" class="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                <div class="text-center py-12 text-gray-400">点击上方按钮加载词汇</div>
            </div>
            
            <div class="mt-4 text-center">
                <button onclick="loadMore()" id="loadMoreBtn" class="hidden px-6 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full text-sm font-medium transition-all">加载更多</button>
            </div>
        </section>

        <!-- GAME SECTION -->
        <section id="wordgame" class="section hidden-section fade-in">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h2 class="text-2xl font-bold text-gray-900">🎮 词汇守卫战</h2>
                    <p class="text-sm text-gray-500">在单词落地前选择正确释义消灭它们！</p>
                </div>
                <div class="flex gap-2">
                    <select id="gameDiff" class="px-3 py-2 border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-pink-500 outline-none">
                        <option value="easy">简单模式</option>
                        <option value="normal" selected>普通模式</option>
                        <option value="hard">困难模式</option>
                        <option value="mixed">混合挑战</option>
                    </select>
                    <button onclick="startGame()" id="startBtn" class="px-6 py-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-full font-bold hover:shadow-lg transition-all">开始游戏</button>
                </div>
            </div>

            <div class="grid grid-cols-4 gap-3 mb-4">
                <div class="glass rounded-xl p-3 text-center border-l-4 border-yellow-400">
                    <div class="text-xs text-gray-500 mb-1">得分</div>
                    <div class="text-2xl font-bold text-gray-900 game-font" id="score">0</div>
                </div>
                <div class="glass rounded-xl p-3 text-center border-l-4 border-orange-400">
                    <div class="text-xs text-gray-500 mb-1">连击</div>
                    <div class="text-2xl font-bold text-orange-600" id="combo">x0</div>
                </div>
                <div class="glass rounded-xl p-3 text-center border-l-4 border-blue-400">
                    <div class="text-xs text-gray-500 mb-1">剩余时间</div>
                    <div class="text-2xl font-bold text-blue-600" id="time">60</div>
                </div>
                <div class="glass rounded-xl p-3 text-center border-l-4 border-green-400">
                    <div class="text-xs text-gray-500 mb-1">护盾</div>
                    <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                        <div id="healthBar" class="h-full bg-gradient-to-r from-green-500 to-green-400 rounded-full transition-all duration-300" style="width: 100%"></div>
                    </div>
                </div>
            </div>

            <div id="gameArea" class="relative bg-gradient-to-b from-indigo-900 via-purple-900 to-pink-900 rounded-2xl h-[400px] overflow-hidden mb-4 shadow-inner">
                <div id="gameLayer" class="absolute inset-0"></div>
                <div id="gameOverlay" class="absolute inset-0 flex items-center justify-center">
                    <div class="text-center text-white">
                        <div class="text-6xl mb-4">🎮</div>
                        <p class="text-lg opacity-90">点击"开始游戏"加载词汇</p>
                        <p class="text-sm opacity-60 mt-2">使用 A/S/D/F 或鼠标点击选择</p>
                    </div>
                </div>
            </div>

            <div id="shootControls" class="grid grid-cols-4 gap-3 opacity-50 pointer-events-none">
                <button onclick="shoot(0)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg relative group" id="btn0">
                    <span id="opt0">-</span>
                    <span class="absolute top-1 right-2 text-xs opacity-50">A</span>
                </button>
                <button onclick="shoot(1)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg relative group" id="btn1">
                    <span id="opt1">-</span>
                    <span class="absolute top-1 right-2 text-xs opacity-50">S</span>
                </button>
                <button onclick="shoot(2)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg relative group" id="btn2">
                    <span id="opt2">-</span>
                    <span class="absolute top-1 right-2 text-xs opacity-50">D</span>
                </button>
                <button onclick="shoot(3)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg relative group" id="btn3">
                    <span id="opt3">-</span>
                    <span class="absolute top-1 right-2 text-xs opacity-50">F</span>
                </button>
            </div>
        </section>

        <!-- WRITING SECTION -->
        <section id="writing" class="section hidden-section fade-in">
            <div class="mb-6">
                <h2 class="text-2xl font-bold text-gray-900">AI写作精批</h2>
                <p class="text-gray-600 text-sm">字数要求：Task 1 ≥130词，Task 2 ≥220词</p>
            </div>

            <div class="glass rounded-2xl p-6 shadow-sm">
                <div class="flex gap-2 mb-4">
                    <button onclick="setTask('task1')" id="btn-task1" class="px-4 py-2 rounded-full text-sm border hover:bg-gray-50 transition-all">Task 1</button>
                    <button onclick="setTask('task2')" id="btn-task2" class="px-4 py-2 rounded-full text-sm bg-teal-600 text-white shadow-md">Task 2</button>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg mb-4 text-sm text-gray-700" id="promptDisplay">
                    Some people think that the best way to reduce crime is to give longer prison sentences. Others believe there are better ways. Discuss both views.
                </div>

                <textarea id="essayInput" rows="12" class="w-full p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all text-sm" placeholder="在此输入作文..." oninput="updateWordCount()"></textarea>

                <div class="mt-4 flex items-center justify-between">
                    <span class="text-sm text-gray-500" id="wordCountDisplay">字数：0 / 220+</span>
                    <button onclick="submitEssay()" id="submitBtn" class="px-6 py-2 bg-teal-600 text-white rounded-full font-medium hover:bg-teal-700 transition-all flex items-center gap-2 shadow-md">
                        <span id="btnText">提交评分</span>
                        <span id="btnLoader" class="loading hidden"></span>
                    </button>
                </div>
            </div>

            <div id="resultArea" class="hidden mt-6 glass rounded-2xl p-6 shadow-sm border-l-4 border-teal-500">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-bold text-gray-900">评分结果</h3>
                    <div class="text-3xl font-bold text-teal-600" id="overallBand">-</div>
                </div>
                <div class="grid grid-cols-4 gap-3 mb-4">
                    <div class="p-3 bg-gray-50 rounded-lg text-center"><div class="text-xs text-gray-500 mb-1">TR</div><div class="font-bold text-teal-600 text-lg" id="trScore">-</div></div>
                    <div class="p-3 bg-gray-50 rounded-lg text-center"><div class="text-xs text-gray-500 mb-1">CC</div><div class="font-bold text-teal-600 text-lg" id="ccScore">-</div></div>
                    <div class="p-3 bg-gray-50 rounded-lg text-center"><div class="text-xs text-gray-500 mb-1">LR</div><div class="font-bold text-teal-600 text-lg" id="lrScore">-</div></div>
                    <div class="p-3 bg-gray-50 rounded-lg text-center"><div class="text-xs text-gray-500 mb-1">GRA</div><div class="font-bold text-teal-600 text-lg" id="graScore">-</div></div>
                </div>
                <div class="bg-gray-900 text-white rounded-xl p-4">
                    <div class="font-bold mb-2 text-teal-400">改进建议</div>
                    <ul id="suggestionsList" class="space-y-1 text-gray-300 text-sm"></ul>
                </div>
            </div>
        </section>

        <!-- SPEAKING SECTION -->
        <section id="speaking" class="section hidden-section fade-in">
            <div class="mb-6">
                <h2 class="text-2xl font-bold text-gray-900">口语Part 2评分</h2>
                <p class="text-gray-600 text-sm">输入你的Part 2回答文本，AI按流利度、词汇、语法、发音评估</p>
            </div>

            <div class="glass rounded-2xl p-6 shadow-sm">
                <div class="bg-purple-50 p-4 rounded-lg mb-4 border border-purple-100">
                    <h3 class="font-bold text-gray-900 mb-2">Describe a difficult decision you made.</h3>
                    <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside">
                        <li>What the decision was</li>
                        <li>When you made it</li>
                        <li>Why it was difficult</li>
                        <li>And explain how you felt after deciding</li>
                    </ul>
                </div>

                <textarea id="speakingInput" rows="8" class="w-full p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-sm" placeholder="在此输入你的Part 2回答（建议100-150词）..."></textarea>

                <button onclick="submitSpeaking()" id="speakBtn" class="mt-4 w-full py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-full font-medium hover:shadow-lg transition-all flex items-center justify-center gap-2">
                    <span id="speakBtnText">提交口语评分</span>
                    <span id="speakLoader" class="loading hidden"></span>
                </button>
            </div>

            <div id="speakingResult" class="hidden mt-6 glass rounded-2xl p-6 shadow-sm border-l-4 border-purple-500">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-bold text-gray-900">口语评分</h3>
                    <div class="text-3xl font-bold text-purple-600" id="speakOverall">-</div>
                </div>
                <div class="space-y-3 mb-4">
                    <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg"><span class="text-sm font-medium">流利度与连贯性</span><span class="font-bold text-purple-600" id="fluencyScore">-</span></div>
                    <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg"><span class="text-sm font-medium">词汇多样性</span><span class="font-bold text-purple-600" id="speakLrScore">-</span></div>
                    <div class="flex justify-between items-center p-3 bg-gray-50 rounded-lg"><span class="text-sm font-medium">语法范围</span><span class="font-bold text-purple-600" id="speakGrScore">-</span></div>
                </div>
                <div class="bg-purple-900 text-white rounded-xl p-4">
                    <div class="font-bold mb-2 text-purple-300">提升建议</div>
                    <ul id="speakSuggestions" class="space-y-1 text-purple-100 text-sm"></ul>
                </div>
            </div>
        </section>

    </main>

    <script>
        // ==================== 导航功能 ====================
        let currentSection = 'dashboard';
        let currentVocabBand = 'band7';
        let currentVocabPage = 0;
        let vocabCache = [];
        
        function showSection(sectionId) {
            document.querySelectorAll('.section').forEach(s => {
                s.classList.add('hidden-section');
                s.classList.remove('fade-in');
            });
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('nav-active'));
            
            const target = document.getElementById(sectionId);
            target.classList.remove('hidden-section');
            target.classList.add('fade-in');
            
            const navBtn = document.getElementById('nav-' + sectionId);
            if (navBtn) navBtn.classList.add('nav-active');
            
            currentSection = sectionId;
            
            // 初始化加载
            if (sectionId === 'vocabulary' && vocabCache.length === 0) {
                loadVocab('band7');
            }
        }

        // ==================== 词汇库功能 ====================
        async function loadVocab(band) {
            currentVocabBand = band;
            currentVocabPage = 0;
            vocabCache = [];
            
            const container = document.getElementById('vocabList');
            container.innerHTML = '<div class="text-center py-8"><div class="inline-block w-8 h-8 border-4 border-teal-600 border-t-transparent rounded-full animate-spin"></div><p class="text-sm text-gray-500 mt-2">加载中...</p></div>';
            document.getElementById('loadMoreBtn').classList.add('hidden');
            
            try {
                const res = await fetch(`/api/vocab/${band}?page=0&limit=20`);
                const data = await res.json();
                vocabCache = data.words;
                renderVocabList(data.words, data.metadata);
            } catch (e) {
                container.innerHTML = '<div class="text-center py-8 text-red-500">加载失败，请检查数据文件是否存在</div>';
            }
        }

        function renderVocabList(words, meta) {
            const container = document.getElementById('vocabList');
            
            if (words.length === 0) {
                container.innerHTML = '<div class="text-center py-8 text-gray-400">暂无词汇数据</div>';
                return;
            }
            
            const html = words.map(w => `
                <div class="glass rounded-xl p-4 shadow-sm hover:shadow-md transition-all cursor-pointer group" onclick="playAudio('${w.word}')">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white font-bold text-lg shadow-md group-hover:scale-110 transition-transform">
                                ${w.word.charAt(0).toUpperCase()}
                            </div>
                            <div>
                                <div class="flex items-center gap-2 flex-wrap">
                                    <span class="font-bold text-lg text-gray-900">${w.word}</span>
                                    <span class="text-sm text-gray-500 font-mono">${w.phonetic || ''}</span>
                                    <span class="px-2 py-0.5 bg-orange-100 text-orange-700 rounded text-xs font-medium">Band ${w.band}</span>
                                    ${meta.band === 'academic' ? '<span class="px-2 py-0.5 bg-purple-100 text-purple-700 rounded text-xs">AWL</span>' : ''}
                                </div>
                                <div class="text-gray-700 font-medium">${w.meaning}</div>
                                ${w.examples && w.examples[0] ? `<div class="text-sm text-gray-500 mt-1 italic">"${w.examples[0]}"</div>` : ''}
                            </div>
                        </div>
                        <button onclick="event.stopPropagation(); playAudio('${w.word}')" class="p-3 hover:bg-teal-50 rounded-full transition-all text-xl" title="播放发音">
                            🔊
                        </button>
                    </div>
                </div>
            `).join('');
            
            container.innerHTML = html;
            
            if (meta.has_more) {
                document.getElementById('loadMoreBtn').classList.remove('hidden');
            } else {
                document.getElementById('loadMoreBtn').classList.add('hidden');
            }
        }

        async function loadMore() {
            currentVocabPage++;
            const btn = document.getElementById('loadMoreBtn');
            btn.textContent = '加载中...';
            btn.disabled = true;
            
            try {
                const res = await fetch(`/api/vocab/${currentVocabBand}?page=${currentVocabPage}&limit=20`);
                const data = await res.json();
                
                if (data.words.length > 0) {
                    vocabCache = [...vocabCache, ...data.words];
                    
                    // 追加而不是替换
                    const container = document.getElementById('vocabList');
                    const html = data.words.map(w => `
                        <div class="glass rounded-xl p-4 shadow-sm hover:shadow-md transition-all cursor-pointer group" onclick="playAudio('${w.word}')">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-4">
                                    <div class="w-12 h-12 rounded-full bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white font-bold text-lg shadow-md group-hover:scale-110 transition-transform">
                                        ${w.word.charAt(0).toUpperCase()}
                                    </div>
                                    <div>
                                        <div class="flex items-center gap-2 flex-wrap">
                                            <span class="font-bold text-lg text-gray-900">${w.word}</span>
                                            <span class="text-sm text-gray-500 font-mono">${w.phonetic || ''}</span>
                                            <span class="px-2 py-0.5 bg-orange-100 text-orange-700 rounded text-xs font-medium">Band ${w.band}</span>
                                        </div>
                                        <div class="text-gray-700 font-medium">${w.meaning}</div>
                                    </div>
                                </div>
                                <button onclick="event.stopPropagation(); playAudio('${w.word}')" class="p-3 hover:bg-teal-50 rounded-full transition-all text-xl">🔊</button>
                            </div>
                        </div>
                    `).join('');
                    container.insertAdjacentHTML('beforeend', html);
                }
                
                if (!data.metadata.has_more) {
                    btn.classList.add('hidden');
                } else {
                    btn.textContent = '加载更多';
                    btn.disabled = false;
                }
            } catch (e) {
                btn.textContent = '加载失败，重试';
                btn.disabled = false;
            }
        }

        async function searchVocab() {
            const q = document.getElementById('vocabSearch').value.trim();
            if (!q) {
                loadVocab('band7');
                return;
            }
            
            document.getElementById('vocabList').innerHTML = '<div class="text-center py-8"><div class="inline-block w-8 h-8 border-4 border-teal-600 border-t-transparent rounded-full animate-spin"></div><p class="text-sm text-gray-500 mt-2">搜索中...</p></div>';
            document.getElementById('loadMoreBtn').classList.add('hidden');
            
            try {
                const res = await fetch(`/api/vocab/search?q=${encodeURIComponent(q)}&limit=50`);
                const data = await res.json();
                
                if (data.results.length === 0) {
                    document.getElementById('vocabList').innerHTML = '<div class="text-center py-8 text-gray-400">未找到匹配词汇</div>';
                    return;
                }
                
                // 渲染搜索结果
                const container = document.getElementById('vocabList');
                const html = data.results.map(w => `
                    <div class="glass rounded-xl p-4 shadow-sm hover:shadow-md transition-all cursor-pointer group border-l-4 border-teal-400" onclick="playAudio('${w.word}')">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-4">
                                <div class="w-12 h-12 rounded-full bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white font-bold text-lg shadow-md">
                                    ${w.word.charAt(0).toUpperCase()}
                                </div>
                                <div>
                                    <div class="flex items-center gap-2 flex-wrap">
                                        <span class="font-bold text-lg text-gray-900">${w.word}</span>
                                        <span class="text-sm text-gray-500 font-mono">${w.phonetic || ''}</span>
                                        <span class="px-2 py-0.5 bg-orange-100 text-orange-700 rounded text-xs">Band ${w.band}</span>
                                        <span class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded text-xs text-capitalize">${w.source}</span>
                                    </div>
                                    <div class="text-gray-700 font-medium">${w.meaning}</div>
                                </div>
                            </div>
                            <button onclick="event.stopPropagation(); playAudio('${w.word}')" class="p-3 hover:bg-teal-50 rounded-full transition-all text-xl">🔊</button>
                        </div>
                    </div>
                `).join('');
                container.innerHTML = html;
                
            } catch (e) {
                document.getElementById('vocabList').innerHTML = '<div class="text-center py-8 text-red-500">搜索失败</div>';
            }
        }

        function playAudio(word) {
            if ('speechSynthesis' in window) {
                // 取消之前的
                window.speechSynthesis.cancel();
                
                const utter = new SpeechSynthesisUtterance(word);
                utter.lang = 'en-US';
                utter.rate = 0.8;
                utter.pitch = 1;
                
                // 尝试获取更好的语音
                const voices = window.speechSynthesis.getVoices();
                const englishVoice = voices.find(v => v.lang.includes('en-US') && v.name.includes('Female')) || 
                                    voices.find(v => v.lang.includes('en'));
                if (englishVoice) utter.voice = englishVoice;
                
                window.speechSynthesis.speak(utter);
            } else {
                alert('您的浏览器不支持语音播放');
            }
        }

        // ==================== 游戏功能（词汇守卫战）====================
        let gameWords = [];
        let gameActive = false;
        let gameScore = 0;
        let gameCombo = 0;
        let gameHealth = 100;
        let gameTime = 60;
        let gameLoopId = null;
        let spawnTimer = null;
        let fallingWords = [];
        let currentTarget = null;
        let isPaused = false;

        async function startGame() {
            const diff = document.getElementById('gameDiff').value;
            const btn = document.getElementById('startBtn');
            
            btn.disabled = true;
            btn.textContent = '加载词汇...';
            
            try {
                const res = await fetch(`/api/game/words?count=15&difficulty=${diff}`);
                const data = await res.json();
                gameWords = data.words;
                
                if (gameWords.length < 5) {
                    throw new Error('词汇不足');
                }
                
                // 初始化游戏
                gameActive = true;
                gameScore = 0;
                gameCombo = 0;
                gameHealth = 100;
                gameTime = 60;
                fallingWords = [];
                isPaused = false;
                
                // 清空游戏区域
                document.getElementById('gameLayer').innerHTML = '';
                document.getElementById('gameOverlay').classList.add('hidden');
                document.getElementById('shootControls').classList.remove('opacity-50', 'pointer-events-none');
                
                updateGameUI();
                
                btn.textContent = '游戏中...';
                
                // 开始倒计时
                if (gameLoopId) clearInterval(gameLoopId);
                gameLoopId = setInterval(() => {
                    if (!isPaused) {
                        gameTime--;
                        document.getElementById('time').textContent = gameTime;
                        if (gameTime <= 0) endGame();
                    }
                }, 1000);
                
                // 立即生成第一个单词
                spawnGameWord();
                
                // 定时生成
                if (spawnTimer) clearInterval(spawnTimer);
                const spawnRate = diff === 'easy' ? 4000 : diff === 'hard' ? 2000 : 3000;
                spawnTimer = setInterval(spawnGameWord, spawnRate);
                
            } catch (e) {
                alert('游戏加载失败：' + e.message);
                btn.disabled = false;
                btn.textContent = '开始游戏';
            }
        }

        function spawnGameWord() {
            if (!gameActive || gameHealth <= 0 || gameTime <= 0) return;
            if (fallingWords.length >= 5) return; // 最多同时5个
            
            const wordData = gameWords[Math.floor(Math.random() * gameWords.length)];
            const el = document.createElement('div');
            el.className = 'falling-word';
            el.textContent = wordData.word;
            el.style.left = Math.random() * 70 + 15 + '%'; // 15%-85% 避免边缘
            el.style.top = '-60px';
            
            document.getElementById('gameLayer').appendChild(el);
            
            const wordObj = {
                el: el,
                data: wordData,
                y: -60,
                speed: 1.5 + Math.random(), // 随机速度 1.5-2.5
                fallInterval: null
            };
            fallingWords.push(wordObj);
            
            // 生成选项（1个正确 + 3个干扰项）
            const options = [wordData.meaning, ...wordData.distractors];
            // 打乱顺序
            const shuffled = options.sort(() => Math.random() - 0.5);
            
            // 更新按钮
            for (let i = 0; i < 4; i++) {
                const btn = document.getElementById('btn' + i);
                document.getElementById('opt' + i).textContent = shuffled[i];
                btn.dataset.meaning = shuffled[i];
                btn.classList.remove('correct', 'wrong');
            }
            
            // 设置当前目标（最下方的单词）
            currentTarget = wordObj;
            
            // 开始下落动画
            animateFall(wordObj);
        }

        function animateFall(wordObj) {
            const gameArea = document.getElementById('gameArea');
            const maxY = gameArea.offsetHeight - 60;
            
            wordObj.fallInterval = setInterval(() => {
                if (isPaused || !gameActive) return;
                
                wordObj.y += wordObj.speed;
                wordObj.el.style.top = wordObj.y + 'px';
                
                // 危险警告（快到底部）
                if (wordObj.y > maxY - 100 && !wordObj.el.classList.contains('danger')) {
                    wordObj.el.classList.add('danger');
                }
                
                // 落地检测
                if (wordObj.y >= maxY) {
                    clearInterval(wordObj.fallInterval);
                    
                    // 扣血
                    gameHealth = Math.max(0, gameHealth - 15);
                    gameCombo = 0; // 重置连击
                    updateGameUI();
                    
                    // 震动效果
                    gameArea.style.animation = 'shake 0.3s';
                    setTimeout(() => gameArea.style.animation = '', 300);
                    
                    // 移除单词
                    wordObj.el.remove();
                    fallingWords = fallingWords.filter(w => w !== wordObj);
                    
                    if (currentTarget === wordObj) {
                        currentTarget = fallingWords.length > 0 ? fallingWords[fallingWords.length - 1] : null;
                    }
                    
                    if (gameHealth <= 0) {
                        endGame();
                    }
                }
            }, 20);
        }

        function shoot(index) {
            if (!gameActive || !currentTarget) return;
            
            const selectedMeaning = document.getElementById('btn' + index).dataset.meaning;
            const correctMeaning = currentTarget.data.meaning;
            const btn = document.getElementById('btn' + index);
            
            if (selectedMeaning === correctMeaning) {
                // ✅ 正确！
                gameCombo++;
                const points = 10 * Math.min(gameCombo, 5); // 最高5倍
                gameScore += points;
                
                // 视觉效果
                btn.classList.add('correct');
                
                // 停止下落并移除
                clearInterval(currentTarget.fallInterval);
                currentTarget.el.style.transform = 'scale(1.2)';
                currentTarget.el.style.opacity = '0';
                setTimeout(() => currentTarget.el.remove(), 200);
                
                fallingWords = fallingWords.filter(w => w !== currentTarget);
                currentTarget = null;
                
                setTimeout(() => btn.classList.remove('correct'), 300);
                
                // 立即生成新单词（如果场上少于2个）
                if (fallingWords.length < 2 && gameTime > 0) {
                    setTimeout(spawnGameWord, 500);
                }
                
            } else {
                // ❌ 错误！
                gameCombo = 0;
                gameHealth = Math.max(0, gameHealth - 5);
                btn.classList.add('wrong');
                
                setTimeout(() => btn.classList.remove('wrong'), 500);
                
                if (gameHealth <= 0) endGame();
            }
            
            updateGameUI();
        }

        function updateGameUI() {
            document.getElementById('score').textContent = gameScore;
            document.getElementById('combo').textContent = 'x' + gameCombo;
            
            const healthBar = document.getElementById('healthBar');
            healthBar.style.width = gameHealth + '%';
            
            // 颜色变化
            healthBar.className = 'h-full rounded-full transition-all duration-300 ' + 
                (gameHealth > 60 ? 'bg-gradient-to-r from-green-500 to-green-400' : 
                 gameHealth > 30 ? 'bg-gradient-to-r from-yellow-500 to-yellow-400' : 
                 'bg-gradient-to-r from-red-600 to-red-500');
        }

        function endGame() {
            gameActive = false;
            
            if (gameLoopId) clearInterval(gameLoopId);
            if (spawnTimer) clearInterval(spawnTimer);
            fallingWords.forEach(w => clearInterval(w.fallInterval));
            
            // 显示结果
            document.getElementById('gameOverlay').classList.remove('hidden');
            document.getElementById('gameOverlay').innerHTML = `
                <div class="text-center text-white bg-black/40 p-8 rounded-2xl backdrop-blur-md">
                    <div class="text-5xl mb-4">🏆</div>
                    <h3 class="text-2xl font-bold mb-2">游戏结束</h3>
                    <div class="text-4xl font-bold text-yellow-400 mb-4">${gameScore}</div>
                    <div class="space-y-1 text-sm mb-6">
                        <p>最高连击: <span class="font-bold text-orange-400">x${gameCombo}</span></p>
                        <p>剩余生命: <span class="font-bold ${gameHealth > 0 ? 'text-green-400' : 'text-red-400'}">${gameHealth}%</span></p>
                        <p>剩余时间: <span class="font-bold text-blue-400">${gameTime}秒</span></p>
                    </div>
                    <button onclick="resetGame()" class="px-8 py-3 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full font-bold hover:shadow-lg transition-all transform hover:scale-105">
                        再来一局 ↺
                    </button>
                </div>
            `;
            
            document.getElementById('shootControls').classList.add('opacity-50', 'pointer-events-none');
            
            const btn = document.getElementById('startBtn');
            btn.disabled = false;
            btn.textContent = '开始游戏';
        }

        function resetGame() {
            document.getElementById('gameLayer').innerHTML = '';
            document.getElementById('gameOverlay').innerHTML = `
                <div class="text-center text-white">
                    <div class="text-6xl mb-4">🎮</div>
                    <p class="text-lg opacity-90">点击"开始游戏"加载词汇</p>
                    <p class="text-sm opacity-60 mt-2">使用 A/S/D/F 或鼠标点击选择</p>
                </div>
            `;
            document.getElementById('gameOverlay').classList.remove('hidden');
            
            gameScore = 0;
            gameCombo = 0;
            gameHealth = 100;
            gameTime = 60;
            updateGameUI();
            document.getElementById('time').textContent = '60';
        }

        // 键盘控制（游戏）
        document.addEventListener('keydown', (e) => {
            if (!gameActive) return;
            
            if (e.code === 'Space') {
                e.preventDefault();
                isPaused = !isPaused;
                return;
            }
            
            const keyMap = {'a': 0, 's': 1, 'd': 2, 'f': 3, 'A': 0, 'S': 1, 'D': 2, 'F': 3};
            if (keyMap.hasOwnProperty(e.key)) {
                shoot(keyMap[e.key]);
            }
        });

        // ==================== 写作功能 ====================
        let currentTask = 'task2';
        
        function setTask(task) {
            currentTask = task;
            document.getElementById('btn-task1').className = task === 'task1' ? 'px-4 py-2 rounded-full text-sm bg-teal-600 text-white shadow-md' : 'px-4 py-2 rounded-full text-sm border hover:bg-gray-50 transition-all';
            document.getElementById('btn-task2').className = task === 'task2' ? 'px-4 py-2 rounded-full text-sm bg-teal-600 text-white shadow-md' : 'px-4 py-2 rounded-full text-sm border hover:bg-gray-50 transition-all';
            document.getElementById('wordCountDisplay').textContent = `字数：0 / ${task === 'task1' ? '130+' : '220+'}`;
        }

        function updateWordCount() {
            const text = document.getElementById('essayInput').value;
            const count = text.trim() ? text.trim().split(/\\s+/).length : 0;
            const min = currentTask === 'task1' ? 130 : 220;
            document.getElementById('wordCountDisplay').textContent = `字数：${count} / ${min}+`;
            
            // 字数不足警告
            const display = document.getElementById('wordCountDisplay');
            if (count < min) {
                display.classList.add('text-orange-500');
                display.classList.remove('text-gray-500', 'text-green-600');
            } else {
                display.classList.remove('text-orange-500', 'text-gray-500');
                display.classList.add('text-green-600');
            }
        }

        async function submitEssay() {
            const essay = document.getElementById('essayInput').value;
            const btn = document.getElementById('submitBtn');
            const loader = document.getElementById('btnLoader');
            
            btn.disabled = true;
            document.getElementById('btnText').textContent = '评分中...';
            loader.classList.remove('hidden');
            
            try {
                const res = await fetch('/api/grade_writing', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        essay: essay,
                        task_type: currentTask,
                        prompt: '',
                        target_band: 7.0
                    })
                });
                
                const data = await res.json();
                
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('resultArea').classList.remove('hidden');
                    document.getElementById('overallBand').textContent = data.overall_band;
                    document.getElementById('trScore').textContent = data.breakdown.TR.score;
                    document.getElementById('ccScore').textContent = data.breakdown.CC.score;
                    document.getElementById('lrScore').textContent = data.breakdown.LR.score;
                    document.getElementById('graScore').textContent = data.breakdown.GRA.score;
                    
                    const list = document.getElementById('suggestionsList');
                    list.innerHTML = data.detailed_feedback.weaknesses.map(w => `<li>• ${w}</li>`).join('');
                }
            } catch (e) {
                alert('评分失败：' + e.message);
            }
            
            btn.disabled = false;
            document.getElementById('btnText').textContent = '提交评分';
            loader.classList.add('hidden');
        }

        // ==================== 口语功能 ====================
        async function submitSpeaking() {
            const text = document.getElementById('speakingInput').value;
            const btn = document.getElementById('speakBtn');
            const loader = document.getElementById('speakLoader');
            
            if (text.split(/\\s+/).length < 30) {
                alert('回答太短，建议至少30词');
                return;
            }
            
            btn.disabled = true;
            document.getElementById('speakBtnText').textContent = '评分中...';
            loader.classList.remove('hidden');
            
            try {
                const res = await fetch('/api/grade_speaking', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({transcript: text, part: '2'})
                });
                
                const data = await res.json();
                
                document.getElementById('speakingResult').classList.remove('hidden');
                document.getElementById('speakOverall').textContent = data.overall_band;
                document.getElementById('fluencyScore').textContent = data.breakdown.fluency.score;
                document.getElementById('speakLrScore').textContent = data.breakdown.lexical.score;
                document.getElementById('speakGrScore').textContent = data.breakdown.grammar.score;
                
                const list = document.getElementById('speakSuggestions');
                list.innerHTML = data.suggestions.map(s => `<li>• ${s}</li>`).join('');
                
            } catch (e) {
                alert('评分失败');
            }
            
            btn.disabled = false;
            document.getElementById('speakBtnText').textContent = '提交口语评分';
            loader.classList.add('hidden');
        }

        // 初始化
        showSection('dashboard');
        
        // 预加载语音（解决某些浏览器需要用户交互后才能播放的问题）
        document.addEventListener('click', () => {
            if (window.speechSynthesis && window.speechSynthesis.getVoices().length === 0) {
                window.speechSynthesis.getVoices();
            }
        }, { once: true });
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLContent

# Vercel 适配（如果部署到 Vercel）
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    pass

# 本地运行（Windows 调试）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# 文件末尾添加这行（如果还没有的话）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
