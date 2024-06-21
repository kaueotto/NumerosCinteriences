import cv2
import os
import numpy as np
import DescobrirCoordenadas 
import matplotlib.pyplot as plt

def load_components(component_dir):
    components = {}
    for filename in os.listdir(component_dir):
        if filename.endswith('.png'):
            number = int(filename.split('.')[0])
            img_path = os.path.join(component_dir, filename)
            components[number] = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    return components

def split_image_in_plus(image_path):
    DescobrirCoordenadas.paint_white(image_path, 'Parts/Hundreads.png', {(0, 0, 10, 40), (15, 0, 30, 24)})
    DescobrirCoordenadas.paint_white(image_path, 'Parts/Units.png', {(0, 0, 10, 40), (15, 24, 30, 40)})
    DescobrirCoordenadas.paint_white(image_path, 'Parts/Tens.png', {(0, 24, 10, 40), (15, 0, 30, 40)})
    DescobrirCoordenadas.paint_white(image_path, 'Parts/Thousands.png', {(0, 0, 10, 24), (15, 0, 30, 40)})

def binarizar_imagem(imagem):
    if len(imagem.shape) == 3:
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    _, binarizada = cv2.threshold(imagem, 127, 1, cv2.THRESH_BINARY_INV)
    return binarizada

def image_histogram_similarity(img1, img2):
    imagem_bin1 = binarizar_imagem(img1)
    imagem_bin2 = binarizar_imagem(img2)
    diferenca = cv2.absdiff(imagem_bin1, imagem_bin2)
    total_pixels = imagem_bin1.size
    pixels_diferentes = np.count_nonzero(diferenca)
    similaridade = (total_pixels - pixels_diferentes) / total_pixels
    return similaridade

def identify_part(part, components, threshold=0.3):
    max_similarity = 0
    identified_number = None
    for number, component_image in components.items():
        similarity = image_histogram_similarity(part, component_image)
        if similarity > max_similarity:
            max_similarity = similarity
            identified_number = number
    if max_similarity < threshold:
        return 0
    return identified_number

component_dir = 'C:\\Projetos\\Python\\NumerosCIsterience\\Numeros'
output_dir = 'C:\\Projetos\\Python\\NumerosCIsterience\\Parts'
components = load_components(component_dir)
image_path = 'C:\\Projetos\\Python\\NumerosCIsterience\\9938.png'

split_image_in_plus(image_path)

parts_paths = ['Parts/Hundreads.png', 'Parts/Units.png', 'Parts/Tens.png', 'Parts/Thousands.png']
identified_parts = [identify_part(cv2.imread(part_path, cv2.IMREAD_GRAYSCALE), components) for part_path in parts_paths]
print(identified_parts)

identified_number = sum(identified_parts)
print(f"O número identificado é: {identified_number}")
