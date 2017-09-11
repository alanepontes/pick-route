### Navegação nesta página:

1. [Aplicação](#aplicacao)
1. [Pré requisitos e startup](#pre-requisitos-e-startup)
1. [API](#api)

### Aplicação: 

* Pick-route é um exemplo simples para se encontrar o menor caminho e custo dentro de uma malha logística. 
* Uma malha logística baseia-se em um conjunto de de pontos de origem e destinos separados por uma determinada distância. Para se encontrar o menor caminho e custo, é necessário que seja informado a rota, ou seja, origin e destino, o nome da malha na qual a rota está inserida, autonomia do veiculo que fará a rota e o preço por litro de combustível. 
* Exemplo de malha:
  * A primeira linha na malha, refere-se a seu nome.  
  * SP
    A B 10
    B D 15
    A C 20
    C D 30
    B E 50
    D E 30
* Exemplo de busca dentro de uma malha:
  * name = SP, source = A, target = D, autonomy = 10, price_per_litre = 2.50
  * Teríamos como resultado, então: A B D, com custo de 6.25

### Pré requisitos e startup: 

* É necessário ter as seguintes dependências instaladas: 
  * Python
  * MySQL

* Ademais, é necessário rodar o seguinte comando, dentro do folder do projeto:
```
$ pip install -r requirements/development.txt
``` 
* Para subir o servidor e iniciar a aplicação:
```
$ python app.py
``` 

### API:

* Rotas:
    * /logistics-routes (GET)
        * Retorna uma lista de logistics routes    
    * /logistics-routes/<IDENTIFIER> (GET)
        * Retorna um logistic route
    * /logistics-routes/IDENTIFIER (DELETE)
        * Deleta uma logistic route 
    * /shortests-routes
        * Parâmetros: 
            * name (nome da malha)
            * source
            * target
            * autonomy
            * price_per_litre
        * Retorna o caminho mais curto entre origem e destino e o menor custo.
* Identifier pode ser o nome da malha ou id.
* Exemplos das requisições feitas com POSTMAN podem ser encontradas no folder /docs. 



