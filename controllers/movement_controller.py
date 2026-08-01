"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: movement_controller.py
 Descrição...: Controle das movimentações do rack
=========================================================
"""


from database import Database



class MovementController:


    def __init__(self):

        self.db = Database()



    # =====================================
    # CRIAR MOVIMENTAÇÃO
    # =====================================

    def criar_movimento(
            self,
            origem,
            destino
    ):

        self.db.registrar_movimento(
            origem,
            destino,
            "Aguardando"
        )



    # =====================================
    # LISTAR MOVIMENTAÇÕES
    # =====================================

    def listar_movimentos(self):

        return self.db.listar_movimentos()