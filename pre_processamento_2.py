import os
import matplotlib.pyplot as plt
import cv2
import pytesseract
from matplotlib.widgets import Button

def pre_processamento_2(imagem_placa):
    # Converter a imagem para tons de cinza
    imagem_cinza = cv2.cvtColor(imagem_placa, cv2.COLOR_BGR2GRAY)

    # Aplicar filtros para remover ruídos
    imagem_cinza = cv2.bilateralFilter(imagem_cinza, 9, 75, 75)
    imagem_cinza = cv2.GaussianBlur(imagem_cinza, (5, 5), 0)

    # Aplicar limiarização adaptativa para tornar os caracteres mais destacados
    imagem_limiarizada = cv2.adaptiveThreshold(imagem_cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Aplicar operação de fechamento para preencher regiões de contornos
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    imagem_processada = cv2.morphologyEx(imagem_limiarizada, cv2.MORPH_CLOSE, kernel)

    plt.imshow(cv2.cvtColor(imagem_processada, cv2.COLOR_BGR2RGB))
    plt.show()

    # mostrar os contornos da imagem processada
    contornos, _ = cv2.findContours(imagem_processada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contornos