"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: mission_controller.py
 Descrição...: Controle da fila de missões da empilhadeira
=========================================================
"""


from database import Database
from controllers.movement_controller import MovementController




class MissionController:


    def __init__(self):

        self.db = Database()

        self.movement = MovementController()



    # =====================================
    # BUSCAR PRÓXIMA MISSÃO
    # =====================================

    def proxima_missao(self):


        missoes = self.db.listar_missoes_pendentes()



        if not missoes:


            return None



        return missoes[0]



    # =====================================
    # INICIAR MISSÃO
    # =====================================

    def iniciar_missao(
            self,
            id_missao
    ):


        self.movement.iniciar_movimento(
            id_missao
        )



        return {

            "sucesso": True,

            "mensagem":
            f"Missão {id_missao} iniciada"

        }



    # =====================================
    # FINALIZAR MISSÃO
    # =====================================

    def finalizar_missao(
            self,
            id_missao
    ):


        self.movement.finalizar_movimento(
            id_missao
        )



        return {

            "sucesso": True,

            "mensagem":
            f"Missão {id_missao} finalizada"

        }



    # =====================================
    # LISTAR FILA
    # =====================================

    def listar_fila(self):


        return self.db.listar_missoes_pendentes()