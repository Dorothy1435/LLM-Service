# routers/notice.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

from utils.gpt import ask_gpt  # GPT 응답 함수
from glob import glob

router = APIRouter(prefix="/notice", tags=["공지"])

NOTICE_DIR = "./data/notice"  # 공지사항 폴더 경로

# 요청 형식 정의
class NoticeRequest(BaseModel):
    question: str

# 응답 형식 정의
class NoticeResponse(BaseModel):
    answer: str

@router.post("/", response_model=NoticeResponse)
async def get_notice_answer(req: NoticeRequest):
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="질문이 비어 있습니다.")

    # 최신 공지사항 3개 불러오기
    notice_files = sorted(glob(os.path.join(NOTICE_DIR, "*.txt")), reverse=True)[:3]

    if not notice_files:
        raise HTTPException(status_code=404, detail="공지사항이 없습니다.")

    # 텍스트 통합
    combined_notice = ""
    for f in notice_files:
        with open(f, "r", encoding="utf-8") as file:
            combined_notice += f"\n\n[공지: {os.path.basename(f)}]\n" + file.read()

    # GPT 프롬프트 생성
    prompt = f"""
다음은 학과 공지사항입니다:

{combined_notice}

질문: "{question}"
위 공지사항을 기반으로 정확하게 대답해 주세요. 공지사항에 없는 내용은 모른다고 답하세요.
"""

    # GPT 응답
    gpt_answer = ask_gpt(prompt)
    return NoticeResponse(answer=gpt_answer)
