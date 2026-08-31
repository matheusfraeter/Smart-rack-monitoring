"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: rack_controller.py
 Descrição...: Controle das operações do Rack
=========================================================
"""

from database import Database

from controllers.forklift_controller import ForkliftController


class RackController:

    def __init__(self, mks=None):

        self.db = Database()

        self.mks = mks

        self.forklift = None

        if self.mks is not None:

            self.forklift = ForkliftController(
                self.mks
            )


    # =================================================
    # LISTAR POSIÇÕES
    # =================================================

    def listar_posicoes(self):

        return self.db.listar_posicoes()


    # =================================================
    # ARMAZENAR PALLET
    #
    # Primeiro a empilhadeira executa.
    # Só depois o banco é atualizado.
    # =================================================

    def armazenar_pallet(
        self,
        endereco,
        pallet
    ):

        # ---------------------------------------------
        # VERIFICAR CONTROLADOR
        # ---------------------------------------------

        if self.forklift is None:

            print(
                "ERRO: controlador da empilhadeira não configurado."
            )

            return False


        # ---------------------------------------------
        # VERIFICAR CONEXÃO
        # ---------------------------------------------

        if not self.mks.conectado:

            print(
                "ERRO: MKS desconectada."
            )

            return False


        # ---------------------------------------------
        # EXECUTAR ARMAZENAMENTO FÍSICO
        # ---------------------------------------------

        sucesso = self.forklift.armazenar_pallet(
            endereco
        )


        if not sucesso:

            print(
                "ERRO: armazenamento não concluído."
            )

            return False


        # ---------------------------------------------
        # ATUALIZAR BANCO
        # ---------------------------------------------

        self.db.ocupar_posicao(
            endereco,
            pallet
        )


        self.db.registrar_movimento(
            "Recebimento",
            endereco,
            "Armazenado"
        )


        print(
            f"Pallet {pallet} armazenado em {endereco}."
        )


        return True


    # =================================================
    # RETIRAR PALLET
    #
    # Primeiro a empilhadeira executa.
    # Só depois o banco é atualizado.
    # =================================================

    def retirar_pallet(
        self,
        endereco
    ):

        # ---------------------------------------------
        # VERIFICAR CONTROLADOR
        # ---------------------------------------------

        if self.forklift is None:

            print(
                "ERRO: controlador da empilhadeira não configurado."
            )

            return False


        # ---------------------------------------------
        # VERIFICAR CONEXÃO
        # ---------------------------------------------

        if not self.mks.conectado:

            print(
                "ERRO: MKS desconectada."
            )

            return False


        # ---------------------------------------------
        # PEGAR O PALLET ATUAL
        # ---------------------------------------------

        dados = self.db.buscar_posicao(
            endereco
        )


        if dados is None:

            print(
                "ERRO: posição não encontrada:",
                endereco
            )

            return False


        ocupado = dados[1]

        pallet = dados[2]


        if not ocupado:

            print(
                "ERRO: posição vazia:",
                endereco
            )

            return False


        # ---------------------------------------------
        # EXECUTAR RETIRADA FÍSICA
        # ---------------------------------------------

        sucesso = self.forklift.retirar_pallet(
            endereco
        )


        if not sucesso:

            print(
                "ERRO: retirada não concluída."
            )

            return False


        # ---------------------------------------------
        # ATUALIZAR BANCO
        # ---------------------------------------------

        self.db.liberar_posicao(
            endereco
        )


        self.db.registrar_movimento(
            endereco,
            "Expedição",
            "Retirado"
        )


        print(
            f"Pallet {pallet} retirado de {endereco}."
        )


        return True


    # =================================================
    # BUSCAR POSIÇÃO
    # =================================================

    def buscar_posicao(
        self,
        endereco
    ):

        return self.db.buscar_posicao(
            endereco
        )