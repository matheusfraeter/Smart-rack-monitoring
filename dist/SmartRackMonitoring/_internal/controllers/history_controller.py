"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: history_controller.py
 Descrição...: Controle do histórico de movimentações
=========================================================
"""


from database import Database



class HistoryController:


    def __init__(self):

        self.db = Database()



    # =====================================
    # LISTAR MOVIMENTAÇÕES
    # =====================================

    def listar_movimentos(self):

        return self.db.listar_movimentos()