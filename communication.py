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
                return True


        except:

            self.conectado = False


        return False




    def enviar_comando(self, comando):

        if not self.conectado:

            return False


        try:

            resposta = requests.post(
                f"http://{self.ip}/command",
                data=comando,
                timeout=5
            )


            return resposta.status_code == 200


        except:

            return False