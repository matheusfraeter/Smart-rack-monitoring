"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: gcode_generator.py
 Descrição...: Geração de comandos G-code para FluidNC
=========================================================
"""


from modules.coordinate_mapper import CoordinateMapper



class GCodeGenerator:


    def __init__(self):

        self.mapper = CoordinateMapper()



    # =====================================
    # CABEÇALHO PADRÃO
    # =====================================

    def cabecalho(self):

        return [
            "G21",
            "G90"
        ]



    # =====================================
    # MOVIMENTO ATÉ POSIÇÃO
    # =====================================

    def mover_para(
            self,
            endereco
    ):


        coordenada = self.mapper.converter(
            endereco
        )


        return [

            f"G0 X{coordenada['X']} Y{coordenada['Y']}",

            "G0 Z50"

        ]



    # =====================================
    # PEGAR PALLET
    # =====================================

    def pegar_pallet(self):

        return [

            "G0 Z0",

            "M3",

            "G4 P1",

            "M5"

        ]



    # =====================================
    # SOLTAR PALLET
    # =====================================

    def soltar_pallet(self):

        return [

            "G0 Z0",

            "M3",

            "G4 P1",

            "M5"

        ]



    # =====================================
    # GERAR MISSÃO COMPLETA
    # =====================================

    def gerar_movimentacao(
            self,
            origem,
            destino
    ):


        codigo = []


        codigo.extend(
            self.cabecalho()
        )


        # Vai buscar pallet

        codigo.extend(
            self.mover_para(origem)
        )


        codigo.extend(
            self.pegar_pallet()
        )



        # Vai entregar pallet

        codigo.extend(
            self.mover_para(destino)
        )


        codigo.extend(
            self.soltar_pallet()
        )



        return codigo