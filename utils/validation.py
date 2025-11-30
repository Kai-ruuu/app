from magic import from_buffer

image_mimes = { 'image/jpeg', 'image/png' }

def validate_single_image(contents: bytes):
   return from_buffer(contents, mime = True) in image_mimes

def validate_batch_images(contents_list: list[dict]) -> dict:
   validation_results = []
   
   for contents in contents_list:
      content_is_valid = False
      content_bytes = contents.get('content_bytes')
      content_is_decoded = contents.get('is_decoded')
      content_filename = contents.get('content_filename')
      
      if content_is_decoded:
         content_is_valid = validate_single_image(content_bytes)

      validation_results.append({
         'is_valid': content_is_valid,
         'is_decoded': content_is_decoded,
         'content_bytes': content_bytes,
         'content_filename': content_filename,
      })
   
   return validation_results