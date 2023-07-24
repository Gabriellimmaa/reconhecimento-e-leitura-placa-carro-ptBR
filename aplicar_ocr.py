import os
import matplotlib.pyplot as plt
import cv2
import pytesseract
from matplotlib.widgets import Button
from utils import exibir_resultado, substituir_letras_por_numeros, gerar_possibilidades_mercosul
import re


def encontrar_placa(string):
    # Expressão regular para procurar a placa com 3 letras seguidas de 4 números
    padrao = r'[A-Z]{3}\d{4}'

    # Procurar todas as ocorrências do padrão na string
    placas_encontradas = re.findall(padrao, string)

    # Retornar a primeira placa encontrada ou None se nenhuma placa for encontrada
    return placas_encontradas[0] if placas_encontradas else None


def encontrar_placa_mercosul(string):
    # Expressão regular para procurar a placa Mercosul
    padrao = r'[A-Z]{3}[0-9][0-9A-Z][0-9]{2}'

    # Procurar todas as ocorrências do padrão na string
    placas_encontradas = re.findall(padrao, string)

    # Retornar a primeira placa encontrada ou None se nenhuma placa for encontrada
    return placas_encontradas[0] if placas_encontradas else None


def aplicar_ocr(possiveis_placas):
    for tupla in possiveis_placas:
        placa_recortada, placa_recortada_processada = tupla

        x, y, w, h = cv2.boundingRect(placa_recortada_processada)

        # possivel placa modelo antigo
        # caso o recorte tenha mais de 120 pixels de altura, remover 30 pixels da parte de cima e 10 pixels da parte de baixo
        if(h > 120):
            placa_recortada_processada = placa_recortada_processada[30:]
            placa_recortada_processada = placa_recortada_processada[:-10]

        # Executar o OCR com o Tesseract para detectar a placa em português
        resultado_tesseract_por = pytesseract.image_to_string(
            placa_recortada_processada, lang='por', config=r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6 --oem 3')
        placa_detectada_por = "".join(
            filter(str.isalnum, resultado_tesseract_por))

        placa_mercosul = encontrar_placa_mercosul(placa_detectada_por)
        if placa_mercosul:
            return placa_mercosul, placa_recortada, placa_recortada_processada
        placa_antiga = encontrar_placa(placa_detectada_por)
        if placa_antiga:
            return placa_antiga, placa_recortada, placa_recortada_processada

        # Executar o OCR com o Tesseract para detectar a placa em inglês
        resultado_tesseract_eng = pytesseract.image_to_string(
            placa_recortada_processada, lang='eng', config=r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 --psm 6 --oem 3')

        placa_detectada_eng = "".join(
            filter(str.isalnum, resultado_tesseract_eng))

        placa_mercosul = encontrar_placa_mercosul(placa_detectada_eng)
        if placa_mercosul:
            return placa_mercosul, placa_recortada, placa_recortada_processada
        placa_antiga = encontrar_placa(placa_detectada_eng)
        if placa_antiga:
            return placa_antiga, placa_recortada, placa_recortada_processada

        # pegar os ultimos quatro caracteres da placa detectada por e aplicar o array para substituir letras por números
        ultimos_4_caracteres = placa_detectada_por[-4:]

        # possibilidades placa normal
        possibilidades = substituir_letras_por_numeros(ultimos_4_caracteres)
        # converter um array em uma lista string com quebra de linha
        result = ""
        for i in range(len(possibilidades)):
            result += placa_detectada_por[:3] + \
                possibilidades[i] + "\n"
        result += "\nMercosul:\n"

        # possibilidades placa mercosul
        possibilidades_mercosul = gerar_possibilidades_mercosul(
            ultimos_4_caracteres)
        for i in range(len(possibilidades_mercosul)):
            result += placa_detectada_por[:3] + \
                possibilidades_mercosul[i] + "\n"

        return result, placa_recortada, placa_recortada_processada
