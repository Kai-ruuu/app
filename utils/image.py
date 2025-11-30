from fastapi import UploadFile

async def get_batch_image_contents(images: list[UploadFile]) -> list[dict]:
   decode_results = []
   
   for image in images:
      is_decoded = False
      
      try:
         content_filename = image.filename
         content_bytes = await image.read()
         is_decoded = True
      except:
         is_decoded = False
      
      decode_results.append({
         'is_decoded': is_decoded,
         'content_bytes': content_bytes,
         'content_filename': content_filename,
      })
   
   return decode_results