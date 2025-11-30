from api.test import bg_remover_batch as bgrb_api
from api.test import bg_remover_single as bgrs_api

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
   CORSMiddleware,
   allow_headers = ["*"],
   allow_methods = ["*"],
   allow_origins = ["*"],
   allow_credentials = True
)

app.get('/')
async def index():
   return 'hey'

app.include_router(bgrb_api.router, prefix = '/api/remove-batch')
app.include_router(bgrs_api.router, prefix = '/api/remove-single')