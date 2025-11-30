from services.bg_remover import remove_bg_batch

from typing import List
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post('')
async def route_remove_bg(images: List[UploadFile] = File(None)):
   return await remove_bg_batch(images)