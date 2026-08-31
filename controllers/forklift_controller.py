"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: forklift_controller.py
 Descrição...: Controle automático da empilhadeira
=========================================================
"""

from database import Database


class ForkliftController:

    def __init__(self, mks):

        self.mks = mks

        self.db = Database()

        self.executando = False


        # =================================================
        # VELOCIDADES
        # =================================================

        self.velocidade_xy = 1000

        self.velocidade_z = 500


    # =====================================================
    # VERIFICAR CONEXÃO
    # =====================================================

    def conectado(self):

        return bool(
            self.mks.conectado
        )


    # =====================================================
    # ENVIAR COMANDO
    # =====================================================

    def enviar(self, comando):

        if not self.conectado():

            print(
                "ERRO: MKS desconectada."
            )

            return False


        print()
        print(
            "===================================="
        )

        print(
            " COMANDO AUTOMÁTICO"
        )

        print(
            "===================================="
        )

        print(
            comando
        )

        print(
            "===================================="
        )


        return self.mks.enviar_comando(
            comando
        )


    # =====================================================
    # MOVER X
    # =====================================================

    def mover_x(
        self,
        x
    ):

        try:

            x = float(x)

        except (
            ValueError,
            TypeError
        ):

            print(
                "ERRO: X inválido:",
                x
            )

            return False


        comando = (
            "G90\n"
            f"G0 X{x:g} F{self.velocidade_xy}"
        )


        return self.enviar(
            comando
        )


    # =====================================================
    # MOVER Y
    # =====================================================

    def mover_y(
        self,
        y
    ):

        try:

            y = float(y)

        except (
            ValueError,
            TypeError
        ):

            print(
                "ERRO: Y inválido:",
                y
            )

            return False


        comando = (
            "G90\n"
            f"G0 Y{y:g} F{self.velocidade_xy}"
        )


        return self.enviar(
            comando
        )


    # =====================================================
    # MOVER Z
    # =====================================================

    def mover_z(
        self,
        z
    ):

        try:

            z = float(z)

        except (
            ValueError,
            TypeError
        ):

            print(
                "ERRO: Z inválido:",
                z
            )

            return False


        comando = (
            "G90\n"
            f"G0 Z{z:g} F{self.velocidade_z}"
        )


        return self.enviar(
            comando
        )


    # =====================================================
    # MOVER XY
    #
    # PRIMEIRO X
    # DEPOIS Y
    # =====================================================

    def mover_xy(
        self,
        x,
        y
    ):

        if not self.mover_x(x):

            return False


        if not self.mover_y(y):

            return False


        return True


    # =====================================================
    # OBTER COORDENADAS DO RACK
    # =====================================================

    def obter_coordenadas(
        self,
        endereco
    ):

        coordenadas = self.db.obter_coordenadas(
            endereco
        )


        if coordenadas is None:

            print(
                "ERRO: coordenadas não encontradas:",
                endereco
            )

            return None


        return coordenadas


    # =====================================================
    # OBTER POSIÇÃO ESPECIAL
    #
    # RECEBIMENTO
    # EXPEDICAO
    # Z_TRANSPORTE
    # =====================================================

    def obter_posicao_maquina(
        self,
        nome
    ):

        posicao = self.db.obter_posicao_maquina(
            nome
        )


        if posicao is None:

            print(
                "ERRO: posição da máquina não encontrada:",
                nome
            )

            return None


        return posicao


    # =====================================================
    # MOVER PARA POSIÇÃO ESPECIAL
    # =====================================================

    def mover_para_posicao_maquina(
        self,
        nome
    ):

        posicao = self.obter_posicao_maquina(
            nome
        )


        if posicao is None:

            return False


        print()
        print(
            "===================================="
        )

        print(
            " POSIÇÃO DA MÁQUINA"
        )

        print(
            "===================================="
        )

        print(
            "Nome:",
            nome
        )

        print(
            "X:",
            posicao["X"]
        )

        print(
            "Y:",
            posicao["Y"]
        )

        print(
            "Z:",
            posicao["Z"]
        )

        print(
            "===================================="
        )


        # -----------------------------------------
        # X
        # -----------------------------------------

        if not self.mover_x(
            posicao["X"]
        ):

            return False


        # -----------------------------------------
        # Y
        # -----------------------------------------

        if not self.mover_y(
            posicao["Y"]
        ):

            return False


        # -----------------------------------------
        # Z
        # -----------------------------------------

        if not self.mover_z(
            posicao["Z"]
        ):

            return False


        return True


    # =====================================================
    # IR PARA Z DE TRANSPORTE
    # =====================================================

    def ir_para_z_transporte(self):

        posicao = self.obter_posicao_maquina(
            "Z_TRANSPORTE"
        )


        if posicao is None:

            return False


        z = posicao["Z"]


        print(
            "Z de transporte:",
            z
        )


        return self.mover_z(
            z
        )


    # =====================================================
    # MOVER PARA CÉLULA
    # =====================================================

    def mover_para_celula(
        self,
        endereco
    ):

        coordenadas = self.obter_coordenadas(
            endereco
        )


        if coordenadas is None:

            return False


        print()
        print(
            "===================================="
        )

        print(
            " MOVENDO PARA CÉLULA"
        )

        print(
            "===================================="
        )

        print(
            "Célula:",
            endereco
        )

        print(
            "X:",
            coordenadas["X"]
        )

        print(
            "Y:",
            coordenadas["Y"]
        )

        print(
            "Z:",
            coordenadas["Z"]
        )

        print(
            "===================================="
        )


        # -----------------------------------------
        # XY
        # -----------------------------------------

        if not self.mover_xy(
            coordenadas["X"],
            coordenadas["Y"]
        ):

            return False


        # -----------------------------------------
        # Z
        # -----------------------------------------

        if not self.mover_z(
            coordenadas["Z"]
        ):

            return False


        return True


    # =====================================================
    # ACIONAR GARFO
    #
    # SEM ESPERA
    #
    # M3 S1000
    # M3 S0
    # =====================================================

    def acionar_garfo(self):

        if not self.conectado():

            return False


        comando = (
            "M3 S1000\n"
            "M3 S0"
        )


        return self.enviar(
            comando
        )


    # =====================================================
    # ARMAZENAR PALLET
    #
    # RECEBIMENTO
    # ↓
    # GARFO
    # ↓
    # Z TRANSPORTE
    # ↓
    # CÉLULA
    # ↓
    # GARFO
    # ↓
    # Z TRANSPORTE
    # =====================================================

    def armazenar_pallet(
        self,
        destino
    ):

        if not self.conectado():

            return False


        if self.executando:

            print(
                "ERRO: já existe uma operação em andamento."
            )

            return False


        self.executando = True


        try:

            print()
            print(
                "===================================="
            )

            print(
                " ARMAZENAR PALLET"
            )

            print(
                "===================================="
            )

            print(
                "Destino:",
                destino
            )

            print(
                "===================================="
            )


            # -----------------------------------------
            # 1. IR PARA RECEBIMENTO
            # -----------------------------------------

            print(
                "ETAPA 1 - RECEBIMENTO"
            )


            if not self.mover_para_posicao_maquina(
                "RECEBIMENTO"
            ):

                return False


            # -----------------------------------------
            # 2. PEGAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 2 - PEGAR PALLET"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 3. SUBIR PARA TRANSPORTE
            # -----------------------------------------

            print(
                "ETAPA 3 - Z TRANSPORTE"
            )


            if not self.ir_para_z_transporte():

                return False


            # -----------------------------------------
            # 4. IR PARA DESTINO
            # -----------------------------------------

            print(
                "ETAPA 4 - DESTINO"
            )


            if not self.mover_para_celula(
                destino
            ):

                return False


            # -----------------------------------------
            # 5. SOLTAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 5 - SOLTAR PALLET"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 6. SUBIR PARA TRANSPORTE
            # -----------------------------------------

            print(
                "ETAPA 6 - Z TRANSPORTE"
            )


            if not self.ir_para_z_transporte():

                return False


            print()
            print(
                "===================================="
            )

            print(
                " ARMAZENAMENTO CONCLUÍDO"
            )

            print(
                "===================================="
            )


            return True


        finally:

            self.executando = False


    # =====================================================
    # RETIRAR PALLET
    #
    # CÉLULA
    # ↓
    # GARFO
    # ↓
    # Z TRANSPORTE
    # ↓
    # EXPEDIÇÃO
    # ↓
    # GARFO
    # ↓
    # Z TRANSPORTE
    # =====================================================

    def retirar_pallet(
        self,
        origem
    ):

        if not self.conectado():

            return False


        if self.executando:

            print(
                "ERRO: já existe uma operação em andamento."
            )

            return False


        self.executando = True


        try:

            print()
            print(
                "===================================="
            )

            print(
                " RETIRAR PALLET"
            )

            print(
                "===================================="
            )

            print(
                "Origem:",
                origem
            )

            print(
                "===================================="
            )


            # -----------------------------------------
            # 1. IR PARA CÉLULA
            # -----------------------------------------

            print(
                "ETAPA 1 - ORIGEM"
            )


            if not self.mover_para_celula(
                origem
            ):

                return False


            # -----------------------------------------
            # 2. PEGAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 2 - PEGAR PALLET"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 3. SUBIR PARA TRANSPORTE
            # -----------------------------------------

            print(
                "ETAPA 3 - Z TRANSPORTE"
            )


            if not self.ir_para_z_transporte():

                return False


            # -----------------------------------------
            # 4. IR PARA EXPEDIÇÃO
            # -----------------------------------------

            print(
                "ETAPA 4 - EXPEDIÇÃO"
            )


            if not self.mover_para_posicao_maquina(
                "EXPEDICAO"
            ):

                return False


            # -----------------------------------------
            # 5. SOLTAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 5 - SOLTAR PALLET"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 6. SUBIR PARA TRANSPORTE
            # -----------------------------------------

            print(
                "ETAPA 6 - Z TRANSPORTE"
            )


            if not self.ir_para_z_transporte():

                return False


            print()
            print(
                "===================================="
            )

            print(
                " RETIRADA CONCLUÍDA"
            )

            print(
                "===================================="
            )


            return True


        finally:

            self.executando = False