# FitCLI — Pesquisa de exercícios com a API wger

Aplicação de linha de comandos desenvolvida em Python para consultar e organizar exercícios físicos através da API pública [wger](https://wger.de/api/v2/).

O projeto foi desenvolvido no âmbito de um trabalho académico e permite pesquisar exercícios, consultar informações sobre cada exercício e criar uma lista de treino com base em músculos, categorias e tipo de esforço.

## Funcionalidades

- **Top:** apresenta os exercícios mais recentes, com nome, categoria e equipamento.
- **Search:** pesquisa exercícios por músculo ou categoria.
- **Type:** classifica um exercício como `compound`, `isolated`, `cardio` ou `other`.
- **Equipment:** conta as menções a diferentes equipamentos nas descrições dos exercícios de uma categoria.

## Tecnologias utilizadas

- Python
- [Typer](https://typer.tiangolo.com/) — criação dos comandos de terminal
- [Requests](https://requests.readthedocs.io/) — pedidos à API
- `re` — pesquisa de termos nas descrições
- `json` — apresentação dos resultados em JSON
- `csv` — exportação dos resultados

## Requisitos

- Python 3
- Ligação à Internet

## Instalação

1. Clona este repositório:

   ```bash
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DA_PASTA>
   ```

2. Cria e ativa um ambiente virtual:

   **macOS / Linux**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   **Windows**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Instala as dependências:

   ```bash
   pip install typer requests
   ```

## Como utilizar

Executa os comandos no terminal, dentro da pasta do projeto.

### 1. Listar exercícios recentes

Apresenta os 3 exercícios mais recentes:

```bash
python wger.py top 3
```

### 2. Pesquisar exercícios

Pesquisa até 5 exercícios relacionados com o termo `biceps`:

```bash
python wger.py search biceps 5
```

O termo pode corresponder a um músculo ou a uma categoria.

### 3. Consultar o tipo de esforço

Classifica um exercício através do seu ID na API:

```bash
python wger.py type ID
```

Substitui `ID` por um identificador válido de exercício.

### 4. Contar menções a equipamentos

Conta as menções a equipamentos nas descrições dos exercícios da categoria indicada:

```bash
python wger.py equipment Legs
```

### 5. Criar uma lista de treino

Procura até 3 exercícios por músculo para bíceps e tríceps:

```bash
python wger.py workout --musculos biceps,triceps --n 3
```

Também é possível pesquisar por categorias:

```bash
python wger.py workout --categorias Arms,Legs --n 2
```

Para filtrar pelo tipo de esforço:

```bash
python wger.py workout --musculos biceps --tipo compound --n 3
```

Os tipos aceites são `compound`, `isolated` e `any`.

## API utilizada

O projeto utiliza a API pública do [wger](https://wger.de/api/v2/). Os pedidos são feitos ao endpoint de informações dos exercícios:

```text
https://wger.de/api/v2/exerciseinfo/
```

As consultas utilizam o idioma inglês (`language=2`). A aplicação verifica o estado das respostas e apresenta uma mensagem quando ocorre um erro de requisição.

## Nota sobre a classificação

A classificação do tipo de esforço é feita através de regras simples baseadas na descrição, categoria e músculos associados ao exercício. Por isso, o resultado é uma estimativa e pode não corresponder à classificação técnica de todos os exercícios.

## Autor

Projeto académico desenvolvido por @angelica-lima

## Licença

Este projeto foi desenvolvido para fins académicos.