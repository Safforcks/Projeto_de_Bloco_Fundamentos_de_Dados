from datetime import datetime

def data():

  """
  Retorna a data e hora atual.
  Exemplo: '2025-08-23 14:32'
  """

  return datetime.now().strftime("%Y-%m-%d %H:%M")

# Adicionar tarefa

def adicionar_tarefa(listas):

  """
  Parâmetros: 
  - listas (list): estrutura principal de dados. Cada item é uma lista no formato mínimo ["casa X", "Nome", "concluído?" opcional, "criado: AAAA-MM-DD HH:MM" opcional].

  Comportamento:
  - Se o número da casa já existir, atualiza o morador.
  - Se a casa não existir, cria um novo item.
  - Registra discretamente a data de criação como um metadado de string ("criado: ..."), sem mudar o formato principal que você já vinha usando.
  - Retorna a própria lista
  """
  
  casa = int(input("\nQual é o número de casa: "))
  morador = input("Qual é o nome do morador(a): ")

  if 1 <= casa <= len(listas):
    numero = listas[casa - 1]

    if len(numero) >= 1:
      
      # adiciona metadado leve se ainda não existir
      metadado = False
      for x in numero:
          if isinstance(x, str) and x.startswith("criado: "):
              metadado = True
              break
      if not metadado:
          numero.append(f"criado: {data()}")
      else:
          numero[1] = morador
  else:
      # novo registro já com metadado simples
      listas.append([f"casa {casa}", morador, f"criado: {data()}"])
  return listas

# Listar tarefas

def listar_tarefas(listas):

  """
  listas (list): estrutura com as tarefas
  - Lista todas as tarefas para saber se o pagamento foi realizado ou não. 
  - Pode ajudar a saber quantidade de tarefas listadas para testes/validação
  """

  print("")
  for numero in range(len(listas)):

    if "concluído" in listas[numero]:
      print(f"{numero + 1}. Pagamento realizado:     {listas[numero]}")

    else:
       print(f"{numero + 1}. Pagamento não realizado: {listas[numero]}")

# Marcar tarefa como concluída
def marcar_tarefa(listas):

  """
  listas (list): estrutura com as tarefas
  - Marca uma tarefa específica como concluída.
  - Usuário informa o índice da lista a ser concluída.
  - Se ainda não tiver "concluído", adiciona.
  - bool: True se marcou como concluída, False caso contrário.
  """
  
  marca = int(input("Qual é o número da lista você marca para concluir que já pagou? "))

  if 1 <= marca <= len(listas):
    numero = listas[marca - 1]

    if len(numero) == 1:
      print("\nNão pode marcar, porque essa casa não tem morador cadastrado!")
      return False
    
    elif "concluído" in numero:
      print("\nJá foi concluído ")
      return False

    else:
      numero.insert(2, "concluído")
      return False
  
  else:
     print("\nÍndice inválido")
     return False

# Remover tarefa

def remover_tarefa(listas):

  """
  listas (list): estrutura com as tarefas
  - Remove o 'morador' (o nome) ou o marcador 'concluído' de uma tarefa.
  - Pergunta ao usuário o que deseja remover: 'morador' ou 'concluído', depois o número da tarefa.
  - Se for 'morador', remove o elemento de índice 1 (se existir).
  - Se for 'concluído', remove a ocorrência da string 'concluído' (se existir).
  - bool: True se algo foi removido, False caso contrário.
  """

  pergunta = input("\nO que você gostaria de remover? Digite apenas 'morador' ou 'concluído': ").lower().strip()
  remove = int(input(f"Que número da lista selecione para remover '{pergunta}'? "))

  if 1 <= remove <= len(listas):
    numero = listas[remove - 1]

    if pergunta in numero:
      numero.remove(pergunta)
      return True

    elif pergunta == "morador":
      if len(numero) >= 2: 
        # remove o nome do morador (posição 1)
        numero.pop(1)
        # remove "concluído" depois do nome removido so se tiver 
        if "concluído" in numero:
          numero.remove("concluído")
          return True
        
        return True

    else:
      print(f"\nNão há nenhum item '{pergunta}' no {remove}ª tarefa.")
      return False

  else:
    print(f"Não existe o número {remove}")
    return False     