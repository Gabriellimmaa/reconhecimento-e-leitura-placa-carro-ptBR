import os
import matplotlib.pyplot as plt
import cv2
import pytesseract
from matplotlib.widgets import Button
from utils import exibir_resultado
from aplicar_ocr import aplicar_ocr


def processar_contornos(imagem_original, imagem_processada):
    contornos, _ = cv2.findContours(
        imagem_processada, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    possiveis_placas = []

    for contorno in contornos:
        # Aproximar o contorno por um polígono
        perimetro = cv2.arcLength(contorno, True)
        aprox = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)
        area = cv2.contourArea(contorno)
        x, y, w, h = cv2.boundingRect(contorno)

        # verificar se a altura é maior que a largura
        if h > w:
            continue

        # verificar se há uma proporcao onde a altura é menor que 20% da largura
        if h < (w * 0.2):
            continue

        if area < 10000 or area > 70000:
            continue

        # Se o polígono tiver quatro lados, consideramos que é um retângulo
        if len(aprox) >= 4 and len(aprox) < 10:
            cv2.drawContours(imagem_original, [aprox], -1, (0, 255, 0), 2)

            # recortar a imagem da placa
            x, y, w, h = cv2.boundingRect(contorno)
            imagem_recortada = imagem_original[y:y + h, x:x + w]

            # converter a imagem da placa para tons de cinza
            imagem_recortada_cinza = cv2.cvtColor(
                imagem_recortada, cv2.COLOR_BGR2GRAY)

            # aplicar limiarização para tornar os caracteres mais destacados
            _, imagem_recortada_limiarizada = cv2.threshold(
                imagem_recortada_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # aplicar operação de fechamento para preencher regiões de contornos
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            imagem_recortada_processada = cv2.morphologyEx(
                imagem_recortada_limiarizada, cv2.MORPH_CLOSE, kernel)

            # aplicar operação de abertura para remover ruídos
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            imagem_recortada_processada = cv2.morphologyEx(
                imagem_recortada_processada, cv2.MORPH_OPEN, kernel)

            # aplicar operação de dilatação para aumentar a espessura dos caracteres
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            imagem_recortada_processada = cv2.dilate(
                imagem_recortada_processada, kernel, iterations=1)

            # aplicar operação de erosão para reduzir a espessura dos caracteres
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            imagem_recortada_processada = cv2.erode(
                imagem_recortada_processada, kernel, iterations=1)

            possiveis_placas.append(
                (imagem_recortada, imagem_recortada_processada))

    return possiveis_placas
