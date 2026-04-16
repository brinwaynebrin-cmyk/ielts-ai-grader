#!/usr/bin/env python3
"""
雅思词汇转换工具
将Excel/CSV转换为JSON格式，支持9000+词汇
"""

import pandas as pd
import json
import os
from pathlib import Path

def create_vocab_json(input_file, output_dir="data/vocab"):
    """转换主词汇库"""
    print(f"📖 Reading {input_file}...")
    
    # 读取数据
    if input_file.endswith('.xlsx'):
        df = pd.read_excel(input_file)
    else:
        df = pd.read_csv(input_file)
    
    total = len(df)
    print(f"✅ Loaded {total} words")
    
    # 按Band分组
    bands = {
        'band6': {'min': 6.0, 'max': 6.9, 'words': []},
        'band7': {'min': 7.0, 'max': 7.9, 'words': []},
        'band8': {'min': 8.0, 'max': 9.0, 'words': []}
    }
    
    for idx, row in df.iterrows():
        # 处理每一行数据
        band_score = float(row.get('band', 6.0))
        
        word_entry = {
            "id": f"word_{idx:05d}",
            "word": str(row['word']).strip(),
            "phonetic": str(row.get('phonetic', '')).strip(),
            "pos": str(row.get('pos', 'v')).strip(),
            "meaning": str(row['meaning']).strip(),
            "en_meaning": str(row.get('en_meaning', '')).strip(),
            "examples": [ex.strip() for ex in str(row.get('example', '')).split('|') if ex.strip()],
            "collocations": [col.strip() for col in str(row.get('collocations', '')).split(',') if col.strip()],
            "synonyms": [syn.strip() for syn in str(row.get('synonyms', '')).split(',') if syn.strip()],
            "topics": [t.strip() for t in str(row.get('topics', 'general')).split(',') if t.strip()],
            "band": band_score,
            "frequency": int(row.get('frequency', 50)) if pd.notna(row.get('frequency')) else 50,
            "difficulty": band_score
        }
        
        # 分类到对应band
        for band_key, band_info in bands.items():
            if band_info['min'] <= band_score <= band_info['max']:
                word_entry['id'] = f"{band_key}_{len(band_info['words']):04d}"
                band_info['words'].append(word_entry)
                break
        
        # 显示进度
        if (idx + 1) % 500 == 0:
            print(f"   Processed {idx + 1}/{total} words...")
    
    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 保存文件
    for band_key, band_info in bands.items():
        if band_info['words']:
            output_file = os.path.join(output_dir, f"{band_key}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "metadata": {
                        "band": band_key.replace('band', ''),
                        "total": len(band_info['words']),
                        "version": "2024.1",
                        "generated_from": input_file
                    },
                    "words": band_info['words']
                }, f, ensure_ascii=False, indent=2)
            print(f"✅ Generated {band_key}.json with {len(band_info['words'])} words")

def create_topic_files(df, output_dir="data/topics"):
    """按话题生成分类文件"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 提取所有话题
    all_topics = set()
    for topics_str in df['topics'].dropna():
        all_topics.update([t.strip() for t in str(topics_str).split(',')])
    
    print(f"📁 Found {len(all_topics)} topics: {', '.join(all_topics)}")
    
    for topic in all_topics:
        topic_words = []
        for _, row in df.iterrows():
            if pd.notna(row['topics']) and topic in str(row['topics']):
                topic_words.append({
                    "word": row['word'],
                    "meaning": row['meaning'],
                    "band": float(row.get('band', 6.0)),
                    "usage": row.get('collocations', '').split(',')[0] if pd.notna(row.get('collocations')) else ''
                })
        
        if topic_words:
            output_file = os.path.join(output_dir, f"{topic}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "topic": topic,
                    "topic_cn": topic,  # 可以映射中文名
                    "total": len(topic_words),
                    "words": topic_words
                }, f, ensure_ascii=False, indent=2)
            print(f"✅ Generated {topic}.json with {len(topic_words)} words")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python convert_vocab.py <input.xlsx or input.csv> [--topics]")
        print("Example: python convert_vocab.py ielts_words.xlsx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    generate_topics = "--topics" in sys.argv
    
    create_vocab_json(input_file)
    
    if generate_topics:
        print("\n📚 Generating topic files...")
        df = pd.read_excel(input_file) if input_file.endswith('.xlsx') else pd.read_csv(input_file)
        create_topic_files(df)
    
    print("\n🎉 All done! Files are ready in data/ directory")
