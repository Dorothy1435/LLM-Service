# routers/graduate.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os

router = APIRouter(prefix="/graduate", tags=["졸업 판단"])

# 경로 설정
GRAD_RULE_PATH = "./data/graduate_rule.json"

# 입력 형식
class GraduateRequest(BaseModel):
    student_id: str
    total_credit: int
    major_credit: int
    taken_courses: List[str]

# 응답 형식
class GraduateResponse(BaseModel):
    student_id: str
    graduation_possible: bool
    missing_courses: List[str]
    credit_status: str

@router.post("/", response_model=GraduateResponse)
async def check_graduation(req: GraduateRequest):
    # 졸업 요건 불러오기
    if not os.path.exists(GRAD_RULE_PATH):
        raise HTTPException(status_code=500, detail="졸업 요건 파일을 찾을 수 없습니다.")

    with open(GRAD_RULE_PATH, "r", encoding="utf-8") as f:
        rules = json.load(f)

    # 필수 항목 검사
    missing_courses = [course for course in rules["required_courses"] if course not in req.taken_courses]
    enough_credit = req.total_credit >= rules["min_credit"]
    enough_major = req.major_credit >= rules["min_major_credit"]

    graduation_possible = (len(missing_courses) == 0 and enough_credit and enough_major)

    credit_status = f"총 학점 {req.total_credit}/{rules['min_credit']} | 전공 {req.major_credit}/{rules['min_major_credit']}"

    return GraduateResponse(
        student_id=req.student_id,
        graduation_possible=graduation_possible,
        missing_courses=missing_courses,
        credit_status=credit_status
    )
