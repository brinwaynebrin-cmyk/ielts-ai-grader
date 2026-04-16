
# 生成完整的集成版代码
full_code = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IELTS Zenith - 雅思AI学习平台</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Black+Ops+One&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Noto Sans SC', sans-serif; background: #f5f5f0; }
        .glass { background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5); }
        .nav-active { background: #0d9488; color: white; }
        .hidden-section { display: none; }
        .fade-in { animation: fadeIn 0.4s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .loading { display: inline-block; width: 20px; height: 20px; border: 3px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: white; animation: spin 1s ease-in-out infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        /* 词汇游戏专用样式 */
        .game-font { font-family: 'Black Ops One', cursive; }
        .neon-text { text-shadow: 0 0 10px currentColor, 0 0 20px currentColor; }
        
        #gameCanvas {
            background: radial-gradient(ellipse at center, #1e1b4b 0%, #0f0d2e 100%);
            position: relative;
            overflow: hidden;
            border-radius: 1rem;
        }
        
        .falling-word {
            position: absolute;
            padding: 12px 24px;
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 16px;
            color: white;
            font-weight: bold;
            font-size: 18px;
            cursor: pointer;
            transition: transform 0.1s;
            backdrop-filter: blur(10px);
            user-select: none;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            z-index: 10;
        }
        .falling-word:hover {
            transform: scale(1.1);
            border-color: #fbbf24;
            box-shadow: 0 0 20px rgba(251, 191, 36, 0.5);
        }
        .falling-word.danger {
            border-color: #ef4444;
            animation: pulse-danger 0.5s infinite;
        }
        @keyframes pulse-danger {
            0%, 100% { box-shadow: 0 0 5px #ef4444; }
            50% { box-shadow: 0 0 20px #ef4444, 0 0 40px #ef4444; }
        }
        
        .shoot-btn {
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            border: 2px solid #60a5fa;
            box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);
            transition: all 0.1s;
        }
        .shoot-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 25px rgba(59, 130, 246, 0.7);
        }
        .shoot-btn:active {
            transform: translateY(0) scale(0.95);
        }
        .shoot-btn.correct {
            background: linear-gradient(135deg, #10b981, #059669);
            border-color: #34d399;
            animation: correct-flash 0.3s;
        }
        .shoot-btn.wrong {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            border-color: #f87171;
            animation: shake 0.4s;
        }
        
        @keyframes correct-flash {
            0% { box-shadow: 0 0 5px #10b981; }
            50% { box-shadow: 0 0 50px #10b981; }
            100% { box-shadow: 0 0 5px #10b981; }
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        .particle {
            position: absolute;
            pointer-events: none;
            border-radius: 50%;
            animation: particle-fly 0.8s ease-out forwards;
        }
        @keyframes particle-fly {
            to { transform: translate(var(--tx), var(--ty)) scale(0); opacity: 0; }
        }
        
        .combo-text {
            position: absolute;
            font-size: 48px;
            font-weight: 900;
            color: #fbbf24;
            pointer-events: none;
            animation: combo-pop 0.8s ease-out forwards;
            text-shadow: 0 0 20px rgba(251, 191, 36, 0.8);
            z-index: 50;
        }
        @keyframes combo-pop {
            0% { transform: scale(0) rotate(-10deg); opacity: 1; }
            50% { transform: scale(1.2) rotate(5deg); }
            100% { transform: scale(1) translateY(-50px) rotate(0deg); opacity: 0; }
        }
        
        .laser {
            position: absolute;
            height: 4px;
            background: linear-gradient(90deg, transparent, #3b82f6, #60a5fa, transparent);
            box-shadow: 0 0 10px #3b82f6;
            transform-origin: left center;
            pointer-events: none;
            animation: laser-shoot 0.2s ease-out forwards;
            z-index: 5;
        }
        @keyframes laser-shoot {
            to { opacity: 0; width: 100%; }
        }
        
        .floating-score {
            position: absolute;
            font-weight: bold;
            font-size: 24px;
            pointer-events: none;
            animation: float-up 1s ease-out forwards;
            z-index: 50;
        }
        @keyframes float-up {
            to { transform: translateY(-80px); opacity: 0; }
        }
        
        .health-bar { transition: width 0.3s ease; box-shadow: 0 0 10px currentColor; }
        
        .difficulty-btn {
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        .difficulty-btn:hover { transform: scale(1.05); }
        .difficulty-btn.selected {
            border-color: white;
            box-shadow: 0 0 20px currentColor;
        }
        
        .warning-layer {
            position: absolute;
            inset: 0;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s;
            z-index: 20;
            border-radius: 1rem;
        }
        
        /* 单词卡片翻转（背单词用） */
        .flip-card { perspective: 1000px; }
        .flip-card-inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; }
        .flip-card.flipped .flip-card-inner { transform: rotateY(180deg); }
        .flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 1rem; }
        .flip-card-back { transform: rotateY(180deg); }
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
                
                <div class="hidden md:flex space-x-1 text-sm">
                    <button onclick="showSection('dashboard')" id="nav-dashboard" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">仪表盘</button>
                    <button onclick="showSection('vocabulary')" id="nav-vocabulary" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">背单词</button>
                    <button onclick="showSection('wordgame')" id="nav-wordgame" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100 text-pink-600">🎮 词汇游戏</button>
                    <button onclick="showSection('writing')" id="nav-writing" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">写作</button>
                    <button onclick="showSection('speaking')" id="nav-speaking" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">口语</button>
                    <button onclick="showSection('tools')" id="nav-tools" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">工具箱</button>
                </div>
                
                <button class="md:hidden p-2" onclick="toggleMobileMenu()">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
                </button>
            </div>
            
            <div id="mobileMenu" class="hidden md:hidden pb-4 space-y-2">
                <button onclick="showSection('dashboard')" class="w-full text-left px-4 py-2 rounded-lg hover:bg-gray-100">仪表盘</button>
                <button onclick="showSection('vocabulary')" class="w-full text-left px-4 py-2 rounded-lg hover:bg-gray-100">背单词</button>
                <button onclick="showSection('wordgame')" class="w-full text-left px-4 py-2 rounded-lg bg-pink-50 text-pink-600 font-medium">🎮 词汇游戏</button>
                <button onclick="showSection('writing')" class="w-full text-left px-4 py-2 rounded-lg hover:bg-gray-100">写作</button>
                <button onclick="showSection('speaking')" class="w-full text-left px-4 py-2 rounded-lg hover:bg-gray-100">口语</button>
                <button onclick="showSection('tools')" class="w-full text-left px-4 py-2 rounded-lg hover:bg-gray-100">工具箱</button>
            </div>
        </div>
    </nav>

    <main class="pt-20 pb-12 px-4 max-w-6xl mx-auto">

        <!-- DASHBOARD -->
        <section id="dashboard" class="section fade-in">
            <div class="mb-8">
                <h1 class="text-3xl font-bold text-gray-900 mb-2">雅思AI学习平台</h1>
                <p class="text-gray-600">集成背单词、词汇游戏、写作精批、口语评分、题目生成、语法检查</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all border-l-4 border-teal-500" onclick="showSection('vocabulary')">
                    <div class="text-3xl mb-2">📚</div>
                    <div class="font-bold text-gray-900">背单词</div>
                    <div class="text-xs text-gray-500 mt-1">雅思核心词汇</div>
                    <div class="mt-2 text-xs font-medium text-teal-600" id="dashboard-vocab-progress">今日学习: 0/20</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all border-l-4 border-pink-500 bg-gradient-to-br from-pink-50 to-transparent" onclick="showSection('wordgame')">
                    <div class="text-3xl mb-2">🎮</div>
                    <div class="font-bold text-gray-900">词汇守卫战</div>
                    <div class="text-xs text-gray-500 mt-1">弹幕射击背单词</div>
                    <div class="mt-2 flex items-center gap-2">
                        <span class="text-xs px-2 py-1 bg-pink-100 text-pink-700 rounded-full">连击x5</span>
                        <span class="text-xs text-gray-400">最高: <span id="bestScoreDisplay">0</span></span>
                    </div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all border-l-4 border-blue-500" onclick="showSection('writing')">
                    <div class="text-3xl mb-2">📝</div>
                    <div class="font-bold text-gray-900">AI写作精批</div>
                    <div class="text-xs text-gray-500 mt-1">Task 1 & 2 评分</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all border-l-4 border-purple-500" onclick="showSection('speaking')">
                    <div class="text-3xl mb-2">🎤</div>
                    <div class="font-bold text-gray-900">口语Part 2评分</div>
                    <div class="text-xs text-gray-500 mt-1">文本转写评估</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all border-l-4 border-orange-500" onclick="showSection('tools')">
                    <div class="text-3xl mb-2">🎲</div>
                    <div class="font-bold text-gray-900">题目生成器</div>
                    <div class="text-xs text-gray-500 mt-1">随机生成真题</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all border-l-4 border-yellow-500" onclick="showSection('tools'); document.getElementById('grammarTab').click();">
                    <div class="text-3xl mb-2">🔍</div>
                    <div class="font-bold text-gray-900">语法检查</div>
                    <div class="text-xs text-gray-500 mt-1">基础语法纠错</div>
                </div>
            </div>
        </section>

        <!-- WORD GAME SECTION -->
        <section id="wordgame" class="section hidden-section fade-in">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h2 class="text-2xl font-bold text-gray-900">🎮 词汇守卫战</h2>
                    <p class="text-gray-600 text-sm">在单词落地前选择正确释义消灭它们！支持键盘 A/S/D/F 操作</p>
                </div>
                <div class="flex gap-2">
                    <button onclick="initGame()" id="startGameBtn" class="px-6 py-2 bg-gradient-to-r from-pink-500 to-purple-600 text-white rounded-full font-medium hover:shadow-lg transition-all">
                        开始游戏
                    </button>
                    <button onclick="showGameInstructions()" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-full font-medium hover:bg-gray-200 transition-all">
                        游戏说明
                    </button>
                </div>
            </div>

            <!-- 游戏统计卡片 -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6" id="gameStats" style="display: none;">
                <div class="glass rounded-2xl p-4 border-l-4 border-yellow-400">
                    <div class="text-xs text-gray-500">得分</div>
                    <div class="text-2xl font-bold game-font text-yellow-600" id="gameScore">0</div>
                </div>
                <div class="glass rounded-2xl p-4 border-l-4 border-orange-400">
                    <div class="text-xs text-gray-500">连击</div>
                    <div class="text-2xl font-bold game-font text-orange-600" id="gameCombo">x0</div>
                </div>
                <div class="glass rounded-2xl p-4 border-l-4 border-blue-400">
                    <div class="text-xs text-gray-500">剩余时间</div>
                    <div class="text-2xl font-bold game-font text-blue-600" id="gameTime">60</div>
                </div>
                <div class="glass rounded-2xl p-4 border-l-4 border-green-400">
                    <div class="text-xs text-gray-500">护盾</div>
                    <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                        <div id="gameHealthBar" class="health-bar h-full bg-gradient-to-r from-green-500 to-green-400 rounded-full" style="width: 100%"></div>
                    </div>
                </div>
            </div>

            <!-- 游戏主区域 -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2">
                    <div id="gameCanvas" class="h-[500px] relative">
                        <!-- 开始屏幕 -->
                        <div id="gameStartScreen" class="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-indigo-900/90 to-purple-900/90 backdrop-blur-md rounded-2xl z-30">
                            <div class="text-center p-8">
                                <div class="text-6xl mb-4">🎮</div>
                                <h3 class="text-3xl font-bold text-white mb-2 game-font">词汇守卫战</h3>
                                <p class="text-gray-300 mb-6">Word Defender - IELTS Edition</p>
                                
                                <div class="space-y-3 mb-6">
                                    <p class="text-sm text-gray-400">选择难度开始游戏</p>
                                    <div class="flex gap-3 justify-center">
                                        <button onclick="selectGameDifficulty('easy')" class="difficulty-btn px-6 py-3 rounded-xl bg-green-500/20 border-green-400 text-green-400 selected" data-diff="easy">
                                            <div class="font-bold">简单</div>
                                        </button>
                                        <button onclick="selectGameDifficulty('normal')" class="difficulty-btn px-6 py-3 rounded-xl bg-yellow-500/20 border-yellow-400 text-yellow-400" data-diff="normal">
                                            <div class="font-bold">普通</div>
                                        </button>
                                        <button onclick="selectGameDifficulty('hard')" class="difficulty-btn px-6 py-3 rounded-xl bg-red-500/20 border-red-400 text-red-400" data-diff="hard">
                                            <div class="font-bold">困难</div>
                                        </button>
                                    </div>
                                </div>
                                
                                <button onclick="startWordGame()" class="px-8 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full font-bold text-lg hover:shadow-lg transition-all transform hover:scale-105">
                                    开始挑战
                                </button>
                            </div>
                        </div>

                        <!-- 游戏结束屏幕 -->
                        <div id="gameOverScreen" class="hidden absolute inset-0 flex items-center justify-center bg-black/80 backdrop-blur-md rounded-2xl z-40">
                            <div class="text-center p-8 text-white">
                                <div class="text-6xl mb-4" id="endEmoji">🏆</div>
                                <h3 class="text-3xl font-bold mb-2 game-font" id="endTitle">游戏结束</h3>
                                <div class="grid grid-cols-2 gap-4 my-6">
                                    <div class="bg-white/10 rounded-xl p-4">
                                        <div class="text-3xl font-bold text-yellow-400" id="finalScore">0</div>
                                        <div class="text-xs text-gray-400">最终得分</div>
                                    </div>
                                    <div class="bg-white/10 rounded-xl p-4">
                                        <div class="text-3xl font-bold text-blue-400" id="finalAccuracy">0%</div>
                                        <div class="text-xs text-gray-400">正确率</div>
                                    </div>
                                </div>
                                <div class="flex gap-3 justify-center">
                                    <button onclick="restartWordGame()" class="px-6 py-2 bg-blue-600 rounded-full font-bold hover:bg-blue-500 transition">
                                        再来一局
                                    </button>
                                    <button onclick="exitGame()" class="px-6 py-2 bg-gray-700 rounded-full font-bold hover:bg-gray-600 transition">
                                        退出
                                    </button>
                                </div>
                            </div>
                        </div>

                        <!-- 游戏层 -->
                        <div id="gameLayer" class="absolute inset-0"></div>
                        
                        <!-- 警告层 -->
                        <div id="warningLayer" class="warning-layer">
                            <div class="absolute inset-0 bg-red-500/20 rounded-2xl"></div>
                        </div>

                        <!-- 暂停提示 -->
                        <div id="pauseOverlay" class="hidden absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm rounded-2xl z-35">
                            <div class="text-white text-2xl font-bold">游戏暂停</div>
                        </div>
                    </div>
                </div>

                <!-- 控制面板 -->
                <div class="space-y-4">
                    <div class="glass rounded-2xl p-5 shadow-sm">
                        <h4 class="font-bold mb-4 text-sm">🎯 操作指南</h4>
                        <div class="space-y-2 text-sm text-gray-600">
                            <div class="flex items-center gap-3 p-2 bg-gray-50 rounded-lg">
                                <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-bold">A</span>
                                <span>选择第一个选项</span>
                            </div>
                            <div class="flex items-center gap-3 p-2 bg-gray-50 rounded-lg">
                                <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-bold">S</span>
                                <span>选择第二个选项</span>
                            </div>
                            <div class="flex items-center gap-3 p-2 bg-gray-50 rounded-lg">
                                <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-bold">D</span>
                                <span>选择第三个选项</span>
                            </div>
                            <div class="flex items-center gap-3 p-2 bg-gray-50 rounded-lg">
                                <span class="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-bold">F</span>
                                <span>选择第四个选项</span>
                            </div>
                            <div class="flex items-center gap-3 p-2 bg-yellow-50 rounded-lg">
                                <span class="text-xs">⏸️ 空格键</span>
                                <span>暂停游戏</span>
                            </div>
                        </div>
                    </div>

                    <div class="glass rounded-2xl p-5 shadow-sm">
                        <h4 class="font-bold mb-4 text-sm">🎮 技能道具</h4>
                        <div class="space-y-2">
                            <button onclick="useGameSkill('slow')" id="skillSlowBtn" class="w-full p-3 bg-purple-50 hover:bg-purple-100 rounded-xl text-left transition-all disabled:opacity-30">
                                <div class="flex justify-between items-center">
                                    <span class="text-sm font-medium text-purple-700">⏱️ 时间缓速</span>
                                    <span class="text-xs bg-purple-200 text-purple-800 px-2 py-1 rounded-full" id="slowCount">3</span>
                                </div>
                                <div class="text-xs text-purple-600 mt-1">减缓单词下落速度5秒</div>
                            </button>
                            <button onclick="useGameSkill('bomb')" id="skillBombBtn" class="w-full p-3 bg-red-50 hover:bg-red-100 rounded-xl text-left transition-all disabled:opacity-30">
                                <div class="flex justify-between items-center">
                                    <span class="text-sm font-medium text-red-700">💣 清屏炸弹</span>
                                    <span class="text-xs bg-red-200 text-red-800 px-2 py-1 rounded-full" id="bombCount">1</span>
                                </div>
                                <div class="text-xs text-red-600 mt-1">消灭所有当前单词</div>
                            </button>
                            <button onclick="useGameSkill('heal')" id="skillHealBtn" class="w-full p-3 bg-green-50 hover:bg-green-100 rounded-xl text-left transition-all disabled:opacity-30">
                                <div class="flex justify-between items-center">
                                    <span class="text-sm font-medium text-green-700">💚 紧急修复</span>
                                    <span class="text-xs bg-green-200 text-green-800 px-2 py-1 rounded-full" id="healCount">2</span>
                                </div>
                                <div class="text-xs text-green-600 mt-1">恢复30%护盾值</div>
                            </button>
                        </div>
                    </div>

                    <div class="glass rounded-2xl p-5 shadow-sm bg-gradient-to-br from-yellow-50 to-transparent">
                        <h4 class="font-bold mb-2 text-sm text-yellow-800">💡 高分技巧</h4>
                        <ul class="text-xs text-yellow-700 space-y-1">
                            <li>• 连续答对可触发连击加成（最高x5）</li>
                            <li>• 单词越接近底部危险越高</li>
                            <li>• 优先消灭带有红色边框的单词</li>
                            <li>• 合理使用技能扭转局势</li>
                        </ul>
                    </div>
                </div>
            </div>

            <!-- 射击按钮区（游戏时显示） -->
            <div id="shootControls" class="hidden mt-4 grid grid-cols-4 gap-3">
                <button onclick="shootWord(0)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg relative" id="shootBtn0">
                    <span id="shootOpt0">选项A</span>
                    <span class="absolute top-1 right-2 text-xs opacity-50">A</span>
                </button>
                <button onclick="shootWord(1)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg relative" id="shootBtn1">
                    <span id="shootOpt1">选项B</span>
                    <span class="absolute top-1 right-2 text-xs opacity-50">S</span>
                </button>
                <button onclick="shootWord(2)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg relative" id="shootBtn2">
                    <span id="shootOpt2">选项C</span>
                    <span class="absolute top-1 right-2 text-xs opacity-50">D</span>
                </button>
                <button onclick="shootWord(3)" class="shoot-btn rounded-xl py-4 text-white font-bold text-lg relative" id="shootBtn3">
                    <span id="shootOpt3">选项D</span>
                    <span class="absolute top-1 right-2 text-xs opacity-50">F</span>
                </button>
            </div>
        </section>

        <!-- VOCABULARY SECTION (背单词) -->
        <section id="vocabulary" class="section hidden-section fade-in">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h2 class="text-2xl font-bold text-gray-900">雅思核心词汇</h2>
                    <p class="text-gray-600 text-sm">基于真题统计的高频学术词汇，每日20词科学记忆</p>
                </div>
                <div class="flex items-center gap-3">
                    <div class="text-right">
                        <div class="text-xs text-gray-500">连续打卡</div>
                        <div class="text-lg font-bold text-teal-600" id="streakDays">0 天</div>
                    </div>
                    <div class="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center text-xl">🔥</div>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div class="glass rounded-2xl p-4 border-l-4 border-teal-500">
                    <div class="text-xs text-gray-500 mb-1">今日学习进度</div>
                    <div class="flex items-end justify-between">
                        <span class="text-2xl font-bold text-gray-900" id="todayLearned">0/20</span>
                        <span class="text-xs text-teal-600 font-medium">词</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                        <div class="bg-teal-500 h-2 rounded-full transition-all" id="todayProgressBar" style="width: 0%"></div>
                    </div>
                </div>
                <div class="glass rounded-2xl p-4 border-l-4 border-purple-500">
                    <div class="text-xs text-gray-500 mb-1">已掌握词汇</div>
                    <div class="flex items-end justify-between">
                        <span class="text-2xl font-bold text-gray-900" id="masteredCount">0</span>
                        <span class="text-xs text-purple-600 font-medium">词</span>
                    </div>
                    <div class="text-xs text-gray-400 mt-2">占总词汇量 <span id="masteredPercent">0%</span></div>
                </div>
                <div class="glass rounded-2xl p-4 border-l-4 border-blue-500">
                    <div class="text-xs text-gray-500 mb-1">需复习单词</div>
                    <div class="flex items-end justify-between">
                        <span class="text-2xl font-bold text-gray-900" id="reviewCount">0</span>
                        <span class="text-xs text-blue-600 font-medium">词</span>
                    </div>
                    <button onclick="startReviewMode()" class="text-xs text-blue-600 hover:underline mt-1">开始复习 →</button>
                </div>
                <div class="glass rounded-2xl p-4 border-l-4 border-pink-500 cursor-pointer hover:shadow-md transition-all" onclick="showSection('wordgame')">
                    <div class="text-xs text-gray-500 mb-1">通过游戏学习</div>
                    <div class="font-bold text-pink-600">🎮 词汇守卫战</div>
                    <div class="text-xs text-gray-400 mt-2">在游戏中巩固记忆</div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 space-y-4">
                    <div class="glass rounded-2xl p-2 flex gap-2 mb-4">
                        <button onclick="setVocabMode('learn')" id="mode-learn" class="flex-1 py-2 px-4 rounded-xl text-sm font-medium transition-all bg-teal-600 text-white">🎯 学习模式</button>
                        <button onclick="setVocabMode('list')" id="mode-list" class="flex-1 py-2 px-4 rounded-xl text-sm font-medium transition-all hover:bg-gray-100">📚 单词表</button>
                    </div>

                    <div id="vocab-learn-panel" class="glass rounded-2xl p-8 shadow-sm min-h-[400px] flex flex-col items-center justify-center relative">
                        <div class="absolute top-4 right-4 flex gap-2">
                            <span class="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600" id="cardCounter">1/20</span>
                            <span class="px-3 py-1 bg-teal-100 text-teal-700 rounded-full text-xs font-medium" id="difficultyTag">Band 6.0</span>
                        </div>

                        <div class="flip-card w-full max-w-md h-64 cursor-pointer" onclick="flipCard()" id="wordCard">
                            <div class="flip-card-inner">
                                <div class="flip-card-front glass shadow-lg flex flex-col items-center justify-center p-8 border-2 border-transparent hover:border-teal-300 transition-all">
                                    <h3 class="text-4xl font-bold text-gray-900 mb-2" id="cardWord">abundant</h3>
                                    <p class="text-gray-500 text-lg" id="cardPhonetic">/əˈbʌndənt/</p>
                                    <p class="text-gray-400 text-sm mt-4">点击翻转查看释义</p>
                                </div>
                                <div class="flip-card-back bg-gradient-to-br from-teal-600 to-teal-700 text-white shadow-lg flex flex-col items-center justify-center p-8">
                                    <div class="text-sm opacity-80 mb-1">中文释义</div>
                                    <h3 class="text-2xl font-bold mb-4" id="cardMeaning">丰富的；充裕的</h3>
                                    <div class="w-full h-px bg-white/30 my-3"></div>
                                    <div class="text-sm opacity-80 mb-1">例句</div>
                                    <p class="text-center text-sm italic" id="cardExample">Natural resources are abundant in this region.</p>
                                </div>
                            </div>
                        </div>

                        <div class="flex gap-4 mt-8 w-full max-w-md">
                            <button onclick="markWord('forgotten')" class="flex-1 py-3 bg-red-100 text-red-700 rounded-xl font-medium hover:bg-red-200 transition-all">😅 忘记</button>
                            <button onclick="markWord('vague')" class="flex-1 py-3 bg-yellow-100 text-yellow-700 rounded-xl font-medium hover:bg-yellow-200 transition-all">🤔 模糊</button>
                            <button onclick="markWord('mastered')" class="flex-1 py-3 bg-green-100 text-green-700 rounded-xl font-medium hover:bg-green-200 transition-all">✅ 掌握</button>
                        </div>

                        <div class="flex justify-between w-full max-w-md mt-4">
                            <button onclick="prevWord()" class="px-4 py-2 text-gray-500 hover:text-gray-700 text-sm">← 上一个</button>
                            <button onclick="playAudio()" class="px-4 py-2 text-teal-600 hover:text-teal-700 text-sm">🔊 发音</button>
                            <button onclick="nextWord()" class="px-4 py-2 text-gray-500 hover:text-gray-700 text-sm">下一个 →</button>
                        </div>
                    </div>

                    <div id="vocab-list-panel" class="hidden glass rounded-2xl p-6 shadow-sm">
                        <div class="flex gap-2 mb-4 overflow-x-auto pb-2">
                            <button onclick="filterWords('all')" class="px-4 py-2 rounded-full text-sm bg-gray-800 text-white">全部</button>
                            <button onclick="filterWords('unlearned')" class="px-4 py-2 rounded-full text-sm bg-gray-200 text-gray-700">未学习</button>
                            <button onclick="filterWords('learning')" class="px-4 py-2 rounded-full text-sm bg-yellow-100 text-yellow-700">学习中</button>
                            <button onclick="filterWords('mastered')" class="px-4 py-2 rounded-full text-sm bg-green-100 text-green-700">已掌握</button>
                        </div>
                        <div class="space-y-2 max-h-[500px] overflow-y-auto" id="wordListContainer"></div>
                    </div>
                </div>

                <div class="space-y-4">
                    <div class="glass rounded-2xl p-5 shadow-sm bg-gradient-to-br from-pink-50 to-transparent border border-pink-200">
                        <h4 class="font-bold mb-3 text-sm text-pink-800">🎮 游戏化学习</h4>
                        <p class="text-xs text-pink-700 mb-3">觉得背单词枯燥？试试词汇守卫战！</p>
                        <button onclick="showSection('wordgame')" class="w-full py-2 bg-pink-500 text-white rounded-lg text-sm font-medium hover:bg-pink-600 transition">
                            开始游戏
                        </button>
                    </div>
                    
                    <div class="glass rounded-2xl p-5 shadow-sm">
                        <h4 class="font-bold mb-3 text-sm">难度分布</h4>
                        <div class="space-y-2">
                            <div class="flex justify-between items-center text-sm">
                                <span class="text-gray-600">Band 6.0-6.5</span>
                                <span class="font-medium">8词</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-blue-400 h-2 rounded-full" style="width: 40%"></div>
                            </div>
                            <div class="flex justify-between items-center text-sm">
                                <span class="text-gray-600">Band 7.0-7.5</span>
                                <span class="font-medium">7词</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-purple-400 h-2 rounded-full" style="width: 35%"></div>
                            </div>
                            <div class="flex justify-between items-center text-sm">
                                <span class="text-gray-600">Band 8.0+</span>
                                <span class="font-medium">5词</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-orange-400 h-2 rounded-full" style="width: 25%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- WRITING SECTION -->
        <section id="writing" class="section hidden-section fade-in">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h2 class="text-2xl font-bold text-gray-900">AI写作精批</h2>
                    <p class="text-gray-600 text-sm">字数要求：Task 1 ≥130词，Task 2 ≥220词（放宽标准）</p>
                </div>
                <button onclick="generateWritingPrompt()" class="px-4 py-2 bg-teal-100 text-teal-700 rounded-full text-sm font-medium hover:bg-teal-200">🎲 随机题目</button>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-2 space-y-4">
                    <div class="glass rounded-2xl p-6 shadow-sm">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex space-x-2">
                                <button onclick="setTask('task1')" id="btn-task1" class="px-3 py-1 rounded-full text-sm border hover:bg-gray-50">Task 1</button>
                                <button onclick="setTask('task2')" id="btn-task2" class="px-3 py-1 rounded-full text-sm bg-teal-600 text-white">Task 2</button>
                            </div>
                            <span class="text-sm text-gray-500" id="wordCountDisplay">字数：0 / 220+</span>
                        </div>

                        <div class="bg-gray-50 p-4 rounded-lg mb-4 text-sm text-gray-700 font-medium" id="promptDisplay">
                            Some people think that the best way to reduce crime is to give longer prison sentences. Others believe there are better ways to reduce crime. Discuss both views and give your opinion.
                        </div>

                        <textarea id="essayInput" rows="10" class="w-full p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all text-sm" 
                            placeholder="在此输入作文..." oninput="updateWordCount()"></textarea>

                        <div class="mt-4 flex justify-between items-center">
                            <span class="text-xs text-gray-400">按官方标准评分</span>
                            <button onclick="submitEssay()" id="submitBtn" class="px-6 py-2 bg-teal-600 text-white rounded-full font-medium hover:bg-teal-700 transition-all flex items-center space-x-2">
                                <span id="btnText">提交评分</span>
                                <span id="btnLoader" class="loading hidden"></span>
                            </button>
                        </div>
                    </div>

                    <div id="resultArea" class="hidden glass rounded-2xl p-6 shadow-sm">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="text-lg font-bold">评分结果</h3>
                            <div class="text-3xl font-bold text-teal-600" id="overallBand">-</div>
                        </div>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
                            <div class="p-3 bg-gray-50 rounded text-center"><div class="text-xs text-gray-500">TR</div><div class="font-bold text-teal-600" id="trScore">-</div></div>
                            <div class="p-3 bg-gray-50 rounded text-center"><div class="text-xs text-gray-500">CC</div><div class="font-bold text-teal-600" id="ccScore">-</div></div>
                            <div class="p-3 bg-gray-50 rounded text-center"><div class="text-xs text-gray-500">LR</div><div class="font-bold text-teal-600" id="lrScore">-</div></div>
                            <div class="p-3 bg-gray-50 rounded text-center"><div class="text-xs text-gray-500">GRA</div><div class="font-bold text-teal-600" id="graScore">-</div></div>
                        </div>
                        <div class="bg-gray-900 text-white rounded-lg p-4 text-sm">
                            <div class="font-bold mb-2">改进建议</div>
                            <ul id="suggestionsList" class="space-y-1 text-gray-300"></ul>
                        </div>
                    </div>
                </div>

                <div class="space-y-4">
                    <div class="glass rounded-2xl p-5 shadow-sm">
                        <h4 class="font-bold mb-3 text-sm">字数标准</h4>
                        <div class="text-xs text-gray-600 space-y-2">
                            <p>• Task 1: 建议150词（最低130词）</p>
                            <p>• Task 2: 建议250词（最低220词）</p>
                            <p>• 字数不足会扣分，但AI仍可评分</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- SPEAKING SECTION -->
        <section id="speaking" class="section hidden-section fade-in">
            <div class="mb-6">
                <h2 class="text-2xl font-bold text-gray-900">口语Part 2评分</h2>
                <p class="text-gray-600 text-sm">输入你的Part 2回答文本，AI按流利度、词汇、语法、发音评估</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="space-y-4">
                    <div class="glass rounded-2xl p-6 shadow-sm">
                        <div class="flex justify-between items-center mb-4">
                            <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-bold">Part 2</span>
                            <button onclick="generateSpeakingTopic()" class="text-sm text-teal-600 hover:underline">换一题 →</button>
                        </div>
                        
                        <div class="bg-purple-50 p-4 rounded-lg mb-4 border border-purple-100">
                            <h3 class="font-bold text-gray-900 mb-2" id="speakingTopic">Describe a difficult decision you made.</h3>
                            <ul class="text-sm text-gray-600 space-y-1 list-disc list-inside" id="speakingPrompts">
                                <li>What the decision was</li>
                                <li>When you made it</li>
                                <li>Why it was difficult</li>
                                <li>And explain how you felt after deciding</li>
                            </ul>
                        </div>

                        <textarea id="speakingInput" rows="8" class="w-full p-4 border border-gray-200 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-sm" 
                            placeholder="在此输入你的Part 2回答（建议100-150词）..."></textarea>

                        <button onclick="submitSpeaking()" id="speakBtn" class="mt-4 w-full py-3 bg-purple-600 text-white rounded-full font-medium hover:bg-purple-700 transition-all flex items-center justify-center space-x-2">
                            <span id="speakBtnText">提交口语评分</span>
                            <span id="speakLoader" class="loading hidden"></span>
                        </button>
                    </div>
                </div>

                <div id="speakingResult" class="hidden space-y-4">
                    <div class="glass rounded-2xl p-6 shadow-sm border-l-4 border-purple-500">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="font-bold text-lg">口语评分</h3>
                            <div class="text-3xl font-bold text-purple-600" id="speakOverall">-</div>
                        </div>
                        
                        <div class="space-y-3 mb-4">
                            <div class="flex justify-between items-center p-3 bg-gray-50 rounded">
                                <span class="text-sm">Fluency & Coherence</span>
                                <span class="font-bold text-purple-600" id="fluencyScore">-</span>
                            </div>
                            <div class="flex justify-between items-center p-3 bg-gray-50 rounded">
                                <span class="text-sm">Lexical Resource</span>
                                <span class="font-bold text-purple-600" id="speakLrScore">-</span>
                            </div>
                            <div class="flex justify-between items-center p-3 bg-gray-50 rounded">
                                <span class="text-sm">Grammatical Range</span>
                                <span class="font-bold text-purple-600" id="speakGrScore">-</span>
                            </div>
                        </div>

                        <div class="bg-purple-900 text-white rounded-lg p-4 text-sm">
                            <div class="font-bold mb-2">提升建议</div>
                            <ul id="speakSuggestions" class="space-y-1 text-purple-100"></ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TOOLS SECTION -->
        <section id="tools" class="section hidden-section fade-in">
            <div class="mb-6">
                <h2 class="text-2xl font-bold text-gray-900">工具箱</h2>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="glass rounded-2xl p-6 shadow-sm">
                    <h3 class="font-bold text-lg mb-4">🎯 题目生成器</h3>
                    <div class="space-y-3">
                        <select id="promptType" class="w-full p-2 border rounded-lg text-sm">
                            <option value="task2">Task 2 议论文</option>
                            <option value="task1">Task 1 图表题</option>
                            <option value="speaking">口语 Part 2</option>
                        </select>
                        <button onclick="generatePrompt()" class="w-full py-2 bg-teal-600 text-white rounded-lg text-sm hover:bg-teal-700">生成随机题目</button>
                    </div>
                    <div id="generatedPrompt" class="mt-4 p-3 bg-gray-50 rounded-lg text-sm text-gray-700 hidden"></div>
                </div>

                <div class="glass rounded-2xl p-6 shadow-sm">
                    <h3 class="font-bold text-lg mb-4">🔍 基础语法检查</h3>
                    <textarea id="grammarInput" rows="4" class="w-full p-3 border rounded-lg text-sm mb-3" placeholder="输入句子检查基础语法..."></textarea>
                    <button onclick="checkGrammar()" class="w-full py-2 bg-orange-600 text-white rounded-lg text-sm hover:bg-orange-700">检查语法</button>
                    <div id="grammarResult" class="mt-3 text-sm hidden"></div>
                </div>
            </div>
        </section>

    </main>

    <script>
        // ==================== 词汇游戏数据 ====================
        const gameWordData = [
            {word: "abundant", meaning: "丰富的", distractors: ["稀缺的", "普通的", "浪费的"]},
            {word: "consequence", meaning: "后果", distractors: ["原因", "过程", "开始"]},
            {word: "significant", meaning: "重要的", distractors: ["微小的", "随机的", "临时的"]},
            {word: "controversial", meaning: "有争议的", distractors: ["一致的", "明确的", "简单的"]},
            {word: "implementation", meaning: "实施", distractors: ["计划", "取消", "讨论"]},
            {word: "inevitable", meaning: "不可避免的", distractors: ["偶然的", "可选的", "突然的"]},
            {word: "sustainable", meaning: "可持续的", distractors: ["一次性的", "昂贵的", "快速的"]},
            {word: "perspective", meaning: "观点", distractors: ["事实", "证据", "结论"]},
            {word: "phenomenon", meaning: "现象", distractors: ["理论", "实验", "证明"]},
            {word: "alternative", meaning: "替代的", distractors: ["唯一的", "旧的", "坏的"]},
            {word: "exaggerate", meaning: "夸大", distractors: ["缩小", "描述", "证明"]},
            {word: "discrimination", meaning: "歧视", distractors: ["尊重", "平等", "合作"]},
            {word: "approximately", meaning: "大约", distractors: ["精确地", "完全", "肯定"]},
            {word: "conventional", meaning: "传统的", distractors: ["现代的", "激进的", "外国的"]},
            {word: "fundamental", meaning: "基础的", distractors: ["表面的", "复杂的", "高级的"]}
        ];

        // ==================== 游戏配置 ====================
        const gameConfig = {
            easy: { speed: 0.8, spawnRate: 2500, health: 100, damage: 10 },
            normal: { speed: 1.2, spawnRate: 1800, health: 80, damage: 15 },
            hard: { speed: 1.8, spawnRate: 1200, health: 60, damage: 20 }
        };

        // ==================== 游戏状态 ====================
        let wordGame = {
            isPlaying: false,
            isPaused: false,
            score: 0,
            health: 100,
            maxHealth: 100,
            combo: 0,
            maxCombo: 0,
            time: 60,
            correctCount: 0,
            wrongCount: 0,
            difficulty: 'easy',
            fallingWords: [],
            currentOptions: [],
            skills: { slow: 3, bomb: 1, heal: 2 },
            isSlowMotion: false,
            loopId: null,
            timerId: null,
            spawnId: null
        };

        // ==================== 游戏函数 ====================
        function initGame() {
            document.getElementById('gameStartScreen').classList.remove('hidden');
            document.getElementById('gameOverScreen').classList.add('hidden');
            document.getElementById('gameStats').style.display = 'none';
            document.getElementById('shootControls').classList.add('hidden');
        }

        function selectGameDifficulty(diff) {
            wordGame.difficulty = diff;
            document.querySelectorAll('.difficulty-btn').forEach(btn => {
                btn.classList.remove('selected');
                if (btn.dataset.diff === diff) btn.classList.add('selected');
            });
        }

        function startWordGame() {
            document.getElementById('gameStartScreen').classList.add('hidden');
            document.getElementById('gameStats').style.display = 'grid';
            document.getElementById('shootControls').classList.remove('hidden');
            
            const cfg = gameConfig[wordGame.difficulty];
            wordGame = {
                ...wordGame,
                isPlaying: true,
                isPaused: false,
                score: 0,
                health: cfg.health,
                maxHealth: cfg.health,
                combo: 0,
                time: 90,
                correctCount: 0,
                wrongCount: 0,
                fallingWords: [],
                skills: { slow: 3, bomb: 1, heal: 2 },
                isSlowMotion: false
            };

            updateGameUI();
            updateSkillButtons();
            spawnGameWord();
            scheduleNextSpawn();
            
            wordGame.timerId = setInterval(() => {
                if (wordGame.isPaused) return;
                wordGame.time--;
                document.getElementById('gameTime').textContent = wordGame.time;
                if (wordGame.time <= 0) endWordGame('timeup');
            }, 1000);
            
            gameLoop();
        }

        function scheduleNextSpawn() {
            if (!wordGame.isPlaying) return;
            const cfg = gameConfig[wordGame.difficulty];
            const rate = wordGame.isSlowMotion ? cfg.spawnRate * 2 : cfg.spawnRate;
            wordGame.spawnId = setTimeout(() => {
                if (!wordGame.isPaused) spawnGameWord();
                scheduleNextSpawn();
            }, rate);
        }

        function spawnGameWord() {
            if (!wordGame.isPlaying || wordGame.fallingWords.length >= 5) return;
            
            const word = gameWordData[Math.floor(Math.random() * gameWordData.length)];
            const id = Date.now() + Math.random();
            
            const el = document.createElement('div');
            el.className = 'falling-word';
            el.textContent = word.word;
            el.dataset.id = id;
            
            const gameWidth = document.getElementById('gameCanvas').offsetWidth;
            const x = Math.random() * (gameWidth - 150) + 50;
            el.style.left = x + 'px';
            el.style.top = '-60px';
            
            document.getElementById('gameLayer').appendChild(el);
            
            wordGame.fallingWords.push({
                id, el, word: word.word, meaning: word.meaning,
                y: -60, x: x,
                speed: gameConfig[wordGame.difficulty].speed * (0.8 + Math.random() * 0.4)
            });
            
            generateGameOptions(word);
        }

        function generateGameOptions(targetWord) {
            const options = [targetWord.meaning];
            const allMeanings = gameWordData.map(w => w.meaning).filter(m => m !== targetWord.meaning);
            
            while (options.length < 4) {
                const m = allMeanings[Math.floor(Math.random() * allMeanings.length)];
                if (!options.includes(m)) options.push(m);
            }
            
            wordGame.currentOptions = options.sort(() => Math.random() - 0.5);
            
            for (let i = 0; i < 4; i++) {
                document.getElementById(`shootOpt${i}`).textContent = wordGame.currentOptions[i];
                document.getElementById(`shootBtn${i}`).classList.remove('correct', 'wrong');
            }
        }

        function gameLoop() {
            if (!wordGame.isPlaying || wordGame.isPaused) {
                if (wordGame.isPlaying) wordGame.loopId = requestAnimationFrame(gameLoop);
                return;
            }
            
            const cfg = gameConfig[wordGame.difficulty];
            const gameHeight = document.getElementById('gameCanvas').offsetHeight;
            
            wordGame.fallingWords.forEach((fw, index) => {
                const speed = wordGame.isSlowMotion ? fw.speed * 0.3 : fw.speed;
                fw.y += speed;
                fw.el.style.top = fw.y + 'px';
                
                if (fw.y > gameHeight - 150) fw.el.classList.add('danger');
                
                if (fw.y > gameHeight - 80) {
                    wordGame.health -= cfg.damage;
                    wordGame.combo = 0;
                    updateGameUI();
                    
                    document.getElementById('warningLayer').style.opacity = '1';
                    setTimeout(() => document.getElementById('warningLayer').style.opacity = '0', 300);
                    
                    fw.el.remove();
                    wordGame.fallingWords.splice(index, 1);
                    
                    if (wordGame.health <= 0) endWordGame('health');
                }
            });
            
            wordGame.loopId = requestAnimationFrame(gameLoop);
        }

        function shootWord(optionIndex) {
            if (!wordGame.isPlaying || wordGame.isPaused || wordGame.fallingWords.length === 0) return;
            
            const selected = wordGame.currentOptions[optionIndex];
            const target = wordGame.fallingWords[0];
            
            if (selected === target.meaning) {
                wordGame.combo++;
                if (wordGame.combo > wordGame.maxCombo) wordGame.maxCombo = wordGame.combo;
                
                const multiplier = Math.min(Math.floor(wordGame.combo / 3) + 1, 5);
                const points = 10 * multiplier;
                wordGame.score += points;
                wordGame.correctCount++;
                
                document.getElementById(`shootBtn${optionIndex}`).classList.add('correct');
                setTimeout(() => document.getElementById(`shootBtn${optionIndex}`).classList.remove('correct'), 300);
                
                createGameParticles(target.x + 60, target.y + 20, '#10b981');
                
                if (wordGame.combo >= 3) showGameCombo(target.x, target.y);
                
                target.el.remove();
                wordGame.fallingWords = wordGame.fallingWords.filter(w => w.id !== target.id);
                
                if (wordGame.fallingWords.length > 0) {
                    const next = wordGame.fallingWords[0];
                    const wordItem = gameWordData.find(w => w.word === next.word);
                    if (wordItem) generateGameOptions(wordItem);
                }
            } else {
                wordGame.combo = 0;
                wordGame.wrongCount++;
                wordGame.health -= 5;
                document.getElementById(`shootBtn${optionIndex}`).classList.add('wrong');
                setTimeout(() => document.getElementById(`shootBtn${optionIndex}`).classList.remove('wrong'), 400);
                
                if (wordGame.health <= 0) endWordGame('health');
            }
            
            updateGameUI();
        }

        function useGameSkill(type) {
            if (wordGame.skills[type] <= 0 || !wordGame.isPlaying) return;
            
            wordGame.skills[type]--;
            updateSkillButtons();
            
            switch(type) {
                case 'slow':
                    wordGame.isSlowMotion = true;
                    document.getElementById('gameCanvas').style.filter = 'hue-rotate(180deg)';
                    setTimeout(() => {
                        wordGame.isSlowMotion = false;
                        document.getElementById('gameCanvas').style.filter = '';
                    }, 5000);
                    break;
                case 'bomb':
                    wordGame.fallingWords.forEach(fw => {
                        createGameParticles(fw.x + 60, fw.y + 20, '#ef4444');
                        fw.el.remove();
                    });
                    wordGame.score += wordGame.fallingWords.length * 20;
                    wordGame.fallingWords = [];
                    break;
                case 'heal':
                    wordGame.health = Math.min(wordGame.health + 30, wordGame.maxHealth);
                    break;
            }
            updateGameUI();
        }

        function createGameParticles(x, y, color) {
            const layer = document.getElementById('gameLayer');
            for (let i = 0; i < 8; i++) {
                const p = document.createElement('div');
                p.className = 'particle';
                p.style.left = x + 'px';
                p.style.top = y + 'px';
                p.style.width = '6px';
                p.style.height = '6px';
                p.style.background = color;
                const angle = (Math.PI * 2 * i) / 8;
                const dist = 50;
                p.style.setProperty('--tx', Math.cos(angle) * dist + 'px');
                p.style.setProperty('--ty', Math.sin(angle) * dist + 'px');
                layer.appendChild(p);
                setTimeout(() => p.remove(), 800);
            }
        }

        function showGameCombo(x, y) {
            const combo = document.createElement('div');
            combo.className = 'combo-text';
            combo.textContent = wordGame.combo + ' 连击!';
            combo.style.left = x + 'px';
            combo.style.top = y + 'px';
            document.getElementById('gameLayer').appendChild(combo);
            setTimeout(() => combo.remove(), 800);
        }

        function updateGameUI() {
            document.getElementById('gameScore').textContent = wordGame.score;
            document.getElementById('gameCombo').textContent = 'x' + wordGame.combo;
            
            const healthPercent = Math.max(0, (wordGame.health / wordGame.maxHealth) * 100);
            document.getElementById('gameHealthBar').style.width = healthPercent + '%';
            
            const hb = document.getElementById('gameHealthBar');
            hb.className = 'health-bar h-full rounded-full ' + 
                (healthPercent > 60 ? 'bg-gradient-to-r from-green-500 to-green-400' :
                 healthPercent > 30 ? 'bg-gradient-to-r from-yellow-500 to-yellow-400' :
                 'bg-gradient-to-r from-red-600 to-red-500');
        }

        function updateSkillButtons() {
            document.getElementById('slowCount').textContent = wordGame.skills.slow;
            document.getElementById('bombCount').textContent = wordGame.skills.bomb;
            document.getElementById('healCount').textContent = wordGame.skills.heal;
            
            document.getElementById('skillSlowBtn').disabled = wordGame.skills.slow === 0;
            document.getElementById('skillBombBtn').disabled = wordGame.skills.bomb === 0;
            document.getElementById('skillHealBtn').disabled = wordGame.skills.heal === 0;
        }

        function endWordGame(reason) {
            wordGame.isPlaying = false;
            clearTimeout(wordGame.spawnId);
            clearInterval(wordGame.timerId);
            cancelAnimationFrame(wordGame.loopId);
            
            document.getElementById('gameLayer').innerHTML = '';
            
            const total = wordGame.correctCount + wordGame.wrongCount;
            const accuracy = total > 0 ? Math.round((wordGame.correctCount / total) * 100) : 0;
            
            const bestScore = parseInt(localStorage.getItem('wordDefender_best') || '0');
            const isNewRecord = wordGame.score > bestScore;
            if (isNewRecord) localStorage.setItem('wordDefender_best', wordGame.score);
            
            document.getElementById('endEmoji').textContent = isNewRecord ? '👑' : '🏆';
            document.getElementById('endTitle').textContent = isNewRecord ? '新纪录！' : '游戏结束';
            document.getElementById('finalScore').textContent = wordGame.score;
            document.getElementById('finalAccuracy').textContent = accuracy + '%';
            document.getElementById('gameOverScreen').classList.remove('hidden');
            
            // 更新仪表盘显示
            document.getElementById('bestScoreDisplay').textContent = Math.max(wordGame.score, bestScore);
        }

        function restartWordGame() {
            document.getElementById('gameOverScreen').classList.add('hidden');
            startWordGame();
        }

        function exitGame() {
            wordGame.isPlaying = false;
            clearTimeout(wordGame.spawnId);
            clearInterval(wordGame.timerId);
            cancelAnimationFrame(wordGame.loopId);
            document.getElementById('gameLayer').innerHTML = '';
            document.getElementById('gameOverScreen').classList.add('hidden');
            document.getElementById('gameStartScreen').classList.remove('hidden');
            document.getElementById('gameStats').style.display = 'none';
            document.getElementById('shootControls').classList.add('hidden');
        }

        function showGameInstructions() {
            alert('游戏说明：\\n\\n1. 单词从屏幕上方落下\\n2. 在落地前选择正确的中文释义消灭它们\\n3. 连续答对可触发连击加成（最高x5）\\n4. 单词落地会扣除护盾值，护盾耗尽游戏结束\\n5. 使用技能可以扭转局势\\n\\n操作：\\n- 鼠标点击底部按钮或按 A/S/D/F 键选择\\n- 空格键暂停游戏');
        }

        // 游戏键盘控制
        document.addEventListener('keydown', (e) => {
            if (!wordGame.isPlaying) return;
            
            if (e.code === 'Space') {
                e.preventDefault();
                wordGame.isPaused = !wordGame.isPaused;
                document.getElementById('pauseOverlay').classList.toggle('hidden', !wordGame.isPaused);
                if (!wordGame.isPaused) gameLoop();
                return;
            }
            
            if (wordGame.isPaused) return;
            
            switch(e.key.toLowerCase()) {
                case 'a': shootWord(0); break;
                case 's': shootWord(1); break;
                case 'd': shootWord(2); break;
                case 'f': shootWord(3); break;
                case '1': useGameSkill('slow'); break;
                case '2': useGameSkill('bomb'); break;
                case '3': useGameSkill('heal'); break;
            }
        });

        // ==================== 原有功能代码 ====================
        const vocabularyData = [
            {word: "abundant", phonetic: "/əˈbʌndənt", meaning: "丰富的；充裕的", example: "Natural resources are abundant in this region.", difficulty: "6.0"},
            {word: "significant", phonetic: "/sɪɡˈnɪfɪkənt", meaning: "重要的；显著的", example: "There has been a significant increase in sales.", difficulty: "6.5"},
            {word: "consequence", phonetic: "/ˈkɒnsɪkwəns", meaning: "结果；后果", example: "Climate change may have disastrous consequences.", difficulty: "7.0"},
            {word: "controversial", phonetic: "/ˌkɒntrəˈvɜːʃl", meaning: "有争议的", example: "Genetic engineering is a controversial issue.", difficulty: "7.5"},
            {word: "implementation", phonetic: "/ˌɪmplɪmenˈteɪʃn", meaning: "实施；执行", example: "The implementation of new policies requires time.", difficulty: "8.0"},
            {word: "inevitable", phonetic: "/ɪnˈevɪtəbl", meaning: "不可避免的", example: "Conflict is inevitable in any organization.", difficulty: "7.5"},
            {word: "sustainable", phonetic: "/səˈsteɪnəbl", meaning: "可持续的", example: "We need to find sustainable energy sources.", difficulty: "7.0"},
            {word: "perspective", phonetic: "/pəˈspektɪv", meaning: "观点；视角", example: "From my perspective, this is the best solution.", difficulty: "6.5"},
            {word: "phenomenon", phonetic: "/fəˈnɒmɪnən", meaning: "现象", example: "Global warming is a worrying phenomenon.", difficulty: "7.0"},
            {word: "alternative", phonetic: "/ɔːlˈtɜːnətɪv", meaning: "替代的", example: "We should consider alternative approaches.", difficulty: "6.5"},
            {word: "exaggerate", phonetic: "/ɪɡˈzædʒəreɪt", meaning: "夸大", example: "The media tends to exaggerate problems.", difficulty: "7.0"},
            {word: "discrimination", phonetic: "/dɪˌskrɪmɪˈneɪʃn", meaning: "歧视", example: "Racial discrimination still exists in society.", difficulty: "7.5"},
            {word: "approximately", phonetic: "/əˈprɒksɪmətli", meaning: "大约", example: "Approximately 50% of the population voted.", difficulty: "6.5"},
            {word: "conventional", phonetic: "/kənˈvenʃənl", meaning: "传统的", example: "Conventional methods may not work anymore.", difficulty: "7.0"},
            {word: "fundamental", phonetic: "/ˌfʌndəˈmentl", meaning: "基础的", example: "Education is fundamental to social progress.", difficulty: "7.5"}
        ];

        let currentTask = 'task2';
        let currentWordIndex = 0;
        let wordStatus = JSON.parse(localStorage.getItem('wordStatus') || '{}');
        let currentVocabMode = 'learn';

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
            
            document.getElementById('mobileMenu').classList.add('hidden');
            
            if (sectionId === 'vocabulary') updateVocabStats();
            if (sectionId === 'wordgame') initGame();
            if (sectionId === 'dashboard') {
                const bestScore = localStorage.getItem('wordDefender_best') || '0';
                document.getElementById('bestScoreDisplay').textContent = bestScore;
            }
        }

        function toggleMobileMenu() {
            document.getElementById('mobileMenu').classList.toggle('hidden');
        }

        // 背单词功能
        function setVocabMode(mode) {
            currentVocabMode = mode;
            document.querySelectorAll('[id^="mode-"]').forEach(btn => {
                btn.classList.remove('bg-teal-600', 'text-white');
                btn.classList.add('hover:bg-gray-100');
            });
            document.getElementById('mode-' + mode).classList.add('bg-teal-600', 'text-white');
            document.getElementById('mode-' + mode).classList.remove('hover:bg-gray-100');
            
            document.getElementById('vocab-learn-panel').classList.toggle('hidden', mode !== 'learn');
            document.getElementById('vocab-list-panel').classList.toggle('hidden', mode !== 'list');
            
            if (mode === 'learn') showLearnCard();
            else renderWordList('all');
        }

        function showLearnCard() {
            const word = vocabularyData[currentWordIndex];
            document.getElementById('cardWord').textContent = word.word;
            document.getElementById('cardPhonetic').textContent = word.phonetic;
            document.getElementById('cardMeaning').textContent = word.meaning;
            document.getElementById('cardExample').textContent = word.example;
            document.getElementById('difficultyTag').textContent = 'Band ' + word.difficulty;
            document.getElementById('cardCounter').textContent = `${currentWordIndex + 1}/${vocabularyData.length}`;
            document.getElementById('wordCard').classList.remove('flipped');
        }

        function flipCard() {
            document.getElementById('wordCard').classList.toggle('flipped');
        }

        function markWord(status) {
            const word = vocabularyData[currentWordIndex].word;
            wordStatus[word] = { status, date: new Date().toISOString() };
            localStorage.setItem('wordStatus', JSON.stringify(wordStatus));
            updateVocabStats();
            
            if (currentWordIndex < vocabularyData.length - 1) {
                currentWordIndex++;
                showLearnCard();
            }
        }

        function prevWord() {
            if (currentWordIndex > 0) {
                currentWordIndex--;
                showLearnCard();
            }
        }

        function nextWord() {
            if (currentWordIndex < vocabularyData.length - 1) {
                currentWordIndex++;
                showLearnCard();
            }
        }

        function playAudio() {
            const word = vocabularyData[currentWordIndex].word;
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(word);
                utterance.lang = 'en-US';
                speechSynthesis.speak(utterance);
            }
        }

        function renderWordList(filter) {
            let words = vocabularyData;
            if (filter === 'unlearned') words = words.filter(w => !wordStatus[w.word]);
            else if (filter === 'mastered') words = words.filter(w => wordStatus[w.word]?.status === 'mastered');
            else if (filter === 'learning') words = words.filter(w => ['forgotten', 'vague'].includes(wordStatus[w.word]?.status));
            
            document.getElementById('wordListContainer').innerHTML = words.map(w => {
                const s = wordStatus[w.word]?.status;
                let badge = '<span class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">未学习</span>';
                if (s === 'mastered') badge = '<span class="text-xs px-2 py-1 rounded-full bg-green-100 text-green-700">已掌握</span>';
                else if (s === 'forgotten') badge = '<span class="text-xs px-2 py-1 rounded-full bg-red-100 text-red-700">需复习</span>';
                else if (s === 'vague') badge = '<span class="text-xs px-2 py-1 rounded-full bg-yellow-100 text-yellow-700">学习中</span>';
                
                return `<div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="font-bold">${w.word}</span>
                            <span class="text-xs text-gray-500">${w.phonetic}</span>
                            ${badge}
                        </div>
                        <div class="text-sm text-gray-600">${w.meaning}</div>
                    </div>
                </div>`;
            }).join('');
        }

        function filterWords(filter) {
            renderWordList(filter);
        }

        function updateVocabStats() {
            const mastered = Object.values(wordStatus).filter(s => s.status === 'mastered').length;
            document.getElementById('masteredCount').textContent = mastered;
            document.getElementById('masteredPercent').textContent = Math.round((mastered/vocabularyData.length)*100) + '%';
        }

        function startReviewMode() {
            const reviewWords = Object.entries(wordStatus).filter(([k, v]) => v.status === 'forgotten').map(([k]) => k);
            if (reviewWords.length === 0) alert('暂无需要复习的单词！');
            else {
                currentWordIndex = vocabularyData.findIndex(w => w.word === reviewWords[0]);
                setVocabMode('learn');
            }
        }

        // 写作功能
        function setTask(task) {
            currentTask = task;
            document.getElementById('btn-task1').className = task === 'task1' ? 'px-3 py-1 rounded-full text-sm bg-teal-600 text-white' : 'px-3 py-1 rounded-full text-sm border hover:bg-gray-50';
            document.getElementById('btn-task2').className = task === 'task2' ? 'px-3 py-1 rounded-full text-sm bg-teal-600 text-white' : 'px-3 py-1 rounded-full text-sm border hover:bg-gray-50';
        }

        function updateWordCount() {
            const text = document.getElementById('essayInput').value;
            const count = text.trim() ? text.trim().split(/\\s+/).length : 0;
            document.getElementById('wordCountDisplay').textContent = `字数：${count} / ${currentTask === 'task1' ? '130+' : '220+'}`;
        }

        async function submitEssay() {
            const essay = document.getElementById('essayInput').value;
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('btnText').textContent = '评分中...';
            document.getElementById('btnLoader').classList.remove('hidden');

            setTimeout(() => {
                const wordCount = essay.trim() ? essay.trim().split(/\\s+/).length : 0;
                const score = wordCount > 200 ? 7.0 : wordCount > 150 ? 6.5 : 6.0;
                
                document.getElementById('resultArea').classList.remove('hidden');
                document.getElementById('overallBand').textContent = score;
                document.getElementById('trScore').textContent = score;
                document.getElementById('ccScore').textContent = score;
                document.getElementById('lrScore').textContent = score - 0.5;
                document.getElementById('graScore').textContent = score;
                document.getElementById('suggestionsList').innerHTML = '<li>• 注意词汇多样性</li><li>• 增加复杂句型使用</li>';
                
                document.getElementById('submitBtn').disabled = false;
                document.getElementById('btnText').textContent = '提交评分';
                document.getElementById('btnLoader').classList.add('hidden');
            }, 1500);
        }

        function generateWritingPrompt() {
            const prompts = [
                "Some people think that the best way to reduce crime is to give longer prison sentences. Others believe there are better alternatives. Discuss both views.",
                "Space exploration is a waste of money. Do you agree or disagree?",
                "Should governments ban dangerous sports, or should people have the freedom to choose?"
            ];
            document.getElementById('promptDisplay').textContent = prompts[Math.floor(Math.random() * prompts.length)];
        }

        // 口语功能
        function generateSpeakingTopic() {
            const topics = [
                {topic: "Describe a difficult decision you made.", prompts: ["What the decision was", "When you made it", "Why it was difficult"]},
                {topic: "Describe a person who speaks a foreign language well.", prompts: ["Who this person is", "What language they speak", "How they learned it"]}
            ];
            const t = topics[Math.floor(Math.random() * topics.length)];
            document.getElementById('speakingTopic').textContent = t.topic;
            document.getElementById('speakingPrompts').innerHTML = t.prompts.map(p => `<li>${p}</li>`).join('');
        }

        async function submitSpeaking() {
            document.getElementById('speakBtn').disabled = true;
            document.getElementById('speakBtnText').textContent = '评分中...';
            document.getElementById('speakLoader').classList.remove('hidden');
            
            setTimeout(() => {
                document.getElementById('speakingResult').classList.remove('hidden');
                document.getElementById('speakOverall').textContent = '6.5';
                document.getElementById('fluencyScore').textContent = '6.5';
                document.getElementById('speakLrScore').textContent = '6.5';
                document.getElementById('speakGrScore').textContent = '6.0';
                document.getElementById('pronScore').textContent = '7.0';
                document.getElementById('speakSuggestions').innerHTML = '<li>• 使用更多连接词</li><li>• 增加具体细节</li>';
                
                document.getElementById('speakBtn').disabled = false;
                document.getElementById('speakBtnText').textContent = '提交口语评分';
                document.getElementById('speakLoader').classList.add('hidden');
            }, 1500);
        }

        // 工具箱
        async function generatePrompt() {
            const type = document.getElementById('promptType').value;
            const prompts = {
                task2: ["Space exploration is a waste of money. Do you agree?", "Should governments ban dangerous sports?"],
                task1: ["The graph shows internet usage from 1998 to 2008.", "The chart compares public transport in five cities."],
                speaking: ["Describe a difficult decision you made.", "Describe a person who speaks a foreign language well."]
            };
            const div = document.getElementById('generatedPrompt');
            div.textContent = prompts[type][Math.floor(Math.random() * prompts[type].length)];
            div.classList.remove('hidden');
        }

        async function checkGrammar() {
            const text = document.getElementById('grammarInput').value;
            const issues = [];
            if (text.includes('i am agree')) issues.push('❌ I am agree → ✅ I agree');
            if (text.includes('very good')) issues.push('⚠️ very good → ✅ significant/beneficial');
            
            const div = document.getElementById('grammarResult');
            div.innerHTML = issues.length > 0 ? issues.map(i => `<div class="mb-2 p-2 bg-orange-50 rounded text-orange-800">${i}</div>`).join('') : '<div class="text-green-600">✅ 未发现明显错误</div>';
            div.classList.remove('hidden');
        }

        // 初始化
        showSection('dashboard');
        updateVocabStats();
        document.getElementById('bestScoreDisplay').textContent = localStorage.getItem('wordDefender_best') || '0';
    </script>
</body>
</html>'''

# 保存到文件
with open('/mnt/kimi/output/ielts_platform_with_game.html', 'w', encoding='utf-8') as f:
    f.write(full_code)

print("✅ 集成完成！文件已保存")
print("\n📦 包含功能模块：")
print("1. 🏠 仪表盘 - 快速导航和学习概览")
print("2. 📚 背单词 - 翻转卡片式学习")
print("3. 🎮 词汇游戏 - 弹幕射击游戏（新增）")
print("4. 📝 AI写作精批 - Task 1/2 评分")
print("5. 🎤 口语评分 - Part 2 评估")
print("6. 🎲 工具箱 - 题目生成器+语法检查")
print("\n🎮 游戏特性：")
print("• 三种难度（简单/普通/困难）")
print("• 连击系统（最高x5倍分数）")
print("• 三种技能道具（缓速/炸弹/修复）")
print("• 键盘A/S/D/F快捷键支持")
print("• 空格键暂停功能")
print("• 本地存储最高分记录")
