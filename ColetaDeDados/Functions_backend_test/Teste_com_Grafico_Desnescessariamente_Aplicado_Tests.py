import chess.pgn
import datetime
import time
import matplotlib.pyplot as plt
from tqdm import tqdm  # Corrigido o erro de digitação

def validate_game(game):
    """Valida a partida verificando movimentos e cabeçalhos"""
    # Verificação dos cabeçalhos (opcional)
    if not game.headers.get("White") or not game.headers.get("Black"):
        return False  # Cabeçalhos ausentes, inválido

    # Validar movimentos
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

def process_pgn_file(input_file, valid_file, invalid_file):
    """Processa o arquivo PGN, validando e escrevendo no arquivo correspondente"""
    total_games = total_games_in_pgn(input_file)  # Contar total de jogos para a barra de progresso

    analyzed_games = []
    times = []
    start_time = time.time()

    with open(input_file, "r") as f_in, open(valid_file, "w") as f_valid, open(invalid_file, "w") as f_invalid:
        # Inicializar variáveis para escrever cabeçalhos (caso necessário)
        first_valid = True
        first_invalid = True

        with tqdm(total=total_games, desc="Processando jogos", unit="jogo") as pbar:
            game_count = 0
            while True:
                game = chess.pgn.read_game(f_in)
                if game is None:  # Fim do arquivo
                    break

                # Validação do jogo
                if validate_game(game):
                    # Escrever no arquivo de jogos válidos
                    if first_valid:
                        first_valid = False  # Ignorar o primeiro cabeçalho que já está presente no arquivo
                    else:
                        f_valid.write("\n")  # Adicionar uma linha em branco entre jogos

                    game.accept(chess.pgn.FileExporter(f_valid))
                else:
                    # Escrever no arquivo de jogos inválidos
                    if first_invalid:
                        first_invalid = False
                    else:
                        f_invalid.write("\n")

                    game.accept(chess.pgn.FileExporter(f_invalid))

                # Liberar memória após processar o jogo
                del game

                # Atualizar barra de progresso
                pbar.update(1)

                # Atualizar dados para o gráfico
                game_count += 1
                current_time = time.time() - start_time
                analyzed_games.append(game_count)
                times.append(current_time)

    # Exibir o gráfico no terminal
    plt.figure()
    plt.plot(times, analyzed_games, label="Jogos Analisados")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Jogos Analisados")
    plt.title("Progresso da Análise de Jogos")
    plt.legend()
    plt.grid()
    plt.show()

    print(f"Jogos válidos salvos em: {valid_file}")
    print(f"Jogos inválidos salvos em: {invalid_file}")

# Exemplos de uso:
inicial_time = datetime.datetime.now()
hour = datetime.datetime.now()
hour = str(hour).replace(" ", "_").replace(":", "-")
input_file = "ColetaDeDados\lichess_db_standard_rated_2014-09.pgn"  # Arquivo PGN de entrada
valid_file = "Pass1_valid_games_" + hour + ".pgn"  # Arquivo de jogos válidos
invalid_file = "Pass1_invalid_games_" + hour + ".pgn"  # Arquivo de jogos inválidos

process_pgn_file(input_file, valid_file, invalid_file)
