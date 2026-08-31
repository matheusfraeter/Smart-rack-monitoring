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
    # EXECUTAR MOVIMENTAÇÃO
    # =====================================

    def executar_movimento(
            self,
            origem,
            destino
    ):


        pallet = self.db.verificar_pallet(
            origem
        )


        if pallet is None:

            return {
                "sucesso": False,
                "mensagem":
                f"Origem {origem} sem pallet"
            }



        if self.db.verificar_posicao_livre(destino) is False:

            return {
                "sucesso": False,
                "mensagem":
                f"Destino {destino} ocupado"
            }



        # Libera origem

        self.db.liberar_posicao(
            origem
        )


        # Ocupa destino

        self.db.ocupar_posicao(
            destino,
            pallet
        )


        # Registra conclusão

        self.db.registrar_movimento(
            origem,
            destino,
            "Concluído"
        )



        return {

            "sucesso": True,

            "mensagem":
            f"Pallet {pallet} movido de {origem} para {destino}"

        }

            # =====================================
    # INICIAR MOVIMENTO
    # =====================================

    def iniciar_movimento(
            self,
            id_movimento
    ):

        self.db.alterar_status_movimento(
            id_movimento,
            "Em movimento"
        )



    # =====================================
    # FINALIZAR MOVIMENTO
    # =====================================

    def finalizar_movimento(
            self,
            id_movimento
    ):

        self.db.alterar_status_movimento(
            id_movimento,
            "Concluído"
        )



    # =====================================
    # CANCELAR MOVIMENTO
    # =====================================

    def cancelar_movimento(
            self,
            id_movimento
    ):

        self.db.alterar_status_movimento(
            id_movimento,
            "Erro"
        )



    # =====================================
    # LISTAR MOVIMENTAÇÕES
    # =====================================

    def listar_movimentos(self):

        return self.db.listar_movimentos()