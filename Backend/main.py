from fastapi import FastAPI
from routers import notice, graduate, schedule, professor, faq
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정 (React/HTML에서 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중에는 "*" 나중엔 도메인 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기능별 라우터 등록
app.include_router(notice.router)
app.include_router(graduate.router)
app.include_router(schedule.router)  
app.include_router(faq.router) 
@app.get("/")
async def root():
    return {"message": "학과 챗봇 서버 정상 작동 중"}
