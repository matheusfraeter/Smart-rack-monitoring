from database import Database


db = Database()


posicoes = db.listar_posicoes()


print("POSIÇÕES DO RACK:")
print("-----------------")


for posicao in posicoes:

    endereco = posicao[0]
    ocupado = posicao[1]
    pallet = posicao[2]


    print(
        f"{endereco} | Ocupado: {ocupado} | Pallet: {pallet}"
    )