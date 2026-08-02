from database import Database


db = Database()


posicoes = [
    "A1",
    "C3"
]


for posicao in posicoes:

    resultado = db.buscar_posicao(
        posicao
    )

    print(
        posicao,
        resultado
    )