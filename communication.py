import requests


class MKSConnection:


    def __init__(self):

        self.ip = "192.168.4.1"
        self.conectado = False



    def conectar(self):

        try:

            resposta = requests.get(
                f"http://{self.ip}",
                timeout=5
            )


            if resposta.status_code == 200:

                self.conectado = True

                print("MKS conectada")

                return True


        except Exception as erro:

            print("Erro conexão:")
            print(erro)



        self.conectado = False

        return False




    def enviar_comando(self, comando):

        if not self.conectado:

            print("MKS desconectada")

            return False



        try:

            resposta = requests.post(
                f"http://{self.ip}/command",
                data=comando,
                timeout=5
            )


            print("====================")
            print("Enviado:")
            print(comando)

            print("Resposta:")
            print(resposta.text)


            return True



        except Exception as erro:

            print("Erro comando:")
            print(erro)

            return False