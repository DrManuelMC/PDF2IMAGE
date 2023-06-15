import os
from pdf2image import convert_from_bytes
from flask_restful import Resource
from flask import current_app as app
from flask import request
import threading
#from watchdog.events import FileSystemEventHandler

# class MyHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         print(f'event type: {event.event_type}  path : {event.src_path}')
#         arquivo_pdf = open(event.src_path, 'rb').read()
#         threading.Thread(target=pdf_to_images, args=(arquivo_pdf,)).start()

def pdf_to_images(arquivo_pdf, file_name):
    images = convert_from_bytes(arquivo_pdf, dpi=300)
    os.makedirs(f'output/{file_name}', exist_ok=True)
    # Guarda cada imagen como TIFF
    for i, image in enumerate(images):
        
        tiff_path = os.path.join(f'output/{file_name}', f'{file_name}_page_{i+1}.tiff')
        image.save(tiff_path, format='TIFF')
    print('PDF convertido a TIFF')
    

class Pdf2Tiff(Resource):

    def get(self):
        file_name = request.files['file'].filename
        arquivo_pdf = request.files['file'].read()
        if not arquivo_pdf:
            return {'message': 'arquivo não subido'}, 400

        threading.Thread(target=pdf_to_images, args=(arquivo_pdf, file_name.split('.')[0])).start()

        return {'message': 'PDF converted to TIFF'}, 200
