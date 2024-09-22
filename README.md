# Micro-Livraria: Exemplo Prático de Microsserviços

Este repositório contem um exemplo simples de uma livraria virtual construída usando uma **arquitetura de microsserviços**.

O exemplo foi projetado para ser usado em uma **aula prática sobre microsserviços**, que pode, por exemplo, ser realizada após o estudo do [Capítulo 7](https://engsoftmoderna.info/cap7.html) do livro [Engenharia de Software Moderna](https://engsoftmoderna.info).

O objetivo da aula é permitir que o aluno tenha um primeiro contato com microsserviços e com tecnologias normalmente usadas nesse tipo de arquitetura, tais como **Django**, **REST** e **Docker**.

Como nosso objetivo é didático, na livraria virtual estão à venda apenas três livros, conforme pode ser visto na próxima figura, que mostra a interface Web do sistema. Além disso, a operação de compra apenas simula a ação do usuário, não efetuando mudanças no estoque. Assim, os clientes da livraria podem realizar apenas duas operações: (1) listar os produtos à venda; (2) calcular o frete de envio.

<p align="center">
    <img width="70%" src="https://user-images.githubusercontent.com/7620947/108773349-f68f3500-753c-11eb-8c4f-434ca9a9deec.png" />
</p>

No restante deste documento vamos:

-   Descrever o sistema, com foco na sua arquitetura.
-   Apresentar instruções para sua execução local, usando o código disponibilizado no repositório.
-   Descrever duas tarefas práticas para serem realizadas pelos alunos, as quais envolvem:
    -   Tarefa Prática #1: Implementação de uma nova operação em um dos microsserviços
    -   Tarefa Prática #2: Criação de containers Docker para facilitar a execução dos microsserviços.

## Arquitetura

A micro-livraria possui três microsserviços:

-   Front-end: microsserviço responsável pela interface com usuário, conforme mostrado na figura anterior.
-   Shipping: microserviço para cálculo de frete.
-   Inventory: microserviço para controle do estoque da livraria.

Os microsserviços estão implementados em **Python** e **javaScript**, usando o Django REST Framework (DRF), em python para execução dos serviços no back-end e JavaScript, Css e Html para execucao do Front-end.

No entanto, **você conseguirá completar as tarefas práticas mesmo se nunca programou em Python e/ou JavaScript**. O motivo é que o nosso roteiro já inclui os trechos de código que devem ser copiados para o sistema.

Para facilitar a execução e entendimento do sistema, também não usamos bancos de dados ou serviços externos.

## Protocolos de Comunicação

Nessa adaptação, a comunicação entre o front-end e o back-end é baseada em uma **API REST**, que é uma abordagem comum em sistemas web. 

O protocolo utilizado para essa comunicação é HTTP/HTTPS, garantindo uma troca de informações eficiente e segura.

Optamos por usar HTTP/HTTPS no back-end para a comunicação entre os serviços, pois, além de ser amplamente suportado, é uma solução consolidada e simples para o desenvolvimento de APIs REST. A comunicação entre os microsserviços acontece por meio de chamadas HTTP, em que as requisições são feitas com métodos como `GET`, `POST`, `PUT` e `DELETE`, e os dados são geralmente trocados no formato JSON.

<p align="center">
    <img width="70%" src="https://github.com/user-attachments/assets/63b44b80-8fa1-4e57-b32f-487c2d06f4df" />
</p>

A escolha por HTTP/HTTPS para a implementação da API REST se deu pela simplicidade e facilidade de integração entre os microsserviços, mantendo a eficiência na comunicação e a compatibilidade com diversas ferramentas e plataformas. Embora gRPC ofereça benefícios como maior desempenho em alguns cenários, o uso de HTTP/HTTPS é mais que suficiente para as necessidades da nossa aplicação.

## Executando o Sistema

A seguir vamos descrever a sequência de passos para você executar o sistema localmente em sua máquina. Ou seja, todos os microsserviços estarão rodando na sua máquina.

**IMPORTANTE:** Você deve seguir esses passos antes de implementar as tarefas práticas descritas nas próximas seções.

1. Faça um fork do repositório. Para isso, basta clicar no botão **Fork** no canto superior direito desta página.

2. Vá para o terminal do seu sistema operacional e clone o projeto (lembre-se de incluir o seu usuário GitHub na URL antes de executar)

    ```bash
    git clone https://github.com/<SEU_USUÁRIO>/micro-livraria.git
    ```

3. É também necessário ter o `Python` e o `pip` instalado na sua máquina. Se você não tem, siga as instruções para instalação contidas nessa [página](https://www.python.org/downloads/) para instalar o python e nessa  [página](https://pip.pypa.io/en/stable/installation/) para instalar o pip, que eh um gerenciador de pacotes python.

4. Em um terminal, vá para o diretório no qual o projeto foi clonado e instale as dependências necessárias para execução dos microsserviços:

    ```bash
    cd micro-livraria
    python -m venv venv
    source ven/bin/activate
    pip install -r requirements
    ```

5. Inicie os microsserviços através dos comandos abaixo:

    * Rodando o microserviço de shipping
        ```bash
        nohup python services/shipping_service/manage.py runserver &> iventory.log &
        ```

    * Rodando o microserviço de inventory
        ```bash
        nohup python services/inventory_service/manage.py runserver 8001 &> service.log &
        ```

    * Rodando o microserviço do frontend
        ```bash
        nohup python -m http.server 5000 --directory services/frontend &> frontend.log &
        ```

6.  Para fins de teste, efetue uma requisição para o microsserviço reponsável pela API do backend.

-   Se tiver o `curl` instalado na sua máquina, basta usar:

    ```bash
    curl -i -X GET http://localhost:80001/api/products
    ```

-   Caso contrário, você pode fazer uma requisição acessando, no seu navegador, a seguinte URL: `http://localhost:8001/api/products`.

7. Teste agora o sistema como um todo, abrindo o front-end em um navegador: http://localhost:5000. Faça então um teste das principais funcionalidades da livraria.

## Tarefa Prática #1: Implementando uma Nova Operação

Nesta primeira tarefa, você irá implementar uma nova operação no serviço `Inventory`.  A operação que vamos implementar é chamada `search_product_by_id` e vai permitir que um cliente obtenha os detalhes de um produto específico, baseado no seu ID.

A tarefa está dividida em dois passos principais: definir a operação e configurá-la para ser acessível via uma nova rota.

#### Passo 1

Para começar, você deve criar uma função que lidere a busca de um produto pelo seu ID no arquivo `views.py`. Vamos carregar os dados de um arquivo JSON, que nesse caso simula o nosso banco de dados,  e retornar o produto correspondente ao ID informado. Caso o produto não seja encontrado, retornaremos uma mensagem de erro.


1. Abra o arquivo `services/inventory_service/inventory/views.py`:

2. Adicione a seguinte função no arquivo, logo após a função já existente de `search_all_products`:

    ```python
    # Função para buscar um produto pelo ID
    @api_view(['GET'])
    def search_product_by_id(request, id):
        # Obter o diretório atual e encontrar o caminho para o arquivo products.json
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, '..', 'products.json')
    
        # Abrir o arquivo products.json e carregar os dados
        with open(file_path, 'r') as file:
            data = json.load(file)
    
        # Procurar o produto com o ID fornecido
        product = next((item for item in data if item["id"] == int(id)), None)
    
        # Se o produto for encontrado, retorná-lo
        if product:
            return Response(product)
    
        # Caso contrário, retornar uma mensagem de erro com status 404
        else:
            return Response({"error": "Product not found"}, status=404)
    ```
3. Explicando o código:
    * `@api_view(['GET']):` Esse decorador define que a função responderá a requisições HTTP GET.
    * `os.path.dirname(__file__)` e `os.path.join(...):` Estamos localizando o caminho correto do arquivo `products.json`.
    * `json.load(file):` Lê o conteúdo do arquivo JSON e converte para uma lista de dicionários.
    * `next((item for item in data if item["id"] == int(id)), None):` Este trecho percorre os itens do JSON e retorna o produto cujo id corresponde ao parâmetro fornecido. Se não encontrar, retorna `None`.
    * **Resposta HTTP**: Caso o produto seja encontrado, retornamos seus dados com `Response(product)`. Se não for encontrado, retornamos um erro `404` com uma mensagem `"Product not found".

#### Passo 2

Agora que a função `search_product_by_id` foi definida, precisamos garantir que ela seja acessível a partir de uma URL específica. Para isso, vamos adicionar uma rota no arquivo `urls.py` que vai mapear a URL solicitada para a função.

1. Abra o arquivo `services/inventory_service/inventory/urls.py`:

2. Adicione a seguinte rota para o novo endpoint:

    ```python
    from django.urls import path
    from .views import search_all_products, search_product_by_id

    # Definindo as URLs que mapeiam para as funções de visualização
    urlpatterns = [
        # Rota para buscar todos os produtos
        path('products/', search_all_products, name='search_all_products'),

        # Rota para buscar um produto específico pelo ID
        path('product/<int:id>/', search_product_by_id, name='search_product_by_id'),
    ]

    ```

3. Explicando o Código:
   * `path('products/', search_all_products):` Essa rota já existente mapeia a URL `products/` para a função que retorna todos os produtos.
   * `path('product/<int:id>/', search_product_by_id):` A nova rota define que ao acessar uma URL do tipo `/product/1/`, a função `search_product_by_id` será chamada, com o valor 1 sendo passado como o parâmetro id.
   *  Neste exemplo, `id` é um número inteiro, como especificado pelo `<int:id>` na URL. O Django automaticamente valida o tipo de dado e repassa esse valor para a função.

Finalize, efetuando uma chamada no novo endpoint da API: http://localhost:3000/product/1

Para ficar claro: até aqui, apenas implementamos a nova operação no backend. A sua incorporação no frontend ficará pendente, pois requer mudar a interface Web, para, por exemplo, incluir um botão "Pesquisar Livro".

**IMPORTANTE**: Se tudo funcionou corretamente, dê um **COMMIT & PUSH** (e certifique-se de que seu repositório no GitHub foi atualizado).

```bash
git add --all
git commit -m "Tarefa prática #1 - Microservices"
git push origin main
```

## Tarefa Prática #2: Criando um Container Docker

Nesta segunda tarefa, você irá criar um container Docker para o seu microserviço. Os containers são importantes para isolar e distribuir os microserviços em ambientes de produção. Em outras palavras, uma vez "copiado" para um container, um microsserviço pode ser executado em qualquer ambiente, seja ele sua máquina local, o servidor de sua universidade, ou um sistema de cloud (como Amazon AWS, Google Cloud, etc).

Como nosso primeiro objetivo é didático, iremos criar apenas uma imagem Docker para exemplificar o uso de containers.

Caso você não tenha o Docker instaldo em sua máquina, é preciso instalá-lo antes de iniciar a tarefa. Um passo-a-passo de instalação pode ser encontrado na [documentação oficial](https://docs.docker.com/get-docker/).

#### Passo 1



Crie um arquivo chamado `Dockerfile` dentro da raiz da pasta do micro servico `shipping_service` com o comando:

```bash
touch /services/shipping_service/Dockerfile
```

copie o `requirements.txt` para dentro do `shipping_service` com o comando `cp`:

```bash
cp requirements.txt /services/shipping_service/requirements.txt
```

Como ilustrado na próxima figura, o Dockerfile é utilizado para gerar uma imagem. A partir dessa imagem, você pode criar várias instâncias de uma aplicação. Com isso, conseguimos escalar o microsserviço de `Shipping` de forma horizontal.

<p align="center">
    <img width="70%" src="https://user-images.githubusercontent.com/7620947/108651385-67ccda80-74a0-11eb-9390-80df6ea6fd8c.png" />
</p>

No Dockerfile, você precisa incluir cinco instruções

-   `FROM`: tecnologia que será a base de criação da imagem.
-   `WORKDIR`: diretório da imagem na qual os comandos serão executados.
-   `COPY`: comando para copiar o código fonte para a imagem.
-   `RUN`: comando para instalação de dependências.
-   `EXPOSE`: comando para expor uma porta disponivel no ambiente.
-   `CMD`: comando para executar o seu código quando o container for criado.

Ou seja, nosso Dockerfile terá as seguintes linhas:

```Dockerfile
# Imagem base derivada do Python
FROM python:3.12

# Diretório de trabalho
WORKDIR /app

# Comando para copiar os arquivos para a pasta /app da imagem
COPY . /app

# Comando para instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

#Comando para expor uma porta disponivel no ambiente.
EXPOSE 8000

# Comando para inicializar (executar) a aplicação
CMD ["python", "manage.py", "runserver", "0.0.shiping"]
```

#### Passo 2

Agora nós vamos compilar o Dockerfile e criar a imagem. Para isto, execute o seguinte comando em um terminal do seu sistema operacional (esse comando precisa ser executado na raiz do projeto; ele pode também demorar um pouco mais para ser executado).

```
docker build -t micro-livraria/shipping -f services/shipping/Dockerfile ./
```

onde:

-   `docker build`: comando de compilação do Docker.
-   `-t micro-livraria/shipping`: tag de identificação da imagem criada.
-   `-f service/shipping_service/Dockerfile`: Caminho ate o dockerfile a ser compilado.

O `./` no final indica que estamos executando os comandos do Dockerfile tendo como referência a raiz do projeto.


#### Passo 3

Lembra de quando inciamos os micro servicos com o comando:
```bash
  nohup python services/shipping_service/manage.py runserver &> iventory.log &
```

Se executarmos o container que nos buildamos, ele tera conflito, pois teremos dois processos do computador tentando acessar a mesma porta. Para isso nao ocorrer, precisamos para o processo executando o comando:
```bash
  lsof -i 8000
```
Este comando retornara o processo que usa a porta 8000, tendo uma saida similar a essa:
```bash
COMMAND   PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python   12345   user   4u   IPv4 123456   0t0  TCP *:8000 (LISTEN)
```
O PID, eh o id do processo, usamos o comando `kill` para acabar com o processo:
```bash
  kill <PID>
```
nesse caso fictiocion, a resposta do comando retorunou o procesos python de PID (id do processo) igual a `1234`, o comando seria:
```bash
  kill 12345
```
Preste **MUITA** atencao ao usar o comando kill, caso voce coloque o PID errado, pode acabar matando processos bem importantes do seu sistema.


Por fim, para executar a imagem criada no passo anterior (ou seja, colocar de novo o microsserviço de `Shipping` no ar), basta usar o comando:

```
docker run -ti --name shipping -p 8000:8000 micro-livraria/shipping
```

onde:

-   `docker run`: comando de execução de uma imagem docker.
-   `-ti`: habilita a interação com o container via terminal.
-   `--name shipping`: define o nome do container criado.
-   `-p 8000:8000`: redireciona a porta 8000 do container para sua máquina.
-   `micro-livraria/shipping`: especifica qual a imagem deve-se executar.

Se tudo estiver correto, você irá receber a seguinte mensagem em seu terminal:
```
Shipping Service running
```
E o Controller pode acessar o serviço diretamente através do container Docker.

**Mas qual foi exatamente a vantagem de criar esse container?** Agora, você pode levá-lo para qualquer máquina ou sistema operacional e colocar o microsserviço para rodar sem instalar mais nada (incluindo bibliotecas, dependências externas, módulos de runtime, etc). Isso vai ocorrer com containers implementados em JavaScript, como no nosso exemplo, mas também com containers implementados em qualquer outra linguagem.

**IMPORTANTE**: Se tudo funcionou corretamente, dê um **COMMIT & PUSH** (e certifique-se de que seu repositório no GitHub foi atualizado).

```bash
git add --all
git commit -m "Tarefa prática #2 - Docker"
git push origin main
```

## Tarefa Pratica Extra

Nesta tarefa extra iremos implementar uma comunicacao entre container dockers, um docker compose, que é uma ferramenta para definir e gerenciar múltiplos contêineres Docker em um único arquivo YAML, facilitando a configuração e o gerenciamento de aplicações que dependem de vários serviços. Você pode especificar a imagem, volumes, redes e variáveis de ambiente, permitindo iniciar todos os serviços com um único comando.



caso voce nao tenha o docker compose instalado na sua maquina, ele pode ser instalado atraves da [documentação oficial](https://docs.docker.com/compose/install/).

repita a `tarefa pratica dois` com o micro servico `inventory_service`:

Com base na logica usada, tente seguir o mesmo passo a passo implementando cada etapa, lembre de trocar os nomes.

Fique atento a utilizacao da porta de do micro servico `inventory_service`, em vez de utilizar a porta 8000, iremos utilizar a porta 8001.

no final do processo teremos um Dockerfile seguindo essa estrutura:

```Dockerfile
# Imagem base derivada do Python
FROM python:3.12

# Diretório de trabalho
WORKDIR /app

# Comando para copiar os arquivos para a pasta /app da imagem
COPY . /app

# Comando para instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

#Comando para expor uma porta disponivel no ambiente.
EXPOSE 8001

# Comando para inicializar (executar) a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
```

Para fazermos o Dockerfile do micro servico `frontend` usaremos comando diferentes, pois a maneira que rodamos o microservico usando um servidor nginx, uma solucao amplamente usada para subirmos aplicacoes web html, javascript e css.

```Dockerfile
# Use the official Nginx image as the base
FROM nginx:alpine

# Set the working directory to /usr/share/nginx/html
WORKDIR /usr/share/nginx/html

# Remove default nginx static files
RUN rm -rf ./*

# Copy your static website files into the container
COPY . .

# Expose port 80 to the outside world
EXPOSE 5000

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
```

Ao final teremos os 3 Dockerfiles, cada um na raiz do seu respectivo diretorio, para subirmos todos os containewr em conjunto usaremos o docker compose para isso criaremos o arquivo `docker-compose.yml` na raiz do projeto.

```bash
touch docker-compose.yml
```

No docker-compose.yml, você precisa incluir várias chaves e suas respectivas configurações:

services: define os serviços que compõem sua aplicação, permitindo agrupar diferentes componentes, como frontend e backend, em containers separados.  

- `build`: especifica como construir a imagem Docker para um serviço, contendo configurações para o contexto e o arquivo Dockerfile.  
- `context`: determina o diretório que contém o Dockerfile e os arquivos necessários para a construção da imagem, devendo ser relativo ao local do arquivo docker-compose.yml.  
- `dockerfile`: indica o nome do arquivo Dockerfile a ser utilizado na construção da imagem; por padrão, o Docker procura um arquivo chamado Dockerfile, mas você pode definir um nome diferente.  
- `ports`: mapeia as portas do host para as portas do container, permitindo acesso aos serviços, no formato <porta_host>:<porta_container>.  
- `command`: define o comando a ser executado quando o container é iniciado, personalizando o que acontece ao inicializar o serviço, como iniciar um servidor ou executar um script.  

Teremos um Dockerfile seguindo essa estrutura:  

```Dockerfile
version: '3.8'  # Define a versão do Docker Compose a ser utilizada

services:  # Início da definição dos serviços

  inventory_service:  # Serviço de inventário
    build:  # Configurações para construir a imagem
      context: ./services/inventory_service  # Diretório onde está o Dockerfile
      dockerfile: Dockerfile  # Nome do arquivo Dockerfile
    ports:  # Configurações de portas
      - "8001:8001"  # Mapeia a porta 8001 do host para a porta 8001 do container
    command: python manage.py runserver 0.0.0.0:8001  # Comando para iniciar o serviço

  shipping_service:  # Serviço de envio
    build:  # Configurações para construir a imagem
      context: ./services/shipping_service  # Diretório onde está o Dockerfile
      dockerfile: Dockerfile  # Nome do arquivo Dockerfile
    ports:  # Configurações de portas
      - "8000:8000"  # Mapeia a porta 8000 do host para a porta 8000 do container
    command: python manage.py runserver 0.0.0.0:8000  # Comando para iniciar o serviço

  frontend:  # Serviço frontend
    build:  # Configurações para construir a imagem
      context: ./services/frontend  # Diretório onde está o Dockerfile
      dockerfile: Dockerfile  # Nome do arquivo Dockerfile
    ports:  # Configurações de portas
      - "5000:80"  # Mapeia a porta 5000 do host para a porta 80 do container
```

O projeto estara com essa estrutura:

micro-livraria
│  
├── docker-compose.yml
├── LICENSE
├── README.md
└── services
    ├── frontend
    │   ├── Dockerfile
    │   ├── img
    │   │   ├── design.png
    │   │   ├── esm.png
    │   │   └── refactoring.png
    │   ├── index.css
    │   ├── index.html
    │   └── index.js
    ├── inventory_service
    │   ├── Dockerfile
    │   ├── inventory
    │   │   ├── __init__.py
    │   │   ├── __pycache__
    │   │   │   ├── admin.cpython-312.pyc
    │   │   │   ├── apps.cpython-312.pyc
    │   │   │   ├── __init__.cpython-312.pyc
    │   │   │   ├── models.cpython-312.pyc
    │   │   │   ├── serializers.cpython-312.pyc
    │   │   │   ├── urls.cpython-312.pyc
    │   │   │   └── views.cpython-312.pyc
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   ├── inventory_service
    │   │   ├── __init__.py
    │   │   ├── settings.py
    │   │   └── urls.py
    │   ├── manage.py
    │   ├── products.json
    │   └── requirements.txt
    └── shipping_service
        ├── Dockerfile
        ├── manage.py
        ├── requirements.txt
        ├── shipping
        │   ├── __init__.py
        │   ├── __pycache__
        │   │   ├── admin.cpython-312.pyc
        │   │   ├── apps.cpython-312.pyc
        │   │   ├── __init__.cpython-312.pyc
        │   │   ├── models.cpython-312.pyc
        │   │   ├── urls.cpython-312.pyc
        │   │   └── views.cpython-312.pyc
        │   ├── tests.py
        │   ├── urls.py
        │   └── views.py
        └── shipping_service
            ├── __init__.py
            ├── __pycache__
            │   ├── __init__.cpython-312.pyc
            │   ├── settings.cpython-312.pyc
            │   ├── urls.cpython-312.pyc
            │   └── wsgi.cpython-312.pyc
            ├── settings.py
            └── urls.py

12 directories, 48 files

verifique se a estrura esta a mesma do seu projeto, o comando `tree` pode te ajudar nisso!  (para instalar rode o comando `sudo apt install tree` e depois rode `tree`)

Agora comite as novos mudancas feitas seguindo os comandos que voce ja conhece!

## Comentários Finais

Nesta aula, trabalhamos em uma aplicação baseada em microsserviços. Apesar de pequena, ela ilustra os princípios básicos de microsserviços, bem como algumas tecnologias importantes quando se implementa esse tipo de arquitetura.

No entanto, é importante ressaltar que em uma aplicação real existem outros componentes, como bancos de dados, balanceadores de carga e orquestradores.

A função de um **balanceador de carga** é dividir as requisições quando temos mais de uma instância do mesmo microsserviço. Imagine que o microsserviço de frete da loja virtual ficou sobrecarregado e, então, tivemos que colocar para rodar múltiplas instâncias do mesmo. Nesse caso, precisamos de um balanceador para dividir as requisições que chegam entre essas instâncias.

Já um **orquestrador** gerencia o ciclo de vida de containers. Por exemplo, se um servidor para de funcionar, ele automaticamente move os seus containers para um outro servidor. Se o número de acessos ao sistema aumenta bruscamente, um orquestrador também aumenta, em seguida, o número de containers. [Kubernetes](https://kubernetes.io/) é um dos orquestradores mais usados atualmente.

Se quiser estudar um segundo sistema de demonstração de microsserviços, sugerimos este [repositório](https://github.com/GoogleCloudPlatform/microservices-demo), mantido pelo serviço de nuvem do Google.

## Créditos

Este exercício prático, incluindo o seu código, foi elaborado por **Rodrigo Brito**, aluno de mestrado do DCC/UFMG, como parte das suas atividades na disciplina Estágio em Docência, cursada em 2020/2, sob orientação do **Prof. Marco Tulio Valente**.

O código deste repositório possui uma licença MIT. O roteiro descrito acima possui uma licença CC-BY.
