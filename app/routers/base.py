from fastapi import APIRouter , Depends
from app.core.config import Settings, get_settings

router = APIRouter(
    prefix="/api/v1",
    tags=["base"],
)

@router.get("/")
async def welcome(app_settings : Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {
        "message": f"Welcome to {app_name}!",
        "version": app_version
    }
