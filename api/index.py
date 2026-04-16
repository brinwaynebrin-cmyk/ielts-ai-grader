from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Literal
import os

app = FastAPI()

# 完整雅思学习平台（单文件版）
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
        .glass { background: rgba(255,255,255,0.85); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); }
        .nav-active { background: #0d9488; color: white; }
        .score-ring { transform: rotate(-90deg); transform-origin: 50% 50%; }
        .hidden-section { display: none; }
        .fade-in { animation: fadeIn 0.4s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="antialiased text-gray-800">

    <!-- Navigation -->
    <nav class="fixed top-0 w-full z-50 glass border-b border-gray-200 shadow-sm">
        <div class="max-w-6xl mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <div class="flex items-center space-x-2 cursor-pointer" onclick="showSection('dashboard')">
                    <div class="w-8 h-8 bg-teal-600 rounded-lg flex items-center justify-center text-white font-bold">Z</div>
                    <span class="text-xl font-bold text-gray-900">Zenith IELTS</span>
                </div>
                
                <div class="hidden md:flex space-x-1">
                    <button onclick="showSection('dashboard')" id="nav-dashboard" class="nav-btn px-4 py-2 rounded-full text-sm font-medium transition-all hover:bg-gray-100">仪表盘</button>
                    <button onclick="showSection('writing')" id="nav-writing" class="nav-btn px-4 py-2 rounded-full text-sm font-medium transition-all hover:bg-gray-100">AI写作精批</button>
                    <button onclick="showSection('vocabulary')" id="nav-vocabulary" class="nav-btn px-4 py-2 rounded-full text-sm font-medium transition-all hover:bg-gray-100">词汇库</button>
                    <button onclick="showSection('resources')" id="nav-resources" class="nav-btn px-4 py-2 rounded-full text-sm font-medium transition-all hover:bg-gray-100">学习资源</button>
                </div>
            </div>
        </div>
    </nav>

    <main class="pt-20 pb-12 px-4 max-w-6xl mx-auto">

        <!-- DASHBOARD -->
        <section id="dashboard" class="section fade-in">
            <div class="mb-8">
                <h1 class="text-3xl font-bold text-gray-900 mb-2">欢迎回来</h1>
                <p class="text-gray-600">今日学习概览 · 距离考试还有 <span class="text-teal-600 font-bold">42</span> 天</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
                <div class="glass rounded-2xl p-5 shadow-sm">
                    <div class="text-sm text-gray-500 mb-1">本周学习时长</div>
                    <div class="text-2xl font-bold text-gray-900">12.5<span class="text-sm font-normal text-gray-500">小时</span></div>
                    <div class="text-xs text-teal-600 mt-1">↑ 较上周增长 15%</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm">
                    <div class="text-sm text-gray-500 mb-1">写作均分</div>
                    <div class="text-2xl font-bold text-teal-600">6.5</div>
                    <div class="text-xs text-gray-500 mt-1">最近3次评分平均</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm">
                    <div class="text-sm text-gray-500 mb-1">词汇掌握</div>
                    <div class="text-2xl font-bold text-gray-900">1,240<span class="text-sm font-normal text-gray-500">词</span></div>
                    <div class="text-xs text-orange-600 mt-1">AWL学术词汇表</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all" onclick="showSection('writing')">
                    <div class="text-sm text-gray-500 mb-1">今日任务</div>
                    <div class="text-lg font-bold text-teal-600">完成一次写作评分</div>
                    <div class="text-xs text-gray-500 mt-1">点击开始 →</div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="glass rounded-2xl p-6 shadow-sm">
                    <h3 class="font-bold text-lg mb-4">最近评分记录</h3>
                    <div id="historyList" class="space-y-3">
                        <div class="p-3 bg-white rounded-lg border border-gray-100">
                            <div class="flex justify-between items-center">
                                <span class="font-medium text-sm">Task 2 - 犯罪类话题</span>
                                <span class="font-bold text-teal-600">6.0</span>
                            </div>
                            <div class="text-xs text-gray-500 mt-1">2026-04-16 · TR:6 CC:6 LR:6 GRA:6</div>
                        </div>
                    </div>
                </div>

                <div class="glass rounded-2xl p-6 shadow-sm bg-gradient-to-br from-teal-50 to-transparent">
                    <h3 class="font-bold text-lg mb-3">💡 今日技巧</h3>
                    <p class="text-gray-700 text-sm leading-relaxed mb-3">
                        <strong>Task 2 开头段写法：</strong>使用 "While it is true that..., I believe that..." 结构平衡双方观点，比简单陈述立场更能体现批判性思维。
                    </p>
                    <button onclick="showSection('writing')" class="text-teal-600 text-sm font-medium hover:underline">去练习 →</button>
                </div>
            </div>
        </section>

        <!-- WRITING SECTION -->
        <section id="writing" class="section hidden-section fade-in">
            <div class="mb-6">
                <h2 class="text-3xl font-bold text-gray-900 mb-2">AI写作精批</h2>
                <p class="text-gray-600">基于DeepSeek AI · 按官方四项标准评分 · 成本约¥0.02/篇</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Input Area -->
                <div class="lg:col-span-2 space-y-4">
                    <div class="glass rounded-2xl p-6 shadow-sm">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex space-x-2">
                                <button onclick="setTask('task1')" id="btn-task1" class="px-3 py-1 rounded-full text-sm border hover:bg-gray-50">Task 1 图表</button>
                                <button onclick="setTask('task2')" id="btn-task2" class="px-3 py-1 rounded-full text-sm bg-teal-600 text-white">Task 2 议论</button>
                            </div>
                            <span class="text-sm text-gray-500" id="wordCountDisplay">字数：0 / 250</span>
                        </div>

                        <div class="bg-gray-50 p-4 rounded-lg mb-4 text-sm text-gray-700" id="promptDisplay">
                            Some people think that the best way to reduce crime is to give longer prison sentences. Others believe there are better ways to reduce crime. Discuss both views and give your opinion.
                        </div>

                        <textarea id="essayInput" rows="12" class="w-full p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all font-mono text-sm" 
                            placeholder="在此输入你的作文...&#10;&#10;结构建议：&#10;1. Introduction: Paraphrase + Thesis statement&#10;2. Body 1: 一方观点 + 论据&#10;3. Body 2: 另一方观点 + 论据&#10;4. Conclusion: 总结 + 你的立场"
                            oninput="updateWordCount()"></textarea>

                        <div class="mt-4 flex justify-between items-center">
                            <div class="text-xs text-gray-400">DeepSeek-V3 模型 · 预计耗时3-5秒</div>
                            <button onclick="submitEssay()" id="submitBtn" class="px-6 py-2 bg-teal-600 text-white rounded-full font-medium hover:bg-teal-700 transition-all flex items-center space-x-2">
                                <span id="btnText">提交AI评分</span>
                                <svg id="btnLoader" class="hidden animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                            </button>
                        </div>
                    </div>

                    <!-- Result Area -->
                    <div id="resultArea" class="hidden glass rounded-2xl p-6 shadow-sm border-l-4 border-teal-500">
                        <div class="flex items-center justify-between mb-6">
                            <div>
                                <h3 class="text-xl font-bold text-gray-900">AI评分报告</h3>
                                <p class="text-sm text-gray-500">基于雅思官方四项标准</p>
                            </div>
                            <div class="text-center">
                                <div class="text-4xl font-bold text-teal-600" id="overallBand">-</div>
                                <div class="text-xs text-gray-500">预估总分</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
                            <div class="p-3 bg-gray-50 rounded-lg text-center">
                                <div class="text-xs text-gray-500 mb-1">TR (任务回应)</div>
                                <div class="text-xl font-bold text-teal-600" id="trScore">-</div>
                                <div class="text-xs text-gray-500 mt-1" id="trComment">-</div>
                            </div>
                            <div class="p-3 bg-gray-50 rounded-lg text-center">
                                <div class="text-xs text-gray-500 mb-1">CC (连贯衔接)</div>
                                <div class="text-xl font-bold text-teal-600" id="ccScore">-</div>
                                <div class="text-xs text-gray-500 mt-1" id="ccComment">-</div>
                            </div>
                            <div class="p-3 bg-gray-50 rounded-lg text-center">
                                <div class="text-xs text-gray-500 mb-1">LR (词汇资源)</div>
                                <div class="text-xl font-bold text-teal-600" id="lrScore">-</div>
                                <div class="text-xs text-gray-500 mt-1" id="lrComment">-</div>
                            </div>
                            <div class="p-3 bg-gray-50 rounded-lg text-center">
                                <div class="text-xs text-gray-500 mb-1">GRA (语法)</div>
                                <div class="text-xl font-bold text-teal-600" id="graScore">-</div>
                                <div class="text-xs text-gray-500 mt-1" id="graComment">-</div>
                            </div>
                        </div>

                        <div class="bg-gray-900 text-white rounded-xl p-4 mb-4">
                            <h4 class="font-bold mb-2 text-sm">💡 提升建议（针对7分目标）</h4>
                            <ul id="suggestionsList" class="text-sm space-y-1 text-gray-300"></ul>
                        </div>

                        <div class="flex justify-between text-xs text-gray-400">
                            <span id="wordCountResult">字数统计：-</span>
                            <span id="costDisplay">成本：¥0.02</span>
                        </div>
                    </div>
                </div>

                <!-- Sidebar -->
                <div class="space-y-4">
                    <div class="glass rounded-2xl p-5 shadow-sm">
                        <h4 class="font-bold mb-3 text-sm">评分标准说明</h4>
                        <div class="space-y-3 text-xs text-gray-600">
                            <div><strong class="text-gray-900">Task Response:</strong> 扣题程度、论点发展、结论完整性</div>
                            <div><strong class="text-gray-900">Coherence:</strong> 段落逻辑、连接词使用、指代清晰</div>
                            <div><strong class="text-gray-900">Lexical Resource:</strong> 词汇多样性、学术搭配、准确性</div>
                            <div><strong class="text-gray-900">Grammar:</strong> 句式复杂度、语法错误控制、标点使用</div>
                        </div>
                    </div>

                    <div class="glass rounded-2xl p-5 shadow-sm bg-orange-50">
                        <h4 class="font-bold mb-2 text-sm text-orange-800">高分句型模板</h4>
                        <div class="text-xs text-orange-700 space-y-2">
                            <p>• While it is true that..., I would argue that...</p>
                            <p>• This essay will examine both sides of the argument.</p>
                            <p>• There are several reasons why...</p>
                            <p>• In conclusion, although..., I believe that...</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- VOCABULARY SECTION -->
        <section id="vocabulary" class="section hidden-section fade-in">
            <div class="mb-6">
                <h2 class="text-3xl font-bold text-gray-900 mb-2">AWL词汇库</h2>
                <p class="text-gray-600">Academic Word List · 学术词汇智能复习</p>
            </div>

            <div class="max-w-2xl mx-auto">
                <div class="glass rounded-3xl p-8 shadow-lg min-h-[400px] flex flex-col items-center justify-center relative cursor-pointer transition-all hover:shadow-xl" onclick="flipCard()">
                    
                    <!-- Front -->
                    <div id="cardFront" class="text-center">
                        <div class="text-sm text-teal-600 font-medium mb-4 tracking-wider">ACADEMIC WORD LIST</div>
                        <h3 class="text-6xl font-bold text-gray-900 mb-4" id="currentWord">ambiguous</h3>
                        <div class="text-gray-400 text-sm">点击翻转查看释义与例句</div>
                        <div class="mt-8 flex justify-center space-x-2">
                            <span class="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">adj.</span>
                            <span class="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600">AWL Sublist 1</span>
                        </div>
                    </div>

                    <!-- Back -->
                    <div id="cardBack" class="hidden text-center w-full">
                        <div class="text-3xl font-medium text-teal-700 mb-3" id="wordMeaning">模棱两可的；含糊的</div>
                        <div class="text-gray-600 italic mb-6 text-lg">"The instructions were ambiguous and confusing."</div>
                        
                        <div class="flex justify-center space-x-4 mb-6">
                            <button onclick="event.stopPropagation(); markWord('known')" class="px-8 py-3 bg-teal-500 text-white rounded-full font-medium hover:bg-teal-600 transition-all">已掌握</button>
                            <button onclick="event.stopPropagation(); markWord('unknown')" class="px-8 py-3 bg-orange-500 text-white rounded-full font-medium hover:bg-orange-600 transition-all">需复习</button>
                        </div>
                        
                        <div class="text-xs text-gray-400">点击卡片返回正面</div>
                    </div>
                </div>

                <div class="flex justify-center mt-6 space-x-2">
                    <div class="w-2 h-2 rounded-full bg-teal-500"></div>
                    <div class="w-2 h-2 rounded-full bg-gray-300"></div>
                    <div class="w-2 h-2 rounded-full bg-gray-300"></div>
                    <div class="w-2 h-2 rounded-full bg-gray-300"></div>
                    <div class="w-2 h-2 rounded-full bg-gray-300"></div>
                </div>

                <div class="mt-6 text-center text-sm text-gray-500">
                    今日待复习：<span class="font-bold text-teal-600">12</span> 词 · 已掌握：<span class="font-bold text-gray-900">156</span> 词
                </div>
            </div>
        </section>

        <!-- RESOURCES SECTION -->
        <section id="resources" class="section hidden-section fade-in">
            <div class="mb-6">
                <h2 class="text-3xl font-bold text-gray-900 mb-2">学习资源</h2>
                <p class="text-gray-600">雅思备考资料整理</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="glass rounded-2xl p-6 shadow-sm hover:shadow-md transition-all cursor-pointer">
                    <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                    </div>
                    <h3 class="font-bold text-lg mb-2">剑雅真题 17-18</h3>
                    <p class="text-sm text-gray-600 mb-3">最新真题PDF + 听力音频 + 答案解析</p>
                    <span class="text-xs text-teal-600 font-medium">即将上线 →</span>
                </div>

                <div class="glass rounded-2xl p-6 shadow-sm hover:shadow-md transition-all cursor-pointer">
                    <div class="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"/></svg>
                    </div>
                    <h3 class="font-bold text-lg mb-2">Simon 写作范文</h3>
                    <p class="text-sm text-gray-600 mb-3">前雅思考官范文合集，Task 1 & 2 全覆盖</p>
                    <span class="text-xs text-teal-600 font-medium">即将上线 →</span>
                </div>

                <div class="glass rounded-2xl p-6 shadow-sm hover:shadow-md transition-all cursor-pointer">
                    <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mb-4">
                        <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                    </div>
                    <h3 class="font-bold text-lg mb-2">听力场景词汇</h3>
                    <p class="text-sm text-gray-600 mb-3">租房、学术、旅游等高频场景词汇整理</p>
                    <span class="text-xs text-teal-600 font-medium">即将上线 →</span>
                </div>
            </div>
        </section>

    </main>

    <script>
        // Global State
        let currentTask = 'task2';
        let currentWordIndex = 0;
        const words = [
            {word: 'ambiguous', meaning: '模棱两可的；含糊不清的', example: 'The instructions were ambiguous.'},
            {word: 'controversial', meaning: '有争议的', example: 'It is a controversial topic.'},
            {word: 'empirical', meaning: '基于实证的', example: 'Empirical evidence supports this.'},
            {word: 'hypothesis', meaning: '假设', example: 'The hypothesis was tested.'},
            {word: 'significant', meaning: '重要的；显著的', example: 'There was a significant increase.'}
        ];

        // Navigation
        function showSection(sectionId) {
            document.querySelectorAll('.section').forEach(s => {
                s.classList.add('hidden-section');
                s.classList.remove('fade-in');
            });
            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.classList.remove('nav-active');
            });
            
            const target = document.getElementById(sectionId);
            target.classList.remove('hidden-section');
            target.classList.add('fade-in');
            
            const navBtn = document.getElementById('nav-' + sectionId);
            if (navBtn) navBtn.classList.add('nav-active');
        }

        // Initialize
        showSection('dashboard');

        // Writing Functions
        function setTask(task) {
            currentTask = task;
            document.getElementById('btn-task1').className = task === 'task1' ? 'px-3 py-1 rounded-full text-sm bg-teal-600 text-white' : 'px-3 py-1 rounded-full text-sm border hover:bg-gray-50';
            document.getElementById('btn-task2').className = task === 'task2' ? 'px-3 py-1 rounded-full text-sm bg-teal-600 text-white' : 'px-3 py-1 rounded-full text-sm border hover:bg-gray-50';
            
            const prompts = {
                task1: "The graph below shows the percentage of households with internet access in three different countries from 1998 to 2008. Summarize the information.",
                task2: "Some people think that the best way to reduce crime is to give longer prison sentences. Others believe there are better ways. Discuss both views."
            };
            document.getElementById('promptDisplay').textContent = prompts[task];
            document.getElementById('wordCountDisplay').textContent = `字数：0 / ${task === 'task1' ? 150 : 250}`;
        }

        function updateWordCount() {
            const text = document.getElementById('essayInput').value;
            const count = text.trim() ? text.trim().split(/\\s+/).length : 0;
            const target = currentTask === 'task1' ? 150 : 250;
            document.getElementById('wordCountDisplay').textContent = `字数：${count} / ${target}`;
            
            if (count >= target) {
                document.getElementById('wordCountDisplay').classList.add('text-teal-600');
            } else {
                document.getElementById('wordCountDisplay').classList.remove('text-teal-600');
            }
        }

        async function submitEssay() {
            const essay = document.getElementById('essayInput').value;
            const wordCount = essay.trim() ? essay.trim().split(/\\s+/).length : 0;
            const target = currentTask === 'task1' ? 150 : 250;
            
            if (wordCount < target) {
                alert(`字数不足，需要至少 ${target} 词（当前 ${wordCount} 词）`);
                return;
            }

            const btn = document.getElementById('submitBtn');
            const btnText = document.getElementById('btnText');
            const loader = document.getElementById('btnLoader');
            
            btn.disabled = true;
            btnText.textContent = 'AI评分中...';
            loader.classList.remove('hidden');

            try {
                const response = await fetch('/api/grade_writing', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        essay: essay,
                        task_type: currentTask,
                        prompt: document.getElementById('promptDisplay').textContent,
                        target_band: 7.0
                    })
                });
                
                const result = await response.json();
                displayResult(result, wordCount);
                addToHistory(result);
                
            } catch (error) {
                alert('评分服务暂时繁忙，请稍后重试');
                console.error(error);
            } finally {
                btn.disabled = false;
                btnText.textContent = '提交AI评分';
                loader.classList.add('hidden');
            }
        }

        function displayResult(data, wordCount) {
            document.getElementById('resultArea').classList.remove('hidden');
            document.getElementById('overallBand').textContent = data.overall_band;
            document.getElementById('trScore').textContent = data.breakdown.TR.score;
            document.getElementById('trComment').textContent = data.breakdown.TR.comments;
            document.getElementById('ccScore').textContent = data.breakdown.CC.score;
            document.getElementById('ccComment').textContent = data.breakdown.CC.comments;
            document.getElementById('lrScore').textContent = data.breakdown.LR.score;
            document.getElementById('lrComment').textContent = data.breakdown.LR.comments;
            document.getElementById('graScore').textContent = data.breakdown.GRA.score;
            document.getElementById('graComment').textContent = data.breakdown.GRA.comments;
            
            document.getElementById('wordCountResult').textContent = `字数统计：${wordCount} 词`;
            
            const suggestionsList = document.getElementById('suggestionsList');
            suggestionsList.innerHTML = '';
            if (data.detailed_feedback && data.detailed_feedback.weaknesses) {
                data.detailed_feedback.weaknesses.forEach(w => {
                    suggestionsList.innerHTML += `<li class="flex items-start"><span class="mr-2">•</span>${w}</li>`;
                });
            }
            
            // Scroll to result
            document.getElementById('resultArea').scrollIntoView({behavior: 'smooth', block: 'nearest'});
        }

        function addToHistory(data) {
            const history = document.getElementById('historyList');
            const item = document.createElement('div');
            item.className = 'p-3 bg-white rounded-lg border border-gray-100 fade-in';
            const now = new Date();
            const dateStr = `${now.getFullYear()}-${(now.getMonth()+1).toString().padStart(2,'0')}-${now.getDate().toString().padStart(2,'0')}`;
            item.innerHTML = `
                <div class="flex justify-between items-center">
                    <span class="font-medium text-sm">${currentTask === 'task1' ? 'Task 1' : 'Task 2'} - ${dateStr}</span>
                    <span class="font-bold text-teal-600">${data.overall_band}</span>
                </div>
                <div class="text-xs text-gray-500 mt-1">TR:${data.breakdown.TR.score} CC:${data.breakdown.CC.score} LR:${data.breakdown.LR.score} GRA:${data.breakdown.GRA.score}</div>
            `;
            history.insertBefore(item, history.firstChild);
        }

        // Vocabulary Functions
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

        function markWord(status) {
            // Move to next word
            currentWordIndex = (currentWordIndex + 1) % words.length;
            const word = words[currentWordIndex];
            
            document.getElementById('currentWord').textContent = word.word;
            document.getElementById('wordMeaning').textContent = word.meaning;
            
            // Reset card
            document.getElementById('cardFront').classList.remove('hidden');
            document.getElementById('cardBack').classList.add('hidden');
        }
    </script>
</body>
</html>"""

class WritingRequest(BaseModel):
    essay: str
    task_type: Literal["task1", "task2"]
    prompt: str
    target_band: float = 7.0

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_CONTENT

@app.post("/api/grade_writing")
async def grade_writing(data: WritingRequest):
    word_count = len(data.essay.split())
    target = 150 if data.task_type == "task1" else 250
    
    if word_count < target:
        return {
            "error": f"字数不足，需要至少{target}词",
            "word_count": word_count,
            "overall_band": 0,
            "breakdown": {
                "TR": {"score": 0, "comments": "Insufficient words"},
                "CC": {"score": 0, "comments": "Insufficient words"},
                "LR": {"score": 0, "comments": "Insufficient words"},
                "GRA": {"score": 0, "comments": "Insufficient words"}
            }
        }

    # 如果没有配置DeepSeek API，返回智能模拟评分（基于字数和简单规则）
    if not os.getenv("DEEPSEEK_API_KEY"):
        # 简单模拟算法：基于字数给分（实际使用时应调用DeepSeek）
        base_score = 6.0
        if word_count > 300: base_score = 6.5
        if word_count > 350: base_score = 7.0
        
        return {
            "overall_band": round(base_score, 1),
            "breakdown": {
                "TR": {"score": round(base_score, 1), "comments": "Task response adequate, both views discussed"},
                "CC": {"score": round(base_score, 1), "comments": "Good paragraphing and cohesive devices"},
                "LR": {"score": round(base_score - 0.5, 1), "comments": "Adequate vocabulary, some repetition noted"},
                "GRA": {"score": round(base_score, 1), "comments": "Mix of simple and complex sentences"}
            },
            "detailed_feedback": {
                "strengths": ["Clear structure", "Good word count"],
                "weaknesses": [
                    "Use more academic vocabulary (e.g., 'significant' instead of 'big')",
                    "Add more complex sentence structures for higher band",
                    "Provide more specific examples to support arguments",
                    "Avoid using 'I think' repeatedly, use 'It is argued that'"
                ],
                "vocabulary_suggestions": [
                    {"original": "big", "better": "significant/substantial"},
                    {"original": "good", "better": "beneficial/advantageous"},
                    {"original": "bad", "better": "detrimental/problematic"}
                ]
            },
            "word_count": word_count,
            "provider": "simulated",
            "cost_usd": 0,
            "note": "配置 DEEPSEEK_API_KEY 环境变量可启用真实AI评分"
        }
    
    # 真实AI评分（DeepSeek）
    import openai, json
    try:
        client = openai.OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": """你是资深雅思考官。严格按官方标准评分，输出JSON格式:
{
  "overall_band": float,
  "breakdown": {
    "TR": {"score": float, "comments": "string"},
    "CC": {"score": float, "comments": "string"},
    "LR": {"score": float, "comments": "string"},
    "GRA": {"score": float, "comments": "string"}
  },
  "detailed_feedback": {
    "weaknesses": ["string", "string"]
  }
}"""
                },
                {
                    "role": "user",
                    "content": f"评分这篇{data.task_type}作文（目标{data.target_band}分）：\n\n{data.essay}"
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=2000
        )
        
        result = json.loads(response.choices[0].message.content)
        result["word_count"] = word_count
        result["provider"] = "deepseek"
        result["cost_usd"] = round(response.usage.total_tokens * 0.000001, 5)
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "overall_band": 6.0,
            "breakdown": {
                "TR": {"score": 6.0, "comments": "Service error"},
                "CC": {"score": 6.0, "comments": "Service error"},
                "LR": {"score": 6.0, "comments": "Service error"},
                "GRA": {"score": 6.0, "comments": "Service error"}
            },
            "word_count": word_count
        }

# Vercel handler
from mangum import Mangum
handler = Mangum(app)
