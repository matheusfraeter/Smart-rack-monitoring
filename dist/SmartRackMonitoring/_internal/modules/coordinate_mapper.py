"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: coordinate_mapper.py
 Descrição...: Conversão de posições do rack para coordenadas
=========================================================
"""


class CoordinateMapper:


    def __init__(self):


        # Distância entre posições
        self.distancia_x = 200   # mm
        self.distancia_y = 200   # mm
        self.distancia_z = 300   # mm



    # =====================================
    # CONVERTER ENDEREÇO DO RACK
    # =====================================

    def converter(
            self,
            endereco
    ):


        linha = endereco[0]

        coluna = int(
            endereco[1]
        )



        mapa_linhas = {

            "A": 0,

            "B": 1,

            "C": 2,

            "D": 3

        }



        y = mapa_linhas[linha] * self.distancia_y


        x = (coluna - 1) * self.distancia_x



        return {

            "X": x,

            "Y": y,

            "Z": 0

        }



    # =====================================
    # TESTE DE POSIÇÃO
    # =====================================

    def mostrar(
            self,
            endereco
    ):


        coordenada = self.converter(
            endereco
        )


        return (
            f"{endereco} → "
            f"X:{coordenada['X']} "
            f"Y:{coordenada['Y']} "
            f"Z:{coordenada['Z']}"
        )