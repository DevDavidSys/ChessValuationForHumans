import chess.pgn
import datetime
from tqdm import tqdm

def classify_time_control(time_control):
    """Classifica o controle de tempo baseado apenas no tempo inicial"""
    try:
        time_control_int = int(time_control)

        if time_control_int <= 2:
            return "Bullet"
        elif 2 < time_control_int <= 5:
            return "Blitz"
        elif 5 < time_control_int < 30:
            return "Rapid"
        elif time_control_int >= 30:
            return "Classic"
        else:
            return "Unknown"
    except ValueError:
        return "Unknown"  # Erro ao analisar o campo TimeControl

def totalGamesInPgn(input_file):
    """Conta o número total de jogos em um arquivo PGN"""
    count = 0
    with open(input_file, "r") as f_in:
        while True:
            game = chess.pgn.read_game(f_in)
            if game is None:
                break
            count += 1
    return count


def classify_games(input_file, output_file):
    """Classifica os jogos no arquivo PGN baseado no tempo inicial"""
    totalGames = totalGamesInPgn(input_file)

    with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
        totalGames = totalGamesInPgn(input_file)
        with tqdm(total=totalGames, desc="Classificando jogos", unit=" jogo") as pbar:
            while True:
                game = chess.pgn.read_game(f_in)
                if game is None:  # Fim do arquivo
                    break

                # Obter o campo TimeControl e classificar
                time_control = game.headers.get("TimeControl", "").split("+")[0]
                increment_control = game.headers.get("TimeControl", "").split("+")[1] if len(game.headers.get("TimeControl", "")) > 1 else "N/A"
                game_type = classify_time_control(time_control)
                # Adicionar a classificação aos cabeçalhos
            
                game.headers["GameType"] = game_type
                game.headers["Increment"] = increment_control

                # Escrever o jogo classificado no arquivo de saída
                game.accept(chess.pgn.FileExporter(f_out))
                pbar.update(1)
                f_out.write("\n")  # Adicionar separação entre jogos
                

    print(f"Jogos classificados salvos em: {output_file}")


hour = datetime.datetime.now()
hour = str(hour).replace(" ","_").replace(":","-")
# Exemplo de uso

input_file = r"Pass1_InicialValid_games_2024-12-11_17-49-36.809872.pgn"  # Arquivo de jogos válidos
output_file = r"Pass2_Base_classified_games_"+hour+r".pgn"  # Arquivo com os jogos classificados

classify_games(input_file, output_file)