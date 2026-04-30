import { create } from "zustand";

export interface GameState {
  // Global stats
  xp: number;
  streak: number;
  addXP: (amount: number) => void;
  resetStreak: () => void;

  // Current session
  currentModule: string | null;
  setCurrentModule: (module: string | null) => void;

  // Typing session
  wpm: number;
  accuracy: number;
  setTypingStats: (wpm: number, accuracy: number) => void;

  // Game scores
  gameScore: number;
  gameAccuracy: number;
  setGameScore: (score: number, accuracy: number) => void;
}

export const useGameStore = create<GameState>((set) => ({
  xp: 0,
  streak: 0,
  addXP: (amount) => set((state) => ({ xp: state.xp + amount })),
  resetStreak: () => set({ streak: 0 }),

  currentModule: null,
  setCurrentModule: (module) => set({ currentModule: module }),

  wpm: 0,
  accuracy: 0,
  setTypingStats: (wpm, accuracy) => set({ wpm, accuracy }),

  gameScore: 0,
  gameAccuracy: 0,
  setGameScore: (score, accuracy) => set({ gameScore: score, gameAccuracy: accuracy }),
}));
