from utils.image import get_batch_image_contents
from utils.setup import remover_single_model, remover_batch_model 
from utils.validation import validate_single_image, validate_batch_images

from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from urllib.parse import quote
from fastapi.responses import StreamingResponse
from fastapi import UploadFile, HTTPException, status

async def remove_bg_single(image: UploadFile):
   if not image:
      raise HTTPException(
         status_code = status.HTTP_400_BAD_REQUEST,
         detail = 'No file was uploaded.'
      )
   
   try:
      content = await image.read()
   except:
      raise HTTPException(
         status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
         detail = 'Failed to decode the image.'
      )

   if not validate_single_image(content):
      raise HTTPException(
         status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
         detail = f'{image.filename} is not a valid image file.'
      )
   
   try:      
      buffer = BytesIO()
      result = remover_single_model.remove_background(content)
      result.save(buffer, format='PNG')
      buffer.seek(0)
      
      output_media_type = 'image/png'
      output_filename = Path(image.filename).stem + '.png'
      output_headers = {'Content-Disposition': f'attachment; filename={output_filename}'}
      return StreamingResponse(buffer, media_type = output_media_type, headers=output_headers)
   except:
      raise HTTPException(
         status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
         detail = 'Failed to remove image background.'
      )

async def remove_bg_batch(images: list[UploadFile]):
   decoded_image_contents = await get_batch_image_contents(images)
   validated_image_contents = validate_batch_images(decoded_image_contents)
   processed_bytes = []
   error_messages = []
   
   for image in validated_image_contents:
      content_filename = image.get("content_filename")
      
      if not image.get('is_decoded'):
         error_messages.append(f'Failed to decode {content_filename}.')
      elif not image.get('is_valid'):
         error_messages.append(f'{content_filename} is not a valid image file.')
      else:
         try:
            buffer = BytesIO()
            result = remover_batch_model.remove_background(image.get('content_bytes'))
            result.save(buffer, format='PNG')
            buffer.seek(0)

            output_filename = Path(content_filename).stem + '.png'
            processed_bytes.append({ 'image_bytes': buffer, 'image_filename': output_filename })
         except:
            error_messages.append(f'Failed to remove {content_filename}\'s background.')
   
   zip_buffer = BytesIO()

   with ZipFile(zip_buffer, mode='w') as zip_file_:
      for bytes_ in processed_bytes:
         zip_file_.writestr(bytes_.get('image_filename'), bytes_.get('image_bytes').getvalue())
      
      zip_file_.writestr('errors.txt', "\n".join(error_messages))
   
   zip_buffer.seek(0)
   output_media_type = 'application/zip'
   output_headers = { 'Content-Disposition': f'attachment; filename="images.zip"; filename*=UTF-8\'\'{quote("images.zip")}'}
   return StreamingResponse(zip_buffer, media_type = output_media_type, headers = output_headers)