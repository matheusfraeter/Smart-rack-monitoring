"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: communication.py
 Descrição...: Comunicação HTTP com MKS DLC32 / ESP3D
=========================================================
"""


import requests



class MKSConnection:


    def __init__(self):

        self.ip = "192.168.4.1"

        self.conectado = False


        # Última resposta recebida da MKS

        self.ultima_resposta = ""


        # Dados locais da máquina

        self.status = {

            "estado": "Desconectada",

            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0

        }





    # =====================================
    # CONECTAR MKS
    # =====================================

    def conectar(self):

        try:


            resposta = requests.get(

                f"http://{self.ip}",

                timeout=5

            )



            if resposta.status_code == 200:


                self.conectado = True


                self.status["estado"] = "Conectada"



                print(
                    "MKS conectada"
                )


                return True





        except Exception as erro:


            print(
                "Erro conexão MKS:"
            )

            print(
                erro
            )





        self.conectado = False


        self.status["estado"] = "Desconectada"


        return False









    # =====================================
    # ENVIA G-CODE
    # =====================================

    def enviar_comando(self, comando):


        if not self.conectado:


            print(
                "MKS desconectada"
            )


            return False





        try:


            resposta = requests.post(


                f"http://{self.ip}/command",


                data=comando,


                timeout=5


            )





            self.ultima_resposta = resposta.text





            print("===================")

            print(
                "Comando enviado:"
            )

            print(
                comando
            )


            print(
                "Resposta MKS:"
            )

            print(
                resposta.text
            )





            return True





        except Exception as erro:


            print(
                "Erro comando:"
            )


            print(
                erro
            )


            return False









    # =====================================
    # ZERAR EIXOS (HOME)
    # =====================================

    def zerar_eixos(self):


        enviado = self.enviar_comando(

            "$H"

        )





        if not enviado:


            return False





        # Se a MKS retornar erro

        if "ALARM" in self.ultima_resposta:


            self.status["estado"] = "ERRO HOME"


            return False





        # Atualização local

        self.status["X"] = 0.0

        self.status["Y"] = 0.0

        self.status["Z"] = 0.0


        self.status["estado"] = "ZERO"





        return True









    # =====================================
    # STATUS PARA GUI
    # =====================================

    def ler_status(self):


        return self.status