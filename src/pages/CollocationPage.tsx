import { useState } from 'react'
import { motion } from 'framer-motion'
import { collocations as allCollocations } from '@/data/ieltsData'
import { Check, RotateCcw, Target, Zap } from 'lucide-react'

function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

export default function CollocationPage() {
  const [collocations] = useState(() => shuffleArray(allCollocations))
  const [gameState, setGameState] = useState<'idle' | 'playing' | 'result'>('idle')
  const [currentRound, setCurrentRound] = useState(0)
  const [selectedVerb, setSelectedVerb] = useState<string | null>(null)
  const [matchedPairs, setMatchedPairs] = useState<Set<number>>(new Set())
  const [score, setScore] = useState(0)
  const [roundScore, setRoundScore] = useState(0)
  const [shakeItem, setShakeItem] = useState<number | null>(null)

  const rounds: typeof allCollocations[] = []
  for (let i = 0; i < collocations.length; i += 4) {
    const round = collocations.slice(i, i + 4)
    if (round.length === 4) rounds.push(round)
  }

  const currentRoundData = rounds[currentRound] || []
  const shuffledVerbs = [...currentRoundData].sort(() => Math.random() - 0.5)
  const totalRounds = rounds.length

  const handleVerbClick = (verb: string) => {
    if (selectedVerb === verb) {
      setSelectedVerb(null)
    } else {
      setSelectedVerb(verb)
    }
  }

  const handleSentenceClick = (item: typeof currentRoundData[0], index: number) => {
    if (!selectedVerb || matchedPairs.has(index)) return

    if (selectedVerb === item.verb) {
      const newMatched = new Set(matchedPairs)
      newMatched.add(index)
      setMatchedPairs(newMatched)
      setScore(prev => prev + 10)
      setRoundScore(prev => prev + 10)
      setSelectedVerb(null)

      if (newMatched.size === 4) {
        setTimeout(() => {
          if (currentRound < rounds.length - 1) {
            setCurrentRound(prev => prev + 1)
            setMatchedPairs(new Set())
            setRoundScore(0)
            setSelectedVerb(null)
          } else {
            setGameState('result')
          }
        }, 800)
      }
    } else {
      setShakeItem(index)
      setTimeout(() => setShakeItem(null), 500)
      setSelectedVerb(null)
    }
  }

  const startGame = () => {
    setGameState('playing')
    setCurrentRound(0)
    setMatchedPairs(new Set())
    setScore(0)
    setRoundScore(0)
    setSelectedVerb(null)
  }

  const reset = () => {
    setGameState('idle')
    setCurrentRound(0)
    setMatchedPairs(new Set())
    setScore(0)
    setRoundScore(0)
    setSelectedVerb(null)
  }

  if (gameState === 'idle') {
    return (
      <div className="max-w-2xl mx-auto text-center space-y-8">
        <div>
          <h1 className="text-4xl font-black mb-3">固定搭配</h1>
          <p className="text-lg text-muted-foreground">选择正确的动词，匹配对应的句子。掌握动词短语是雅思写作和口语提分的关键。</p>
        </div>

        <div className="bg-card border border-border rounded-2xl p-8 space-y-4">
          <div className="text-6xl">🔗</div>
          <h3 className="text-xl font-bold">游戏规则</h3>
          <ul className="text-left text-muted-foreground space-y-2 max-w-md mx-auto">
            <li className="flex items-start gap-2">
              <Target size={18} className="text-primary shrink-0 mt-0.5" />
              <span>每轮有4个动词和4个句子</span>
            </li>
            <li className="flex items-start gap-2">
              <Zap size={18} className="text-primary shrink-0 mt-0.5" />
              <span>先点击选择动词，再点击句子进行匹配</span>
            </li>
            <li className="flex items-start gap-2">
              <Check size={18} className="text-primary shrink-0 mt-0.5" />
              <span>正确匹配 +10 分，错误不扣分</span>
            </li>
          </ul>
          <button
            onClick={startGame}
            className="px-8 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity"
          >
            开始挑战
          </button>
        </div>
      </div>
    )
  }

  if (gameState === 'result') {
    return (
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-card border border-border rounded-2xl p-8 text-center space-y-6"
        >
          <div className="text-6xl">🎯</div>
          <h2 className="text-3xl font-black text-primary">挑战完成!</h2>
          <div className="bg-secondary rounded-xl p-6">
            <div className="text-sm text-muted-foreground mb-2">总得分</div>
            <div className="text-5xl font-black text-yellow-400">{score}</div>
          </div>
          <p className="text-muted-foreground">
            你完成了 {totalRounds} 轮搭配练习，共 {totalRounds * 4} 组固定搭配。
          </p>
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
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black">固定搭配</h1>
          <p className="text-muted-foreground mt-1">选择动词，匹配正确的句子</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <div className="text-sm text-muted-foreground">得分</div>
            <div className="text-xl font-black text-primary">{score}</div>
          </div>
          <button onClick={reset} className="p-2 hover:bg-secondary rounded-lg transition-colors">
            <RotateCcw size={18} />
          </button>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-yellow-500 to-amber-400 rounded-full"
            animate={{ width: `${((currentRound + (matchedPairs.size === 4 ? 1 : 0)) / totalRounds) * 100}%` }}
          />
        </div>
        <span className="text-sm text-muted-foreground">{currentRound + 1}/{totalRounds}</span>
      </div>

      <div className="text-center">
        <span className="text-sm text-muted-foreground">本轮得分: </span>
        <span className="font-bold text-yellow-400">{roundScore}</span>
      </div>

      <div>
        <h3 className="text-sm font-medium text-muted-foreground mb-3">选择动词</h3>
        <div className="grid grid-cols-4 gap-3">
          {shuffledVerbs.map((item, idx) => (
            <motion.button
              key={`${currentRound}-${item.verb}-${idx}`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleVerbClick(item.verb)}
              className={`p-4 rounded-xl font-bold text-lg border-2 transition-all ${
                selectedVerb === item.verb
                  ? 'border-primary bg-primary/20 neon-glow text-primary'
                  : 'border-border bg-card hover:border-primary/50'
              }`}
            >
              {item.verb}
            </motion.button>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-sm font-medium text-muted-foreground mb-3">点击句子进行匹配</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {currentRoundData.map((item, idx) => {
            const isMatched = matchedPairs.has(idx)
            const isShaking = shakeItem === idx

            return (
              <motion.button
                key={`${currentRound}-sent-${idx}`}
                onClick={() => handleSentenceClick(item, idx)}
                disabled={isMatched}
                animate={isShaking ? { x: [-8, 8, -4, 4, 0] } : {}}
                transition={{ duration: 0.4 }}
                className={`p-4 rounded-xl border-2 text-left transition-all ${
                  isMatched
                    ? 'border-green-500 bg-green-500/10 neon-success'
                    : 'border-border bg-card hover:border-primary/50'
                }`}
              >
                <p className="text-sm font-medium">
                  {item.fullSentence.replace(item.verb + ' ' + item.preposition, '_____')}
                </p>
                <p className="text-xs text-muted-foreground mt-1">{item.chineseMeaning}</p>
                {isMatched && (
                  <div className="flex items-center gap-1 mt-2 text-green-400 text-xs">
                    <Check size={12} />
                    <span>正确! {item.verb} {item.preposition}</span>
                  </div>
                )}
              </motion.button>
            )
          })}
        </div>
      </div>
    </div>
  )
}
