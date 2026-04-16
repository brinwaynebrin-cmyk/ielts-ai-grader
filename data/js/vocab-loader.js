
/**
 * 雅思词汇加载管理器
 * 支持懒加载、本地缓存、分级加载
 */

class VocabManager {
  constructor() {
    this.cache = new Map();
    this.loadedModules = new Set();
    this.totalWords = 0;
    this.wordIndex = new Map(); // 快速查找索引
  }

  // 加载指定模块的词汇
  async loadModule(moduleName, options = {}) {
    // 检查缓存
    if (this.cache.has(moduleName) && !options.forceReload) {
      return this.cache.get(moduleName);
    }

    try {
      // 动态加载JSON文件
      const response = await fetch(`data/vocab/${moduleName}.json`);
      const data = await response.json();
      
      // 处理数据
      const processed = this.processVocabulary(data);
      
      // 存入缓存
      this.cache.set(moduleName, processed);
      this.loadedModules.add(moduleName);
      
      // 建立索引
      this.buildIndex(processed.words, moduleName);
      
      console.log(`[VocabManager] Loaded ${moduleName}: ${processed.words.length} words`);
      return processed;
    } catch (error) {
      console.error(`[VocabManager] Failed to load ${moduleName}:`, error);
      return null;
    }
  }

  // 处理词汇数据
  processVocabulary(data) {
    return {
      metadata: data.metadata,
      words: data.words.map(w => ({
        ...w,
        searchText: `${w.word} ${w.meaning} ${w.en_meaning || ''}`.toLowerCase()
      }))
    };
  }

  // 建立快速索引
  buildIndex(words, moduleName) {
    words.forEach(word => {
      this.wordIndex.set(word.id, { ...word, module: moduleName });
    });
  }

  // 搜索词汇（支持9000+词汇实时搜索）
  search(query, options = {}) {
    const { module = 'all', limit = 50 } = options;
    const searchText = query.toLowerCase();
    
    let candidates = [];
    
    if (module === 'all') {
      // 全局搜索
      for (let [id, word] of this.wordIndex) {
        if (word.searchText.includes(searchText)) {
          candidates.push(word);
          if (candidates.length >= limit) break;
        }
      }
    } else {
      // 指定模块搜索
      const moduleData = this.cache.get(module);
      if (moduleData) {
        candidates = moduleData.words
          .filter(w => w.searchText.includes(searchText))
          .slice(0, limit);
      }
    }
    
    return candidates;
  }

  // 按话题获取词汇
  async getByTopic(topic) {
    try {
      const response = await fetch(`data/topics/${topic}.json`);
      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`[VocabManager] Failed to load topic ${topic}:`, error);
      return null;
    }
  }

  // 获取随机词汇（用于游戏）
  getRandomWords(count, band = null) {
    let allWords = [];
    for (let [, word] of this.wordIndex) {
      if (!band || word.difficulty >= band) {
        allWords.push(word);
      }
    }
    
    // Fisher-Yates 洗牌算法
    for (let i = allWords.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [allWords[i], allWords[j]] = [allWords[j], allWords[i]];
    }
    
    return allWords.slice(0, count);
  }

  // 预加载核心词汇
  async preloadCore() {
    await Promise.all([
      this.loadModule('academic'),
      this.loadModule('band7')
    ]);
  }

  // 获取学习统计
  getStats() {
    return {
      totalLoaded: this.wordIndex.size,
      modules: Array.from(this.loadedModules),
      cacheSize: this.cache.size
    };
  }
}

// 全局实例
const vocabManager = new VocabManager();

// 导出
if (typeof module !== 'undefined') {
  module.exports = VocabManager;
}
