"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: fluidnc_monitor.py
 Descrição...: Monitoramento do estado do FluidNC
=========================================================
"""


import requests
import re



class FluidNCMonitor:


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

                    "online": True,

                    "mensagem":
                    "FluidNC conectado"

                }


        except Exception as erro:


            return {

                "online": False,

                "erro":
                str(erro)

            }



        return {

            "online": False,

            "mensagem":
            "Sem resposta"

        }



    # =====================================
    # LER STATUS DA MÁQUINA
    # =====================================

    def ler_status(self):


        try:


            resposta = requests.post(

                f"{self.url}/command",

                data="?",

                timeout=5

            )


            texto = resposta.text


            # DEBUG TEMPORÁRIO
            print("\n--- RESPOSTA FLUIDNC ---")
            print(texto)
            print("------------------------\n")



            return self.interpretar(
                texto
            )



        except Exception as erro:


            return {


                "online": False,


                "estado":
                "Offline",


                "x":
                0.0,


                "y":
                0.0,


                "z":
                0.0,


                "erro":
                str(erro)

            }



    # =====================================
    # INTERPRETAR RESPOSTA
    # =====================================

    def interpretar(
            self,
            texto
    ):



        dados = {


            "online": True,


            "estado":
            "Desconhecido",


            "x":
            0.0,


            "y":
            0.0,


            "z":
            0.0

        }



        # -----------------------------
        # Estado
        # -----------------------------


        estados = [

            "Idle",

            "Run",

            "Hold",

            "Alarm",

            "Door",

            "Jog"

        ]



        for estado in estados:


            if f"<{estado}" in texto:


                dados["estado"] = estado

                break




        # -----------------------------
        # Coordenadas MPos
        # -----------------------------


        posicao = re.search(

            r"MPos:([-0-9.]+),([-0-9.]+),([-0-9.]+)",

            texto

        )


        if posicao:


            dados["x"] = float(
                posicao.group(1)
            )


            dados["y"] = float(
                posicao.group(2)
            )


            dados["z"] = float(
                posicao.group(3)
            )



        # -----------------------------
        # Coordenadas WPos (caso use)
        # -----------------------------


        posicao_w = re.search(

            r"WPos:([-0-9.]+),([-0-9.]+),([-0-9.]+)",

            texto

        )


        if posicao_w:


            dados["x"] = float(
                posicao_w.group(1)
            )


            dados["y"] = float(
                posicao_w.group(2)
            )


            dados["z"] = float(
                posicao_w.group(3)
            )



        return dados