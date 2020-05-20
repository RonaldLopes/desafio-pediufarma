# Desafio Pediu Farma
Este é um readme explicativo do desafio e do processo de solução. O banco de dados se encontra aqui https://pediufarma.com.br/banco.zip 
## Tarefa 1
Obter as informações abaixo a partir do arquivo sysfar.sql:
- Preço do produto;
- Código de barras do produto (EAN); 
- Quantidade em estoque;

OBS: Existem 2 preços o preço cheio(PMC), e o preço de promoção, quando houver promoção ela se sobrepõem ao preço cheio.

OBS: O preço da promoão só vale se estiver dentro da validade.

Primeiramente, a extensão .sql remete ao processo conhecido como dump (despejo) de banco de dados que geralmente contém um registro da estrutura de tabela e ou dados de um banco de dados na forma de uma lista de declarações SQL. Um dump de banco de dados é muito usado para realização de cópia de segurança de um banco.

A partir desta informação junto a uma breve analise do conteúdo do arquivo sysfar.sql, podemos rapidamente confirmar a hipótese e partir para o processo de restauração desse banco para análise dos dados. Para restaurar o banco, primeiro criamos uma database vazia de nome 'desafio' onde irá armazenar uma cópia do banco a ser analizado. Utilizei a linha abaixo para efetuar a restauração:

>  mysql -u USER -pSENHA desafio < sysfar.sql 

O passo seguinte foi analisar as tabelas, dentre as tabelas analisadas, a tabela estoque foi identificada como 'estoque' contendo os parâmetros necessários. A seguinte relação foi estabelecida entre os campos da tabela para a obtenção dos dados necessários:

- validade - foi considerado como valor referente a validade da promoção;
- pmc - foi considerado como valor referente ao preço cheio (PMC);
- barra - foi considerado como valor referente ao código de barras do produto (EAN);
- quantidade - foi considerado como valor referente a quantidade em estoque;

Para obter o preço do produto foi observado os requisitos previamente apresentados, estes foram filtrados por meio de query sql, a seguir o trecho responsável pelo filtro:

>SELECT descricao, CASE \
WHEN validade is null THEN pmc \
WHEN promocao is null THEN pmc \
WHEN validade > curdate() THEN promocao \
WHEN validade = curdate() THEN promocao \
WHEN validade < curdate() THEN IF(pmc is null, promocao, pmc) \
END AS preco_final, promocao, pmc, validade, barra,quantidade FROM desafio.estoque where quantidade>0 and pmc is not null; 

Primeiro é realizado uma verificação se o campo de validade da promoção foi definido, caso esteja nulo admite-se que não existe promoção definida e o valor referente ao PMC é retornado. 

>  WHEN validade is null THEN pmc

Em seguinda é realizado a verificação da existência de promoção, caso nulo admite-se que não possui promoção e o valor referente ao PMC é retornado.

> WHEN promocao is null THEN pmc

As duas próximas linhas referem-se a verificação se a promoção está válida ou não, uma verificação entre o campo validade e a data atual(curdate()), caso esteja dentro do prazo o valor de promoção é retornado como o preço do produto.

> WHEN validade > curdate() THEN promocao \
> WHEN validade = curdate() THEN promocao 

A ultima linha trata a situação em que a promoção venceu e não está mais válida, retornando o valor de pmc.

> WHEN validade < curdate() THEN IF(pmc is null, promocao, pmc) 


O restante da query seleciona a tabela e filtra para pegar os casos em que a quantidade em estoque é maior do que 0 e o valor de pmc não é nulo.

> .... FROM desafio.estoque where quantidade>0 and pmc is not null; 


## Tarefa 2
A tarefa 2 consistia em escrever um script na linguagem que se sentir mais confortável que gere uma lista json com as informações da tarefa 1.

OBS: 
> Formato de exemplo - [
                                { "ean":789000000, "preco":1.99,"estoque":38},
                                { "ean":789000001, "preco":3.99,"estoque":18},
                                ...
                                ]

Para isso foi definido um método denominado de converte_para_lista_json() que recebe o retorno do método busca_estoque() pertencente a classe DatabaseController e que contem o resultado da aplicação da query já detalhada acima. 

Este método possui como retorno uma lista json conforme o solicitado e que salva em um arquivo de nome desafio.json.



OBS: Para mais detalhes favor consultar o código fonte.



## Executando o código

Para executar o código é necessário instalar as dependências por meio do arquivo requirements.txt . Para isso, em um ambiente virtual (virtualenv), execute a linha abaixo:

> pip install -r requirements.txt

Em seguida execute: 
> python main.py

OBS: Lembrando que o banco presente no arquivo sysfar.sql precisa ser restaurado, procedimento o qual já foi explicado acima, para o mysql antes de executar este script.