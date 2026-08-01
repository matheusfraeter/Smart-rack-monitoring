"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: rack_controller.py
 Descrição...: Controle das operações do Rack
=========================================================
"""


from database import Database



class RackController:


    def __init__(self):

        self.db = Database()



    # =====================================
    # LISTAR POSIÇÕES
    # =====================================

    def listar_posicoes(self):

        return self.db.listar_posicoes()



    # =====================================
    # ARMAZENAR PALLET
    # =====================================

    def armazenar_pallet(
            self,
            endereco,
            pallet
    ):

        self.db.ocupar_posicao(
            endereco,
            pallet
        )


        self.db.registrar_movimento(
            "Recebimento",
            endereco,
            "Armazenado"
        )



    # =====================================
    # RETIRAR PALLET
    # =====================================

    def retirar_pallet(
            self,
            endereco
    ):

        self.db.liberar_posicao(
            endereco
        )


        self.db.registrar_movimento(
            endereco,
            "Expedição",
            "Retirado"
        )



    # =====================================
    # BUSCAR POSIÇÃO
    # =====================================

    def buscar_posicao(
            self,
            endereco
    ):

        posicoes = self.db.listar_posicoes()


        for posicao in posicoes:

            if posicao[0] == endereco:

                return posicao


        return None