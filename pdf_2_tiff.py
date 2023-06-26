import os
from pdf2image import convert_from_bytes
from flask_restful import Resource
from flask import current_app as app
from flask import request
import threading
import time
import zipfile
import cv2
import numpy as np
from PIL import Image
#from watchdog.events import FileSystemEventHandler

# class MyHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         print(f'event type: {event.event_type}  path : {event.src_path}')
#         arquivo_pdf = open(event.src_path, 'rb').read()
#         threading.Thread(target=pdf_to_images, args=(arquivo_pdf,)).start()

def pdf_to_images(arquivo_pdf, file_name, j, k):
    try:
        images = convert_from_bytes(arquivo_pdf, dpi=300)
        images = [cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) for image in images]
        os.makedirs(f'output/{file_name}', exist_ok=True)
    except:
        return
    # Guarda cada imagen como TIFF
    for i, image in enumerate(images):
        
        tiff_path = os.path.join(f'output/{file_name}', f'{file_name}_page_{i+1}.tiff')
        cv2.imwrite(tiff_path, image)
    print(f'PDF {file_name} convertido a TIFF, contrato {j} de {k}')

def get_all_files_from_zip(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        i =0
        k = len(zip_ref.namelist())
        for file in zip_ref.namelist():
            if i == 3:
                break
            i += 1
            if file.endswith('.pdf'):
                zip_ref.extract(file, 'temp/')
                arquivo_pdf = open(f'temp/{file}', 'rb').read()
                pdf_to_images(arquivo_pdf, file.split('.')[0], i, k)
                os.remove(f'temp/{file}')
                

class Pdf2Tiff(Resource):

    def get(self):
        s = time.time()

        arquivo_zip = request.files['file']
        if not arquivo_zip:
            return {'message': 'arquivo não subido'}, 400

        get_all_files_from_zip(arquivo_zip)
        t = time.time() - s
        
        return {'message': 'convertindo pdfs para tiff', 'tempo de processamento de 1 contrato': t}, 200
