/**
 * 口语情景化学习引擎
 * 提供对话模拟、评分、升级建议
 */

class SpeakingEngine {
  constructor() {
    this.scenarios = new Map();
    this.currentScenario = null;
  }

  // 加载情景
  async loadScenario(scenarioId) {
    if (this.scenarios.has(scenarioId)) {
      return this.scenarios.get(scenarioId);
    }

    try {
      const response = await fetch(`data/speaking/${scenarioId}.json`);
      const data = await response.json();
      this.scenarios.set(scenarioId, data);
      return data;
    } catch (error) {
      console.error(`[SpeakingEngine] Failed to load scenario ${scenarioId}:`, error);
      return null;
    }
  }

  // 获取词汇在情景中的使用
  getWordInScenario(word, scenarioId) {
    const scenario = this.scenarios.get(scenarioId);
    if (!scenario) return null;

    const vocabEntry = scenario.vocabulary_bank.find(v => v.word === word);
    if (!vocabEntry) return null;

    return {
      word: vocabEntry.word,
      contexts: vocabEntry.contexts,
      collocations: vocabEntry.collocations || [],
      related: this.findRelatedWords(word, scenario)
    };
  }

  // 查找相关词汇
  findRelatedWords(word, scenario) {
    return scenario.vocabulary_bank
      .filter(v => v.word !== word)
      .slice(0, 3);
  }

  // 生成对话模拟
  generateDialogue(scenarioId, part = 'Part 1', level = 'band7') {
    const scenario = this.scenarios.get(scenarioId);
    if (!scenario) return null;

    const contexts = scenario.vocabulary_bank
      .flatMap(v => v.contexts)
      .filter(c => c.part === part);

    return contexts.map(ctx => ({
      question: ctx.question,
      answer: ctx.answers ? ctx.answers[level] : ctx.sample_answer,
      tips: ctx.tips,
      followUps: ctx.follow_ups || []
    }));
  }

  // 评估回答并给出升级建议
  evaluateAnswer(userAnswer, targetWord) {
    const hasWord = userAnswer.toLowerCase().includes(targetWord.toLowerCase());
    const wordCount = userAnswer.split(/\s+/).length;
    
    let feedback = {
      score: 0,
      level: 'band6',
      suggestions: []
    };

    if (!hasWord) {
      feedback.suggestions.push(`尝试使用目标词汇 "${targetWord}"`);
    }

    if (wordCount < 15) {
      feedback.suggestions.push("回答可以更长一些，添加细节");
      feedback.level = 'band6';
    } else if (wordCount < 30) {
      feedback.level = 'band7';
      feedback.score = 7;
    } else {
      feedback.level = 'band8';
      feedback.score = 8;
      feedback.suggestions.push("很好！尝试使用更复杂的句式");
    }

    return feedback;
  }

  // 获取升级表达
  getUpgradeExpression(word, currentLevel) {
    const levels = ['band6', 'band7', 'band8'];
    const currentIdx = levels.indexOf(currentLevel);
    
    // 这里应该查询词库中的升级版本
    return {
      current: word,
      next: currentIdx < 2 ? levels[currentIdx + 1] : null,
      alternatives: []
    };
  }
}

const speakingEngine = new SpeakingEngine();
