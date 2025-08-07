# utils/gpt.py

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # .env 또는 환경변수에 저장

def ask_gpt(prompt: str, model="gpt-3.5-turbo") -> str:
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "당신은 학과 공지를 잘 설명하는 챗봇입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[GPT Error] {e}")
        return "⚠️ 답변을 생성하는 중 오류가 발생했습니다."
