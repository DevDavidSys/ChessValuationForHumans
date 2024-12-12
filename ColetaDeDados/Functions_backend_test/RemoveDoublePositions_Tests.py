import os
from time import sleep

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def RemoveDoublePositions(input_file,output_file):
   #Fazer a verificação de arquivo e após adicionar o valor se possível
   positions = []
   if(os.path.exists(input_file)):     
        with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
            count_total_positions = 0
            count_repeated_positions = 0
            for line in f_in.readlines():
                count_total_positions = count_total_positions+1
                
                fen = line.split(" ")
                del fen[0:2]
                fen = " ".join(map(str,fen))
                if(fen not in positions):
                    f_out.write(fen)
                    positions.append(fen)
                    
                else:
                    count_repeated_positions = count_repeated_positions +1
                limpar_terminal()
                print(count_total_positions,count_repeated_positions)



            
                

input_file = r"ColetaDeDados\Base_de_Testes\Passo3\Pass_3_fen_positions.txt"
output_file = r"ColetaDeDados\Base_de_Testes\Passo4\Moins5.txt"


RemoveDoublePositions(input_file,output_file)
