import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { sentences as allSentences } from '@/data/ieltsData'
import { RotateCcw, Trophy, Zap, Target, Clock } from 'lucide-react'

function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

export default function TypingPage() {
  const [sentences] = useState(() => shuffleArray(allSentences).slice(0, 10))
  const [currentIndex, setCurrentIndex] = useState(0)
  const [input, setInput] = useState('')
  const [started, setStarted] = useState(false)
  const [finished, setFinished] = useState(false)
  const [startTime, setStartTime] = useState<number | null>(null)
  const [endTime, setEndTime] = useState<number | null>(null)
  const [correctChars, setCorrectChars] = useState(0)
  const [totalChars, setTotalChars] = useState(0)
  const [wpmHistory, setWpmHistory] = useState<number[]>([])
  const inputRef = useRef<HTMLInputElement>(null)

  const currentSentence = sentences[currentIndex]
  const totalSentences = sentences.length

  const elapsed = startTime && !finished ? (Date.now() - startTime) / 1000 : endTime && startTime ? (endTime - startTime) / 1000 : 0
  const minutes = elapsed / 60
  const wpm = minutes > 0 ? Math.round((correctChars / 5) / minutes) : 0
  const accuracy = totalChars > 0 ? Math.round((correctChars / totalChars) * 100) : 100

  useEffect(() => {
    if (!started || finished) return
    const interval = setInterval(() => {
      const mins = (Date.now() - (startTime || Date.now())) / 1000 / 60
      if (mins > 0) {
        const currentWpm = Math.round((correctChars / 5) / mins)
        setWpmHistory(prev => [...prev.slice(-9), currentWpm])
      }
    }, 2000)
    return () => clearInterval(interval)
  }, [started, finished, startTime, correctChars])

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!currentSentence || finished) return

    if (!started) {
      setStarted(true)
      setStartTime(Date.now())
    }

    const val = e.target.value
    const target = currentSentence.englishText
    setInput(val)
    setTotalChars(prev => prev + 1)

    if (val.length > 0) {
      const lastIdx = val.length - 1
      if (target[lastIdx] === val[lastIdx]) {
        setCorrectChars(prev => prev + 1)
      }
    }

    if (val === target) {
      if (currentIndex < totalSentences - 1) {
        setCurrentIndex(prev => prev + 1)
        setInput('')
      } else {
        const end = Date.now()
        setEndTime(end)
        setFinished(true)
      }
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Backspace') {
      setTotalChars(prev => Math.max(0, prev - 1))
    }
  }

  const reset = () => {
    setCurrentIndex(0)
    setInput('')
    setStarted(false)
    setFinished(false)
    setStartTime(null)
    setEndTime(null)
    setCorrectChars(0)
    setTotalChars(0)
    setWpmHistory([])
    inputRef.current?.focus()
  }

  const renderSentence = () => {
    if (!currentSentence) return null
    const target = currentSentence.englishText
    return target.split('').map((char: string, idx: number) => {
      let className = 'text-muted-foreground'
      let decoration = ''

      if (idx < input.length) {
        if (input[idx] === char) {
          className = 'text-foreground font-bold'
        } else {
          className = 'text-destructive font-bold'
          decoration = 'line-through'
        }
      } else if (idx === input.length) {
        className = 'text-primary font-bold typing-cursor'
      }

      return (
        <span key={idx} className={`${className} ${decoration} text-xl lg:text-2xl leading-relaxed`}>
          {char}
        </span>
      )
    })
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black">打字特训</h1>
          <p className="text-muted-foreground mt-1">输入经典雅思句子，训练肌肉记忆</p>
        </div>
        <button
          onClick={reset}
          className="flex items-center gap-2 px-4 py-2 bg-secondary rounded-lg hover:bg-secondary/80 transition-colors"
        >
          <RotateCcw size={16} />
          <span>重置</span>
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {[
          { label: 'WPM', value: wpm, icon: Zap, color: 'text-yellow-400' },
          { label: '准确率', value: `${accuracy}%`, icon: Target, color: 'text-green-400' },
          { label: '时间', value: `${Math.round(elapsed)}s`, icon: Clock, color: 'text-blue-400' },
          { label: '进度', value: `${currentIndex + 1}/${totalSentences}`, icon: Trophy, color: 'text-purple-400' },
        ].map((stat) => (
          <div key={stat.label} className="bg-card border border-border rounded-xl p-3 text-center">
            <div className={`flex items-center justify-center gap-1 mb-1 ${stat.color}`}>
              <stat.icon size={14} />
              <span className="text-xs">{stat.label}</span>
            </div>
            <span className="text-xl font-black font-mono">{stat.value}</span>
          </div>
        ))}
      </div>

      <div className="relative bg-card border border-border rounded-2xl p-8 lg:p-12 min-h-[300px] flex flex-col items-center justify-center">
        <AnimatePresence mode="wait">
          {!finished ? (
            <motion.div
              key={currentIndex}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="w-full"
            >
              {currentSentence?.chineseTranslation && (
                <p className="text-center text-sm text-muted-foreground mb-6">
                  {currentSentence.chineseTranslation}
                </p>
              )}

              <div className="text-center mb-8 flex flex-wrap justify-center gap-0">
                {renderSentence()}
              </div>

              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                className="absolute opacity-0 top-0 left-0 w-full h-full cursor-text"
                autoComplete="off"
                autoCapitalize="off"
                spellCheck={false}
                autoFocus
              />

              {!started && (
                <p className="text-center text-sm text-muted-foreground animate-pulse">
                  点击此处开始打字...
                </p>
              )}
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="text-center space-y-6"
            >
              <div className="text-6xl mb-4">🎉</div>
              <h2 className="text-3xl font-black text-primary">训练完成!</h2>

              <div className="grid grid-cols-3 gap-4">
                <div className="bg-secondary rounded-xl p-4">
                  <div className="text-sm text-muted-foreground mb-1">平均 WPM</div>
                  <div className="text-3xl font-black text-yellow-400">{wpm}</div>
                </div>
                <div className="bg-secondary rounded-xl p-4">
                  <div className="text-sm text-muted-foreground mb-1">准确率</div>
                  <div className="text-3xl font-black text-green-400">{accuracy}%</div>
                </div>
                <div className="bg-secondary rounded-xl p-4">
                  <div className="text-sm text-muted-foreground mb-1">用时</div>
                  <div className="text-3xl font-black text-blue-400">{Math.round(elapsed)}s</div>
                </div>
              </div>

              {wpmHistory.length > 0 && (
                <div className="bg-secondary rounded-xl p-4">
                  <div className="text-sm text-muted-foreground mb-3">WPM 走势</div>
                  <div className="flex items-end gap-1 h-24">
                    {wpmHistory.map((w, i) => (
                      <motion.div
                        key={i}
                        initial={{ height: 0 }}
                        animate={{ height: `${Math.min((w / Math.max(...wpmHistory, 1)) * 100, 100)}%` }}
                        className="flex-1 bg-primary/60 rounded-t"
                        transition={{ delay: i * 0.05 }}
                      />
                    ))}
                  </div>
                </div>
              )}

              <button
                onClick={reset}
                className="px-8 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity"
              >
                再来一组
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <div className="w-full h-1 bg-secondary rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-primary rounded-full"
          animate={{ width: `${((currentIndex + (finished ? 1 : 0)) / totalSentences) * 100}%` }}
          transition={{ duration: 0.3 }}
        />
      </div>
    </div>
  )
}
