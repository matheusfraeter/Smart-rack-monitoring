"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: fluidnc_sender.py
 Descrição...: Comunicação com FluidNC da MKS DLC32
=========================================================
"""


import requests
import time



class FluidNCSender:


    def __init__(
            self,
            ip="192.168.4.1"
    ):

        self.ip = ip

        self.url = (
            f"http://{self.ip}"
        )



    # =====================================
    # TESTAR CONEXÃO
    # =====================================

    def testar_conexao(self):

        try:

            resposta = requests.get(
                self.url,
                timeout=3
            )


            if resposta.status_code == 200:

                return {

                    "sucesso": True,

                    "mensagem":
                    "FluidNC conectado"

                }


        except Exception as erro:


            return {

                "sucesso": False,

                "mensagem":
                str(erro)

            }



        return {

            "sucesso": False,

            "mensagem":
            "Sem resposta da controladora"

        }



    # =====================================
    # ENVIAR UM COMANDO G-CODE
    # =====================================

    def enviar_comando(
            self,
            comando
    ):


        try:


            resposta = requests.post(

                f"{self.url}/command",

                data=comando,

                timeout=5

            )


            return {

                "sucesso": True,

                "resposta":
                resposta.text

            }


        except Exception as erro:


            return {

                "sucesso": False,

                "erro":
                str(erro)

            }



    # =====================================
    # ENVIAR PROGRAMA COMPLETO
    # =====================================

    def enviar_programa(
            self,
            lista_gcode
    ):


        resultados = []


        for linha in lista_gcode:


            resultado = self.enviar_comando(
                linha
            )


            resultados.append(
                resultado
            )


            time.sleep(
                0.2
            )


        return resultados