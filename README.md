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

Os quatro microsserviços estão implementados em **Python**, usando o Django REST Framework (DRF) para execução dos serviços no back-end.

No entanto, **você conseguirá completar as tarefas práticas mesmo se nunca programou em Python**. O motivo é que o nosso roteiro já inclui os trechos de código que devem ser copiados para o sistema.

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
    git clone https://github.com/<SEU USUÁRIO>/micro-livraria.git
    ```

3. É também necessário ter o `Python` instalado na sua máquina. Se você não tem, siga as instruções para instalação contidas nessa [página](https://www.python.org/downloads/).

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

Nesta primeira tarefa, você irá implementar uma nova operação no serviço `Inventory`. Essa operação, chamada `SearchProductByID` vai pesquisar por um produto, dado o seu ID.

#### Passo 1

Primeiro, você deve declarar a assinatura da nova operação. Para isso, inclua a definição dessa assinatura no arquivo `services/inventory_service/inventory/views.py`:

```python
@api_view(['GET'])
def search_product_by_id(request, id):
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, '..', 'products.json')

    with open(file_path, 'r') as file:
        data = json.load(file)
    
    product = next((item for item in data if item["id"] == int(id)), None)
    if product:
        return Response(product)
    else:
        return Response({"error": "Product not found"}, status=404)
```

#### Passo 2

Inclua a nova rota no arquivo `services/inventory_service/inventory/urls.py`:

```python
from django.urls import path
from .views import search_all_products, search_product_by_id

urlpatterns = [
    path('products/', search_all_products, name='search_all_products'),
    path('product/<int:id>/', search_product_by_id, name='search_product_by_id'),
]
```

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

Crie um arquivo na raiz do projeto com o nome `shipping.Dockerfile`. Este arquivo armazenará as instruções para criação de uma imagem Docker para o serviço `Shipping`.

Como ilustrado na próxima figura, o Dockerfile é utilizado para gerar uma imagem. A partir dessa imagem, você pode criar várias instâncias de uma aplicação. Com isso, conseguimos escalar o microsserviço de `Shipping` de forma horizontal.

<p align="center">
    <img width="70%" src="https://user-images.githubusercontent.com/7620947/108651385-67ccda80-74a0-11eb-9390-80df6ea6fd8c.png" />
</p>

No Dockerfile, você precisa incluir cinco instruções

-   `FROM`: tecnologia que será a base de criação da imagem.
-   `WORKDIR`: diretório da imagem na qual os comandos serão executados.
-   `COPY`: comando para copiar o código fonte para a imagem.
-   `RUN`: comando para instalação de dependências.
-   `CMD`: comando para executar o seu código quando o container for criado.

Ou seja, nosso Dockerfile terá as seguintes linhas:

```Dockerfile
# Imagem base derivada do Node
FROM node

# Diretório de trabalho
WORKDIR /app

# Comando para copiar os arquivos para a pasta /app da imagem
COPY . /app

# Comando para instalar as dependências
RUN npm install

# Comando para inicializar (executar) a aplicação
CMD ["node", "/app/services/shipping/index.js"]
```

#### Passo 2

Agora nós vamos compilar o Dockerfile e criar a imagem. Para isto, execute o seguinte comando em um terminal do seu sistema operacional (esse comando precisa ser executado na raiz do projeto; ele pode também demorar um pouco mais para ser executado).

```
docker build -t micro-livraria/shipping -f shipping.Dockerfile ./
```

onde:

-   `docker build`: comando de compilação do Docker.
-   `-t micro-livraria/shipping`: tag de identificação da imagem criada.
-   `-f shipping.Dockerfile`: dockerfile a ser compilado.

O `./` no final indica que estamos executando os comandos do Dockerfile tendo como referência a raiz do projeto.

#### Passo 3

Antes de iniciar o serviço via container Docker, precisamos remover a inicialização do serviço de Shipping do comando `npm run start`. Para isso, basta remover o sub-comando `start-shipping` localizado na linha 7 do arquivo [package.json](https://github.com/aserg-ufmg/micro-livraria/blob/main/package.json), conforme mostrado no próximo diff (a linha com o símbolo "-" no início representa a linha original do arquivo; a linha com o símbolo "+" representa como essa linha deve ficar após a sua alteração):

```diff
diff --git a/package.json b/package.json
index 25ff65c..552a04e 100644
--- a/package.json
+++ b/package.json
@@ -4,7 +4,7 @@
     "description": "Toy example of microservice",
     "main": "",
     "scripts": {
-        "start": "run-p start-frontend start-controller start-shipping start-inventory",
+        "start": "run-p start-frontend start-controller start-inventory",
         "start-controller": "nodemon services/controller/index.js",
         "start-shipping": "nodemon services/shipping/index.js",
         "start-inventory": "nodemon services/inventory/index.js",

```

Em seguida, você precisa parar o comando antigo (basta usar um CTRL-C no terminal) e rodar o comando `npm run start` para efetuar as mudanças.

Por fim, para executar a imagem criada no passo anterior (ou seja, colocar de novo o microsserviço de `Shipping` no ar), basta usar o comando:

```
docker run -ti --name shipping -p 3001:3001 micro-livraria/shipping
```

onde:

-   `docker run`: comando de execução de uma imagem docker.
-   `-ti`: habilita a interação com o container via terminal.
-   `--name shipping`: define o nome do container criado.
-   `-p 3001:3001`: redireciona a porta 3001 do container para sua máquina.
-   `micro-livraria/shipping`: especifica qual a imagem deve-se executar.

Se tudo estiver correto, você irá receber a seguinte mensagem em seu terminal:

```
Shipping Service running
```

E o Controller pode acessar o serviço diretamente através do container Docker.

**Mas qual foi exatamente a vantagem de criar esse container?** Agora, você pode levá-lo para qualquer máquina ou sistema operacional e colocar o microsserviço para rodar sem instalar mais nada (incluindo bibliotecas, dependências externas, módulos de runtime, etc). Isso vai ocorrer com containers implementados em JavaScript, como no nosso exemplo, mas também com containers implementados em qualquer outra linguagem.

**IMPORTANTE**: Se tudo funcionou corretamente, dê um **COMMIT & PUSH** (e certifique-se de que seu repositório no GitHub foi atualizado; isso é fundamental para seu trabalho ser devidamente corrigido).

```bash
git add --all
git commit -m "Tarefa prática #2 - Docker"
git push origin main
```

## Comentários Finais

Nesta aula, trabalhamos em uma aplicação baseada em microsserviços. Apesar de pequena, ela ilustra os princípios básicos de microsserviços, bem como algumas tecnologias importantes quando se implementa esse tipo de arquitetura.

No entanto, é importante ressaltar que em uma aplicação real existem outros componentes, como bancos de dados, balanceadores de carga e orquestradores.

A função de um **balanceador de carga** é dividir as requisições quando temos mais de uma instância do mesmo microsserviço. Imagine que o microsserviço de frete da loja virtual ficou sobrecarregado e, então, tivemos que colocar para rodar múltiplas instâncias do mesmo. Nesse caso, precisamos de um balanceador para dividir as requisições que chegam entre essas instâncias.

Já um **orquestrador** gerencia o ciclo de vida de containers. Por exemplo, se um servidor para de funcionar, ele automaticamente move os seus containers para um outro servidor. Se o número de acessos ao sistema aumenta bruscamente, um orquestrador também aumenta, em seguida, o número de containers. [Kubernetes](https://kubernetes.io/) é um dos orquestradores mais usados atualmente.

Se quiser estudar um segundo sistema de demonstração de microsserviços, sugerimos este [repositório](https://github.com/GoogleCloudPlatform/microservices-demo), mantido pelo serviço de nuvem do Google.

## Créditos

Este exercício prático, incluindo o seu código, foi elaborado por **Rodrigo Brito**, aluno de mestrado do DCC/UFMG, como parte das suas atividades na disciplina Estágio em Docência, cursada em 2020/2, sob orientação do **Prof. Marco Tulio Valente**.

O código deste repositório possui uma licença MIT. O roteiro descrito acima possui uma licença CC-BY.
