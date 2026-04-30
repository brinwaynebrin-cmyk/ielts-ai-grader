import {
  mysqlTable,
  mysqlEnum,
  serial,
  varchar,
  text,
  timestamp,
  int,
  bigint,
} from "drizzle-orm/mysql-core";

export const users = mysqlTable("users", {
  id: serial("id").primaryKey(),
  unionId: varchar("unionId", { length: 255 }).notNull().unique(),
  name: varchar("name", { length: 255 }),
  email: varchar("email", { length: 320 }),
  avatar: text("avatar"),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  totalXP: int("totalXP").default(0).notNull(),
  currentStreak: int("currentStreak").default(0).notNull(),
  longestStreak: int("longestStreak").default(0).notNull(),
  lastStudyDate: timestamp("lastStudyDate"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt")
    .defaultNow()
    .notNull()
    .$onUpdate(() => new Date()),
  lastSignInAt: timestamp("lastSignInAt").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

export const sentences = mysqlTable("sentences", {
  id: serial("id").primaryKey(),
  englishText: text("englishText").notNull(),
  chineseTranslation: text("chineseTranslation"),
  category: varchar("category", { length: 50 }),
  difficulty: mysqlEnum("difficulty", ["easy", "medium", "hard"]).default("medium").notNull(),
  length: int("length").default(0).notNull(),
  tags: text("tags"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type Sentence = typeof sentences.$inferSelect;

export const grammarQuestions = mysqlTable("grammarQuestions", {
  id: serial("id").primaryKey(),
  questionText: text("questionText").notNull(),
  optionsJSON: text("optionsJSON").notNull(),
  correctAnswerIndex: int("correctAnswerIndex").notNull(),
  explanation: text("explanation"),
  difficulty: mysqlEnum("difficulty", ["easy", "medium", "hard"]).default("medium").notNull(),
  category: varchar("category", { length: 50 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type GrammarQuestion = typeof grammarQuestions.$inferSelect;

export const vocabulary = mysqlTable("vocabulary", {
  id: serial("id").primaryKey(),
  word: varchar("word", { length: 100 }).notNull(),
  phonetic: varchar("phonetic", { length: 100 }),
  partOfSpeech: varchar("partOfSpeech", { length: 50 }),
  chineseMeaning: text("chineseMeaning").notNull(),
  exampleSentence: text("exampleSentence"),
  exampleTranslation: text("exampleTranslation"),
  difficultyBand: mysqlEnum("difficultyBand", ["band5", "band6", "band7", "band8"]).default("band6").notNull(),
  category: varchar("category", { length: 50 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type Vocabulary = typeof vocabulary.$inferSelect;

export const collocations = mysqlTable("collocations", {
  id: serial("id").primaryKey(),
  verb: varchar("verb", { length: 50 }).notNull(),
  preposition: varchar("preposition", { length: 50 }).notNull(),
  fullSentence: text("fullSentence").notNull(),
  chineseMeaning: text("chineseMeaning").notNull(),
  category: varchar("category", { length: 50 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type Collocation = typeof collocations.$inferSelect;

export const listeningTracks = mysqlTable("listeningTracks", {
  id: serial("id").primaryKey(),
  title: varchar("title", { length: 200 }).notNull(),
  transcript: text("transcript").notNull(),
  difficulty: mysqlEnum("difficulty", ["easy", "medium", "hard"]).default("medium").notNull(),
  duration: int("duration").default(0).notNull(),
  category: varchar("category", { length: 50 }),
  blanksJSON: text("blanksJSON"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type ListeningTrack = typeof listeningTracks.$inferSelect;

export const userProgress = mysqlTable("userProgress", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  moduleType: mysqlEnum("moduleType", ["typing", "grammar", "vocabulary", "collocation", "listening", "games"]).notNull(),
  itemId: bigint("itemId", { mode: "number", unsigned: true }).notNull(),
  status: mysqlEnum("status", ["mastered", "review", "new"]).default("new").notNull(),
  nextReviewDate: timestamp("nextReviewDate"),
  xpEarned: int("xpEarned").default(0).notNull(),
  accuracy: int("accuracy").default(0),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
});

export type UserProgress = typeof userProgress.$inferSelect;

export const typingSessions = mysqlTable("typingSessions", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  wpm: int("wpm").default(0).notNull(),
  accuracy: int("accuracy").default(0).notNull(),
  durationSeconds: int("durationSeconds").default(0).notNull(),
  sentenceCount: int("sentenceCount").default(0).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type TypingSession = typeof typingSessions.$inferSelect;

export const gameScores = mysqlTable("gameScores", {
  id: serial("id").primaryKey(),
  userId: bigint("userId", { mode: "number", unsigned: true }).notNull(),
  gameType: mysqlEnum("gameType", ["wordSniper", "syntaxScramble", "fillInBlank"]).notNull(),
  score: int("score").default(0).notNull(),
  accuracy: int("accuracy").default(0),
  durationSeconds: int("durationSeconds").default(0).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type GameScore = typeof gameScores.$inferSelect;
