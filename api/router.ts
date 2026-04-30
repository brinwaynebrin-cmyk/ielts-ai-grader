import { authRouter } from "./auth-router";
import { ieltsRouter, progressRouter, leaderboardRouter } from "./ielts-router";
import { createRouter, publicQuery } from "./middleware";

export const appRouter = createRouter({
  ping: publicQuery.query(() => ({ ok: true, ts: Date.now() })),
  auth: authRouter,
  ielts: ieltsRouter,
  progress: progressRouter,
  leaderboard: leaderboardRouter,
});

export type AppRouter = typeof appRouter;
