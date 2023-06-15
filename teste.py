import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import threading

def pdf_to_images(pdf_path):
    # Convierte el PDF en una lista de imágenes
    images = convert_from_path(pdf_path, dpi=300)
    return images

def perform_ocr(image):
    # Realiza OCR en la imagen utilizando pytesseract
    text = pytesseract.image_to_string(image)
    return text

def process_page(page_number, image):
    # Realiza OCR en la imagen y muestra el resultado
    text = perform_ocr(image)
    print(f'Texto extraído de la página {page_number}:')
    print(text)
    print('---')


pdf_path = 'teste.pdf'

# Convertir el PDF a imágenes
images = pdf_to_images(pdf_path)
import time

start = time.time()
# Procesar cada página en un hilo separado
threads = []
for page_number, image in enumerate(images, 1):
    print(f'Procesando página {page_number}...')
    thread = threading.Thread(target=process_page, args=(page_number, image))
    thread.start()
    threads.append(thread)
finish = time.time()

print(f'Tiempo de ejecución: {finish - start} segundos')
# Esperar a que todos los hilos termine