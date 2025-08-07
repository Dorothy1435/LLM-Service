from fastapi import APIRouter

router = APIRouter(prefix="/professor", tags=["교수 정보"])

@router.get("/")
async def professor_info():
    return {"message": "교수 정보 라우터 정상 작동 중"}
