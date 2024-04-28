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
import pika
from PIL import Image

#from watchdog.events import FileSystemEventHandler

# class MyHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         print(f'event type: {event.event_type}  path : {event.src_path}')
#         arquivo_pdf = open(event.src_path, 'rb').read()
#         threading.Thread(target=pdf_to_images, args=(arquivo_pdf,)).start()

def pdf_to_images():
    folder_path = 'lote'
    
    # load all pdfs in the folder lote and convert each page to tiff
    for file in os.listdir(folder_path):
        try:
            if file.endswith('.pdf'):
                file_path = os.path.join(folder_path, file)
                
                
                print(f'convertendo {file_path}')
                arquivo_pdf = open(file_path, 'rb').read()
                
                images = convert_from_bytes(arquivo_pdf, dpi=300)
                images = [cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) for image in images]
                os.makedirs(f'output/{file}', exist_ok=True)
                file_name = file_path.split('/')[-1]
                for i, image in enumerate(images):
                    
                    tiff_path = os.path.join(f'output/{file_name}', f'{file_name}_page_{i+1}.tiff')
                    cv2.imwrite(tiff_path, image)
        except Exception as e:
            print(e)    
            continue

    return {"message": "pdf convertido para tiff"}


class Pdf2Tiff(Resource):

    def get(self):
        # conection_parameters =  pika.ConnectionParameters(host='localhost')
        # connection = pika.BlockingConnection(conection_parameters)

        # channel = connection.channel()
        # channel.queue_declare(queue='ocr_queue')

        s = time.time()
        # path = request.form.get('path')
        # # arquivo_zip = request.files['file']
        # # if not arquivo_zip:
        # #     return {'message': 'arquivo não subido'}, 400

        file = pdf_to_images()
        t = time.time() - s
        
        return {'message': 'convertindo pdfs para tiff', 'contrato': f'{file}', 'tempo de processamento':t}, 200
