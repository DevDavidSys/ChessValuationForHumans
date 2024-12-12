import chess.pgn
import datetime
import os
from tqdm import tqdm  # Corrigido o erro de digitação

def validate_game(game):
    """Valida a partida verificando movimentos e cabeçalhos"""
    if not game.headers.get("White") or not game.headers.get("Black"):
        return False  # Cabeçalhos ausentes, inválido
    
    board = chess.Board()
    for move in game.mainline_moves():
        if move not in board.legal_moves:
            return False  # Movimento inválido
        board.push(move)
    
    return True  # Partida válida

def total_games_in_pgn(input_file):
    """Conta o número total de jogos em um arquivo PGN"""
    count = 0
    with open(input_file, "r") as f_in:
        while True:
            game = chess.pgn.read_game(f_in)
            if game is None:
                break
            count += 1
    return count

def process_pgn_file(input_file, output_dir):
    """Processa o arquivo PGN, validando e escrevendo no arquivo correspondente"""
    
    # Verifique se o diretório de saída existe. Se não, crie-o.
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Gerar os caminhos completos para os arquivos de jogos válidos e inválidos
    valid_file = os.path.join(output_dir, "Valid_Games_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pgn")
    invalid_file = os.path.join(output_dir, "Invalid_Games_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pgn")
    
    total_games = total_games_in_pgn(input_file)  # Contar total de jogos para a barra de progresso

    with open(input_file, "r") as f_in, open(valid_file, "w") as f_valid, open(invalid_file, "w") as f_invalid:
        first_valid = True
        first_invalid = True

        with tqdm(total=total_games, desc="Processando jogos", unit="jogo") as pbar:
            while True:
                game = chess.pgn.read_game(f_in)
                if game is None:  # Fim do arquivo
                    break

                if validate_game(game):
                    if first_valid:
                        first_valid = False
                    else:
                        f_valid.write("\n")

                    game.accept(chess.pgn.FileExporter(f_valid))
                else:
                    if first_invalid:
                        first_invalid = False
                    else:
                        f_invalid.write("\n")

                    game.accept(chess.pgn.FileExporter(f_invalid))

                del game
                pbar.update(1)

    print(f"Jogos válidos salvos em: {valid_file}")
    print(f"Jogos inválidos salvos em: {invalid_file}")

    # Retornar o caminho absoluto do arquivo válido
    return os.path.abspath(valid_file)  # Retorna o caminho completo do arquivo válido

# Caminho para o arquivo PGN de entrada
input_file = r"C:\Users\IceCube\Documents\Projects\ChessValuationForHumans\ChessValuationForHumans\ColetaDeDados\Base_de_Testes\InicialAnalyses.pgn"

# Caminho para a pasta onde os arquivos de saída serão salvos
output_dir = r"C:\Users\IceCube\Documents\Projects\ChessValuationForHumans\ChessValuationForHumans\ColetaDeDados\Base_de_Testes\Passo1"

# Processar os jogos e obter o caminho do arquivo válido
valid_file_path = process_pgn_file(input_file, output_dir)

# Exiba o caminho do arquivo válido gerado
print(f"Arquivo válido salvo em: {valid_file_path}")
