import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { grammarQuestions as allQuestions } from '@/data/ieltsData'
import { Check, X, Zap, BookOpen } from 'lucide-react'

function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

export default function GrammarPage() {
  const [questions] = useState(() => shuffleArray(allQuestions).slice(0, 15))
  const [currentIndex, setCurrentIndex] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [score, setScore] = useState(0)
  const [combo, setCombo] = useState(0)
  const [maxCombo, setMaxCombo] = useState(0)
  const [finished, setFinished] = useState(false)
  const [results, setResults] = useState<{ correct: boolean; question: string }[]>([])

  const currentQuestion = questions[currentIndex]
  const totalQuestions = questions.length
  const options: string[] = currentQuestion ? JSON.parse(currentQuestion.optionsJSON) as string[] : []
  const isCorrect = selectedAnswer === currentQuestion?.correctAnswerIndex

  const handleSelect = (index: number) => {
    if (showResult || !currentQuestion) return

    setSelectedAnswer(index)
    setShowResult(true)

    const correct = index === currentQuestion.correctAnswerIndex
    if (correct) {
      setScore(prev => prev + 10 + combo * 2)
      setCombo(prev => {
        const newCombo = prev + 1
        setMaxCombo(c => Math.max(c, newCombo))
        return newCombo
      })
    } else {
      setCombo(0)
    }

    setResults(prev => [...prev, { correct, question: currentQuestion.questionText }])
  }

  const handleNext = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex(prev => prev + 1)
      setSelectedAnswer(null)
      setShowResult(false)
    } else {
      setFinished(true)
    }
  }

  const reset = () => {
    setCurrentIndex(0)
    setSelectedAnswer(null)
    setShowResult(false)
    setScore(0)
    setCombo(0)
    setMaxCombo(0)
    setFinished(false)
    setResults([])
  }

  if (finished) {
    const correctCount = results.filter(r => r.correct).length
    const accuracy = Math.round((correctCount / totalQuestions) * 100)

    return (
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-card border border-border rounded-2xl p-8 text-center space-y-6"
        >
          <div className="text-6xl">🏆</div>
          <h2 className="text-3xl font-black text-primary">语法闯关完成!</h2>

          <div className="grid grid-cols-3 gap-4">
            <div className="bg-secondary rounded-xl p-4">
              <div className="text-sm text-muted-foreground mb-1">得分</div>
              <div className="text-3xl font-black text-yellow-400">{score}</div>
            </div>
            <div className="bg-secondary rounded-xl p-4">
              <div className="text-sm text-muted-foreground mb-1">正确率</div>
              <div className="text-3xl font-black text-green-400">{accuracy}%</div>
            </div>
            <div className="bg-secondary rounded-xl p-4">
              <div className="text-sm text-muted-foreground mb-1">最高连击</div>
              <div className="text-3xl font-black text-orange-400">x{maxCombo}</div>
            </div>
          </div>

          <div className="space-y-2 text-left">
            <h3 className="font-bold text-sm text-muted-foreground">答题回顾</h3>
            {results.map((r, i) => (
              <div key={i} className={`flex items-center gap-2 p-2 rounded-lg ${r.correct ? 'bg-green-500/10' : 'bg-red-500/10'}`}>
                {r.correct ? <Check size={16} className="text-green-400 shrink-0" /> : <X size={16} className="text-red-400 shrink-0" />}
                <span className="text-sm truncate">{r.question}</span>
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
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black">语法闯关</h1>
          <p className="text-muted-foreground mt-1">识别语法陷阱，巩固语法基础</p>
        </div>
        <div className="flex items-center gap-4">
          {combo >= 3 && (
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="flex items-center gap-1 text-orange-400 font-bold"
            >
              <Zap size={18} />
              <span>x{combo} Combo!</span>
            </motion.div>
          )}
          <div className="text-right">
            <div className="text-sm text-muted-foreground">得分</div>
            <div className="text-xl font-black text-primary">{score}</div>
          </div>
        </div>
      </div>

      <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
        <motion.div
          className="h-full bg-primary rounded-full"
          animate={{ width: `${(currentIndex / totalQuestions) * 100}%` }}
        />
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={currentIndex}
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -50 }}
          className="bg-card border border-border rounded-2xl p-8 space-y-6"
        >
          <div className="text-xl lg:text-2xl font-medium leading-relaxed">
            {currentQuestion?.questionText}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {options.map((option: string, index: number) => {
              let buttonClass = 'border-border hover:border-primary hover:bg-primary/5'
              let icon = null

              if (showResult) {
                if (index === currentQuestion?.correctAnswerIndex) {
                  buttonClass = 'border-green-500 bg-green-500/10 neon-success'
                  icon = <Check size={20} className="text-green-400" />
                } else if (index === selectedAnswer && !isCorrect) {
                  buttonClass = 'border-red-500 bg-red-500/10'
                  icon = <X size={20} className="text-red-400" />
                } else {
                  buttonClass = 'border-border opacity-50'
                }
              }

              return (
                <motion.button
                  key={index}
                  onClick={() => handleSelect(index)}
                  disabled={showResult}
                  whileHover={!showResult ? { scale: 1.02 } : {}}
                  whileTap={!showResult ? { scale: 0.98 } : {}}
                  className={`relative flex items-center justify-between p-4 border-2 rounded-xl text-left transition-all ${buttonClass}`}
                >
                  <span className="font-medium">{option}</span>
                  {icon}
                </motion.button>
              )
            })}
          </div>

          <AnimatePresence>
            {showResult && currentQuestion?.explanation && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                className="bg-secondary/50 rounded-xl p-4"
              >
                <div className="flex items-center gap-2 mb-2 text-primary">
                  <BookOpen size={16} />
                  <span className="font-bold text-sm">解析</span>
                </div>
                <p className="text-sm text-muted-foreground">{currentQuestion.explanation}</p>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {showResult && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex justify-end"
              >
                <button
                  onClick={handleNext}
                  className="px-6 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity"
                >
                  {currentIndex < totalQuestions - 1 ? '下一题 ->' : '查看结果'}
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </AnimatePresence>

      <p className="text-center text-sm text-muted-foreground">
        {currentIndex + 1} / {totalQuestions}
      </p>
    </div>
  )
}
