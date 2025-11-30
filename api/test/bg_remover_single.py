from app.services.bg_remover import remove_bg_single

from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post('')
async def route_remove_bg(image: UploadFile = File(None)):
   return await remove_bg_single(image)