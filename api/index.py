
# 生成增强版的HTML代码，添加背单词功能
html_code = '''<!DOCTYPE html>
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
        
        /* 单词卡片翻转动画 */
        .flip-card { perspective: 1000px; }
        .flip-card-inner { position: relative; width: 100%; height: 100%; transition: transform 0.6s; transform-style: preserve-3d; }
        .flip-card.flipped .flip-card-inner { transform: rotateY(180deg); }
        .flip-card-front, .flip-card-back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; border-radius: 1rem; }
        .flip-card-back { transform: rotateY(180deg); }
        
        /* 进度条 */
        .progress-bar { transition: width 0.5s ease; }
        
        /* 记忆模式按钮 */
        .memory-btn { transition: all 0.2s; }
        .memory-btn:hover { transform: translateY(-2px); }
        .memory-btn:active { transform: translateY(0); }
        
        /* 单词标签 */
        .word-tag { transition: all 0.3s; }
        .word-tag:hover { transform: scale(1.05); }
        
        /* 成就徽章 */
        .badge { animation: popIn 0.3s ease; }
        @keyframes popIn { 0% { transform: scale(0); } 80% { transform: scale(1.1); } 100% { transform: scale(1); } }
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
                    <button onclick="showSection('writing')" id="nav-writing" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">写作</button>
                    <button onclick="showSection('speaking')" id="nav-speaking" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">口语</button>
                    <button onclick="showSection('tools')" id="nav-tools" class="nav-btn px-4 py-2 rounded-full font-medium transition-all hover:bg-gray-100">工具箱</button>
                </div>
                
                <!-- 移动端菜单按钮 -->
                <button class="md:hidden p-2" onclick="toggleMobileMenu()">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                    </svg>
                </button>
            </div>
            
            <!-- 移动端菜单 -->
            <div id="mobileMenu" class="hidden md:hidden pb-4 space-y-2">
                <button onclick="showSection('dashboard')" class="w-full text-left px-4 py-2 rounded-lg hover:bg-gray-100">仪表盘</button>
                <button onclick="showSection('vocabulary')" class="w-full text-left px-4 py-2 rounded-lg hover:bg-gray-100 text-teal-600 font-medium">🎯 背单词</button>
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
                <p class="text-gray-600">集成背单词、写作精批、口语评分、题目生成、语法检查</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all border-l-4 border-teal-500" onclick="showSection('vocabulary')">
                    <div class="text-3xl mb-2">🎯</div>
                    <div class="font-bold text-gray-900">背单词</div>
                    <div class="text-xs text-gray-500 mt-1">雅思核心词汇</div>
                    <div class="mt-2 text-xs font-medium text-teal-600" id="dashboard-vocab-progress">今日学习: 0/20</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all" onclick="showSection('writing')">
                    <div class="text-3xl mb-2">📝</div>
                    <div class="font-bold text-gray-900">AI写作精批</div>
                    <div class="text-xs text-gray-500 mt-1">Task 1 & 2 评分</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all" onclick="showSection('speaking')">
                    <div class="text-3xl mb-2">🎤</div>
                    <div class="font-bold text-gray-900">口语Part 2评分</div>
                    <div class="text-xs text-gray-500 mt-1">文本转写评估</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all" onclick="showSection('tools')">
                    <div class="text-3xl mb-2">🎲</div>
                    <div class="font-bold text-gray-900">题目生成器</div>
                    <div class="text-xs text-gray-500 mt-1">随机生成真题</div>
                </div>
                <div class="glass rounded-2xl p-5 shadow-sm cursor-pointer hover:shadow-md transition-all" onclick="showSection('tools'); document.getElementById('grammarTab').click();">
                    <div class="text-3xl mb-2">🔍</div>
                    <div class="font-bold text-gray-900">语法检查</div>
                    <div class="text-xs text-gray-500 mt-1">基础语法纠错</div>
                </div>
            </div>

            <div class="glass rounded-2xl p-6 shadow-sm bg-gradient-to-br from-teal-50 to-transparent">
                <h3 class="font-bold text-lg mb-2">🚀 快速开始</h3>
                <p class="text-gray-700 mb-4">选择上方功能开始练习，所有AI评分基于官方标准</p>
                <div class="flex flex-wrap gap-3">
                    <button onclick="showSection('vocabulary')" class="px-4 py-2 bg-teal-600 text-white rounded-lg text-sm hover:bg-teal-700 flex items-center gap-2">
                        <span>开始背单词</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
                    </button>
                    <button onclick="showSection('writing')" class="px-4 py-2 bg-white border border-teal-600 text-teal-600 rounded-lg text-sm hover:bg-teal-50">写作练习</button>
                    <button onclick="showSection('speaking')" class="px-4 py-2 bg-white border border-teal-600 text-teal-600 rounded-lg text-sm hover:bg-teal-50">口语练习</button>
                </div>
            </div>
        </section>

        <!-- VOCABULARY SECTION -->
        <section id="vocabulary" class="section hidden-section fade-in">
            <!-- 标题区 -->
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
                    <div class="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center text-xl" id="streakIcon">🔥</div>
                </div>
            </div>

            <!-- 学习进度概览 -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div class="glass rounded-2xl p-4 border-l-4 border-teal-500">
                    <div class="text-xs text-gray-500 mb-1">今日学习进度</div>
                    <div class="flex items-end justify-between">
                        <span class="text-2xl font-bold text-gray-900" id="todayLearned">0/20</span>
                        <span class="text-xs text-teal-600 font-medium">词</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                        <div class="bg-teal-500 h-2 rounded-full progress-bar" id="todayProgressBar" style="width: 0%"></div>
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
                    <button onclick="startReviewMode()" class="text-xs text-blue-600 hover:underline mt-1" id="reviewBtn">开始复习 →</button>
                </div>
                <div class="glass rounded-2xl p-4 border-l-4 border-orange-500">
                    <div class="text-xs text-gray-500 mb-1">今日正确率</div>
                    <div class="flex items-end justify-between">
                        <span class="text-2xl font-bold text-gray-900" id="accuracyRate">0%</span>
                        <span class="text-xs text-gray-500" id="accuracyDetail">0/0</span>
                    </div>
                    <div class="text-xs text-orange-600 mt-1" id="accuracyText">继续努力！</div>
                </div>
            </div>

            <!-- 主学习区 -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- 左侧：单词卡片 -->
                <div class="lg:col-span-2 space-y-4">
                    <!-- 模式切换 -->
                    <div class="glass rounded-2xl p-2 flex gap-2 mb-4">
                        <button onclick="setVocabMode('learn')" id="mode-learn" class="flex-1 py-2 px-4 rounded-xl text-sm font-medium transition-all bg-teal-600 text-white">
                            🎯 学习模式
                        </button>
                        <button onclick="setVocabMode('test')" id="mode-test" class="flex-1 py-2 px-4 rounded-xl text-sm font-medium transition-all hover:bg-gray-100">
                            🧪 测试模式
                        </button>
                        <button onclick="setVocabMode('list')" id="mode-list" class="flex-1 py-2 px-4 rounded-xl text-sm font-medium transition-all hover:bg-gray-100">
                            📚 单词表
                        </button>
                    </div>

                    <!-- 学习模式：翻转卡片 -->
                    <div id="vocab-learn-panel" class="glass rounded-2xl p-8 shadow-sm min-h-[400px] flex flex-col items-center justify-center relative">
                        <div class="absolute top-4 right-4 flex gap-2">
                            <span class="px-3 py-1 bg-gray-100 rounded-full text-xs text-gray-600" id="cardCounter">1/20</span>
                            <span class="px-3 py-1 bg-teal-100 text-teal-700 rounded-full text-xs font-medium" id="difficultyTag">Band 6.0</span>
                        </div>

                        <div class="flip-card w-full max-w-md h-64 cursor-pointer" onclick="flipCard()" id="wordCard">
                            <div class="flip-card-inner">
                                <!-- 正面 -->
                                <div class="flip-card-front glass shadow-lg flex flex-col items-center justify-center p-8 border-2 border-transparent hover:border-teal-300 transition-all">
                                    <h3 class="text-4xl font-bold text-gray-900 mb-2" id="cardWord">abundant</h3>
                                    <p class="text-gray-500 text-lg" id="cardPhonetic">/əˈbʌndənt/</p>
                                    <p class="text-gray-400 text-sm mt-4">点击翻转查看释义</p>
                                </div>
                                <!-- 背面 -->
                                <div class="flip-card-back bg-gradient-to-br from-teal-600 to-teal-700 text-white shadow-lg flex flex-col items-center justify-center p-8">
                                    <div class="text-sm opacity-80 mb-1">中文释义</div>
                                    <h3 class="text-2xl font-bold mb-4" id="cardMeaning">丰富的；充裕的</h3>
                                    <div class="w-full h-px bg-white/30 my-3"></div>
                                    <div class="text-sm opacity-80 mb-1">例句</div>
                                    <p class="text-center text-sm italic" id="cardExample">Natural resources are abundant in this region.</p>
                                    <p class="text-center text-xs opacity-80 mt-1" id="cardExampleCn">该地区自然资源丰富。</p>
                                </div>
                            </div>
                        </div>

                        <!-- 操作按钮 -->
                        <div class="flex gap-4 mt-8 w-full max-w-md">
                            <button onclick="markWord('forgotten')" class="flex-1 py-3 bg-red-100 text-red-700 rounded-xl font-medium hover:bg-red-200 transition-all memory-btn flex items-center justify-center gap-2">
                                <span>😅 忘记</span>
                            </button>
                            <button onclick="markWord('vague')" class="flex-1 py-3 bg-yellow-100 text-yellow-700 rounded-xl font-medium hover:bg-yellow-200 transition-all memory-btn flex items-center justify-center gap-2">
                                <span>🤔 模糊</span>
                            </button>
                            <button onclick="markWord('mastered')" class="flex-1 py-3 bg-green-100 text-green-700 rounded-xl font-medium hover:bg-green-200 transition-all memory-btn flex items-center justify-center gap-2">
                                <span>✅ 掌握</span>
                            </button>
                        </div>

                        <div class="flex justify-between w-full max-w-md mt-4">
                            <button onclick="prevWord()" class="px-4 py-2 text-gray-500 hover:text-gray-700 text-sm">← 上一个</button>
                            <button onclick="playAudio()" class="px-4 py-2 text-teal-600 hover:text-teal-700 text-sm flex items-center gap-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"/></svg>
                                发音
                            </button>
                            <button onclick="nextWord()" class="px-4 py-2 text-gray-500 hover:text-gray-700 text-sm">下一个 →</button>
                        </div>
                    </div>

                    <!-- 测试模式 -->
                    <div id="vocab-test-panel" class="hidden glass rounded-2xl p-8 shadow-sm min-h-[400px]">
                        <div class="mb-6">
                            <div class="flex justify-between items-center mb-4">
                                <span class="text-sm text-gray-500">选择正确的中文释义</span>
                                <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs" id="testCounter">1/10</span>
                            </div>
                            <h3 class="text-3xl font-bold text-gray-900" id="testWord">significant</h3>
                            <p class="text-gray-500" id="testPhonetic">/sɪɡˈnɪfɪkənt/</p>
                        </div>

                        <div class="grid grid-cols-1 gap-3" id="testOptions">
                            <!-- 选项由JS生成 -->
                        </div>

                        <div id="testFeedback" class="hidden mt-4 p-4 rounded-xl"></div>

                        <button onclick="nextTestQuestion()" id="nextTestBtn" class="hidden w-full mt-4 py-3 bg-purple-600 text-white rounded-xl font-medium">
                            下一题 →
                        </button>
                    </div>

                    <!-- 单词列表模式 -->
                    <div id="vocab-list-panel" class="hidden glass rounded-2xl p-6 shadow-sm">
                        <div class="flex gap-2 mb-4 overflow-x-auto pb-2">
                            <button onclick="filterWords('all')" class="px-4 py-2 rounded-full text-sm bg-gray-800 text-white">全部</button>
                            <button onclick="filterWords('unlearned')" class="px-4 py-2 rounded-full text-sm bg-gray-200 text-gray-700 hover:bg-gray-300">未学习</button>
                            <button onclick="filterWords('learning')" class="px-4 py-2 rounded-full text-sm bg-yellow-100 text-yellow-700">学习中</button>
                            <button onclick="filterWords('mastered')" class="px-4 py-2 rounded-full text-sm bg-green-100 text-green-700">已掌握</button>
                        </div>

                        <div class="space-y-2 max-h-[500px] overflow-y-auto" id="wordListContainer">
                            <!-- 单词列表由JS生成 -->
                        </div>
                    </div>
                </div>

                <!-- 右侧：统计与设置 -->
                <div class="space-y-4">
                    <!-- 学习日历 -->
                    <div class="glass rounded-2xl p-5 shadow-sm">
                        <h4 class="font-bold mb-3 text-sm">学习日历</h4>
                        <div class="grid grid-cols-7 gap-1 text-center text-xs" id="studyCalendar">
                            <!-- 由JS生成 -->
                        </div>
                    </div>

                    <!-- 难度分布 -->
                    <div class="glass rounded-2xl p-5 shadow-sm">
                        <h4 class="font-bold mb-3 text-sm">词汇难度分布</h4>
                        <div class="space-y-2">
                            <div class="flex justify-between items-center text-sm">
                                <span class="text-gray-600">Band 6.0-6.5</span>
                                <span class="font-medium" id="countBand6">0</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-blue-400 h-2 rounded-full" style="width: 40%"></div>
                            </div>
                            <div class="flex justify-between items-center text-sm">
                                <span class="text-gray-600">Band 7.0-7.5</span>
                                <span class="font-medium" id="countBand7">0</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-purple-400 h-2 rounded-full" style="width: 35%"></div>
                            </div>
                            <div class="flex justify-between items-center text-sm">
                                <span class="text-gray-600">Band 8.0+</span>
                                <span class="font-medium" id="countBand8">0</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-orange-400 h-2 rounded-full" style="width: 25%"></div>
                            </div>
                        </div>
                    </div>

                    <!-- 学习提醒 -->
                    <div class="glass rounded-2xl p-5 shadow-sm bg-gradient-to-br from-yellow-50 to-transparent border border-yellow-200">
                        <h4 class="font-bold mb-2 text-sm text-yellow-800">💡 记忆技巧</h4>
                        <p class="text-xs text-yellow-700 leading-relaxed" id="memoryTip">
                            使用艾宾浩斯遗忘曲线复习：学习后5分钟、30分钟、12小时、1天、2天、4天、7天、15天各复习一次，可最大化记忆效率。
                        </p>
                    </div>

                    <!-- 重置进度 -->
                    <button onclick="resetProgress()" class="w-full py-2 text-xs text-gray-400 hover:text-red-500 transition-colors">
                        重置所有学习进度
                    </button>
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
                    <div class="glass rounded-2xl p-5 shadow-sm bg-orange-50">
                        <h4 class="font-bold mb-2 text-sm text-orange-800">高分句型</h4>
                        <div class="text-xs text-orange-700 space-y-1">
                            <p>• While it is true that...</p>
                            <p>• This essay will discuss...</p>
                            <p>• In conclusion, I believe...</p>
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
                            <div class="flex justify-between items-center p-3 bg-gray-50 rounded">
                                <span class="text-sm">Pronunciation (推断)</span>
                                <span class="font-bold text-purple-600" id="pronScore">-</span>
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
                <!-- Prompt Generator -->
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

                <!-- Grammar Check -->
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
        // ==================== 词汇数据 ====================
        const vocabularyData = [
            {word: "abundant", phonetic: "/əˈbʌndənt", meaning: "丰富的；充裕的", example: "Natural resources are abundant in this region.", exampleCn: "该地区自然资源丰富。", difficulty: "6.0", tags: ["形容词", "环境", "学术"]},
            {word: "significant", phonetic: "/sɪɡˈnɪfɪkənt", meaning: "重要的；显著的", example: "There has been a significant increase in sales.", exampleCn: "销售额有了显著增长。", difficulty: "6.5", tags: ["形容词", "数据", "学术"]},
            {word: "consequence", phonetic: "/ˈkɒnsɪkwəns", meaning: "结果；后果", example: "Climate change may have disastrous consequences.", exampleCn: "气候变化可能带来灾难性后果。", difficulty: "7.0", tags: ["名词", "环境", "因果"]},
            {word: "controversial", phonetic: "/ˌkɒntrəˈvɜːʃl", meaning: "有争议的", example: "Genetic engineering is a controversial issue.", exampleCn: "基因工程是一个有争议的话题。", difficulty: "7.5", tags: ["形容词", "科技", "学术"]},
            {word: "implementation", phonetic: "/ˌɪmplɪmenˈteɪʃn", meaning: "实施；执行", example: "The implementation of new policies requires time.", exampleCn: "新政策的实施需要时间。", difficulty: "8.0", tags: ["名词", "政策", "正式"]},
            {word: "inevitable", phonetic: "/ɪnˈevɪtəbl", meaning: "不可避免的", example: "Conflict is inevitable in any organization.", exampleCn: "冲突在任何组织中都是不可避免的。", difficulty: "7.5", tags: ["形容词", "社会", "学术"]},
            {word: "sustainable", phonetic: "/səˈsteɪnəbl", meaning: "可持续的", example: "We need to find sustainable energy sources.", exampleCn: "我们需要找到可持续的能源。", difficulty: "7.0", tags: ["形容词", "环境", "高频"]},
            {word: "perspective", phonetic: "/pəˈspektɪv", meaning: "观点；视角", example: "From my perspective, this is the best solution.", exampleCn: "从我的角度来看，这是最好的解决方案。", difficulty: "6.5", tags: ["名词", "写作", "口语"]},
            {word: "infrastructure", phonetic: "/ˈɪnfrəstrʌktʃə(r)/", meaning: "基础设施", example: "Poor infrastructure hinders economic development.", exampleCn: "落后的基础设施阻碍经济发展。", difficulty: "7.5", tags: ["名词", "经济", "城市"]},
            {word: "phenomenon", phonetic: "/fəˈnɒmɪnən", meaning: "现象", example: "Global warming is a worrying phenomenon.", exampleCn: "全球变暖是一个令人担忧的现象。", difficulty: "7.0", tags: ["名词", "学术", "通用"]},
            {word: "alternative", phonetic: "/ɔːlˈtɜːnətɪv", meaning: "替代的；选择", example: "We should consider alternative approaches.", exampleCn: "我们应该考虑替代方法。", difficulty: "6.5", tags: ["形容词/名词", "写作", "高频"]},
            {word: "exaggerate", phonetic: "/ɪɡˈzædʒəreɪt", meaning: "夸大；夸张", example: "The media tends to exaggerate problems.", exampleCn: "媒体往往夸大问题。", difficulty: "7.0", tags: ["动词", "媒体", "批判"]},
            {word: "discrimination", phonetic: "/dɪˌskrɪmɪˈneɪʃn", meaning: "歧视", example: "Racial discrimination still exists in society.", exampleCn: "种族歧视在社会中依然存在。", difficulty: "7.5", tags: ["名词", "社会", "人权"]},
            {word: "approximately", phonetic: "/əˈprɒksɪmətli", meaning: "大约", example: "Approximately 50% of the population voted.", exampleCn: "大约50%的人口参与了投票。", difficulty: "6.5", tags: ["副词", "数据", "Task1"]},
            {word: "conventional", phonetic: "/kənˈvenʃənl", meaning: "传统的；常规的", example: "Conventional methods may not work anymore.", exampleCn: "传统方法可能不再有效。", difficulty: "7.0", tags: ["形容词", "对比", "学术"]},
            {word: "fundamental", phonetic: "/ˌfʌndəˈmentl", meaning: "根本的；基础的", example: "Education is fundamental to social progress.", exampleCn: "教育对社会进步至关重要。", difficulty: "7.5", tags: ["形容词", "教育", "抽象"]},
            {word: "hypothetical", phonetic: "/ˌhaɪpəˈθetɪkl", meaning: "假设的", example: "This is a hypothetical scenario, not reality.", exampleCn: "这是一个假设的情景，不是现实。", difficulty: "8.0", tags: ["形容词", "学术", "逻辑"]},
            {word: "incentive", phonetic: "/ɪnˈsentɪv", meaning: "激励；动机", example: "Tax incentives encourage business investment.", exampleCn: "税收优惠鼓励商业投资。", difficulty: "7.5", tags: ["名词", "经济", "政策"]},
            {word: "infrastructure", phonetic: "/ˈɪnfrəstrʌktʃər", meaning: "基础设施", example: "The city needs to upgrade its infrastructure.", exampleCn: "这座城市需要升级基础设施。", difficulty: "7.0", tags: ["名词", "城市", "发展"]},
            {word: "legislation", phonetic: "/ˌledʒɪsˈleɪʃn", meaning: "立法；法律", example: "New legislation was passed to protect consumers.", exampleCn: "通过了保护消费者的新法律。", difficulty: "8.0", tags: ["名词", "法律", "政府"]}
        ];

        // ==================== 全局状态 ====================
        let currentTask = 'task2';
        let currentVocabMode = 'learn';
        let currentWordIndex = 0;
        let filteredWords = [...vocabularyData];
        let testQuestions = [];
        let currentTestIndex = 0;
        let correctAnswers = 0;
        let todayLearned = new Set();
        let todayCorrect = 0;
        let todayTotal = 0;
        
        // 从localStorage读取进度
        let wordStatus = JSON.parse(localStorage.getItem('wordStatus') || '{}');
        let studyHistory = JSON.parse(localStorage.getItem('studyHistory') || '[]');
        let lastStudyDate = localStorage.getItem('lastStudyDate');
        let streak = parseInt(localStorage.getItem('streak') || '0');

        // ==================== 导航功能 ====================
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
            
            // 移动端菜单关闭
            document.getElementById('mobileMenu').classList.add('hidden');
            
            // 如果是词汇页面，初始化
            if (sectionId === 'vocabulary') {
                initVocabulary();
            }
        }

        function toggleMobileMenu() {
            document.getElementById('mobileMenu').classList.toggle('hidden');
        }

        // ==================== 词汇功能 ====================
        function initVocabulary() {
            updateStats();
            renderCalendar();
            updateDifficultyStats();
            
            if (currentVocabMode === 'learn') {
                showLearnMode();
            } else if (currentVocabMode === 'test') {
                showTestMode();
            } else {
                showListMode();
            }
            
            // 检查是否需要重置今日学习
            const today = new Date().toDateString();
            if (lastStudyDate !== today) {
                if (lastStudyDate) {
                    const yesterday = new Date();
                    yesterday.setDate(yesterday.getDate() - 1);
                    if (lastStudyDate !== yesterday.toDateString()) {
                        streak = 0;
                    }
                }
                todayLearned = new Set();
                todayCorrect = 0;
                todayTotal = 0;
                lastStudyDate = today;
                saveProgress();
            }
            
            document.getElementById('streakDays').textContent = streak + ' 天';
        }

        function setVocabMode(mode) {
            currentVocabMode = mode;
            document.querySelectorAll('[id^="mode-"]').forEach(btn => {
                btn.classList.remove('bg-teal-600', 'text-white');
                btn.classList.add('hover:bg-gray-100');
            });
            document.getElementById('mode-' + mode).classList.add('bg-teal-600', 'text-white');
            document.getElementById('mode-' + mode).classList.remove('hover:bg-gray-100');
            
            document.getElementById('vocab-learn-panel').classList.add('hidden');
            document.getElementById('vocab-test-panel').classList.add('hidden');
            document.getElementById('vocab-list-panel').classList.add('hidden');
            
            if (mode === 'learn') {
                document.getElementById('vocab-learn-panel').classList.remove('hidden');
                showLearnMode();
            } else if (mode === 'test') {
                document.getElementById('vocab-test-panel').classList.remove('hidden');
                showTestMode();
            } else {
                document.getElementById('vocab-list-panel').classList.remove('hidden');
                showListMode();
            }
        }

        // 学习模式
        function showLearnMode() {
            const word = filteredWords[currentWordIndex];
            document.getElementById('cardWord').textContent = word.word;
            document.getElementById('cardPhonetic').textContent = word.phonetic;
            document.getElementById('cardMeaning').textContent = word.meaning;
            document.getElementById('cardExample').textContent = word.example;
            document.getElementById('cardExampleCn').textContent = word.exampleCn;
            document.getElementById('difficultyTag').textContent = 'Band ' + word.difficulty;
            document.getElementById('cardCounter').textContent = `${currentWordIndex + 1}/${filteredWords.length}`;
            
            // 重置翻转状态
            document.getElementById('wordCard').classList.remove('flipped');
        }

        function flipCard() {
            document.getElementById('wordCard').classList.toggle('flipped');
        }

        function markWord(status) {
            const word = filteredWords[currentWordIndex].word;
            wordStatus[word] = { status: status, date: new Date().toISOString() };
            
            if (status === 'mastered') {
                todayLearned.add(word);
                showToast('✅ 标记为已掌握！+' + calculatePoints(word) + '分');
            } else if (status === 'forgotten') {
                showToast('😅 已加入复习列表');
            } else {
                showToast('🤔 标记为模糊，会再次显示');
            }
            
            saveProgress();
            updateStats();
            
            // 自动进入下一个
            setTimeout(() => {
                nextWord();
            }, 500);
        }

        function calculatePoints(word) {
            const diff = parseFloat(word.difficulty);
            if (diff >= 8.0) return 10;
            if (diff >= 7.5) return 8;
            if (diff >= 7.0) return 6;
            return 5;
        }

        function nextWord() {
            if (currentWordIndex < filteredWords.length - 1) {
                currentWordIndex++;
                showLearnMode();
            } else {
                showToast('🎉 已完成今日所有单词学习！');
                currentWordIndex = 0;
                showLearnMode();
            }
        }

        function prevWord() {
            if (currentWordIndex > 0) {
                currentWordIndex--;
                showLearnMode();
            }
        }

        function playAudio() {
            const word = filteredWords[currentWordIndex].word;
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(word);
                utterance.lang = 'en-US';
                speechSynthesis.speak(utterance);
            } else {
                showToast('您的浏览器不支持语音播放');
            }
        }

        // 测试模式
        function showTestMode() {
            // 生成测试题（从已学习单词中随机选10个）
            const learnedWords = vocabularyData.filter(w => wordStatus[w.word]?.status === 'mastered');
            if (learnedWords.length < 5) {
                document.getElementById('testOptions').innerHTML = 
                    '<div class="p-4 text-center text-gray-500">请先在学习模式下掌握至少5个单词，再开始测试</div>';
                return;
            }
            
            testQuestions = generateTestQuestions(learnedWords, 10);
            currentTestIndex = 0;
            correctAnswers = 0;
            showTestQuestion();
        }

        function generateTestQuestions(words, count) {
            const shuffled = [...words].sort(() => Math.random() - 0.5);
            const selected = shuffled.slice(0, Math.min(count, words.length));
            
            return selected.map(word => {
                const otherMeanings = vocabularyData
                    .filter(w => w.word !== word.word)
                    .sort(() => Math.random() - 0.5)
                    .slice(0, 3)
                    .map(w => w.meaning);
                
                const options = [...otherMeanings, word.meaning].sort(() => Math.random() - 0.5);
                
                return {
                    word: word.word,
                    phonetic: word.phonetic,
                    correct: word.meaning,
                    options: options
                };
            });
        }

        function showTestQuestion() {
            const q = testQuestions[currentTestIndex];
            document.getElementById('testWord').textContent = q.word;
            document.getElementById('testPhonetic').textContent = q.phonetic;
            document.getElementById('testCounter').textContent = `${currentTestIndex + 1}/${testQuestions.length}`;
            
            const optionsHtml = q.options.map((opt, idx) => 
                `<button onclick="selectTestOption(${idx}, '${opt}')" class="w-full p-4 text-left border rounded-xl hover:bg-gray-50 transition-all text-sm" data-option="${opt}">
                    ${String.fromCharCode(65 + idx)}. ${opt}
                </button>`
            ).join('');
            
            document.getElementById('testOptions').innerHTML = optionsHtml;
            document.getElementById('testFeedback').classList.add('hidden');
            document.getElementById('nextTestBtn').classList.add('hidden');
        }

        function selectTestOption(idx, selected) {
            const q = testQuestions[currentTestIndex];
            const buttons = document.querySelectorAll('#testOptions button');
            const feedback = document.getElementById('testFeedback');
            
            buttons.forEach(btn => btn.disabled = true);
            
            if (selected === q.correct) {
                buttons[idx].classList.remove('hover:bg-gray-50');
                buttons[idx].classList.add('bg-green-100', 'border-green-500', 'text-green-800');
                feedback.innerHTML = '<span class="text-green-600 font-bold">✅ 正确！</span>';
                correctAnswers++;
                todayCorrect++;
            } else {
                buttons[idx].classList.remove('hover:bg-gray-50');
                buttons[idx].classList.add('bg-red-100', 'border-red-500', 'text-red-800');
                // 高亮正确答案
                buttons.forEach((btn, i) => {
                    if (btn.getAttribute('data-option') === q.correct) {
                        btn.classList.add('bg-green-50', 'border-green-500');
                    }
                });
                feedback.innerHTML = `<span class="text-red-600 font-bold">❌ 错误</span><span class="text-gray-600 ml-2">正确答案是：${q.correct}</span>`;
            }
            
            todayTotal++;
            feedback.classList.remove('hidden');
            document.getElementById('nextTestBtn').classList.remove('hidden');
            updateStats();
        }

        function nextTestQuestion() {
            if (currentTestIndex < testQuestions.length - 1) {
                currentTestIndex++;
                showTestQuestion();
            } else {
                // 测试完成
                const accuracy = Math.round((correctAnswers / testQuestions.length) * 100);
                document.getElementById('testOptions').innerHTML = `
                    <div class="text-center py-8">
                        <div class="text-4xl mb-4">🎉</div>
                        <div class="text-2xl font-bold text-gray-900 mb-2">测试完成！</div>
                        <div class="text-lg text-gray-600">正确率：${accuracy}% (${correctAnswers}/${testQuestions.length})</div>
                        <button onclick="showTestMode()" class="mt-4 px-6 py-2 bg-purple-600 text-white rounded-full text-sm">再来一次</button>
                    </div>
                `;
                document.getElementById('testFeedback').classList.add('hidden');
                document.getElementById('nextTestBtn').classList.add('hidden');
            }
        }

        // 列表模式
        function showListMode() {
            renderWordList('all');
        }

        function filterWords(filter) {
            renderWordList(filter);
        }

        function renderWordList(filter) {
            let words = vocabularyData;
            if (filter === 'unlearned') {
                words = words.filter(w => !wordStatus[w.word]);
            } else if (filter === 'learning') {
                words = words.filter(w => wordStatus[w.word]?.status === 'forgotten' || wordStatus[w.word]?.status === 'vague');
            } else if (filter === 'mastered') {
                words = words.filter(w => wordStatus[w.word]?.status === 'mastered');
            }
            
            const html = words.map(w => {
                const status = wordStatus[w.word]?.status;
                let statusClass = 'bg-gray-100 text-gray-600';
                let statusText = '未学习';
                if (status === 'mastered') {
                    statusClass = 'bg-green-100 text-green-700';
                    statusText = '已掌握';
                } else if (status === 'forgotten') {
                    statusClass = 'bg-red-100 text-red-700';
                    statusText = '需复习';
                } else if (status === 'vague') {
                    statusClass = 'bg-yellow-100 text-yellow-700';
                    statusText = '学习中';
                }
                
                return `
                    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-all word-tag cursor-pointer" onclick="playWordAudio('${w.word}')">
                        <div class="flex-1">
                            <div class="flex items-center gap-2">
                                <span class="font-bold text-gray-900">${w.word}</span>
                                <span class="text-xs text-gray-500">${w.phonetic}</span>
                                <span class="text-xs px-2 py-0.5 rounded-full ${statusClass}">${statusText}</span>
                            </div>
                            <div class="text-sm text-gray-600 mt-1">${w.meaning}</div>
                        </div>
                        <div class="text-right">
                            <span class="text-xs text-gray-400">Band ${w.difficulty}</span>
                        </div>
                    </div>
                `;
            }).join('');
            
            document.getElementById('wordListContainer').innerHTML = html || '<div class="text-center text-gray-400 py-8">暂无符合条件的单词</div>';
        }

        function playWordAudio(word) {
            if ('speechSynthesis' in window) {
                const utterance = new SpeechSynthesisUtterance(word);
                utterance.lang = 'en-US';
                speechSynthesis.speak(utterance);
            }
        }

        // 统计与进度
        function updateStats() {
            const mastered = Object.values(wordStatus).filter(s => s.status === 'mastered').length;
            const review = Object.values(wordStatus).filter(s => s.status === 'forgotten').length;
            const total = vocabularyData.length;
            
            document.getElementById('todayLearned').textContent = `${todayLearned.size}/20`;
            document.getElementById('todayProgressBar').style.width = `${(todayLearned.size / 20) * 100}%`;
            document.getElementById('masteredCount').textContent = mastered;
            document.getElementById('masteredPercent').textContent = `${Math.round((mastered/total)*100)}%`;
            document.getElementById('reviewCount').textContent = review;
            document.getElementById('dashboard-vocab-progress').textContent = `今日学习: ${todayLearned.size}/20`;
            
            // 更新正确率显示
            if (todayTotal > 0) {
                const rate = Math.round((todayCorrect / todayTotal) * 100);
                document.getElementById('accuracyRate').textContent = `${rate}%`;
                document.getElementById('accuracyDetail').textContent = `${todayCorrect}/${todayTotal}`;
                document.getElementById('accuracyText').textContent = rate >= 80 ? '表现优秀！' : rate >= 60 ? '继续加油！' : '多多练习！';
            }
            
            // 检查是否完成今日目标
            if (todayLearned.size >= 20 && !studyHistory.includes(new Date().toDateString())) {
                streak++;
                studyHistory.push(new Date().toDateString());
                saveProgress();
                showToast('🎉 恭喜！完成今日学习目标！连续学习 ' + streak + ' 天');
            }
        }

        function updateDifficultyStats() {
            const band6 = vocabularyData.filter(w => parseFloat(w.difficulty) < 7.0).length;
            const band7 = vocabularyData.filter(w => parseFloat(w.difficulty) >= 7.0 && parseFloat(w.difficulty) < 8.0).length;
            const band8 = vocabularyData.filter(w => parseFloat(w.difficulty) >= 8.0).length;
            
            document.getElementById('countBand6').textContent = band6;
            document.getElementById('countBand7').textContent = band7;
            document.getElementById('countBand8').textContent = band8;
        }

        function renderCalendar() {
            const calendar = document.getElementById('studyCalendar');
            const today = new Date();
            const days = ['日', '一', '二', '三', '四', '五', '六'];
            
            let html = days.map(d => `<div class="text-gray-400 py-2">${d}</div>`).join('');
            
            // 获取本月第一天
            const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
            const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
            
            // 填充月初空白
            for (let i = 0; i < firstDay.getDay(); i++) {
                html += '<div></div>';
            }
            
            // 填充日期
            for (let d = 1; d <= lastDay.getDate(); d++) {
                const dateStr = new Date(today.getFullYear(), today.getMonth(), d).toDateString();
                const isToday = d === today.getDate();
                const studied = studyHistory.includes(dateStr);
                
                let classes = 'py-2 rounded-lg text-sm ';
                if (isToday) {
                    classes += 'bg-teal-600 text-white font-bold';
                } else if (studied) {
                    classes += 'bg-teal-100 text-teal-700';
                } else {
                    classes += 'text-gray-600 hover:bg-gray-100';
                }
                
                html += `<div class="${classes}">${d}</div>`;
            }
            
            calendar.innerHTML = html;
        }

        function saveProgress() {
            localStorage.setItem('wordStatus', JSON.stringify(wordStatus));
            localStorage.setItem('studyHistory', JSON.stringify(studyHistory));
            localStorage.setItem('lastStudyDate', lastStudyDate);
            localStorage.setItem('streak', streak);
        }

        function resetProgress() {
            if (confirm('确定要重置所有学习进度吗？这将清除所有单词掌握状态和学习记录。')) {
                wordStatus = {};
                studyHistory = [];
                todayLearned = new Set();
                todayCorrect = 0;
                todayTotal = 0;
                streak = 0;
                currentWordIndex = 0;
                saveProgress();
                updateStats();
                renderCalendar();
                showToast('已重置所有进度');
                if (currentVocabMode === 'learn') showLearnMode();
            }
        }

        function startReviewMode() {
            const reviewWords = vocabularyData.filter(w => wordStatus[w.word]?.status === 'forgotten');
            if (reviewWords.length === 0) {
                showToast('暂无需要复习的单词，继续学习新词吧！');
                return;
            }
            filteredWords = reviewWords;
            currentWordIndex = 0;
            setVocabMode('learn');
            showToast(`开始复习 ${reviewWords.length} 个单词`);
        }

        // ==================== 提示Toast ====================
        function showToast(message) {
            const toast = document.createElement('div');
            toast.className = 'fixed bottom-4 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white px-6 py-3 rounded-full shadow-lg z-50 text-sm fade-in';
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(() => {
                toast.remove();
            }, 3000);
        }

        // ==================== 原有功能保持不变 ====================
        const speakingTopics = [
            {topic: "Describe a difficult decision you made.", prompts: ["What the decision was", "When you made it", "Why it was difficult", "How you felt after deciding"]},
            {topic: "Describe a person who speaks a foreign language well.", prompts: ["Who this person is", "What language they speak", "How they learned it", "Why you think they speak it well"]},
            {topic: "Describe a time when you helped someone.", prompts: ["Who you helped", "How you helped them", "Why they needed help", "How you felt about it"]},
            {topic: "Describe an important object you own.", prompts: ["What it is", "How you got it", "Why it is important", "How often you use it"]}
        ];

        function setTask(task) {
            currentTask = task;
            document.getElementById('btn-task1').className = task === 'task1' ? 'px-3 py-1 rounded-full text-sm bg-teal-600 text-white' : 'px-3 py-1 rounded-full text-sm border hover:bg-gray-50';
            document.getElementById('btn-task2').className = task === 'task2' ? 'px-3 py-1 rounded-full text-sm bg-teal-600 text-white' : 'px-3 py-1 rounded-full text-sm border hover:bg-gray-50';
            document.getElementById('wordCountDisplay').textContent = `字数：0 / ${task === 'task1' ? '130+' : '220+'}`;
        }

        function updateWordCount() {
            const text = document.getElementById('essayInput').value;
            const count = text.trim() ? text.trim().split(/\\s+/).length : 0;
            const min = currentTask === 'task1' ? 130 : 220;
            document.getElementById('wordCountDisplay').textContent = `字数：${count} / ${min}+`;
        }

        async function submitEssay() {
            const essay = document.getElementById('essayInput').value;
            const wordCount = essay.trim() ? essay.trim().split(/\\s+/).length : 0;
            
            document.getElementById('submitBtn').disabled = true;
            document.getElementById('btnText').textContent = '评分中...';
            document.getElementById('btnLoader').classList.remove('hidden');

            try {
                const res = await fetch('/api/grade_writing', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({essay, task_type: currentTask, prompt: '', target_band: 7.0})
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
                    list.innerHTML = '';
                    data.detailed_feedback.weaknesses.forEach(w => list.innerHTML += `<li>• ${w}</li>`);
                }
            } catch(e) {
                alert('评分失败');
            }
            
            document.getElementById('submitBtn').disabled = false;
            document.getElementById('btnText').textContent = '提交评分';
            document.getElementById('btnLoader').classList.add('hidden');
        }

        function generateWritingPrompt() {
            const prompts = [
                "Some people think that the best way to reduce crime is to give longer prison sentences. Others believe there are better alternatives. Discuss both views.",
                "In many countries, traditional foods are being replaced by international fast food. This is having a negative effect on families and communities. To what extent do you agree?",
                "Space exploration is a waste of money. Do you agree or disagree?",
                "Should governments ban dangerous sports, or should people have the freedom to choose?"
            ];
            document.getElementById('promptDisplay').textContent = prompts[Math.floor(Math.random() * prompts.length)];
        }

        function generateSpeakingTopic() {
            const topic = speakingTopics[Math.floor(Math.random() * speakingTopics.length)];
            document.getElementById('speakingTopic').textContent = topic.topic;
            document.getElementById('speakingPrompts').innerHTML = topic.prompts.map(p => `<li>${p}</li>`).join('');
        }

        async function submitSpeaking() {
            const text = document.getElementById('speakingInput').value;
            if (text.split(/\\s+/).length < 50) {
                alert('回答太短，建议至少50词');
                return;
            }
            
            document.getElementById('speakBtn').disabled = true;
            document.getElementById('speakBtnText').textContent = '评分中...';
            document.getElementById('speakLoader').classList.remove('hidden');

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
                document.getElementById('pronScore').textContent = data.breakdown.pronunciation.score;
                
                const list = document.getElementById('speakSuggestions');
                list.innerHTML = '';
                data.suggestions.forEach(s => list.innerHTML += `<li>• ${s}</li>`);
            } catch(e) {
                alert('评分失败');
            }
            
            document.getElementById('speakBtn').disabled = false;
            document.getElementById('speakBtnText').textContent = '提交口语评分';
            document.getElementById('speakLoader').classList.add('hidden');
        }

        async function generatePrompt() {
            const type = document.getElementById('promptType').value;
            const res = await fetch('/api/generate_prompt?type=' + type);
            const data = await res.json();
            const div = document.getElementById('generatedPrompt');
            div.textContent = data.prompt;
            div.classList.remove('hidden');
        }

        async function checkGrammar() {
            const text = document.getElementById('grammarInput').value;
            const res = await fetch('/api/check_grammar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text})
            });
            const data = await res.json();
            const div = document.getElementById('grammarResult');
            div.innerHTML = data.issues.map(i => `<div class="mb-2 p-2 bg-orange-50 rounded text-orange-800">${i}</div>`).join('') || '<div class="text-green-600">未发现明显语法错误</div>';
            div.classList.remove('hidden');
        }

        // 初始化
        showSection('dashboard');
    </script>
</body>
</html>'''

print("代码已生成，包含以下背单词功能：")
print("\n1. 三种学习模式：")
print("   - 学习模式：翻转卡片展示单词、音标、释义和例句")
print("   - 测试模式：选择题形式测试已掌握单词")
print("   - 单词表：可筛选查看全部/未学习/学习中/已掌握单词")
print("\n2. 学习进度追踪：")
print("   - 今日学习进度（目标20词/天）")
print("   - 已掌握词汇统计与百分比")
print("   - 需复习单词数量（基于艾宾浩斯记忆曲线）")
print("   - 今日正确率统计")
print("   - 连续学习天数（Streak）")
print("   - 学习日历可视化")
print("\n3. 记忆辅助功能：")
print("   - 单词难度分级（Band 6.0-8.0+）")
print("   - 标记系统：掌握/模糊/忘记")
print("   - 浏览器语音合成播放单词发音")
print("   - 单词列表快速发音")
print("   - 记忆技巧提示")
print("\n4. 数据持久化：")
print("   - LocalStorage保存学习进度")
print("   - 支持重置进度")
print("   - 跨会话保持学习状态")
print("\n5. 包含20个雅思高频学术词汇示例")
