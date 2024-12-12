import pygame
import chess
import chess.svg
import random
from io import BytesIO
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

# Função para carregar FENs de um arquivo
def load_fens_from_file(filename):
    """
    Carrega FENs de um arquivo e retorna como uma lista.
    
    :param filename: Caminho para o arquivo .txt com FENs
    :return: Lista de FENs
    """
    with open(filename, "r") as f:
        fens = [line.strip() for line in f if line.strip()]
    return fens

# Função para gerar a imagem da posição
def generate_chessboard_image(fen):
    """
    Gera uma imagem da posição de xadrez a partir de uma FEN.

    :param fen: FEN da posição
    :return: Imagem da posição no formato de bytes
    """
    board = chess.Board(fen)
    svg_data = chess.svg.board(board)

    # Converte o SVG para um gráfico usando svglib
    drawing = svg2rlg(BytesIO(svg_data.encode('utf-8')))

    # Converte o gráfico para PNG usando svglib (sem precisar de Cairo)
    png_data = BytesIO()
    renderPM.drawToFile(drawing, png_data, fmt="PNG")

    png_data.seek(0)  # Garante que o ponteiro do arquivo esteja no início

    return png_data

# Função principal para exibir a posição gráfica
def display_random_chessboard(fen_list):
    """
    Exibe uma posição aleatória de xadrez usando pygame.

    :param fen_list: Lista de FENs
    """
    pygame.init()

    # Configurações da janela
    window_width, window_height = 600, 600
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Posição de Xadrez Aleatória")

    clock = pygame.time.Clock()

    running = True
    current_fen = random.choice(fen_list)  # Seleciona uma FEN aleatória

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Pressione "Espaço" para mudar de posição
                    current_fen = random.choice(fen_list)

        # Gera a imagem da posição e exibe
        img_data = generate_chessboard_image(current_fen)
        chess_image = pygame.image.load(img_data)
        chess_image = pygame.transform.scale(chess_image, (window_width, window_height))

        # Desenha no ecrã
        screen.fill((255, 255, 255))
        screen.blit(chess_image, (0, 0))
        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

# Caminho para o arquivo de FENs
fen_file = "ColetaDeDados\Base_de_Testes\Passo4\Moins5.txt"  # Substitua pelo seu arquivo de entrada
fens = load_fens_from_file(fen_file)

# Exibir posições aleatórias
display_random_chessboard(fens)

