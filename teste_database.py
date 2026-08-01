from database import Database


db = Database()


# colocar pallet

db.ocupar_posicao(
    "A1",
    "PALLET001"
)


print("Depois de ocupar:")


for item in db.listar_posicoes():

    print(item)



# liberar

db.liberar_posicao(
    "A1"
)


print("\nDepois de liberar:")


for item in db.listar_posicoes():

    print(item)