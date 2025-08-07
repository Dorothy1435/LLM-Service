# routers/faq.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.gpt import ask_gpt
import json
import os

router = APIRouter(prefix="/faq", tags=["FAQ"])

FAQ_PATH = "./data/faq.json"

class FAQRequest(BaseModel):
    question: str

class FAQResponse(BaseModel):
    answer: str
    source: str  # "faq" 또는 "gpt"

@router.post("/", response_model=FAQResponse)
async def answer_faq(req: FAQRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="질문이 비어 있습니다.")

    if not os.path.exists(FAQ_PATH):
        raise HTTPException(status_code=500, detail="FAQ 데이터가 존재하지 않습니다.")

    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        faq_data = json.load(f)

    # 단순 키워드 검색 (향후 유사도 개선 가능)
    for faq in faq_data:
        if faq["question"] in question or question in faq["question"]:
            return FAQResponse(answer=faq["answer"], source="faq")

    # FAQ에서 못 찾으면 GPT 호출
    prompt = f"""
너는 학과 사무실 챗봇이야.
아래 질문에 대해 학생의 입장에서 친절하고 정확하게 답변해줘.

질문: "{question}"
"""
    gpt_reply = ask_gpt(prompt)
    return FAQResponse(answer=gpt_reply, source="gpt")
