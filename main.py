'''
    Desafio Pediu Farma
    Nome: Ronald Lopes
'''
from db_controller import DatabaseController
import json

def converte_para_lista_json(dados_banco):
    lista = []

    for dado in dados_banco:
        lista.append({'preco':dado[0],'ean':dado[1],'estoque':dado[2]})

    return json.dumps(lista)

usuario_mysql = ''
senha_mysql = ''

banco_de_dados = DatabaseController(user=usuario_mysql,password=senha_mysql,database='desafio')

'''
    Tarefa 1 retornar:
        - Preço do produto;
        - Código de barras do produto (EAN);
        - Quantidade em estoque; 
    OBS: Existem 2 preços o preço cheio(PMC), e o preço de promoção, quando houver promoção ela se sobrepõem ao preço cheio.
    OBS: O preço da promoão só vale se estiver dentro da validade.
    
    Solução: Utilizei uma query que já realiza esse filtro na tabela estoque. O método busca_estoque() da classe DatabaseController é responsável por este procedimento.

'''

dados_filtrados = banco_de_dados.busca_estoque()


'''
    Tarefa 2: escrever um script na linguagem que se sentir mais confortável que gere uma lista json com as informações da tarefa 1.
    OBS: Formato de exemplo - [
                                { "ean":789000000, "preco":1.99,"estoque":38},
                                { "ean":789000001, "preco":3.99,"estoque":18},
                                ...
                                ]
    Solução: O método converte_para_lista_json() existente nesse arquivo é responsável por esta operação.
'''

json = converte_para_lista_json(dados_banco=dados_filtrados)

print(json)