import { Outlet, Link, useLocation } from 'react-router'
import {
  Swords,
  Brain,
  BookOpen,
  Headphones,
  Gamepad2,
  Puzzle,
  Flame,
  Gem,
  Home,
} from 'lucide-react'
import { motion } from 'framer-motion'

const navItems = [
  { path: '/', label: '首页', icon: Home },
  { path: '/typing', label: '打字特训', icon: Swords },
  { path: '/grammar', label: '语法闯关', icon: Brain },
  { path: '/vocabulary', label: '高频词汇', icon: BookOpen },
  { path: '/collocation', label: '固定搭配', icon: Puzzle },
  { path: '/listening', label: '听力磨耳', icon: Headphones },
  { path: '/games', label: '娱乐竞技场', icon: Gamepad2 },
]

export default function Layout() {
  const location = useLocation()
  const isActive = (path: string) => location.pathname === path

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Top Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-border">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <span className="text-2xl font-black tracking-tight">
              <span className="text-primary">IELTS</span>
              <span className="text-foreground"> STAR</span>
              <span className="text-yellow-400 ml-0.5">⭐</span>
            </span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive(item.path)
                    ? 'bg-primary/20 text-primary neon-glow'
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
                }`}
              >
                <item.icon size={16} />
                <span>{item.label}</span>
              </Link>
            ))}
          </div>

          {/* Right HUD */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 text-sm">
              <span className="flex items-center gap-1 text-orange-400">
                <Flame size={16} />
                <span className="font-mono font-bold">12</span>
              </span>
              <span className="flex items-center gap-1 text-purple-400">
                <Gem size={16} />
                <span className="font-mono font-bold">0</span>
              </span>
            </div>
          </div>
        </div>

        {/* Mobile Nav Bar */}
        <div className="lg:hidden flex items-center justify-around py-2 border-t border-border overflow-x-auto">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`flex flex-col items-center gap-0.5 px-2 py-1 rounded-md text-xs transition-colors ${
                isActive(item.path)
                  ? 'text-primary'
                  : 'text-muted-foreground'
              }`}
            >
              <item.icon size={18} />
              <span className="whitespace-nowrap">{item.label}</span>
            </Link>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-24 lg:pt-20 pb-8 px-4">
        <motion.div
          key={location.pathname}
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -12 }}
          transition={{ duration: 0.3 }}
          className="max-w-7xl mx-auto"
        >
          <Outlet />
        </motion.div>
      </main>
    </div>
  )
}
