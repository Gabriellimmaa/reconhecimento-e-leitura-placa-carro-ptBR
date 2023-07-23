import os
import matplotlib.pyplot as plt
import cv2
import pytesseract
from matplotlib.widgets import Button

# Configurar o caminho do executável Tesseract (se necessário)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
# Configurar o caminho do executável Tesseract (se necessário)
# pytesseract.pytesseract.tesseract_cmd = 'caminho/para/o/tesseract'

def detectar_placa(imagem_path):
    # Carregar a imagem da placa do carro
    imagem_placa = cv2.imread(imagem_path)

    # Converter a imagem para tons de cinza
    imagem_cinza = cv2.cvtColor(imagem_placa, cv2.COLOR_BGR2GRAY)

    # Aplicar limiarização para tornar os caracteres mais destacados
    _, imagem_limiarizada = cv2.threshold(imagem_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Aplicar operação de fechamento para preencher regiões de contornos
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    imagem_processada = cv2.morphologyEx(imagem_limiarizada, cv2.MORPH_CLOSE, kernel)

    # mostrar os contornos da imagem processada
    contornos, _ = cv2.findContours(imagem_processada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # melhorar a precisão dos contornos
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:5]
    
    # desenhar os contornos na imagem
    for contorno in contornos:
        perimetro = cv2.arcLength(contorno, True)
        approx = cv2.approxPolyDP(contorno, 0.02 * perimetro, True)
        area = cv2.contourArea(contorno)
        x, y, w, h = cv2.boundingRect(contorno)
        
        # verificar se a altura é maior que a largura
        if h > w:
            return
        
        # verificar se há uma proporcao onde a altura é menor que 25% da largura
        if h < (w * 0.25):
            return
        

        if len(approx) < 10:
            # baseando-se na altura e largura descartar 
            
            # exibir os contornos na imagem
            cv2.drawContours(imagem_placa, [approx], -1, (0, 255, 0), 2)

            # recortar a imagem da placa
            x, y, w, h = cv2.boundingRect(contorno)
            imagem_placa_recortada = imagem_placa[y:y + h, x:x + w]

            # converter a imagem da placa para tons de cinza
            imagem_placa_recortada_cinza = cv2.cvtColor(imagem_placa_recortada, cv2.COLOR_BGR2GRAY)

            # aplicar limiarização para tornar os caracteres mais destacados
            _, imagem_placa_recortada_limiarizada = cv2.threshold(imagem_placa_recortada_cinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # aplicar operação de fechamento para preencher regiões de contornos

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

            imagem_placa_recortada_processada = cv2.morphologyEx(imagem_placa_recortada_limiarizada, cv2.MORPH_CLOSE, kernel)

            # aplicar operação de abertura para remover ruídos

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

            imagem_placa_recortada_processada = cv2.morphologyEx(imagem_placa_recortada_processada, cv2.MORPH_OPEN, kernel)

            # aplicar operação de dilatação para aumentar a espessura dos caracteres

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

            imagem_placa_recortada_processada = cv2.dilate(imagem_placa_recortada_processada, kernel, iterations=1)

            # aplicar operação de erosão para reduzir a espessura dos caracteres

            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

            imagem_placa_recortada_processada = cv2.erode(imagem_placa_recortada_processada, kernel, iterations=1)

            # Usar o Tesseract para obter o texto da placa recortada
            placa_detectada = pytesseract.image_to_string(imagem_placa_recortada_processada, lang='por', config='--psm 6')

            # Limpar o resultado removendo caracteres indesejados (como espaços, quebras de linha, etc.)
            placa_detectada = ''.join(filter(str.isalnum, placa_detectada))

            # remover espaços em branco
            placa_detectada = placa_detectada.replace(" ", "")

            if(len(placa_detectada) == 7):
                 # Exibir a imagem_placa com os contornos e informações de texto
                fig = plt.figure(figsize=(12, 6))
                plt.subplots_adjust(bottom=0.2)  # Ajusta a posição do botão

                # Botão "Next"
                btn_next = Button(plt.axes([0.45, 0.05, 0.1, 0.075]), 'Next')
                

                ax1 = plt.subplot2grid((2, 2), (0, 0), rowspan=2)
                ax1.imshow(cv2.cvtColor(imagem_placa, cv2.COLOR_BGR2RGB))
                ax1.set_title("Imagem Original")
                
                # Coluna 2, Linha 1: primeira imagem recortada
                ax2_1 = plt.subplot2grid((2, 2), (0, 1))
                ax2_1.imshow(cv2.cvtColor(imagem_placa_recortada, cv2.COLOR_BGR2RGB))
                ax2_1.set_title(f"Recorte detectado")

                # Coluna 2, Linha 2: segunda imagem recortada (se houver)
                ax2_2 = plt.subplot2grid((2, 2), (1, 1))
                ax2_2.imshow(cv2.cvtColor(imagem_placa_recortada_processada, cv2.COLOR_BGR2RGB))
                ax2_2.set_title(f"Recorte pre-processado")

                # Adicionar um texto com informações acima de tudo
                info_text = f"Placa detectada: {placa_detectada}"

                plt.figtext(0.5, 0.95, info_text, fontsize=12, ha='center', va='center')
                plt.show()
                continue

            # verificar se a placa detectada tem de 7 a 50 caracteres
            if len(placa_detectada) >= 7 and len(placa_detectada) < 50:          
                # fazer uma funcao para remover os caracteres lowercase de uma string
                placa_detectada_sem_minusculas = ''.join([i for i in placa_detectada if not i.islower()])

                if(len(placa_detectada_sem_minusculas) == 7):
                    placa_detectada = placa_detectada_sem_minusculas
                    ax1 = plt.subplot2grid((2, 2), (0, 0), rowspan=2)
                    ax1.imshow(cv2.cvtColor(imagem_placa, cv2.COLOR_BGR2RGB))
                    ax1.set_title("Imagem Original")
                    
                    # Coluna 2, Linha 1: primeira imagem recortada
                    ax2_1 = plt.subplot2grid((2, 2), (0, 1))
                    ax2_1.imshow(cv2.cvtColor(imagem_placa_recortada, cv2.COLOR_BGR2RGB))
                    ax2_1.set_title(f"Recorte detectado")

                    # Coluna 2, Linha 2: segunda imagem recortada (se houver)
                    ax2_2 = plt.subplot2grid((2, 2), (1, 1))
                    ax2_2.imshow(cv2.cvtColor(imagem_placa_recortada_processada, cv2.COLOR_BGR2RGB))
                    ax2_2.set_title(f"Recorte pre-processado")

                    # Adicionar um texto com informações acima de tudo
                    info_text = f"Placa detectada: {placa_detectada}"

                    plt.figtext(0.5, 0.95, info_text, fontsize=12, ha='center', va='center')
                    plt.show()
                    continue

if __name__ == "__main__":
    pasta_imagens = "images"  # Substitua "images" pelo caminho da pasta que contém as imagens
    lista_imagens = os.listdir(pasta_imagens)

    for imagem_file in lista_imagens:
        if imagem_file.lower().endswith(('.jpg', '.jpeg', '.png')):
            imagem_path = os.path.join(pasta_imagens, imagem_file)
            detectar_placa(imagem_path)
            print(f"Imagem: {imagem_file}")