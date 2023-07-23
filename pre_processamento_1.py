import os
import matplotlib.pyplot as plt
import cv2
import pytesseract
from matplotlib.widgets import Button

def pre_processamento_1(imagem_placa):
    # Converter a imagem para tons de cinza
    imagem_cinza = cv2.cvtColor(imagem_placa, cv2.COLOR_BGR2GRAY)

    # Aplicar limiarização para tornar os caracteres mais destacados
    _, imagem_limiarizada = cv2.threshold(imagem_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Aplicar operação de fechamento para preencher regiões de contornos
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    imagem_processada = cv2.morphologyEx(imagem_limiarizada, cv2.MORPH_CLOSE, kernel)
    
    plt.imshow(cv2.cvtColor(imagem_processada, cv2.COLOR_BGR2RGB))
    plt.show()

    # mostrar os contornos da imagem processada
    contornos, _ = cv2.findContours(imagem_processada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # melhorar a precisão dos contornos
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:5]

    return contornos