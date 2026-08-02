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


        # HTTP

        self.conectado = False



        # WebSocket

        self.websocket = None

        self.ws_conectado = False



        # controle thread

        self.executando = True



        # dados reais da máquina

        self.status = {

            "estado": "Desconectada",

            "X": 0.0,

            "Y": 0.0,

            "Z": 0.0

        }



    # =====================================
    # CONEXÃO PRINCIPAL
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



                # inicia websocket separado

                thread = threading.Thread(

                    target=self.monitor_websocket,

                    daemon=True

                )


                thread.start()



                return True



        except Exception as erro:


            print("Erro conexão MKS:")
            print(erro)



        self.conectado = False


        return False





    # =====================================
    # GERENCIADOR WEBSOCKET
    # =====================================


    def monitor_websocket(self):


        while self.executando:


            if not self.ws_conectado:


                self.conectar_websocket()



            time.sleep(5)






    # =====================================
    # CONECTA WEBSOCKET
    # =====================================


    def conectar_websocket(self):


        try:


            print("Conectando WebSocket...")


            self.websocket = websocket.create_connection(

                f"ws://{self.ip}:81",

                timeout=5

            )



            self.ws_conectado = True



            print("WebSocket conectado")



            # pede atualização

            self.websocket.send(

                "subscribe"

            )



            self.receber_status()



        except Exception as erro:


            print("WebSocket desconectado")

            print(erro)



            self.ws_conectado = False



            try:


                if self.websocket:

                    self.websocket.close()


            except:


                pass



            time.sleep(3)






    # =====================================
    # RECEBE STATUS
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



                # posição GRBL

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




                # estado máquina


                if "Idle" in mensagem:


                    self.status["estado"] = "IDLE"



                elif "Run" in mensagem:


                    self.status["estado"] = "MOVENDO"




            except Exception as erro:


                print(
                    "Erro recebendo status:",
                    erro
                )


                self.ws_conectado = False


                break






    # =====================================
    # ENVIA COMANDO G-CODE
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
    # STATUS PARA DASHBOARD
    # =====================================


    def ler_status(self):


        return self.status