# routers/schedule.py

from fastapi import APIRouter, Query
from typing import List
from pydantic import BaseModel
import json
import os
from datetime import datetime

router = APIRouter(prefix="/schedule", tags=["학과 일정"])

SCHEDULE_PATH = "./data/schedule.json"

class ScheduleItem(BaseModel):
    date: str
    title: str

@router.get("/", response_model=List[ScheduleItem])
async def get_schedule(month: str = Query(..., description="예: '2025-08' 형식으로 요청")):
    # 파일 존재 확인
    if not os.path.exists(SCHEDULE_PATH):
        return []

    # 일정 파일 읽기
    with open(SCHEDULE_PATH, "r", encoding="utf-8") as f:
        schedules = json.load(f)

    # 필터링: 해당 월만 추출
    result = [
        item for item in schedules
        if item["date"].startswith(month)
    ]

    return result
