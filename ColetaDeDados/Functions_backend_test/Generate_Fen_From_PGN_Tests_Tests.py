import chess.pgn
from tqdm import tqdm
import time

def count_games_in_pgn(input_file):
    """
    Conta o número total de jogos em um arquivo PGN.

    :param input_file: Caminho para o arquivo PGN
    :return: Número total de jogos
    """
    count = 0
    with open(input_file, "r") as f_in:
        while True:
            game = chess.pgn.read_game(f_in)
            if game is None:
                break
            count += 1
            if count % 100 == 0:  # Atualiza a cada 100 jogos encontrados
                print(f"Quantidade de jogos encontrados: {count}", end="\r")
    print(f"Quantidade de jogos encontrados: {count}")  # Exibe a contagem final
    return count

def generate_fens_from_pgn_file(input_file, output_file):
    """
    Lê um arquivo com múltiplos jogos PGN, gera FENs para cada movimento, e escreve os resultados em um arquivo.

    :param input_file: Caminho para o arquivo PGN de entrada
    :param output_file: Caminho para o arquivo de saída
    """
    print("Contando jogos no arquivo...")
    total_games = count_games_in_pgn(input_file)

    with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
        game_number = 1

        with tqdm(total=total_games, desc="Processando jogos", unit="jogo") as game_bar:
            while True:
                game = chess.pgn.read_game(f_in)
                if game is None:
                    break  # Fim do arquivo

                f_out.write(f"Game {game_number}\n")
                board = game.board()
                move_number = 1

                moves = list(game.mainline_moves())
                with tqdm(total=len(moves), desc=f"Gerando FENs para o Jogo {game_number}", unit="movimento", leave=False) as move_bar:
                    for move in moves:
                        board.push(move)
                        fen = board.fen()
                        f_out.write(f"Move {move_number}: {fen}\n")
                        move_number += 1
                        move_bar.update(1)

                f_out.write("\n")  # Separar jogos com uma linha em branco
                game_number += 1
                game_bar.update(1)

    print(f"Processamento concluído. As FENs foram salvas em: {output_file}")

# Caminhos de exemplo
input_file = r"Pass2_Base_classified_games_2024-12-11_17-51-03.149306.pgn"  # Substitua pelo caminho do seu arquivo de entrada
output_file = r"Pass_3_fen_positions.txt"  # Substitua pelo caminho do arquivo de saída

generate_fens_from_pgn_file(input_file, output_file)
