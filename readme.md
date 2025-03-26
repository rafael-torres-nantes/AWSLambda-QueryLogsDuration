# AWS Lambda - Consultar Logs durante Périodos de Tempo

## 👨‍💻 Projeto desenvolvido por: 
[Rafael Torres Nantes](https://github.com/rafael-torres-nantes)

## Índice

* [📚 Contextualização do projeto](#-contextualização-do-projeto)
* [🛠️ Tecnologias/Ferramentas utilizadas](#%EF%B8%8F-tecnologiasferramentas-utilizadas)
* [🖥️ Funcionamento do sistema](#%EF%B8%8F-funcionamento-do-sistema)
* [🔀 Arquitetura da aplicação](#arquitetura-da-aplicação)
* [📁 Estrutura do projeto](#estrutura-do-projeto)
* [📌 Como executar o projeto](#como-executar-o-projeto)
* [🕵️ Dificuldades Encontradas](#%EF%B8%8F-dificuldades-encontradas)

## 📚 Contextualização do projeto

O projeto tem como objetivo criar uma solução automatizada para consultar logs de duração de execução de funções AWS Lambda, utilizando serviços da AWS como DynamoDB e Boto3. O sistema foi desenhado para monitorar e registrar a duração das execuções, facilitando a análise de desempenho e identificação de possíveis gargalos.

## 🛠️ Tecnologias/Ferramentas utilizadas

[<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white">](https://www.python.org/)
[<img src="https://img.shields.io/badge/Visual_Studio_Code-007ACC?logo=visual-studio-code&logoColor=white">](https://code.visualstudio.com/)
[<img src="https://img.shields.io/badge/Boto3-0073BB?logo=amazonaws&logoColor=white">](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
[<img src="https://img.shields.io/badge/AWS-DynamoDB-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/dynamodb/)
[<img src="https://img.shields.io/badge/AWS-Lambda-FF9900?logo=amazonaws&logoColor=white">](https://aws.amazon.com/lambda/)
[<img src="https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white">](https://github.com/)

## 🖥️ Funcionamento do sistema

O sistema foi desenvolvido utilizando **Python** com a biblioteca **Boto3** para interagir com os serviços da AWS. As principais funcionalidades incluem o registro de logs de execução no DynamoDB e a consulta desses logs para análise de desempenho.

* **Serviços AWS**: A integração com DynamoDB e outras funcionalidades estão localizadas em `services/dynamodb_services.py`.
* **Utilitários**: A pasta `utils` contém funções para importação de credenciais AWS e outras funções auxiliares.

## 🔀 Arquitetura da aplicação

O sistema é baseado em uma arquitetura de microserviços, onde o backend se comunica com os serviços da AWS para monitoramento e registro dos logs de execução das funções Lambda. O DynamoDB desempenha um papel central no armazenamento dos logs, enquanto **Boto3** lida com a interação com os serviços da AWS.

## 📁 Estrutura do projeto

A estrutura do projeto é organizada da seguinte maneira:

```
.
├── controller/
│   └── calculate_execution_time.py
├── services/
│   └── dynamodb_services.py
├── utils/
│   ├── check_aws.py
│   └── import_credentials.py
├── lambda_handler.py
└── README.md
```

## 📌 Como executar o projeto

Para executar o projeto localmente, siga as instruções abaixo:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/rafael-torres-nantes/aws-lambda-query-logs.git
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as credenciais da AWS:**
   Certifique-se de que suas credenciais da AWS estão configuradas corretamente.

4. **Execute a função Lambda localmente:**
   ```bash
   python main.py
   ```

## 🕵️ Dificuldades Encontradas

Durante o desenvolvimento do projeto, algumas dificuldades foram enfrentadas, como:

- **Integração com serviços AWS:** O uso de credenciais e permissões para acessar o DynamoDB e Lambda exigiu cuidados especiais para garantir a segurança e funcionalidade do sistema.
- **Monitoramento de logs:** A implementação do monitoramento e registro de logs de execução das funções Lambda exigiu testes e ajustes para lidar com diferentes cenários e volumes de dados.
