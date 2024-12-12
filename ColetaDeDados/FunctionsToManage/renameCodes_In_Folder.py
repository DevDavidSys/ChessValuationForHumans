import os

def rename_python_files_in_directory(directory):
    """
    Renomeia todos os arquivos .py em um diretório, adicionando "_Tests" antes da extensão .py.
    
    :param directory: Caminho do diretório onde os arquivos .py estão localizados
    """
    # Listar todos os arquivos no diretório
    for filename in os.listdir(directory):
        # Verifica se o arquivo tem a extensão .py
        if filename.endswith(".py"):
            # Cria o novo nome do arquivo
            new_filename = filename.replace(".py", "_Tests.py")
            
            # Caminhos completos dos arquivos
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            
            # Renomeia o arquivo
            os.rename(old_file_path, new_file_path)
            print(f"Renomeado: {filename} -> {new_filename}")

# Defina o caminho para o diretório onde os arquivos .py estão localizados
directory_path = "ColetaDeDados\Functions_backend_test"  # Substitua com o caminho correto

# Chama a função para renomear os arquivos
rename_python_files_in_directory(directory_path)
