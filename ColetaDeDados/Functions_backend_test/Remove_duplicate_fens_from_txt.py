
from tqdm import tqdm  # Corrigido o erro de digitação

def remove_duplicate_fens(input_file, output_file):
    """
    Remove duplicatas de FENs em um arquivo e salva as FENs únicas em um novo arquivo.

    :param input_file: Caminho do arquivo com FENs a serem filtradas
    :param output_file: Caminho do arquivo para salvar as FENs únicas
    """
    seen_fens = set()

    with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
        with tqdm(desc="Filtrando FENs", unit="FEN") as fen_bar:
            for line in f_in:
                # Ignora linhas que não são FENs
                if line.startswith("Move") or line.strip() == "":
                    continue

                fen = line.strip()
                if fen not in seen_fens:
                    seen_fens.add(fen)
                    f_out.write(fen + "\n")
                fen_bar.update(1)

    print(f"Processamento concluído. As FENs únicas foram salvas em: {output_file}")
    
# Caminhos de exemplo
input_fen_file = r"Pass_3_fen_positions.txt"  # Arquivo com FENs geradas
output_unique_fen_file = r"Pass4_unique_fen_positions.txt"  # Arquivo para salvar FENs únicas

remove_duplicate_fens(input_fen_file, output_unique_fen_file)
