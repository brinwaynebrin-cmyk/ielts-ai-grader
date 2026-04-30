import { getDb } from "../api/queries/connection";
import {
  sentences,
  grammarQuestions,
  vocabulary,
  collocations,
  listeningTracks,
} from "./schema";

async function seed() {
  const db = getDb();
  console.log("Seeding database...");

  // Seed sentences for typing practice
  await db.insert(sentences).values([
    { englishText: "The government should take immediate action to address environmental issues.", chineseTranslation: "政府应立即采取行动解决环境问题。", category: "opinion", difficulty: "medium", length: 78, tags: "government,environment,opinion" },
    { englishText: "Many people believe that technology has greatly improved our quality of life.", chineseTranslation: "许多人认为科技极大地改善了我们的生活质量。", category: "technology", difficulty: "easy", length: 76, tags: "technology,quality,life" },
    { englishText: "It is undeniable that education plays a crucial role in personal development.", chineseTranslation: "不可否认，教育在个人发展中起着至关重要的作用。", category: "education", difficulty: "medium", length: 79, tags: "education,development,personal" },
    { englishText: "The rapid advancement of artificial intelligence has sparked intense debate worldwide.", chineseTranslation: "人工智能的快速发展在全球范围内引发了激烈辩论。", category: "technology", difficulty: "hard", length: 88, tags: "AI,debate,technology" },
    { englishText: "Students should be encouraged to develop critical thinking skills from an early age.", chineseTranslation: "应鼓励学生在年幼时培养批判性思维能力。", category: "education", difficulty: "medium", length: 85, tags: "students,thinking,education" },
    { englishText: "Globalization has brought both opportunities and challenges to developing countries.", chineseTranslation: "全球化给发展中国家带来了机遇和挑战。", category: "society", difficulty: "medium", length: 84, tags: "globalization,countries,opportunities" },
    { englishText: "There is growing concern about the impact of social media on mental health.", chineseTranslation: "人们对社交媒体对心理健康的影响越来越担忧。", category: "technology", difficulty: "medium", length: 82, tags: "social,media,mental,health" },
    { englishText: "Traditional culture should be preserved while embracing modern innovations.", chineseTranslation: "在拥抱现代创新的同时，应保护传统文化。", category: "culture", difficulty: "medium", length: 80, tags: "culture,tradition,innovation" },
    { englishText: "The benefits of regular exercise extend far beyond physical health improvements.", chineseTranslation: "定期锻炼的好处远不止身体健康改善。", category: "health", difficulty: "medium", length: 83, tags: "exercise,health,benefits" },
    { englishText: "Effective communication skills are essential for success in the modern workplace.", chineseTranslation: "有效的沟通技巧对于在现代职场中取得成功至关重要。", category: "work", difficulty: "medium", length: 85, tags: "communication,workplace,success" },
    { englishText: "Climate change poses one of the greatest threats to human civilization.", chineseTranslation: "气候变化对人类文明构成了最大威胁之一。", category: "environment", difficulty: "medium", length: 75, tags: "climate,change,threat" },
    { englishText: "Investing in public transportation can significantly reduce urban congestion and pollution.", chineseTranslation: "投资公共交通可以显著减少城市拥堵和污染。", category: "transport", difficulty: "hard", length: 91, tags: "transport,congestion,pollution" },
    { englishText: "Learning a foreign language opens doors to new cultures and perspectives.", chineseTranslation: "学习外语为新的文化和视角打开了大门。", category: "education", difficulty: "easy", length: 76, tags: "language,culture,learning" },
    { englishText: "Remote work has fundamentally changed how companies operate and employees collaborate.", chineseTranslation: "远程工作从根本上改变了公司的运营方式和员工的协作方式。", category: "work", difficulty: "medium", length: 89, tags: "remote,work,collaboration" },
    { englishText: "Balancing economic growth with environmental protection remains a pressing global challenge.", chineseTranslation: "在经济增长和环境保护之间取得平衡仍然是一个紧迫的全球挑战。", category: "environment", difficulty: "hard", length: 93, tags: "economic,environment,challenge" },
  ]);

  // Seed grammar questions
  await db.insert(grammarQuestions).values([
    { questionText: "She has been living here ___ 2010.", optionsJSON: JSON.stringify(["for", "since", "during", "at"]), correctAnswerIndex: 1, explanation: "'Since' is used with a specific point in time (2010). 'For' is used with durations.", difficulty: "easy", category: "prepositions" },
    { questionText: "If I ___ enough money, I would buy a new car.", optionsJSON: JSON.stringify(["have", "had", "would have", "had had"]), correctAnswerIndex: 1, explanation: "Second conditional uses 'if + past simple, would + base verb' for hypothetical present situations.", difficulty: "medium", category: "conditionals" },
    { questionText: "By the time we arrived, the movie ___.", optionsJSON: JSON.stringify(["already started", "has already started", "had already started", "was already starting"]), correctAnswerIndex: 2, explanation: "Past perfect is used for an action completed before another past action.", difficulty: "medium", category: "tenses" },
    { questionText: "The more you practice, ___ you will become.", optionsJSON: JSON.stringify(["the more confident", "more confident", "the confident", "most confident"]), correctAnswerIndex: 0, explanation: "'The + comparative, the + comparative' structure expresses proportional change.", difficulty: "easy", category: "comparatives" },
    { questionText: "Neither the students nor the teacher ___ present at the meeting.", optionsJSON: JSON.stringify(["were", "was", "are", "is"]), correctAnswerIndex: 1, explanation: "With 'neither...nor', the verb agrees with the nearest subject (teacher - singular).", difficulty: "hard", category: "subject-verb agreement" },
    { questionText: "Despite ___ late, we managed to catch the train.", optionsJSON: JSON.stringify(["being", "be", "to be", "was"]), correctAnswerIndex: 0, explanation: "After prepositions like 'despite', we use gerund (-ing form).", difficulty: "medium", category: "gerunds" },
    { questionText: "I suggested that he ___ a doctor.", optionsJSON: JSON.stringify(["sees", "see", "should see", "B and C"]), correctAnswerIndex: 3, explanation: "After 'suggest', we use subjunctive 'see' or 'should see' in formal English.", difficulty: "hard", category: "subjunctive" },
    { questionText: "This is the first time I ___ sushi.", optionsJSON: JSON.stringify(["eat", "ate", "have eaten", "had eaten"]), correctAnswerIndex: 2, explanation: "'This is the first time' is followed by present perfect.", difficulty: "medium", category: "tenses" },
    { questionText: "Hardly ___ the house when it started raining.", optionsJSON: JSON.stringify(["I left", "did I leave", "had I left", "have I left"]), correctAnswerIndex: 2, explanation: "With 'hardly...when', we use past perfect with inversion for the first action.", difficulty: "hard", category: "inversion" },
    { questionText: "Not only ___ English, but he also speaks French.", optionsJSON: JSON.stringify(["he speaks", "does he speak", "he does speak", "speaks he"]), correctAnswerIndex: 1, explanation: "'Not only' at the beginning triggers subject-auxiliary inversion.", difficulty: "hard", category: "inversion" },
    { questionText: "I wish I ___ harder when I was at university.", optionsJSON: JSON.stringify(["study", "studied", "had studied", "would study"]), correctAnswerIndex: 2, explanation: "'I wish' + past perfect expresses regret about a past situation.", difficulty: "medium", category: "subjunctive" },
    { questionText: "The book ___ I borrowed from the library is very interesting.", optionsJSON: JSON.stringify(["who", "whom", "which", "whose"]), correctAnswerIndex: 2, explanation: "For things/objects, we use 'which' or 'that' in relative clauses.", difficulty: "easy", category: "relative clauses" },
    { questionText: "Had I known about the traffic, I ___ earlier.", optionsJSON: JSON.stringify(["would leave", "would have left", "had left", "will leave"]), correctAnswerIndex: 1, explanation: "Inverted conditional (Had I known = If I had known) uses third conditional form.", difficulty: "hard", category: "conditionals" },
    { questionText: "The project ___ by the end of next month.", optionsJSON: JSON.stringify(["will complete", "will be completed", "will have been completed", "is completing"]), correctAnswerIndex: 2, explanation: "Future perfect passive for an action completed before a future time.", difficulty: "hard", category: "passive voice" },
    { questionText: "She insisted on ___ for the dinner.", optionsJSON: JSON.stringify(["paying", "pay", "to pay", "paid"]), correctAnswerIndex: 0, explanation: "'Insist on' is followed by a gerund (verb + -ing).", difficulty: "easy", category: "gerunds" },
  ]);

  // Seed vocabulary (IELTS Band 6-8 words)
  await db.insert(vocabulary).values([
    { word: "Ambiguous", phonetic: "/æmˈbɪɡjuəs/", partOfSpeech: "adjective", chineseMeaning: "模棱两可的，含糊不清的", exampleSentence: "The contract terms were ambiguous and open to interpretation.", exampleTranslation: "合同条款模棱两可，可作多种解释。", difficultyBand: "band7", category: "academic" },
    { word: "Comprehensive", phonetic: "/ˌkɒmprɪˈhensɪv/", partOfSpeech: "adjective", chineseMeaning: "全面的，综合的", exampleSentence: "The report provides a comprehensive analysis of the current situation.", exampleTranslation: "该报告对当前形势进行了全面分析。", difficultyBand: "band6", category: "academic" },
    { word: "Detrimental", phonetic: "/ˌdetrɪˈmentl/", partOfSpeech: "adjective", chineseMeaning: "有害的，不利的", exampleSentence: "Smoking is detrimental to your health.", exampleTranslation: "吸烟有害健康。", difficultyBand: "band7", category: "health" },
    { word: "Ephemeral", phonetic: "/ɪˈfemərəl/", partOfSpeech: "adjective", chineseMeaning: "短暂的，转瞬即逝的", exampleSentence: "Fashion trends are often ephemeral, changing from season to season.", exampleTranslation: "时尚潮流通常是短暂的，季季更替。", difficultyBand: "band8", category: "culture" },
    { word: "Feasible", phonetic: "/ˈfiːzəbl/", partOfSpeech: "adjective", chineseMeaning: "可行的，切实可行的", exampleSentence: "We need to find a feasible solution to this problem.", exampleTranslation: "我们需要找到一个切实可行的解决方案。", difficultyBand: "band6", category: "work" },
    { word: "Inevitable", phonetic: "/ɪnˈevɪtəbl/", partOfSpeech: "adjective", chineseMeaning: "不可避免的，必然发生的", exampleSentence: "With such poor preparation, failure was inevitable.", exampleTranslation: "准备如此不足，失败是不可避免的。", difficultyBand: "band6", category: "general" },
    { word: "Mitigate", phonetic: "/ˈmɪtɪɡeɪt/", partOfSpeech: "verb", chineseMeaning: "减轻，缓和", exampleSentence: "The government is taking steps to mitigate the effects of inflation.", exampleTranslation: "政府正在采取措施缓解通货膨胀的影响。", difficultyBand: "band7", category: "economy" },
    { word: "Paradigm", phonetic: "/ˈpærədaɪm/", partOfSpeech: "noun", chineseMeaning: "范例，范式", exampleSentence: "The discovery caused a paradigm shift in scientific thinking.", exampleTranslation: "这一发现导致了科学思维的范式转变。", difficultyBand: "band8", category: "academic" },
    { word: "Resilient", phonetic: "/rɪˈzɪliənt/", partOfSpeech: "adjective", chineseMeaning: "有弹性的，能迅速恢复的", exampleSentence: "Children are often more resilient than adults think.", exampleTranslation: "孩子们通常比成年人想象的更有韧性。", difficultyBand: "band7", category: "psychology" },
    { word: "Sustainable", phonetic: "/səˈsteɪnəbl/", partOfSpeech: "adjective", chineseMeaning: "可持续的", exampleSentence: "We must develop sustainable energy sources for the future.", exampleTranslation: "我们必须为未来发展可持续的能源。", difficultyBand: "band6", category: "environment" },
    { word: "Ubiquitous", phonetic: "/juːˈbɪkwɪtəs/", partOfSpeech: "adjective", chineseMeaning: "无处不在的，普遍存在的", exampleSentence: "Smartphones have become ubiquitous in modern society.", exampleTranslation: "智能手机在现代社会已无处不在。", difficultyBand: "band8", category: "technology" },
    { word: "Validate", phonetic: "/ˈvælɪdeɪt/", partOfSpeech: "verb", chineseMeaning: "验证，确认", exampleSentence: "The results validate the hypothesis put forward by the research team.", exampleTranslation: "研究结果验证了研究团队提出的假设。", difficultyBand: "band7", category: "academic" },
    { word: "Widespread", phonetic: "/ˈwaɪdspred/", partOfSpeech: "adjective", chineseMeaning: "广泛的，普遍的", exampleSentence: "There is widespread support for the new education policy.", exampleTranslation: "新的教育政策得到了广泛支持。", difficultyBand: "band5", category: "general" },
    { word: "Yield", phonetic: "/jiːld/", partOfSpeech: "verb/noun", chineseMeaning: "产生；屈服；产量", exampleSentence: "The new farming methods yield significantly higher crop production.", exampleTranslation: "新的耕作方法产生了明显更高的作物产量。", difficultyBand: "band6", category: "agriculture" },
    { word: "Zealous", phonetic: "/ˈzeləs/", partOfSpeech: "adjective", chineseMeaning: "热心的，热情的", exampleSentence: "He was zealous in his pursuit of social justice.", exampleTranslation: "他热心追求社会正义。", difficultyBand: "band8", category: "character" },
    { word: "Adequate", phonetic: "/ˈædɪkwət/", partOfSpeech: "adjective", chineseMeaning: "足够的，适当的", exampleSentence: "The city has adequate public transportation for its residents.", exampleTranslation: "这座城市为居民提供了充足的公共交通。", difficultyBand: "band5", category: "general" },
    { word: "Collaborate", phonetic: "/kəˈlæbəreɪt/", partOfSpeech: "verb", chineseMeaning: "合作，协作", exampleSentence: "The two companies decided to collaborate on the new project.", exampleTranslation: "两家公司决定在新项目上合作。", difficultyBand: "band6", category: "work" },
    { word: "Deteriorate", phonetic: "/dɪˈtɪəriəreɪt/", partOfSpeech: "verb", chineseMeaning: "恶化，退化", exampleSentence: "The patient's condition began to deteriorate rapidly.", exampleTranslation: "病人的状况开始迅速恶化。", difficultyBand: "band7", category: "health" },
    { word: "Exacerbate", phonetic: "/ɪɡˈzæsəbeɪt/", partOfSpeech: "verb", chineseMeaning: "加剧，使恶化", exampleSentence: "The new policy may exacerbate the existing inequality.", exampleTranslation: "新政策可能会加剧现有的不平等。", difficultyBand: "band8", category: "society" },
    { word: "Fluctuate", phonetic: "/ˈflʌktʃueɪt/", partOfSpeech: "verb", chineseMeaning: "波动，起伏", exampleSentence: "Prices fluctuate according to supply and demand.", exampleTranslation: "价格根据供需关系波动。", difficultyBand: "band6", category: "economy" },
  ]);

  // Seed collocations
  await db.insert(collocations).values([
    { verb: "pay", preposition: "attention", fullSentence: "Please pay attention to the details in the instructions.", chineseMeaning: "注意细节", category: "general" },
    { verb: "make", preposition: "decision", fullSentence: "It is important to make a decision before the deadline.", chineseMeaning: "做决定", category: "general" },
    { verb: "take", preposition: "advantage", fullSentence: "Students should take advantage of the library resources.", chineseMeaning: "利用优势", category: "education" },
    { verb: "put", preposition: "effort", fullSentence: "Success requires you to put in considerable effort.", chineseMeaning: "付出努力", category: "work" },
    { verb: "give", preposition: "opportunity", fullSentence: "The program gives young people the opportunity to travel abroad.", chineseMeaning: "给予机会", category: "general" },
    { verb: "play", preposition: "role", fullSentence: "Technology plays an important role in modern education.", chineseMeaning: "发挥作用", category: "technology" },
    { verb: "set", preposition: "goal", fullSentence: "It is essential to set realistic goals for yourself.", chineseMeaning: "设定目标", category: "general" },
    { verb: "break", preposition: "record", fullSentence: "The athlete managed to break the world record.", chineseMeaning: "打破纪录", category: "sports" },
    { verb: "catch", preposition: "eye", fullSentence: "The advertisement was designed to catch the eye of potential customers.", chineseMeaning: "引人注目", category: "business" },
    { verb: "keep", preposition: "mind", fullSentence: "Please keep in mind that the deadline is approaching.", chineseMeaning: "记住，牢记", category: "general" },
    { verb: "run", preposition: "risk", fullSentence: "If you don't study, you run the risk of failing the exam.", chineseMeaning: "冒风险", category: "general" },
    { verb: "face", preposition: "challenge", fullSentence: "We need to face the challenge of climate change together.", chineseMeaning: "面对挑战", category: "environment" },
    { verb: "raise", preposition: "question", fullSentence: "The research raises important questions about data privacy.", chineseMeaning: "提出问题", category: "academic" },
    { verb: "meet", preposition: "demand", fullSentence: "The factory is struggling to meet the demand for its products.", chineseMeaning: "满足需求", category: "business" },
    { verb: "draw", preposition: "conclusion", fullSentence: "From the evidence, we can draw the conclusion that he is guilty.", chineseMeaning: "得出结论", category: "academic" },
  ]);

  // Seed listening tracks (with transcript-based content, no audio file needed - we'll simulate)
  await db.insert(listeningTracks).values([
    {
      title: "University Lecture: Climate Change",
      transcript: "Climate change is one of the most pressing issues facing our planet today. Scientists have observed a rapid increase in global temperatures over the past century, primarily due to human activities such as burning fossil fuels and deforestation. The consequences include rising sea levels, extreme weather events, and threats to biodiversity. Governments and organizations worldwide are working to reduce carbon emissions and transition to renewable energy sources. However, significant challenges remain in implementing effective policies and changing public behavior.",
      difficulty: "medium",
      duration: 60,
      category: "academic",
      blanksJSON: JSON.stringify([{ word: "fossil fuels", index: 35 }, { word: "deforestation", index: 38 }, { word: "biodiversity", index: 52 }, { word: "renewable", index: 66 }]),
    },
    {
      title: "Interview: Technology and Education",
      transcript: "In recent years, technology has transformed the educational landscape. Online learning platforms have made education accessible to millions of people worldwide. Students can now access lectures, complete assignments, and interact with instructors from anywhere with an internet connection. However, critics argue that digital learning lacks the personal interaction and social development that traditional classrooms provide. The key is finding a balance between leveraging technology and maintaining meaningful human connections in education.",
      difficulty: "easy",
      duration: 50,
      category: "education",
      blanksJSON: JSON.stringify([{ word: "accessible", index: 14 }, { word: "assignments", index: 20 }, { word: "connection", index: 28 }, { word: "leveraging", index: 49 }]),
    },
    {
      title: "Presentation: Urban Planning",
      transcript: "Modern urban planning requires a holistic approach that considers environmental sustainability, social equity, and economic viability. As cities continue to grow, planners must design efficient public transportation systems, create green spaces, and ensure affordable housing for all residents. Smart city technologies offer innovative solutions for managing traffic, reducing energy consumption, and improving public services. Successful urban development depends on collaboration between government agencies, private developers, and community stakeholders.",
      difficulty: "hard",
      duration: 55,
      category: "academic",
      blanksJSON: JSON.stringify([{ word: "sustainability", index: 10 }, { word: "equity", index: 13 }, { word: "efficient", index: 23 }, { word: "stakeholders", index: 52 }]),
    },
  ]);

  console.log("Done.");
  process.exit(0);
}

seed();
