import { Link } from 'react-router'
import { motion } from 'framer-motion'
import {
  Swords,
  Brain,
  BookOpen,
  Headphones,
  Gamepad2,
  Puzzle,
  Target,
  TrendingUp,
  Award,
  Clock,
} from 'lucide-react'

const modules = [
  {
    path: '/typing',
    title: '打字特训',
    desc: '经典雅思句子打字练习，训练肌肉记忆',
    image: '/typing-module.jpg',
    icon: Swords,
    color: 'from-blue-500/20 to-cyan-500/20',
    borderColor: 'border-blue-500/30',
    iconColor: 'text-blue-400',
  },
  {
    path: '/grammar',
    title: '语法闯关',
    desc: '高频语法陷阱即时判断，选择题训练',
    image: '/grammar-module.jpg',
    icon: Brain,
    color: 'from-green-500/20 to-emerald-500/20',
    borderColor: 'border-green-500/30',
    iconColor: 'text-green-400',
  },
  {
    path: '/vocabulary',
    title: '高频词汇',
    desc: '雅思核心词汇闪卡，间隔重复记忆',
    image: '/vocab-module.jpg',
    icon: BookOpen,
    color: 'from-purple-500/20 to-violet-500/20',
    borderColor: 'border-purple-500/30',
    iconColor: 'text-purple-400',
  },
  {
    path: '/collocation',
    title: '固定搭配',
    desc: '动词短语与介词搭配，拖拽匹配训练',
    image: '/collocation-module.jpg',
    icon: Puzzle,
    color: 'from-yellow-500/20 to-amber-500/20',
    borderColor: 'border-yellow-500/30',
    iconColor: 'text-yellow-400',
  },
  {
    path: '/listening',
    title: '听力磨耳',
    desc: '精听填空与听写复盘，强化听觉敏感',
    image: '/listening-module.jpg',
    icon: Headphones,
    color: 'from-pink-500/20 to-rose-500/20',
    borderColor: 'border-pink-500/30',
    iconColor: 'text-pink-400',
  },
  {
    path: '/games',
    title: '娱乐竞技场',
    desc: '单词狙击、句子重组等游戏化学习',
    image: '/games-module.jpg',
    icon: Gamepad2,
    color: 'from-orange-500/20 to-red-500/20',
    borderColor: 'border-orange-500/30',
    iconColor: 'text-orange-400',
  },
]

const statsCards = [
  { label: '今日练习', value: '0', unit: '题', icon: Target, color: 'text-blue-400' },
  { label: '累计XP', value: '0', unit: '点', icon: TrendingUp, color: 'text-green-400' },
  { label: '最高连击', value: '12', unit: '天', icon: Award, color: 'text-yellow-400' },
  { label: '学习时长', value: '0', unit: '分钟', icon: Clock, color: 'text-purple-400' },
]

export default function Home() {
  const todayProgress = 0
  const dailyGoal = 5
  const progressPercent = Math.min((todayProgress / dailyGoal) * 100, 100)

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <section className="relative rounded-2xl overflow-hidden">
        <div className="absolute inset-0">
          <img src="/hero-bg.jpg" alt="" className="w-full h-full object-cover opacity-40" />
          <div className="absolute inset-0 bg-gradient-to-r from-background via-background/80 to-transparent" />
        </div>
        <div className="relative p-8 lg:p-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h1 className="text-4xl lg:text-5xl font-black mb-3">
              Welcome to <span className="text-primary">IELTS Star</span>.
            </h1>
            <p className="text-lg text-muted-foreground max-w-xl">
              Ready to sharpen your blade? 今日目标：完成{dailyGoal}个练习模块，打牢雅思基础。
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-6 max-w-md"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-muted-foreground">今日任务环</span>
              <span className="text-sm font-bold text-primary">{todayProgress}/{dailyGoal}</span>
            </div>
            <div className="w-full h-3 bg-secondary rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary to-purple-400 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${progressPercent}%` }}
                transition={{ duration: 1, delay: 0.5 }}
              />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats Grid */}
      <section className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statsCards.map((stat, index) => (
          <motion.div
            key={stat.label}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + index * 0.1 }}
            className="bg-card border border-border rounded-xl p-4"
          >
            <div className="flex items-center gap-2 mb-2">
              <stat.icon size={18} className={stat.color} />
              <span className="text-sm text-muted-foreground">{stat.label}</span>
            </div>
            <div className="flex items-baseline gap-1">
              <span className="text-2xl font-black font-mono">{stat.value}</span>
              <span className="text-xs text-muted-foreground">{stat.unit}</span>
            </div>
          </motion.div>
        ))}
      </section>

      {/* Module Cards Grid */}
      <section>
        <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
          <Target className="text-primary" size={24} />
          训练模块
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {modules.map((mod, index) => (
            <motion.div
              key={mod.path}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
            >
              <Link
                to={mod.path}
                className={`group block bg-gradient-to-br ${mod.color} border ${mod.borderColor} rounded-2xl overflow-hidden hover:scale-[1.02] transition-all duration-300`}
              >
                <div className="relative h-40 overflow-hidden">
                  <img
                    src={mod.image}
                    alt={mod.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <div className="absolute bottom-3 left-3 flex items-center gap-2">
                    <div className={`p-2 rounded-lg bg-black/40 backdrop-blur-sm ${mod.iconColor}`}>
                      <mod.icon size={20} />
                    </div>
                  </div>
                </div>
                <div className="p-5">
                  <h3 className="text-xl font-bold mb-1 group-hover:text-primary transition-colors">
                    {mod.title}
                  </h3>
                  <p className="text-sm text-muted-foreground">{mod.desc}</p>
                  <div className="mt-4 flex items-center gap-2 text-sm font-medium text-primary">
                    <span>开始训练</span>
                    <span className="group-hover:translate-x-1 transition-transform">{'->'}</span>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Quick Tip */}
      <section className="bg-secondary/50 border border-border rounded-xl p-6">
        <h3 className="text-lg font-bold mb-2 text-primary">💡 学习小贴士</h3>
        <p className="text-muted-foreground">
          每天坚持练习 30 分钟，胜过偶尔突击 3 小时。建议从「打字特训」开始热身，然后进行「高频词汇」记忆，
          接着挑战「语法闯关」，最后用「听力磨耳」收尾。游戏模块适合在学习间隙放松大脑。
        </p>
      </section>
    </div>
  )
}
