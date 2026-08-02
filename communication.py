"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: communication.py
 Descrição...: Comunicação com MKS DLC32 / ESP3D
=========================================================
"""


import requests
import websocket
import threading
import re
import time




class MKSConnection:



    def __init__(self):


        self.ip = "192.168.4.1"


        self.conectado = False


        self.websocket = None


        self.ws_conectado = False



        # dados reais da máquina

        self.status = {

            "estado": "Desconectada",

            "X": 0.0,

            "Y": 0.0,

            "Z": 0.0

        }





    # =====================================
    # CONEXÃO HTTP
    # =====================================


    def conectar(self):


        try:


            resposta = requests.get(

                f"http://{self.ip}",

                timeout=5

            )



            if resposta.status_code == 200:


                self.conectado = True


                print("MKS conectada")



                # inicia websocket

                self.conectar_websocket()



                return True




        except Exception as erro:


            print("Erro conexão:")

            print(erro)




        self.conectado = False


        return False






    # =====================================
    # WEBSOCKET ESP3D
    # =====================================


    def conectar_websocket(self):


        try:


            self.websocket = websocket.create_connection(

                f"ws://{self.ip}:81",

                timeout=5

            )



            self.ws_conectado = True



            print("WebSocket conectado")



            # ativa atualização

            self.websocket.send(
                "subscribe"
            )



            thread = threading.Thread(

                target=self.receber_status,

                daemon=True

            )


            thread.start()




        except Exception as erro:


            print("Erro WebSocket:")

            print(erro)



            self.ws_conectado = False







    # =====================================
    # RECEBER STATUS
    # =====================================


    def receber_status(self):


        while self.ws_conectado:


            try:


                mensagem = self.websocket.recv()



                if isinstance(
                    mensagem,
                    bytes
                ):


                    mensagem = mensagem.decode()



                # exemplo:
                # <Idle|MPos:35.000,0.000,0.000|FS:0,0>


                if "MPos:" in mensagem:


                    posicao = re.search(

                        r"MPos:([-0-9.]+),([-0-9.]+),([-0-9.]+)",

                        mensagem

                    )



                    if posicao:


                        self.status["X"] = float(
                            posicao.group(1)
                        )


                        self.status["Y"] = float(
                            posicao.group(2)
                        )


                        self.status["Z"] = float(
                            posicao.group(3)
                        )




                if "Idle" in mensagem:


                    self.status["estado"] = "IDLE"



                elif "Run" in mensagem:


                    self.status["estado"] = "MOVENDO"





            except Exception:


                time.sleep(1)






    # =====================================
    # ENVIA G-CODE
    # =====================================


    def enviar_comando(
            self,
            comando
    ):


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





    # =====================================
    # RETORNA STATUS ATUAL
    # =====================================


    def ler_status(self):


        return self.status