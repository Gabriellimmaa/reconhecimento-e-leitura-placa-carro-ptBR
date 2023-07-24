from itertools import product
import os
import matplotlib.pyplot as plt
import cv2
import pytesseract
from matplotlib.widgets import Button

letras_numeros = {
    'I': '1',
    'O': '0',
    'Q': '0',
    'Z': '2',
    'S': ['5', '9'],
    'G': '6',
    'B': '8',
    'A': '4',
    'E': '8',
    'T': '7',
    'Y': '7',
    'L': '1',
    'U': '0',
    'D': '0',
    'R': '2',
    'P': '0',
    'F': '0',
    'J': '1',
    'K': '1',
    'V': '0',
    'W': '0',
    'X': '0',
    'N': '0',
    'M': '0',
    'H': '0',
    'C': '0',
    'Ç': '0',
    'Á': '0',
    'Â': '0',
    'Ã': '0',
    'À': '0',
}


def exibir_resultado(imagem, imagem_processada, imagem_recortada, imagem_recortada_processada, placa_detectada):
    fig = plt.figure(figsize=(10, 6))

    # Coluna 1, Linha 1: imagem original
    ax1 = plt.subplot2grid((2, 2), (0, 0))
    ax1.imshow(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
    ax1.set_title("Imagem Original")

    # Coluna 2, Linha 1: imagem processada
    ax2_1 = plt.subplot2grid((2, 2), (0, 1))
    ax2_1.imshow(cv2.cvtColor(imagem_processada, cv2.COLOR_BGR2RGB))
    ax2_1.set_title(f"Imagem Processada")

    # Coluna 1, Linha 2: imagem recortada
    ax1_2 = plt.subplot2grid((2, 2), (1, 0))
    ax1_2.imshow(cv2.cvtColor(imagem_recortada, cv2.COLOR_BGR2RGB))
    ax1_2.set_title("Imagem Recortada")

    # Coluna 2, Linha 2: imagem recortada processada
    ax2_2 = plt.subplot2grid((2, 2), (1, 1))
    ax2_2.imshow(cv2.cvtColor(imagem_recortada_processada, cv2.COLOR_BGR2RGB))
    ax2_2.set_title(f"Recorte Processado")

    # Adicionar um texto com informações acima de tudo
    info_text = f"Placa Detectada\n{placa_detectada}"

    plt.tight_layout()

    plt.figtext(0.5, 0.7, info_text, fontsize=12, ha='center', va='center')
    plt.show()


def substituir_letras_por_numeros(ultimos_caracteres: str):
    todas_possibilidades = ['']

    for caractere in reversed(ultimos_caracteres):
        possibilidades = []

        try:
            for letra_numero in letras_numeros[caractere]:
                for possibilidade in todas_possibilidades:
                    possibilidades.append(letra_numero + possibilidade)
        except KeyError:
            for possibilidade in todas_possibilidades:
                possibilidades.append(caractere + possibilidade)

        todas_possibilidades = possibilidades

    return todas_possibilidades


def gerar_possibilidades_mercosul(value: str):
    def combinar_elementos(lista, prefixo=''):
        if not lista:
            return [prefixo]

        resultado = []
        elemento_atual = lista[0]
        for item in elemento_atual:
            novo_prefixo = prefixo + item
            resultado.extend(combinar_elementos(lista[1:], novo_prefixo))

        return resultado

    segurar_letra = []
    index = 0
    for caractere in value:
        if caractere in letras_numeros:
            segurar_letra.append((
                caractere, index
            ))
        index += 1

    todas_possibilidades = []
    for letra_travada, index_travado in segurar_letra:
        index = 0
        possibilidades = []
        for caractere in value:
            if(caractere != letra_travada or index != index_travado):
                # Se o caractere for uma letra que pode ser convertida
                if(caractere in letras_numeros):
                    valor_convertido = letras_numeros[caractere]
                    if isinstance(valor_convertido, list):
                        possibilidade_multipla = []
                        for letra_numero in valor_convertido:
                            possibilidade_multipla.append(
                                letra_numero)
                        possibilidades.append(possibilidade_multipla)
                    else:
                        possibilidades.append(valor_convertido)
                else:
                    possibilidades.append(caractere)
            else:
                possibilidades.append(caractere)

            index += 1
        todas_possibilidades.extend(combinar_elementos(possibilidades))
    return todas_possibilidades
