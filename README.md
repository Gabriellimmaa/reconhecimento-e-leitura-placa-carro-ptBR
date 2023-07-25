# Identificação de Placa de Carro com Python e Tesseract
Este repositório contém código em Python que realiza a identificação de placas de carro em imagens utilizando a biblioteca Tesseract OCR.

##### Clique aqui para ler o artigo https://github.com/Gabriellimmaa/reconhecimento-e-leitura-placa-carro-ptBR/blob/main/artigo/artigo.pdf



## Como funciona o código
O código está dividido em várias partes que compõem o processo de identificação da placa de carro:

1. **processar_imagem.py:** Este módulo contém a função `processar_imagem` que recebe uma imagem de placa de carro como entrada e aplica pré-processamento, convertendo-a para tons de cinza, aplicando filtros para remover ruídos e realizando limiarização adaptativa para destacar os caracteres da placa.
   
3. **processar_contornos.py:** Neste módulo, a função `processar_contornos` é responsável por identificar possíveis placas de carro na imagem processada. O algoritmo utiliza técnicas de detecção de contornos para identificar áreas que possam representar placas de carro com base em critérios como proporção altura/largura, área e formato retangular.
   
5. **aplicar_ocr.py:** Neste módulo, a função `aplicar_ocr` executa o OCR (Reconhecimento Óptico de Caracteres) utilizando a biblioteca Tesseract para extrair o texto da placa identificada. O código tenta primeiro reconhecer a placa em português e, caso não seja possível, tenta reconhecê-la em inglês. Além disso, o código também trata a possibilidade de placas do modelo antigo ou modelo Mercosul, aplicando técnicas específicas de processamento para esses casos.
   
7. **utils.py:** Este módulo contém funções utilitárias para exibir os resultados do processamento em uma imagem, destacando as regiões da placa e mostrando o texto detectado.
   
9. **main.py:** O arquivo principal main.py faz uso dos módulos anteriores e é responsável por identificar as placas de carros em uma lista de imagens presentes na pasta "images". O resultado do processamento é exibido para cada imagem processada, mostrando a imagem original, a imagem processada, a região da placa recortada, a região da placa após processamento e o texto da placa detectada.

## Configuração do Tesseract
Antes de executar o código, é necessário configurar o caminho do executável do Tesseract no arquivo `main.py`. Certifique-se de que você tem o Tesseract OCR instalado em seu sistema e, se necessário, ajuste o caminho para o executável na variável `pytesseract.pytesseract.tesseract_cmd`.

## Como usar o código
1. Clone este repositório em seu computador:
     
        git clone https://github.com/Gabriellimmaa/reconhecimento-e-leitura-placa-carro-ptBR.git
      
3. Certifique-se de ter todas as bibliotecas necessárias instaladas (OpenCV, pytesseract) e o Tesseract OCR configurado corretamente.
     
        pip install -r requirements.txt
      
5. Coloque as imagens de carros que você deseja analisar na pasta "images".
6. Execute o arquivo main.py:
     
        python main.py
      
O código processará as imagens presentes na pasta "images", identificará as placas de carros e exibirá os resultados para cada imagem processada.
## Observações
- O código está configurado para identificar placas de carro em imagens que estão localizadas na parte traseira dos veículos, simulando uma situação de parada em um pedágio.
- O pré-processamento das imagens e as técnicas de detecção de contornos podem variar de acordo com as condições das imagens e os cenários de uso. Portanto, é possível ajustar esses parâmetros conforme necessário para melhorar o desempenho do reconhecimento.
- O código pode ser expandido e adaptado para diferentes cenários de uso e para lidar com outros modelos de placas de carro, caso seja necessário.

Aviso: Este código foi desenvolvido para fins educacionais e de aprendizado, e pode não ser adequado para uso em ambientes de produção. O reconhecimento de placas de carro em cenários reais pode ser mais complexo do que demonstrado aqui, e o desempenho pode variar dependendo das condições das imagens e das configurações do Tesseract OCR.

## Contribuição
Contribuições e sugestões são bem-vindas! Se você tiver alguma melhoria ou correção para propor, sinta-se à vontade para enviar um pull request.

Esperamos que este projeto seja útil e ajude você a entender melhor o processo de identificação de placas de carro com Python e Tesseract!

## Autores
| [<img src="https://github.com/Gabriellimmaa.png" width=115><br><sub>Gabriel Lima</sub>](https://github.com/Gabriellimmaa) | [<img src="https://github.com/CarlosAAndrino.png" width=115><br><sub>Carlos Andrino</sub>](https://github.com/CarlosAAndrino) |
| :---: | :---: 
