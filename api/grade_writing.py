from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import json
import os
import hashlib
from typing import Literal
import time

app = FastAPI()

# 双API配置：DeepSeek（主力，便宜）+ OpenAI（备用）
CLIENTS = {
    "deepseek": openai.OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY", ""),
        base_url="https://api.deepseek.com/v1"
    ),
    "openai": openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY", "")
    )
}

# 内存缓存（省钱关键）
CACHE = {}

class WritingRequest(BaseModel):
    essay: str
    task_type: Literal["task1", "task2"]
    prompt: str
    target_band: float = 7.0

def get_cache_key(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()

@app.post("/api/grade_writing")
async def grade_writing(data: WritingRequest):
    start_time = time.time()
    
    # 检查缓存
    cache_key = get_cache_key(data.essay + data.task_type)
    if cache_key in CACHE:
        return {**CACHE[cache_key], "cached": True, "cost_usd": 0}
    
    word_count = len(data.essay.split())
    min_words = 150 if data.task_type == "task1" else 250
    
    if word_count < min_words:
        raise HTTPException(status_code=400, detail=f"字数不足，需要至少{min_words}词")

    system_prompt = f"""你是资深雅思考官，按官方四项标准评分。
输出JSON格式：
{{
  "overall_band": float,
  "breakdown": {{
    "TR": {{"score": float, "comments": "string"}},
    "CC": {{"score": float, "comments": "string"}},
    "LR": {{"score": float, "comments": "string"}},
    "GRA": {{"score": float, "comments": "string"}}
  }},
  "detailed_feedback": {{
    "strengths": ["string"],
    "weaknesses": ["string"],
    "vocabulary_suggestions": [{{"original": "bad", "better": "detrimental"}}]
  }},
  "corrected_paragraphs": [{{"original": "string", "corrected": "string", "focus": "语法/词汇/逻辑"}}]
}}"""

    user_prompt = f"""题目：{data.prompt}
作文（{word_count}词）：{data.essay}
请评分并给出提升到{data.target_band}分的建议。"""

    # 优先DeepSeek（便宜90%）
    for provider, model in [("deepseek", "deepseek-chat"), ("openai", "gpt-3.5-turbo")]:
        try:
            client = CLIENTS[provider]
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
                max_tokens=2000
            )
            
            result = json.loads(response.choices[0].message.content)
            result["word_count"] = word_count
            result["processing_time"] = round(time.time() - start_time, 2)
            result["provider"] = provider
            result["cost_usd"] = round(response.usage.total_tokens * 0.000001, 5)
            CACHE[cache_key] = result
            return result
            
        except Exception as e:
            continue
    
    return {"error": "服务繁忙", "overall_band": 5.5}

from mangum import Mangum
handler = Mangum(app)
