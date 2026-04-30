import { z } from "zod";
import { createRouter, publicQuery, authedQuery } from "./middleware";
import { getDb } from "./queries/connection";
import {
  sentences,
  grammarQuestions,
  vocabulary,
  collocations,
  listeningTracks,
  userProgress,
  typingSessions,
  gameScores,
} from "@db/schema";
import { eq, and, desc, sql, gte } from "drizzle-orm";

export const ieltsRouter = createRouter({
  getSentences: publicQuery
    .input(z.object({ limit: z.number().min(1).max(50).default(10), difficulty: z.enum(["easy", "medium", "hard"]).optional() }))
    .query(async ({ input }: { input: { limit: number; difficulty?: "easy" | "medium" | "hard" } }) => {
      const db = getDb();
      const results = await db.select().from(sentences).limit(input.limit);
      return results.sort(() => Math.random() - 0.5);
    }),

  getGrammarQuestions: publicQuery
    .input(z.object({ limit: z.number().min(1).max(20).default(10), difficulty: z.enum(["easy", "medium", "hard"]).optional() }))
    .query(async ({ input }: { input: { limit: number; difficulty?: "easy" | "medium" | "hard" } }) => {
      const db = getDb();
      const results = await db.select().from(grammarQuestions).limit(input.limit);
      return results.sort(() => Math.random() - 0.5);
    }),

  getVocabulary: publicQuery
    .input(z.object({ limit: z.number().min(1).max(30).default(10), band: z.enum(["band5", "band6", "band7", "band8"]).optional() }))
    .query(async ({ input }: { input: { limit: number; band?: "band5" | "band6" | "band7" | "band8" } }) => {
      const db = getDb();
      const results = await db.select().from(vocabulary).limit(input.limit);
      return results.sort(() => Math.random() - 0.5);
    }),

  getCollocations: publicQuery
    .input(z.object({ limit: z.number().min(1).max(20).default(10) }))
    .query(async ({ input }: { input: { limit: number } }) => {
      const db = getDb();
      const results = await db.select().from(collocations).limit(input.limit);
      return results.sort(() => Math.random() - 0.5);
    }),

  getListeningTracks: publicQuery
    .input(z.object({ limit: z.number().min(1).max(10).default(5), difficulty: z.enum(["easy", "medium", "hard"]).optional() }))
    .query(async ({ input }: { input: { limit: number; difficulty?: "easy" | "medium" | "hard" } }) => {
      const db = getDb();
      return await db.select().from(listeningTracks).limit(input.limit);
    }),
});

export const progressRouter = createRouter({
  submitResult: authedQuery
    .input(z.object({
      moduleType: z.enum(["typing", "grammar", "vocabulary", "collocation", "listening", "games"]),
      itemId: z.number(),
      isCorrect: z.boolean(),
      timeSpent: z.number().optional(),
      wpm: z.number().optional(),
      accuracy: z.number().optional(),
      score: z.number().optional(),
      gameType: z.enum(["wordSniper", "syntaxScramble", "fillInBlank"]).optional(),
    }))
    .mutation(async ({ ctx, input }: { ctx: { user: { id: number; totalXP: number } }; input: { moduleType: string; itemId: number; isCorrect: boolean; timeSpent?: number; wpm?: number; accuracy?: number; score?: number; gameType?: string } }) => {
      const db = getDb();
      const userId = ctx.user.id;

      const baseXP = input.isCorrect ? 10 : 2;
      const bonusXP = input.isCorrect && input.timeSpent && input.timeSpent < 10 ? 5 : 0;
      const totalXP = baseXP + bonusXP;

      await db.update(sentences as any).set({
        totalXP: sql`${ctx.user.totalXP} + ${totalXP}`,
      }).where(eq(sentences.id as any, userId));

      await db.insert(userProgress).values({
        userId,
        moduleType: input.moduleType as any,
        itemId: input.itemId,
        status: input.isCorrect ? "mastered" : "review",
        xpEarned: totalXP,
        accuracy: input.accuracy || (input.isCorrect ? 100 : 0),
      });

      if (input.moduleType === "typing" && input.wpm !== undefined) {
        await db.insert(typingSessions).values({
          userId,
          wpm: input.wpm || 0,
          accuracy: input.accuracy || 0,
          durationSeconds: input.timeSpent || 0,
          sentenceCount: 1,
        });
      }

      if (input.moduleType === "games" && input.gameType) {
        await db.insert(gameScores).values({
          userId,
          gameType: input.gameType as any,
          score: input.score || 0,
          accuracy: input.accuracy || 0,
          durationSeconds: input.timeSpent || 0,
        });
      }

      return { xpEarned: totalXP, success: true };
    }),

  getUserStats: authedQuery.query(async ({ ctx }: { ctx: { user: { id: number; totalXP: number; currentStreak: number; longestStreak: number } } }) => {
    const db = getDb();
    const userId = ctx.user.id;

    const totalProgress = await db.select({ count: sql<number>`count(*)` }).from(userProgress).where(eq(userProgress.userId, userId));
    const typingStats = await db.select().from(typingSessions).where(eq(typingSessions.userId, userId)).orderBy(desc(typingSessions.createdAt)).limit(10);
    const gameStats = await db.select().from(gameScores).where(eq(gameScores.userId, userId)).orderBy(desc(gameScores.createdAt)).limit(10);

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const todayProgress = await db.select({ count: sql<number>`count(*)` }).from(userProgress)
      .where(and(eq(userProgress.userId, userId), gte(userProgress.createdAt, today)));

    return {
      user: ctx.user,
      totalProgress: totalProgress[0]?.count || 0,
      todayProgress: todayProgress[0]?.count || 0,
      typingStats,
      gameStats,
    };
  }),
});

export const leaderboardRouter = createRouter({
  getWeekly: publicQuery.query(async () => {
    const db = getDb();
    const weekAgo = new Date();
    weekAgo.setDate(weekAgo.getDate() - 7);

    const results = await db.select({
      userId: userProgress.userId,
      totalXP: sql<number>`sum(${userProgress.xpEarned})`,
      count: sql<number>`count(*)`,
    })
      .from(userProgress)
      .where(gte(userProgress.createdAt, weekAgo))
      .groupBy(userProgress.userId)
      .orderBy(desc(sql<number>`sum(${userProgress.xpEarned})`))
      .limit(50);

    return results;
  }),
});
