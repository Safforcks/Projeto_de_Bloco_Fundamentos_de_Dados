from codigos import *

def listas_criadas():
  listas = [
      ["casa 1" , "João", "concluído"],
      ["casa 2" , "Pedro"],
      ["casa 3" , "Maria"],
      ["casa 4" , "Pablo"],
      ["casa 5" , "Pietra"],
      ["casa 6" , "Henry"],
      ["casa 7" , "Rafaela"],
      ["casa 8"],
      ["casa 9"],
      ["casa 10"]
      ]
  return listas

listas = listas_criadas()

opcoes = 0
while True:
     opcoes = int(input(
        "\n-------------------------MENSALIDADE DO CONDOMÍNIO-------------------------"
      "\n-----------------------------------MENU-----------------------------------"
      "\nAperta o número 1: Adicionar morador ou casa"
      "\nAperta o número 2: Listar tarefas"
      "\nAperta o número 3: Marcar pagamento como concluído"
      "\nAperta o número 4: Remover 'morador' ou 'concluído'"
      "\nAperta o número 5: Sair"
      "\nAperta um desses números para selecionar uma opção: "
      ))
     
     if opcoes == 1:
          adicionar_tarefa(listas)      

     elif opcoes == 2:
          listar_tarefas(listas)

     elif opcoes == 3:
          marcar_tarefa(listas)
    
     elif opcoes == 4:
          remover_tarefa(listas)

     elif opcoes == 5:
          print("Encerramos")
          break
        
     else:
          print("Erro! Apenas digite um número de 1 a 5.")
