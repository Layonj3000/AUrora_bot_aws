<h1 align="center">Desenvolvimento de Soluções AWS para Conversão de Texto em Áudio e Criação de um Chatbot</h1>

<h2 align="center"><i>Conheça a AUrora, Assistente Virtual da Clínica Veterinária AUmigo</i></h2>

![Imagem|Compass](assets/compass.png)

## 📋 Índice

- [Objetivo](#-objetivo)
- [Descrição](#-descrição)
- [Acesse o Chatbot](#-acesse-o-chatbot-pelo-link)
- [Como Utilizar o Código](#-link-acesse-o-chatbot-pelo-link)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura do Projeto](#️-arquitetura-do-projeto)
- [Dificuldades](#️-dificuldades)
- [Agradecimentos](#-agradecimentos)
- [Autores](#-autores)

## 🎯 Objetivo
   <p style="text-align: justify;"> Desenvolver um endpoint para conversão de texto em áudio e criar um chatbot, que deve ter a opção de enviar a resposta em áudio, utilizando o texto de resposta do chatbot, com uso da API. </p>

## 📖 Descrição
   <p style="text-align: justify;"> O chatbot em questão se chama Aurora e foi desenvolvido para a clínica veterinária AUmigo. </p>
    Este projeto consistiu em duas partes principais:

1. **Endpoint para Conversão de Texto em Áudio (/v1/tts)**
    - Recebe uma frase em formato JSON e converte o texto em áudio utilizando AWS Polly.
    - Armazena o áudio gerado em um bucket público do AWS S3.
    - Salva referências da frase e do áudio no DynamoDB, utilizando um hash code único.
    - Retorna a URL do áudio e outras informações relevantes se a frase já tiver sido processada anteriormente.

2. **Chatbot AUrora com Amazon Lex V2**
    - Desenvolvimento de um chatbot para a clínica veterinária AUmigo, que foi integrado ao Slack.
    - O chatbot possui sete intents distintas e captura informações através de slots.
    - Utiliza response cards para interatividade e possui tratamento de fallback para erros.
    - Pode enviar respostas em áudio utilizando o endpoint /v1/tts.

## :link: Acesse o ChatBot pelo link

## 🚀 Como Utilizar o Código

1. **Configuração do Ambiente**
    - Instale as dependências necessárias:
        ```bash
        pip install boto3 flask
        ```
    - Configure a AWS CLI com suas credenciais.
    - Adicione um arquivo .env conforme o .env.example

2. **Ações na AWS**
    - Crie uma tabela no DynamoDB com a chave primária `unique_id`.
    - Crie um bucket no S3 e configure as permissões para ser público.
    - Crie uma função lambda
    - Import o bot no Amazon Lex
    -      


## 📂 Estrutura do Projeto
```
├── 📁 api-tts
│       ├── dynamodb_operations.py
│       ├── handler.py
│       ├── polly_operations.py
│       ├── s3_operations.py
│       ├── serverless.yml
│       └── utils.py
│
├── 📁 assets
│       └── sprint6-7.jpg
│
└── 📁 chatbot
        ├── 📁 lambda
        │       ├── script
        │       └── setup_aurora_bd.py
        ├── .env.example
        └── Aurora-DRAFT.zip
```


## 💻 Tecnologias Utilizadas

- AWS Polly
- AWS S3
- AWS DynamoDB
- Amazon Lex V2
- Slack
- MySQL
- Flask
- Python (Boto3)
- Kanban

## 🏗️ Arquitetura do Projeto

![Imagem|Diagrama](assets/sprints6-7.jpg)

## 🛠️ Dificuldades

1. <p style="text-align: justify;"> </p>
2. <p style="text-align: justify;"> </p>
3. <p style="text-align: justify;"> </p>

## 🙏 Agradecimentos

<p style="text-align: justify;">É com imensa satisfação que o grupo-6 agradece à CompassUOL por providenciar o acesso aos cursos da Udemy, que geraram o aprendizado e desenvolvimento necessário para esta implementação e muito mais.</p>

## 👥 Autores

**Gabriel Venâncio de Avelar**
- GitHub: https://github.com/GabrielAvelarbr

**Layon José**
- GitHub: https://github.com/Layonj300

**Luiz Fillipe Oliveira Morais**
- GitHub: https://github.com/LuizFillipe1

**Pâmela Aliny Cleto Pavan**
- GitHub: https://github.com/PamelaPavan
