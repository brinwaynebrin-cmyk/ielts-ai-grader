from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Literal, List, Optional
import os
import random
import json
import pathlib

app = FastAPI()

# ============ 数据文件路径处理（适配Vercel） ============
BASE_DIR = pathlib.Path(__file__).parent.parent  # 指向项目根目录
DATA_DIR = BASE_DIR / "data"

def load_json_file(filepath: str):
    """安全加载JSON文件，适配Vercel无服务器环境"""
    try:
        full_path = DATA_DIR / filepath
        if not full_path.exists():
            return None
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

# ============ 原有功能（保留） ============
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
    # 保留原有评分逻辑
    word_count = len(data.essay.split())
    return {
        "overall_band": 6.5,
        "breakdown": {
            "TR": {"score": 6.5, "comments": "Task response adequate"},
            "CC": {"score": 6.5, "comments": "Logical organization"},
            "LR": {"score": 6.0, "comments": "Good vocabulary range"},
            "GRA": {"score": 6.5, "comments": "Complex structures used"}
        },
        "detailed_feedback": {
            "weaknesses": [f"字数：{word_count}", "可增加更多具体例子"]
        },
        "word_count": word_count
    }

@app.post("/api/grade_speaking")
async def grade_speaking(data: SpeakingRequest):
    # 保留原有口语评分
    return {
        "overall_band": 6.5,
        "breakdown": {
            "fluency": {"score": 6.5, "comments": "Good flow"},
            "lexical": {"score": 6.5, "comments": "Adequate vocabulary"},
            "grammar": {"score": 6.0, "comments": "Some errors"},
            "pronunciation": {"score": 7.0, "comments": "Inferred from text"}
        },
        "suggestions": ["使用更多连接词", "增加具体细节"]
    }

# ============ 新增：词汇API ============

@app.get("/api/vocab/{band}")
async def get_vocabulary(
    band: str, 
    page: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None
):
    """获取分级词汇（支持9000+词汇分页）"""
    data = load_json_file(f"vocab/{band}.json")
    if not data:
        raise HTTPException(status_code=404, detail="词汇库不存在")
    
    words = data.get("words", [])
    
    # 搜索过滤
    if search:
        search_lower = search.lower()
        words = [
            w for w in words 
            if search_lower in w["word"].lower() 
            or search_lower in w.get("meaning", "")
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
                        return {"query": q, "total": len(results), "results": results}
    
    return {"query": q, "total": len(results), "results": results}

@app.get("/api/game/words")
async def get_game_words(
    count: int = Query(10, ge=5, le=20),
    difficulty: str = Query("mixed", regex="^(easy|normal|hard|mixed)$")
):
    """为游戏随机抽取词汇"""
    # 根据难度选择源
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
    
    return {"total": len(game_words), "difficulty": difficulty, "words": game_words}

@app.get("/api/speaking/{scenario}")
async def get_speaking_scenario(scenario: str):
    """获取口语情景化数据"""
    data = load_json_file(f"speaking/{scenario}.json")
    if not data:
        raise HTTPException(status_code=404, detail="情景不存在")
    return data

# ============ 前端HTML（内嵌方式） ============

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
        
        /* 游戏样式 */
        .falling-word {
            position: absolute;
            padding: 12px 24px;
            background: rgba(255,255,255,0.95);
            border: 2px solid #3b82f6;
            border-radius: 16px;
            color: #1e3a8a;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
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
            transition: all 0.2s;
        }
        .shoot-btn:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3); }
        .shoot-btn.correct { background: linear-gradient(135deg, #10b981, #059669); }
        .shoot-btn.wrong { background: linear-gradient(135deg, #ef4444, #dc2626); animation: shake 0.5s; }
        @keyframes shake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-10px); } 75% { transform: translateX(10px); } }
    </style>
</head>
<body class="antialiased text-gray-800">

    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 glass border-b border-gray-200 shadow-sm">
        <div class="max-w-6xl mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-2 cursor-pointer" onclick="showSection('dashboard')">
                    <div class="w-8 h-8 bg-teal-600 rounded-lg flex items-center justify-center text-white font-bold">Z</div>
                    <span class="text-xl font-bold">Zenith IELTS</span>
                </div>
                
                <div class="hidden md:flex space-x-1 text-sm">
                    <button onclick="showSection('dashboard')" id="nav-dashboard" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">仪表盘</button>
                    <button onclick="showSection('vocabulary')" id="nav-vocabulary" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">词汇库</button>
                    <button onclick="showSection('wordgame')" id="nav-wordgame" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100 text-pink-600">🎮 游戏</button>
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
                <p class="text-gray-600">基于9000+词汇库 | 情景化口语训练</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="glass rounded-2xl p-5 shadow-sm border-l-4 border-teal-500 cursor-pointer" onclick="showSection('vocabulary')">
                    <div class="text-3xl mb-2">📚</div>
                    <div class="font-bold">分级词汇库</div>
                    <div class="text-xs text-gray-500 mt-1">Band 6/7/8 分级</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm border-l-4 border-pink-500 cursor-pointer" onclick="showSection('wordgame')">
                    <div class="text-3xl mb-2">🎮</div>
                    <div class="font-bold">词汇守卫战</div>
                    <div class="text-xs text-gray-500 mt-1">弹幕射击背单词</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm border-l-4 border-blue-500 cursor-pointer" onclick="showSection('writing')">
                    <div class="text-3xl mb-2">📝</div>
                    <div class="font-bold">AI写作精批</div>
                    <div class="text-xs text-gray-500 mt-1">Task 1 & 2</div>
                </div>
            </div>
        </section>

        <!-- VOCABULARY SECTION -->
        <section id="vocabulary" class="section hidden-section fade-in">
            <div class="mb-6 flex items-center justify-between">
                <h2 class="text-2xl font-bold">雅思分级词汇库</h2>
                <div class="flex gap-2">
                    <input type="text" id="vocabSearch" placeholder="搜索9000+词汇..." 
                        class="px-4 py-2 border rounded-full text-sm w-64 focus:ring-2 focus:ring-teal-500 outline-none"
                        onkeyup="if(event.key==='Enter') searchVocab()">
                    <button onclick="searchVocab()" class="px-4 py-2 bg-teal-600 text-white rounded-full text-sm">搜索</button>
                </div>
            </div>

            <div class="flex gap-4 mb-6">
                <button onclick="loadVocab('academic')" class="px-4 py-2 bg-purple-100 text-purple-700 rounded-full text-sm font-medium hover:bg-purple-200">AWL学术570词</button>
                <button onclick="loadVocab('band6')" class="px-4 py-2 bg-green-100 text-green-700 rounded-full text-sm font-medium hover:bg-green-200">Band 6.0-6.5</button>
                <button onclick="loadVocab('band7')" class="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium hover:bg-blue-200">Band 7.0-7.5</button>
                <button onclick="loadVocab('band8')" class="px-4 py-2 bg-orange-100 text-orange-700 rounded-full text-sm font-medium hover:bg-orange-200">Band 8.0+</button>
            </div>

            <div id="vocabList" class="space-y-3 max-h-[600px] overflow-y-auto">
                <div class="text-center py-12 text-gray-400">点击上方按钮加载词汇</div>
            </div>
            
            <div class="mt-4 text-center">
                <button onclick="loadMore()" id="loadMoreBtn" class="px-6 py-2 bg-gray-100 hover:bg-gray-200 rounded-full text-sm hidden">加载更多</button>
            </div>
        </section>

        <!-- GAME SECTION -->
        <section id="wordgame" class="section hidden-section fade-in">
            <div class="mb-6 flex items-center justify-between">
                <h2 class="text-2xl font-bold">🎮 词汇守卫战</h2>
                <div class="flex gap-2">
                    <select id="gameDiff" class="px-3 py-2 border rounded-lg text-sm">
                        <option value="easy">简单</option>
                        <option value="normal" selected>普通</option>
                        <option value="hard">困难</option>
                    </select>
                    <button onclick="startGame()" id="startBtn" class="px-6 py-2 bg-pink-500 text-white rounded-full font-bold">开始游戏</button>
                </div>
            </div>

            <div class="grid grid-cols-4 gap-4 mb-4">
                <div class="glass rounded-xl p-3 text-center">
                    <div class="text-xs text-gray-500">得分</div>
                    <div class="text-2xl font-bold text-pink-600" id="score">0</div>
                </div>
                <div class="glass rounded-xl p-3 text-center">
                    <div class="text-xs text-gray-500">连击</div>
                    <div class="text-2xl font-bold text-orange-500" id="combo">x0</div>
                </div>
                <div class="glass rounded-xl p-3 text-center">
                    <div class="text-xs text-gray-500">时间</div>
                    <div class="text-2xl font-bold text-blue-500" id="time">60</div>
                </div>
                <div class="glass rounded-xl p-3 text-center">
                    <div class="text-xs text-gray-500">生命</div>
                    <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                        <div id="healthBar" class="h-full bg-green-500 rounded-full" style="width: 100%"></div>
                    </div>
                </div>
            </div>

            <div id="gameArea" class="relative bg-gradient-to-b from-indigo-900 to-purple-900 rounded-2xl h-[400px] overflow-hidden mb-4">
                <div id="gameLayer" class="absolute inset-0"></div>
                <div id="gameOverlay" class="absolute inset-0 flex items-center justify-center bg-black/50 text-white">
                    <div class="text-center">
                        <div class="text-4xl mb-2">🎮</div>
                        <p>点击"开始游戏"加载词汇</p>
                    </div>
                </div>
            </div>

            <div id="shootControls" class="grid grid-cols-4 gap-3 opacity-50 pointer-events-none">
                <button onclick="shoot(0)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg" id="btn0">-</button>
                <button onclick="shoot(1)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg" id="btn1">-</button>
                <button onclick="shoot(2)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg" id="btn2">-</button>
                <button onclick="shoot(3)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg" id="btn3">-</button>
            </div>
        </section>

        <!-- WRITING & SPEAKING (保留原有结构) -->
        <section id="writing" class="section hidden-section fade-in">
            <h2 class="text-2xl font-bold mb-4">AI写作精批</h2>
            <div class="glass rounded-2xl p-6 shadow-sm">
                <textarea id="essayInput" rows="10" class="w-full p-4 border rounded-lg" placeholder="输入作文..."></textarea>
                <button onclick="submitEssay()" class="mt-4 px-6 py-2 bg-teal-600 text-white rounded-full">提交评分</button>
            </div>
        </section>

        <section id="speaking" class="section hidden-section fade-in">
            <h2 class="text-2xl font-bold mb-4">口语评分</h2>
            <div class="glass rounded-2xl p-6 shadow-sm">
                <textarea id="speakingInput" rows="8" class="w-full p-4 border rounded-lg" placeholder="输入口语回答..."></textarea>
                <button onclick="submitSpeaking()" class="mt-4 px-6 py-2 bg-purple-600 text-white rounded-full">提交评分</button>
            </div>
        </section>

    </main>

    <script>
        // ==================== 全局状态 ====================
        let currentSection = 'dashboard';
        let currentVocabPage = 0;
        let currentVocabBand = 'band7';
        let vocabCache = [];

        // ==================== 导航 ====================
        function showSection(sectionId) {
            document.querySelectorAll('.section').forEach(s => {
                s.classList.add('hidden-section');
                s.classList.remove('fade-in');
            });
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('nav-active'));
            
            document.getElementById(sectionId).classList.remove('hidden-section');
            document.getElementById(sectionId).classList.add('fade-in');
            document.getElementById('nav-' + sectionId)?.classList.add('nav-active');
            currentSection = sectionId;
        }

        // ==================== 词汇库功能 ====================
        async function loadVocab(band) {
            currentVocabBand = band;
            currentVocabPage = 0;
            document.getElementById('vocabList').innerHTML = '<div class="text-center py-8"><div class="loading inline-block w-8 h-8 border-4 border-teal-600 border-t-transparent rounded-full animate-spin"></div></div>';
            
            try {
                const res = await fetch(`/api/vocab/${band}?page=0&limit=20`);
                const data = await res.json();
                vocabCache = data.words;
                renderVocabList(data.words, data.metadata);
            } catch (e) {
                document.getElementById('vocabList').innerHTML = '<div class="text-center py-8 text-red-500">加载失败，请重试</div>';
            }
        }

        function renderVocabList(words, meta) {
            if (words.length === 0) {
                document.getElementById('vocabList').innerHTML = '<div class="text-center py-8 text-gray-400">暂无词汇</div>';
                return;
            }
            
            const html = words.map(w => `
                <div class="glass rounded-xl p-4 shadow-sm hover:shadow-md transition-all">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white font-bold text-lg">
                                ${w.word.charAt(0).toUpperCase()}
                            </div>
                            <div>
                                <div class="flex items-center gap-2">
                                    <span class="font-bold text-lg">${w.word}</span>
                                    <span class="text-sm text-gray-500">${w.phonetic || ''}</span>
                                    <span class="px-2 py-0.5 bg-orange-100 text-orange-700 rounded text-xs">Band ${w.band}</span>
                                </div>
                                <div class="text-gray-600">${w.meaning}</div>
                                ${w.examples ? `<div class="text-sm text-gray-400 mt-1 italic">"${w.examples[0]}"</div>` : ''}
                            </div>
                        </div>
                        <button onclick="playAudio('${w.word}')" class="p-2 hover:bg-gray-100 rounded-full">🔊</button>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('vocabList').innerHTML = html;
            document.getElementById('loadMoreBtn').classList.toggle('hidden', !meta.has_more);
        }

        async function loadMore() {
            currentVocabPage++;
            const res = await fetch(`/api/vocab/${currentVocabBand}?page=${currentVocabPage}&limit=20`);
            const data = await res.json();
            vocabCache = [...vocabCache, ...data.words];
            
            // 追加到现有列表
            const html = data.words.map(w => `
                <div class="glass rounded-xl p-4 shadow-sm hover:shadow-md transition-all">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-4">
                            <div class="w-12 h-12 rounded-full bg-gradient-to-br from-teal-400 to-blue-500 flex items-center justify-center text-white font-bold text-lg">
                                ${w.word.charAt(0).toUpperCase()}
                            </div>
                            <div>
                                <div class="flex items-center gap-2">
                                    <span class="font-bold text-lg">${w.word}</span>
                                    <span class="text-sm text-gray-500">${w.phonetic || ''}</span>
                                    <span class="px-2 py-0.5 bg-orange-100 text-orange-700 rounded text-xs">Band ${w.band}</span>
                                </div>
                                <div class="text-gray-600">${w.meaning}</div>
                            </div>
                        </div>
                        <button onclick="playAudio('${w.word}')" class="p-2 hover:bg-gray-100 rounded-full">🔊</button>
                    </div>
                </div>
            `).join('');
            
            document.getElementById('vocabList').insertAdjacentHTML('beforeend', html);
            document.getElementById('loadMoreBtn').classList.toggle('hidden', !data.metadata.has_more);
        }

        async function searchVocab() {
            const q = document.getElementById('vocabSearch').value;
            if (!q) return;
            
            document.getElementById('vocabList').innerHTML = '<div class="text-center py-8"><div class="loading inline-block w-8 h-8 border-4 border-teal-600 border-t-transparent rounded-full animate-spin"></div></div>';
            
            try {
                const res = await fetch(`/api/vocab/search?q=${q}&limit=50`);
                const data = await res.json();
                
                if (data.results.length === 0) {
                    document.getElementById('vocabList').innerHTML = '<div class="text-center py-8 text-gray-400">未找到匹配词汇</div>';
                    return;
                }
                
                // 使用相同渲染函数，但隐藏加载更多
                renderVocabList(data.results, {has_more: false});
                document.getElementById('loadMoreBtn').classList.add('hidden');
            } catch (e) {
                document.getElementById('vocabList').innerHTML = '<div class="text-center py-8 text-red-500">搜索失败</div>';
            }
        }

        function playAudio(word) {
            if ('speechSynthesis' in window) {
                const utter = new SpeechSynthesisUtterance(word);
                utter.lang = 'en-US';
                utter.rate = 0.8;
                speechSynthesis.speak(utter);
            }
        }

        // ==================== 游戏功能 ====================
        let gameWords = [];
        let currentWord = null;
        let gameScore = 0;
        let gameCombo = 0;
        let gameHealth = 100;
        let gameTime = 60;
        let gameInterval;
        let spawnInterval;
        let fallingWords = [];

        async function startGame() {
            const diff = document.getElementById('gameDiff').value;
            document.getElementById('startBtn').disabled = true;
            document.getElementById('startBtn').textContent = '加载中...';
            
            try {
                const res = await fetch(`/api/game/words?count=15&difficulty=${diff}`);
                const data = await res.json();
                gameWords = data.words;
                
                // 初始化游戏状态
                gameScore = 0;
                gameCombo = 0;
                gameHealth = 100;
                gameTime = 60;
                fallingWords = [];
                
                updateGameUI();
                document.getElementById('gameOverlay').classList.add('hidden');
                document.getElementById('shootControls').classList.remove('opacity-50', 'pointer-events-none');
                document.getElementById('startBtn').textContent = '游戏中...';
                
                // 开始倒计时
                gameInterval = setInterval(() => {
                    gameTime--;
                    document.getElementById('time').textContent = gameTime;
                    if (gameTime <= 0) endGame();
                }, 1000);
                
                // 开始生成单词
                spawnWord();
                spawnInterval = setInterval(spawnWord, 3000);
                
            } catch (e) {
                alert('加载失败，请重试');
                document.getElementById('startBtn').disabled = false;
                document.getElementById('startBtn').textContent = '开始游戏';
            }
        }

        function spawnWord() {
            if (gameTime <= 0 || gameHealth <= 0) return;
            if (fallingWords.length >= 5) return;
            
            const wordData = gameWords[Math.floor(Math.random() * gameWords.length)];
            const el = document.createElement('div');
            el.className = 'falling-word';
            el.textContent = wordData.word;
            el.style.left = Math.random() * 70 + 10 + '%';
            el.style.top = '-50px';
            
            document.getElementById('gameLayer').appendChild(el);
            
            const wordObj = {
                el: el,
                data: wordData,
                y: -50,
                speed: 1 + Math.random()
            };
            fallingWords.push(wordObj);
            
            // 设置选项
            const options = [wordData.meaning, ...wordData.distractors].sort(() => Math.random() - 0.5);
            for (let i = 0; i < 4; i++) {
                document.getElementById('btn' + i).textContent = options[i];
                document.getElementById('btn' + i).dataset.meaning = options[i];
                document.getElementById('btn' + i).classList.remove('correct', 'wrong');
            }
            currentWord = wordObj;
            
            // 下落动画
            animateFall(wordObj);
        }

        function animateFall(wordObj) {
            const gameArea = document.getElementById('gameArea');
            const maxY = gameArea.offsetHeight - 50;
            
            const fall = setInterval(() => {
                if (gameTime <= 0 || gameHealth <= 0) {
                    clearInterval(fall);
                    return;
                }
                
                wordObj.y += wordObj.speed;
                wordObj.el.style.top = wordObj.y + 'px';
                
                // 警告效果
                if (wordObj.y > maxY - 100) {
                    wordObj.el.classList.add('danger');
                }
                
                // 落地检测
                if (wordObj.y >= maxY) {
                    clearInterval(fall);
                    gameHealth -= 15;
                    gameCombo = 0;
                    updateGameUI();
                    wordObj.el.remove();
                    fallingWords = fallingWords.filter(w => w !== wordObj);
                    
                    if (gameHealth <= 0) endGame();
                }
            }, 20);
            
            wordObj.fallInterval = fall;
        }

        function shoot(index) {
            if (!currentWord) return;
            
            const selected = document.getElementById('btn' + index).dataset.meaning;
            const correct = currentWord.data.meaning;
            
            if (selected === correct) {
                // 正确
                gameCombo++;
                const points = 10 * Math.min(gameCombo, 5);
                gameScore += points;
                
                document.getElementById('btn' + index).classList.add('correct');
                clearInterval(currentWord.fallInterval);
                currentWord.el.remove();
                fallingWords = fallingWords.filter(w => w !== currentWord);
                currentWord = null;
                
                setTimeout(() => {
                    document.getElementById('btn' + index).classList.remove('correct');
                }, 300);
                
            } else {
                // 错误
                gameCombo = 0;
                gameHealth -= 5;
                document.getElementById('btn' + index).classList.add('wrong');
                setTimeout(() => {
                    document.getElementById('btn' + index).classList.remove('wrong');
                }, 500);
                updateGameUI();
                
                if (gameHealth <= 0) endGame();
            }
            
            updateGameUI();
        }

        function updateGameUI() {
            document.getElementById('score').textContent = gameScore;
            document.getElementById('combo').textContent = 'x' + gameCombo;
            document.getElementById('healthBar').style.width = gameHealth + '%';
            document.getElementById('healthBar').className = 'h-full rounded-full ' + 
                (gameHealth > 60 ? 'bg-green-500' : gameHealth > 30 ? 'bg-yellow-500' : 'bg-red-500');
        }

        function endGame() {
            clearInterval(gameInterval);
            clearInterval(spawnInterval);
            fallingWords.forEach(w => clearInterval(w.fallInterval));
            
            document.getElementById('gameOverlay').classList.remove('hidden');
            document.getElementById('gameOverlay').innerHTML = `
                <div class="text-center bg-white/10 p-8 rounded-2xl backdrop-blur-md">
                    <div class="text-4xl mb-2">🏆</div>
                    <div class="text-2xl font-bold mb-2">游戏结束</div>
                    <div class="text-xl">最终得分: ${gameScore}</div>
                    <div class="text-sm mt-4">最高连击: ${gameCombo}</div>
                    <button onclick="resetGame()" class="mt-4 px-6 py-2 bg-pink-500 text-white rounded-full">再来一局</button>
                </div>
            `;
            document.getElementById('shootControls').classList.add('opacity-50', 'pointer-events-none');
            document.getElementById('startBtn').disabled = false;
            document.getElementById('startBtn').textContent = '开始游戏';
        }

        function resetGame() {
            document.getElementById('gameLayer').innerHTML = '';
            document.getElementById('gameOverlay').innerHTML = `
                <div class="text-center">
                    <div class="text-4xl mb-2">🎮</div>
                    <p>点击"开始游戏"加载词汇</p>
                </div>
            `;
            gameScore = 0;
            gameCombo = 0;
            gameHealth = 100;
            gameTime = 60;
            updateGameUI();
            document.getElementById('time').textContent = '60';
        }

        // ==================== 原有功能保留 ====================
        async function submitEssay() {
            const essay = document.getElementById('essayInput').value;
            const res = await fetch('/api/grade_writing', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({essay, task_type: 'task2', prompt: ''})
            });
            const data = await res.json();
            alert(`写作评分:\\n总分: ${data.overall_band}\\n字数: ${data.word_count}`);
        }

        async function submitSpeaking() {
            const text = document.getElementById('speakingInput').value;
            const res = await fetch('/api/grade_speaking', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({transcript: text, part: '2'})
            });
            const data = await res.json();
            alert(`口语评分: ${data.overall_band}`);
        }

        // 初始化
        showSection('dashboard');
        loadVocab('band7'); // 默认加载
    </script>
</body>
</html>
"""

# 主页路由（修改原有home函数）
@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLContent

# 从mangum导入（如果原有）
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    pass
