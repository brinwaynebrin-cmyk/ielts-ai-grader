import { useState, useEffect, useCallback } from 'react'
import { motion, AnimatePresence, Reorder } from 'framer-motion'
import { vocabulary as allVocab, sentences as allSentences } from '@/data/ieltsData'
import { Zap, Target, Clock, Trophy, ArrowRight, RotateCcw } from 'lucide-react'

// Word Scramble Game
function WordScramble({ onScore }: { onScore: (points: number) => void }) {
  const vocab = allVocab
  const [currentWord, setCurrentWord] = useState(0)
  const [scrambled, setScrambled] = useState('')
  const [userGuess, setUserGuess] = useState('')
  const [feedback, setFeedback] = useState<'correct' | 'wrong' | null>(null)
  const [score, setScore] = useState(0)
  const [timeLeft, setTimeLeft] = useState(60)
  const [gameOver, setGameOver] = useState(false)
  const [wordsSolved, setWordsSolved] = useState(0)

  const shuffleWord = (word: string) => {
    const arr = word.split('')
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]]
    }
    return arr.join('')
  }

  const nextWord = useCallback(() => {
    if (!vocab || vocab.length === 0) return
    const idx = Math.floor(Math.random() * vocab.length)
    setCurrentWord(idx)
    const word = vocab[idx].word
    let shuffled = shuffleWord(word)
    while (shuffled === word && word.length > 1) {
      shuffled = shuffleWord(word)
    }
    setScrambled(shuffled)
    setUserGuess('')
    setFeedback(null)
  }, [vocab])

  useEffect(() => {
    nextWord()
  }, [nextWord])

  useEffect(() => {
    if (timeLeft <= 0) {
      setGameOver(true)
      onScore(score)
      return
    }
    const timer = setInterval(() => setTimeLeft(prev => prev - 1), 1000)
    return () => clearInterval(timer)
  }, [timeLeft, score, onScore])

  const handleSubmit = () => {
    if (!vocab) return
    const word = vocab[currentWord].word
    if (userGuess.toLowerCase().trim() === word.toLowerCase()) {
      setFeedback('correct')
      setScore(prev => prev + 10)
      setWordsSolved(prev => prev + 1)
      setTimeout(nextWord, 500)
    } else {
      setFeedback('wrong')
      setTimeout(() => setFeedback(null), 1000)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') handleSubmit()
  }

  if (gameOver) {
    return (
      <div className="text-center space-y-4">
        <div className="text-5xl">🏆</div>
        <h3 className="text-2xl font-black">时间到!</h3>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-secondary rounded-xl p-4">
            <div className="text-sm text-muted-foreground">得分</div>
            <div className="text-3xl font-black text-yellow-400">{score}</div>
          </div>
          <div className="bg-secondary rounded-xl p-4">
            <div className="text-sm text-muted-foreground">解出单词</div>
            <div className="text-3xl font-black text-green-400">{wordsSolved}</div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-yellow-400">
          <Zap size={18} />
          <span className="font-bold">{score}</span>
        </div>
        <div className="flex items-center gap-2 text-red-400">
          <Clock size={18} />
          <span className="font-bold font-mono">{timeLeft}s</span>
        </div>
      </div>

      <div className="text-center space-y-4">
        <p className="text-sm text-muted-foreground">重组下列字母组成正确的单词</p>
        <div className="bg-secondary rounded-xl p-6">
          <motion.div
            key={scrambled}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="text-3xl font-black tracking-[0.3em] text-primary"
          >
            {scrambled.split('').map((char: string, i: number) => (
              <motion.span
                key={i}
                initial={{ y: -20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: i * 0.05 }}
              >
                {char.toUpperCase()}
              </motion.span>
            ))}
          </motion.div>
        </div>
        {vocab && (
          <p className="text-sm text-muted-foreground">
            提示: {vocab[currentWord]?.chineseMeaning}
          </p>
        )}

        <div className="flex gap-2">
          <input
            type="text"
            value={userGuess}
            onChange={(e) => setUserGuess(e.target.value)}
            onKeyDown={handleKeyDown}
            className={`flex-1 px-4 py-3 bg-secondary border-2 rounded-xl text-center text-lg font-bold uppercase ${
              feedback === 'correct' ? 'border-green-500 text-green-400' :
              feedback === 'wrong' ? 'border-red-500 text-red-400 animate-shake' :
              'border-border'
            }`}
            placeholder="输入单词"
            autoFocus
          />
          <button
            onClick={handleSubmit}
            className="px-6 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity"
          >
            提交
          </button>
        </div>

        <p className="text-xs text-muted-foreground">已解决: {wordsSolved} 个单词</p>
      </div>
    </div>
  )
}

// Sentence Rebuild Game
function SentenceRebuild({ onScore }: { onScore: (points: number) => void }) {
  const sentences = allSentences
  const [currentIdx, setCurrentIdx] = useState(0)
  const [pieces, setPieces] = useState<string[]>([])
  const [originalPieces, setOriginalPieces] = useState<string[]>([])
  const [completed, setCompleted] = useState(false)
  const [score, setScore] = useState(0)
  const [totalSolved, setTotalSolved] = useState(0)

  const prepareSentence = useCallback(() => {
    if (!sentences || sentences.length === 0) return
    const sent = sentences[currentIdx]
    const words = sent.englishText.split(' ')
    const groups: string[] = []
    let i = 0
    while (i < words.length) {
      const groupSize = Math.min(2 + Math.floor(Math.random() * 2), words.length - i)
      groups.push(words.slice(i, i + groupSize).join(' '))
      i += groupSize
    }

    setOriginalPieces(groups)
    setPieces([...groups].sort(() => Math.random() - 0.5))
    setCompleted(false)
  }, [sentences, currentIdx])

  useEffect(() => {
    prepareSentence()
  }, [prepareSentence])

  const checkOrder = (newOrder: string[]) => {
    setPieces(newOrder)
    const isCorrect = newOrder.every((piece: string, idx: number) => piece === originalPieces[idx])
    if (isCorrect && !completed) {
      setCompleted(true)
      setScore(prev => prev + 15)
      setTotalSolved(prev => prev + 1)
      onScore(15)
      setTimeout(() => {
        if (currentIdx < (sentences?.length || 0) - 1) {
          setCurrentIdx(prev => prev + 1)
        } else {
          setCurrentIdx(0)
        }
      }, 1500)
    }
  }

  if (!sentences) return null

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-yellow-400">
          <Zap size={18} />
          <span className="font-bold">{score}</span>
        </div>
        <span className="text-sm text-muted-foreground">已重组: {totalSolved} 句</span>
      </div>

      <div className="text-center space-y-4">
        <p className="text-sm text-muted-foreground">拖拽碎片重新排列成正确的句子</p>

        {sentences[currentIdx]?.chineseTranslation && (
          <p className="text-lg font-medium text-primary">
            {sentences[currentIdx].chineseTranslation}
          </p>
        )}

        {completed && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="text-green-400 font-bold"
          >
            ✓ 正确! +15 分
          </motion.div>
        )}

        <Reorder.Group
          axis="y"
          values={pieces}
          onReorder={checkOrder}
          className="space-y-2"
        >
          {pieces.map((piece: string) => (
            <Reorder.Item
              key={piece}
              value={piece}
              className={`p-4 bg-card border-2 rounded-xl cursor-grab active:cursor-grabbing font-medium ${
                completed ? 'border-green-500 neon-success' : 'border-border hover:border-primary/50'
              }`}
            >
              {piece}
            </Reorder.Item>
          ))}
        </Reorder.Group>
      </div>
    </div>
  )
}

// Fill in the Blank Game
function FillBlankGame({ onScore }: { onScore: (points: number) => void }) {
  const vocab = allVocab
  const [currentIdx, setCurrentIdx] = useState(0)
  const [options, setOptions] = useState<string[]>([])
  const [selected, setSelected] = useState<string | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [score, setScore] = useState(0)
  const [totalAnswered, setTotalAnswered] = useState(0)

  useEffect(() => {
    if (!vocab || vocab.length === 0) return
    const current = vocab[currentIdx]
    const otherWords = vocab.filter((_, i: number) => i !== currentIdx).sort(() => Math.random() - 0.5).slice(0, 3).map((v: typeof vocab[0]) => v.word)
    setOptions([current.word, ...otherWords].sort(() => Math.random() - 0.5))
    setSelected(null)
    setShowResult(false)
  }, [vocab, currentIdx])

  const handleSelect = (word: string) => {
    if (showResult || !vocab) return
    setSelected(word)
    setShowResult(true)
    setTotalAnswered(prev => prev + 1)

    const correct = word === vocab[currentIdx].word
    if (correct) {
      setScore(prev => prev + 10)
      onScore(10)
    }

    setTimeout(() => {
      if (currentIdx < (vocab?.length || 0) - 1) {
        setCurrentIdx(prev => prev + 1)
      } else {
        setCurrentIdx(0)
      }
    }, 1000)
  }

  if (!vocab) return null
  const current = vocab[currentIdx]
  const sentence = current.exampleSentence || `The word _____ is commonly used in IELTS writing.`
  const blankSentence = sentence.replace(current.word, '_____')

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2 text-yellow-400">
          <Zap size={18} />
          <span className="font-bold">{score}</span>
        </div>
        <span className="text-sm text-muted-foreground">已答题: {totalAnswered}</span>
      </div>

      <div className="text-center space-y-6">
        <div className="bg-secondary rounded-xl p-6">
          <p className="text-lg font-medium leading-relaxed">{blankSentence}</p>
        </div>

        <p className="text-muted-foreground">
          词义: {current.chineseMeaning}
        </p>

        {showResult && (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className={selected === current.word ? 'text-green-400 font-bold' : 'text-red-400 font-bold'}
          >
            {selected === current.word ? '✓ 正确!' : `✗ 正确答案是: ${current.word}`}
          </motion.div>
        )}

        <div className="grid grid-cols-2 gap-3">
          {options.map((opt: string) => (
            <motion.button
              key={opt}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => handleSelect(opt)}
              disabled={showResult}
              className={`p-4 border-2 rounded-xl font-bold transition-all ${
                showResult && opt === current.word
                  ? 'border-green-500 bg-green-500/10 text-green-400'
                  : showResult && opt === selected && opt !== current.word
                  ? 'border-red-500 bg-red-500/10 text-red-400'
                  : 'border-border bg-card hover:border-primary/50'
              }`}
            >
              {opt}
            </motion.button>
          ))}
        </div>
      </div>
    </div>
  )
}

// Main Games Page
export default function GamesPage() {
  const [activeGame, setActiveGame] = useState<'menu' | 'scramble' | 'rebuild' | 'fillblank'>('menu')
  const [totalScore, setTotalScore] = useState(0)

  const handleScore = (points: number) => {
    setTotalScore(prev => prev + points)
  }

  const games = [
    {
      id: 'scramble' as const,
      title: '单词重组',
      desc: '打乱字母，重组单词。限时60秒!',
      icon: Zap,
      color: 'from-yellow-500/20 to-amber-500/20',
      borderColor: 'border-yellow-500/30',
    },
    {
      id: 'rebuild' as const,
      title: '句子拼图',
      desc: '拖拽碎片，还原完整句子',
      icon: Target,
      color: 'from-blue-500/20 to-cyan-500/20',
      borderColor: 'border-blue-500/30',
    },
    {
      id: 'fillblank' as const,
      title: '选词填空',
      desc: '根据上下文选择正确的单词',
      icon: Trophy,
      color: 'from-green-500/20 to-emerald-500/20',
      borderColor: 'border-green-500/30',
    },
  ]

  if (activeGame === 'menu') {
    return (
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-black">娱乐竞技场</h1>
          <p className="text-lg text-muted-foreground">通过游戏化学习，在轻松愉快的氛围中巩固知识</p>
        </div>

        {totalScore > 0 && (
          <div className="bg-card border border-border rounded-xl p-4 text-center">
            <span className="text-muted-foreground">本次会话总得分: </span>
            <span className="text-2xl font-black text-yellow-400">{totalScore}</span>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {games.map((game) => (
            <motion.button
              key={game.id}
              whileHover={{ scale: 1.02, y: -4 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => { setActiveGame(game.id); setTotalScore(0); }}
              className={`bg-gradient-to-br ${game.color} border ${game.borderColor} rounded-2xl p-6 text-left space-y-4 hover:shadow-lg transition-shadow`}
            >
              <div className="inline-flex p-3 rounded-xl bg-background/50">
                <game.icon size={28} className="text-primary" />
              </div>
              <div>
                <h3 className="text-xl font-bold mb-1">{game.title}</h3>
                <p className="text-sm text-muted-foreground">{game.desc}</p>
              </div>
              <div className="flex items-center gap-1 text-sm font-medium text-primary">
                <span>开始游戏</span>
                <ArrowRight size={14} />
              </div>
            </motion.button>
          ))}
        </div>
      </div>
    )
  }

  const currentGame = games.find(g => g.id === activeGame)

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setActiveGame('menu')}
            className="p-2 hover:bg-secondary rounded-lg transition-colors"
          >
            ←
          </button>
          <h2 className="text-2xl font-black">{currentGame?.title}</h2>
        </div>
        <button
          onClick={() => { setActiveGame('menu'); setTotalScore(0); }}
          className="p-2 hover:bg-secondary rounded-lg transition-colors"
        >
          <RotateCcw size={18} />
        </button>
      </div>

      <div className="bg-card border border-border rounded-2xl p-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeGame}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
          >
            {activeGame === 'scramble' && <WordScramble onScore={handleScore} />}
            {activeGame === 'rebuild' && <SentenceRebuild onScore={handleScore} />}
            {activeGame === 'fillblank' && <FillBlankGame onScore={handleScore} />}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  )
}
