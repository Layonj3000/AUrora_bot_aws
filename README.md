<h1 align="center">Desenvolvimento de Soluções AWS para Conversão de Texto em Áudio e Criação de um Chatbot</h1>

<h2 align="center"><i>Conheça a AUrora, assistente virtual da Clínica Veterinária AUmigo</i></h2>

![Imagem|Compass](assets/compass.png)

## 📋 Índice

- [Objetivo](#-objetivo)
- [Descrição](#-descrição)
- [Como Utilizar](#-como-utilizar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Arquitetura do Projeto](#️-arquitetura-do-projeto)
- [Dificuldades](#️-dificuldades)
- [Agradecimentos](#-agradecimentos)
- [Autores](#-autores)

## 🎯 Objetivo

Desenvolver um endpoint para conversão de texto em áudio e um chatbot para a clínica veterinária AUmigo, utilizando os serviços AWS Polly, S3, DynamoDB e Amazon Lex V2, a fim de proporcionar uma experiência inovadora e eficiente para os clientes da clínica.

## 📖 Descrição

Este projeto consiste em duas partes principais:

1. **Endpoint para Conversão de Texto em Áudio (/v1/tts)**
    - Recebe uma frase em formato JSON e converte o texto em áudio utilizando AWS Polly.
    - Armazena o áudio gerado em um bucket público do AWS S3.
    - Salva referências da frase e do áudio no DynamoDB, utilizando um hash code único.
    - Retorna a URL do áudio e outras informações relevantes se a frase já tiver sido processada anteriormente.

2. **Chatbot AUrora com Amazon Lex V2**
    - Desenvolve um chatbot para a clínica veterinária AUmigo, que pode ser integrado ao Slack ou à Web.
    - O chatbot possui ao menos 4 intents distintas e captura informações através de slots.
    - Utiliza response cards para interatividade e possui tratamento de fallback para erros.
    - Pode enviar respostas em áudio utilizando o endpoint /v1/tts.

## 🚀 Como Utilizar

1. **Configuração do Ambiente**
    - Instale as dependências necessárias:
        ```bash
        pip install boto3 flask
        ```
    - Configure a AWS CLI com suas credenciais.

2. **Criação da Tabela no DynamoDB e Bucket no S3**
    - Crie uma tabela no DynamoDB com a chave primária `unique_id`.
    - Crie um bucket no S3 e configure as permissões para ser público.


## 📂 Estrutura do Projeto


## 💻 Tecnologias Utilizadas

- AWS Polly
- AWS S3
- AWS DynamoDB
- Amazon Lex V2
- Flask
- Python (Boto3)

## 🏗️ Arquitetura do Projeto

![Imagem|Diagrama](assets/arquitetura.png)

## 🛠️ Dificuldades



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
