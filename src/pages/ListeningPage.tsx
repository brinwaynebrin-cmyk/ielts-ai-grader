import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { listeningTracks as allTracks } from '@/data/ieltsData'
import { Play, Pause, RotateCcw, ChevronRight, Volume2 } from 'lucide-react'
import type { ReactElement } from 'react'

export default function ListeningPage() {
  const [tracks] = useState(allTracks)
  const [currentTrackIdx, setCurrentTrackIdx] = useState(0)
  const [phase, setPhase] = useState<'intro' | 'gapfill' | 'dictation' | 'result'>('intro')
  const [isPlaying, setIsPlaying] = useState(false)
  const [userAnswers, setUserAnswers] = useState<string[]>(['', '', '', ''])
  const [dictationText, setDictationText] = useState('')
  const [showAnswers, setShowAnswers] = useState(false)
  const [score, setScore] = useState(0)
  const [readProgress, setReadProgress] = useState(0)

  const currentTrack = tracks[currentTrackIdx]
  const blanks = currentTrack ? JSON.parse(currentTrack.blanksJSON || '[]') as { word: string; index: number }[] : []

  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const startPlayback = () => {
    setIsPlaying(true)
    setReadProgress(0)
    const duration = 3000
    const step = 100
    let progress = 0

    intervalRef.current = setInterval(() => {
      progress += step
      const pct = Math.min((progress / duration) * 100, 100)
      setReadProgress(pct)

      if (progress >= duration) {
        if (intervalRef.current) clearInterval(intervalRef.current)
        setIsPlaying(false)
      }
    }, step)
  }

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [])

  const handleAnswerChange = (idx: number, value: string) => {
    const newAnswers = [...userAnswers]
    newAnswers[idx] = value
    setUserAnswers(newAnswers)
  }

  const submitGapFill = () => {
    let correct = 0
    userAnswers.forEach((ans, idx) => {
      if (blanks[idx] && ans.toLowerCase().trim() === blanks[idx].word.toLowerCase()) {
        correct++
      }
    })
    setScore(correct * 10)
    setShowAnswers(true)

    setTimeout(() => {
      setPhase('dictation')
      setShowAnswers(false)
      setUserAnswers(['', '', '', ''])
    }, 2000)
  }

  const submitDictation = () => {
    if (!currentTrack) return

    const userWords = dictationText.toLowerCase().split(/\s+/)
    const transcriptWords = currentTrack.transcript.toLowerCase().split(/\s+/)
    let matched = 0
    userWords.forEach((w, i) => {
      if (transcriptWords[i] === w) matched++
    })
    const dictationScore = transcriptWords.length > 0 ? Math.round((matched / transcriptWords.length) * 100) : 0

    setScore(prev => prev + dictationScore)
    setShowAnswers(true)
  }

  const nextTrack = () => {
    if (currentTrackIdx < tracks.length - 1) {
      setCurrentTrackIdx(prev => prev + 1)
      setPhase('intro')
      setUserAnswers(['', '', '', ''])
      setDictationText('')
      setShowAnswers(false)
      setScore(0)
      setReadProgress(0)
      setIsPlaying(false)
    } else {
      setPhase('result')
    }
  }

  const reset = () => {
    setCurrentTrackIdx(0)
    setPhase('intro')
    setIsPlaying(false)
    setUserAnswers(['', '', '', ''])
    setDictationText('')
    setShowAnswers(false)
    setScore(0)
    setReadProgress(0)
  }

  const renderTranscript = (): ReactElement[] => {
    if (!currentTrack) return []
    const text = currentTrack.transcript
    const parts: ReactElement[] = []
    let lastIdx = 0

    blanks.forEach((blank, idx) => {
      if (blank.index > lastIdx) {
        parts.push(<span key={`text-${idx}`}>{text.substring(lastIdx, blank.index)}</span>)
      }

      const isCorrect = showAnswers && userAnswers[idx].toLowerCase().trim() === blank.word.toLowerCase()
      const isWrong = showAnswers && userAnswers[idx] && !isCorrect

      parts.push(
        <span key={`blank-${idx}`} className="inline-block mx-1">
          <input
            type="text"
            value={userAnswers[idx]}
            onChange={(e) => handleAnswerChange(idx, e.target.value)}
            disabled={showAnswers}
            className={`w-28 px-2 py-1 text-center bg-secondary border rounded-lg text-sm font-medium ${
              isCorrect ? 'border-green-500 text-green-400' : isWrong ? 'border-red-500 text-red-400' : 'border-border'
            }`}
            placeholder="?"
          />
          {showAnswers && isWrong && (
            <span className="text-xs text-green-400 ml-1">{blank.word}</span>
          )}
        </span>
      )

      lastIdx = blank.index + blank.word.length
    })

    if (lastIdx < text.length) {
      parts.push(<span key="text-end">{text.substring(lastIdx)}</span>)
    }

    return parts
  }

  if (phase === 'result') {
    return (
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="bg-card border border-border rounded-2xl p-8 text-center space-y-6"
        >
          <div className="text-6xl">🎧</div>
          <h2 className="text-3xl font-black text-primary">听力训练完成!</h2>
          <div className="bg-secondary rounded-xl p-6">
            <div className="text-sm text-muted-foreground mb-2">总得分</div>
            <div className="text-5xl font-black text-primary">{score}</div>
          </div>
          <p className="text-muted-foreground">
            你完成了 {tracks.length} 段听力材料的精听与听写练习。
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
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black">听力磨耳</h1>
          <p className="text-muted-foreground mt-1">
            {phase === 'intro' && '先泛听了解大意'}
            {phase === 'gapfill' && '精听填空，捕捉关键词'}
            {phase === 'dictation' && '听写复盘，强化记忆'}
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-muted-foreground">
            {currentTrackIdx + 1}/{tracks.length}
          </span>
          <button onClick={reset} className="p-2 hover:bg-secondary rounded-lg transition-colors">
            <RotateCcw size={18} />
          </button>
        </div>
      </div>

      <div className="bg-card border border-border rounded-2xl p-6 space-y-4">
        <div className="flex items-center gap-4">
          <button
            onClick={isPlaying ? () => setIsPlaying(false) : startPlayback}
            className="w-12 h-12 flex items-center justify-center bg-primary text-primary-foreground rounded-full hover:opacity-90 transition-opacity"
          >
            {isPlaying ? <Pause size={20} /> : <Play size={20} />}
          </button>
          <div className="flex-1">
            <h3 className="font-bold">{currentTrack?.title || 'Loading...'}</h3>
            <p className="text-sm text-muted-foreground">
              {phase === 'intro' ? 'Phase 1: 泛听理解' : phase === 'gapfill' ? 'Phase 2: 精听填空' : 'Phase 3: 听写'}
            </p>
          </div>
          <Volume2 size={20} className="text-muted-foreground" />
        </div>

        <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-pink-500 to-rose-400 rounded-full"
            animate={{ width: `${readProgress}%` }}
            transition={{ duration: 0.1 }}
          />
        </div>

        {isPlaying && (
          <div className="flex items-center justify-center gap-1 h-12">
            {Array.from({ length: 40 }).map((_, i) => (
              <motion.div
                key={i}
                className="w-1 bg-primary rounded-full"
                animate={{
                  height: [8, 24 + Math.random() * 24, 8],
                }}
                transition={{
                  duration: 0.5 + Math.random() * 0.5,
                  repeat: Infinity,
                  delay: i * 0.02,
                }}
              />
            ))}
          </div>
        )}
      </div>

      <AnimatePresence mode="wait">
        {phase === 'intro' && (
          <motion.div
            key="intro"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-card border border-border rounded-2xl p-8 text-center space-y-6"
          >
            <p className="text-lg">请仔细聆听，捕捉大意。音频播放完毕后，将进入精听填空阶段。</p>
            {!isPlaying && readProgress === 0 && (
              <button
                onClick={startPlayback}
                className="px-8 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity"
              >
                开始播放
              </button>
            )}
            {readProgress === 100 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
              >
                <p className="text-muted-foreground mb-4">泛听结束，准备好进入精听阶段了吗？</p>
                <button
                  onClick={() => setPhase('gapfill')}
                  className="px-8 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity"
                >
                  进入精听填空 →
                </button>
              </motion.div>
            )}
          </motion.div>
        )}

        {phase === 'gapfill' && (
          <motion.div
            key="gapfill"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-card border border-border rounded-2xl p-8 space-y-6"
          >
            <h3 className="font-bold text-lg">根据听到的内容，填写空白处：</h3>
            <div className="leading-loose text-lg">
              {renderTranscript()}
            </div>

            {!showAnswers ? (
              <div className="flex justify-end">
                <button
                  onClick={submitGapFill}
                  className="px-6 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity"
                >
                  提交答案
                </button>
              </div>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center text-green-400 font-medium"
              >
                填空完成！即将进入听写阶段...
              </motion.div>
            )}
          </motion.div>
        )}

        {phase === 'dictation' && (
          <motion.div
            key="dictation"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-card border border-border rounded-2xl p-8 space-y-6"
          >
            <h3 className="font-bold text-lg">听写完整文本：</h3>
            <p className="text-sm text-muted-foreground">请根据记忆，尽可能写出完整的听力原文。</p>

            <textarea
              value={dictationText}
              onChange={(e) => setDictationText(e.target.value)}
              rows={8}
              className="w-full px-4 py-3 bg-secondary border border-border rounded-xl text-base resize-none focus:outline-none focus:border-primary"
              placeholder="在此输入你听写的内容..."
            />

            {!showAnswers ? (
              <div className="flex justify-end">
                <button
                  onClick={submitDictation}
                  className="px-6 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity"
                >
                  提交听写
                </button>
              </div>
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="space-y-4"
              >
                <div className="p-4 bg-secondary/50 rounded-xl">
                  <h4 className="font-bold mb-2 text-sm">标准原文：</h4>
                  <p className="text-sm">{currentTrack?.transcript}</p>
                </div>
                <div className="flex justify-end">
                  <button
                    onClick={nextTrack}
                    className="px-6 py-3 bg-primary text-primary-foreground rounded-xl font-bold hover:opacity-90 transition-opacity flex items-center gap-2"
                  >
                    <span>下一段</span>
                    <ChevronRight size={18} />
                  </button>
                </div>
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}
