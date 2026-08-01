from communication import MKSConnection


mks = MKSConnection()


if mks.conectar():

    print("MKS DLC32 conectada!")

else:

    print("Falha na conexão!")