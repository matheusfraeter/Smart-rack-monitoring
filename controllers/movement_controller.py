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
    # CRIAR MOVIMENTAÇÃO INTELIGENTE
    # =====================================

    def criar_movimento(
            self,
            origem,
            destino
    ):


        # -----------------------------
        # Verifica pallet na origem
        # -----------------------------

        pallet = self.db.verificar_pallet(
            origem
        )


        if pallet is None:

            return {
                "sucesso": False,
                "mensagem":
                f"Origem {origem} sem pallet"
            }



        # -----------------------------
        # Verifica destino livre
        # -----------------------------

        destino_livre = self.db.verificar_posicao_livre(
            destino
        )


        if destino_livre is False:

            return {
                "sucesso": False,
                "mensagem":
                f"Destino {destino} ocupado"
            }



        # -----------------------------
        # Registra movimento
        # -----------------------------

        self.db.registrar_movimento(
            origem,
            destino,
            "Aguardando"
        )


        return {

            "sucesso": True,

            "mensagem":
            f"Movimentação criada: {origem} → {destino}",

            "pallet":
            pallet

        }



    # =====================================
    # LISTAR MOVIMENTAÇÕES
    # =====================================

    def listar_movimentos(self):

        return self.db.listar_movimentos()