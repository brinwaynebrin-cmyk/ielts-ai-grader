import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { vocabulary as allWords } from '@/data/ieltsData'
import { Volume2, ThumbsUp, ThumbsDown, Star } from 'lucide-react'

function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

export default function VocabularyPage() {
  const [words] = useState(() => shuffleArray(allWords).slice(0, 20))
  const [currentIndex, setCurrentIndex] = useState(0)
  const [flipped, setFlipped] = useState(false)
  const [direction, setDirection] = useState<'left' | 'right' | null>(null)
  const [mastered, setMastered] = useState(0)
  const [reviewing, setReviewing] = useState(0)
  const [finished, setFinished] = useState(false)
  const [sessionStats, setSessionStats] = useState<{ word: string; status: 'mastered' | 'review' }[]>([])

  const currentWord = words[currentIndex]
  const totalWords = words.length

  const speakWord = (text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.lang = 'en-US'
      utterance.rate = 0.8
      window.speechSynthesis.speak(utterance)
    }
  }

  const handleFlip = () => {
    setFlipped(!flipped)
    if (!flipped && currentWord) {
      speakWord(currentWord.word)
    }
  }

  const handleResponse = (known: boolean) => {
    if (!currentWord) return

    setDirection(known ? 'right' : 'left')
    if (known) {
      setMastered(prev => prev + 1)
    } else {
      setReviewing(prev => prev + 1)
    }

    setSessionStats(prev => [...prev, { word: currentWord.word, status: known ? 'mastered' : 'review' }])

    setTimeout(() => {
      if (currentIndex < totalWords - 1) {
        setCurrentIndex(prev => prev + 1)
        setFlipped(false)
        setDirection(null)
      } else {
        setFinished(true)
      }
    }, 400)
  }

  const reset = () => {
    setCurrentIndex(0)
    setFlipped(false)
    setDirection(null)
    setMastered(0)
    setReviewing(0)
    setFinished(false)
    setSessionStats([])
  }

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (finished) return
      if (e.code === 'Space') {
        e.preventDefault()
        handleFlip()
      } else if (e.code === 'ArrowRight') {
        handleResponse(true)
      } else if (e.code === 'ArrowLeft') {
        handleResponse(false)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [flipped, currentIndex, finished])

  if (finished) {
    return (
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-card border border-border rounded-2xl p-8 text-center space-y-6"
        >
          <div className="text-6xl">📚</div>
          <h2 className="text-3xl font-black text-primary">本轮完成!</h2>

          <div className="grid grid-cols-2 gap-4">
            <div className="bg-green-500/10 rounded-xl p-4">
              <div className="text-sm text-muted-foreground mb-1">已掌握</div>
              <div className="text-3xl font-black text-green-400">{mastered}</div>
            </div>
            <div className="bg-orange-500/10 rounded-xl p-4">
              <div className="text-sm text-muted-foreground mb-1">需复习</div>
              <div className="text-3xl font-black text-orange-400">{reviewing}</div>
            </div>
          </div>

          <div className="space-y-2 text-left max-h-60 overflow-y-auto">
            {sessionStats.map((s, i) => (
              <div key={i} className={`flex items-center gap-2 p-2 rounded-lg ${s.status === 'mastered' ? 'bg-green-500/5' : 'bg-orange-500/5'}`}>
                {s.status === 'mastered' ? <ThumbsUp size={14} className="text-green-400 shrink-0" /> : <ThumbsDown size={14} className="text-orange-400 shrink-0" />}
                <span className="text-sm font-medium">{s.word}</span>
                <span className="text-xs text-muted-foreground ml-auto">{s.status === 'mastered' ? '已掌握' : '需复习'}</span>
              </div>
            ))}
          </div>

          <button
            onClick={reset}
            className="px-8 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity"
          >
            再来一轮
          </button>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black">高频词汇</h1>
          <p className="text-muted-foreground mt-1">空格翻转卡片，{'<-'}不认识 {'->'}认识</p>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <span className="flex items-center gap-1 text-green-400">
            <ThumbsUp size={14} />
            {mastered}
          </span>
          <span className="flex items-center gap-1 text-orange-400">
            <ThumbsDown size={14} />
            {reviewing}
          </span>
          <span className="text-muted-foreground">
            {currentIndex + 1}/{totalWords}
          </span>
        </div>
      </div>

      <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-gradient-to-r from-purple-500 to-violet-400 rounded-full"
          animate={{ width: `${(currentIndex / totalWords) * 100}%` }}
        />
      </div>

      <div className="perspective-1000">
        <motion.div
          key={currentIndex}
          initial={{ opacity: 0, x: direction === 'left' ? -100 : direction === 'right' ? 100 : 0 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: direction === 'left' ? -200 : direction === 'right' ? 200 : 0 }}
          transition={{ duration: 0.3 }}
          className="cursor-pointer"
          onClick={handleFlip}
        >
          <div className={`flip-card-inner relative w-full h-80 ${flipped ? 'flipped' : ''}`}>
            <div className="flip-card-front absolute inset-0 bg-gradient-to-br from-purple-500/10 to-violet-500/10 border border-purple-500/20 rounded-2xl p-8 flex flex-col items-center justify-center">
              <div className="text-center space-y-4">
                <h2 className="text-4xl font-black">{currentWord?.word}</h2>
                {currentWord?.phonetic && (
                  <p className="text-lg text-muted-foreground font-mono">{currentWord.phonetic}</p>
                )}
                {currentWord?.partOfSpeech && (
                  <span className="inline-block px-3 py-1 bg-purple-500/20 rounded-full text-sm text-purple-300">
                    {currentWord.partOfSpeech}
                  </span>
                )}
                <div className="flex items-center justify-center gap-2 text-muted-foreground">
                  <Volume2 size={16} />
                  <span className="text-sm">点击翻转或按空格键</span>
                </div>
              </div>
            </div>

            <div className="flip-card-back absolute inset-0 bg-gradient-to-br from-violet-500/10 to-purple-500/10 border border-violet-500/20 rounded-2xl p-8 flex flex-col items-center justify-center">
              <div className="text-center space-y-4">
                <p className="text-2xl font-medium text-primary">{currentWord?.chineseMeaning}</p>
                {currentWord?.exampleSentence && (
                  <div className="mt-4 p-4 bg-secondary/50 rounded-xl">
                    <p className="text-sm italic text-muted-foreground">"{currentWord.exampleSentence}"</p>
                    {currentWord.exampleTranslation && (
                      <p className="text-xs text-muted-foreground mt-2">{currentWord.exampleTranslation}</p>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </motion.div>
      </div>

      <div className="flex items-center justify-center gap-4">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => handleResponse(false)}
          className="flex items-center gap-2 px-6 py-3 bg-orange-500/20 border border-orange-500/30 text-orange-400 rounded-xl font-bold hover:bg-orange-500/30 transition-colors"
        >
          <ThumbsDown size={18} />
          <span>不认识 (&lt;-)</span>
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => speakWord(currentWord?.word || '')}
          className="p-3 bg-secondary rounded-xl hover:bg-secondary/80 transition-colors"
        >
          <Volume2 size={20} />
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => handleResponse(true)}
          className="flex items-center gap-2 px-6 py-3 bg-green-500/20 border border-green-500/30 text-green-400 rounded-xl font-bold hover:bg-green-500/30 transition-colors"
        >
          <ThumbsUp size={18} />
          <span>认识 (-&gt;)</span>
        </motion.button>
      </div>

      {currentWord?.difficultyBand && (
        <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
          <Star size={14} className="text-yellow-400" />
          <span>Band {currentWord.difficultyBand.replace('band', '')} 词汇</span>
        </div>
      )}
    </div>
  )
}
