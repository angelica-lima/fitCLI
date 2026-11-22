#bibliotecas
import typer
import requests
import json
import re

#inicialização da app
app = typer.Typer()

#base da API do wger e cabeçalho pedido pelo stor
url = "https://wger.de/api/v2/exerciseinfo/"
headers = {"User-Agent": "FitCLI-Student/1.0"}

#callback permite subcomandos
@app.callback()
def main():
    pass

#alinea a
@app.command()
def  top(n: int = typer.Argument(3)):
    #parâmetros de pesquisa, idioma inglês (2), limite N e ordenação do mais recente para o mais antigo
    params = {
        "language": 2,
        "limit": n,
        "ordering": "-created"
    }

    response = requests.get(url, headers=headers, params=params)

    #verifica se a requisição foi bem sucedida
    if response.status_code == 200:

        dados = response.json()

        exercicios = []

        for item in dados["results"]:

            nome = "Sem nome"

            for traducao in item["translations"]:
                if traducao["language"] == 2:
                    nome = traducao["name"]
                    break

            categoria = item["category"]["name"]

            equipamento = []

            for equip in item["equipment"]:
                equipamento.append(equip["name"])

            exercicio = {
                "name": nome,
                "category": categoria,
                "equipment": equipamento
            }

            exercicios.append(exercicio)
        #imprme a lista final formatada em JSON 
        print(json.dumps(exercicios, indent=4, ensure_ascii=False))

    else:
        print(f"Erro na requisição: {response.status_code}")


#alinea b
#pesquisa de exercícios por músculo
@app.command()
def search(termo: str, n: int = typer.Argument(5)):
    #faz o request de 100 regstros em inglês para facilitar a pesquisa
    params = {"language": 2, "limit": 100}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:

        dados = response.json()
        exercicios = []

        #ciclo para percorrer as paginas de resultados enquanto necessario
        while True:

            for item in dados["results"]:

                nome = "Sem nome"

                for traducao in item["translations"]:
                    if traducao["language"] == 2:
                        nome = traducao["name"]
                        break

                categoria = item["category"]["name"]
                #verifica se o termo pesquisado = categoria ou algum músculo envolvido
                encontrado = False

                if termo.lower() in categoria.lower():
                    encontrado = True

                for musculo in item["muscles"]:
                    if termo.lower() in musculo["name"].lower():
                        encontrado = True
                #adiciona o exercício se houver correspondência e não se tiver atingido o limite n
                if encontrado and len(exercicios) < n:

                    exercicio = {
                        "name": nome,
                        "category": categoria
                    }

                    exercicios.append(exercicio)
            #para se já recolheu n resultados ou se não houver mais páginas
            if len(exercicios) >= n or dados["next"] is None:
                break
            #avança para a próxima página indicada pela API
            response = requests.get(dados["next"], headers=headers)
            dados = response.json()

        print(json.dumps(exercicios, indent=4, ensure_ascii=False))

    else:
        print(f"Erro na requisição: {response.status_code}")

#alinea c
#extrair tipo de esforço de um exercício
@app.command()
def type(exercise_id: int):
    #constroi o URL especifico para o exercicio indicado por exercise_id
    url_exercicio = url + str(exercise_id) + "/"

    params = {"language": 2}

    response = requests.get(url_exercicio, headers=headers, params=params)

    if response.status_code == 200:

        dados = response.json()

        nome = "Sem nome"
        descricao = ""

        for traducao in dados["translations"]:
            if traducao["language"] == 2:
                nome = traducao["name"]
                descricao = traducao["description"]
                break

        categoria = dados["category"]["name"]

        texto = nome + " " + descricao + " " + categoria

        #usa expressão regular com re.search para detetar termos associados a cardio
        if re.search(r"cardio|running|cycling|treadmill|swimming", texto, re.IGNORECASE):
            resultado = "cardio"

        #caso envolva mais que um musculo, classifica como composto (compound)
        elif len(dados["muscles"]) > 1:
            resultado = "compound"

        #se envolver exatamente um musculo, classifica como isolado (isolated)
        elif len(dados["muscles"]) == 1:
            resultado = "isolated"

        else:
            resultado = "other"

        print(resultado)

    else:
        print(f"Erro na requisição: {response.status_code}")

#alinea d
@app.command()
def equipment(categoria: str):

    params = {
        "language": 2,
        "limit": 100
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:

        dados = response.json()
        #dicionario contador para cada equipamento
        equipamentos = {
            "barbell": 0,
            "dumbbell": 0,
            "cable": 0,
            "machine": 0,
            "bodyweight": 0
        }
        #percorre todas as páginas da API para contabilizar todas as ocorrências na categoria x
        while True:

            for item in dados["results"]:

                nome_categoria = item["category"]["name"]
                #filtra apenas os exercicios pertencentes a categoria pedida
                if categoria.lower() == nome_categoria.lower():

                    descricao = ""

                    for traducao in item["translations"]:
                        if traducao["language"] == 2:
                            descricao = traducao["description"] or ""
                            break
                    #procura menções exatas da palavra de cada equipamento (já que \b delimita a palavra)
                    for equipamento in equipamentos:
                        quantidade = len(
                            re.findall(
                                r"\b" + equipamento + r"\b",
                                descricao,
                                re.IGNORECASE
                            )
                        )

                        equipamentos[equipamento] += quantidade

            if dados["next"] is None:
                break

            response = requests.get(dados["next"], headers=headers)

            if response.status_code == 200:
                dados = response.json()
            else:
                print(f"Erro na requisição: {response.status_code}")
                break
        #ordena os equipamentos por contagem decrescente (do maior número de ocorrências para o menor)
        equipamentos_ordenados = dict(
            sorted(equipamentos.items(), key=lambda item: item[1], reverse=True)
        )

        print(json.dumps(equipamentos_ordenados, indent=4, ensure_ascii=False))

    else:
        print(f"Erro na requisição: {response.status_code}")

if __name__ == "__main__":
    app()

