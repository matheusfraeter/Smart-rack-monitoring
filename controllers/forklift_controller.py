"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: forklift_controller.py
 Descrição...: Controle automático da empilhadeira
=========================================================
"""

import time

from database import Database


class ForkliftController:

    def __init__(self, mks):

        self.mks = mks

        self.db = Database()

        self.executando = False

        # =================================================
        # VELOCIDADES PADRÃO
        # =================================================

        self.velocidade_x = 1000
        self.velocidade_y = 1000
        self.velocidade_z = 500

        # =================================================
        # CONFIRMAÇÃO DE MOVIMENTO
        # =================================================

        self.timeout_movimento = 30.0

        self.intervalo_verificacao = 0.05


    # =====================================================
    # VERIFICAR CONEXÃO
    # =====================================================

    def conectado(self):

        return bool(
            self.mks.conectado
        )


    # =====================================================
    # OBTER VELOCIDADE
    # =====================================================

    def obter_velocidade(
        self,
        nome,
        padrao
    ):

        valor = (
            self.db.obter_configuracao_empilhadeira(
                nome
            )
        )

        if valor is None:

            return padrao

        try:

            valor = float(
                valor
            )

        except (
            ValueError,
            TypeError
        ):

            print(
                f"ERRO: velocidade inválida: {nome}"
            )

            return padrao

        if valor <= 0:

            print(
                f"ERRO: velocidade deve ser maior que zero: {nome}"
            )

            return padrao

        return valor


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
    # AGUARDAR POSIÇÃO
    # =====================================================

    def aguardar_posicao(
        self,
        eixo,
        destino,
        posicao_inicial
    ):

        try:

            destino = float(
                destino
            )

            posicao_inicial = float(
                posicao_inicial
            )

        except (
            ValueError,
            TypeError
        ):

            print(
                "ERRO: posição inválida."
            )

            return False


        inicio = time.monotonic()

        movimento_detectado = False


        print()
        print(
            "------------------------------------"
        )

        print(
            f"AGUARDANDO {eixo}"
        )

        print(
            f"Inicial: {posicao_inicial}"
        )

        print(
            f"Destino: {destino}"
        )

        print(
            "------------------------------------"
        )


        while True:

            if not self.conectado():

                print(
                    "ERRO: MKS desconectada durante movimento."
                )

                return False


            status = self.mks.ler_status()


            atual = status.get(
                eixo
            )


            estado = status.get(
                "estado",
                ""
            )


            if atual is None:

                time.sleep(
                    self.intervalo_verificacao
                )

                continue


            try:

                atual = float(
                    atual
                )

            except (
                ValueError,
                TypeError
            ):

                time.sleep(
                    self.intervalo_verificacao
                )

                continue


            # -----------------------------------------
            # Detectar deslocamento
            # -----------------------------------------

            if atual != posicao_inicial:

                movimento_detectado = True


            print(
                f"{eixo}: {atual} | "
                f"Destino: {destino} | "
                f"Estado: {estado}"
            )


            # -----------------------------------------
            # CONFIRMAÇÃO EXATA
            # -----------------------------------------

            if (
                movimento_detectado
                and atual == destino
            ):

                print(
                    f"{eixo} chegou exatamente em {destino}."
                )

                return True


            # -----------------------------------------
            # Já estava no destino
            # -----------------------------------------

            if (
                not movimento_detectado
                and atual == destino
            ):

                print(
                    f"{eixo} já estava em {destino}."
                )

                return True


            # -----------------------------------------
            # TIMEOUT
            # -----------------------------------------

            if (
                time.monotonic() - inicio
                >= self.timeout_movimento
            ):

                print()
                print(
                    "ERRO: timeout aguardando movimento."
                )

                print(
                    f"Eixo: {eixo}"
                )

                print(
                    f"Esperado: {destino}"
                )

                print(
                    f"Atual: {atual}"
                )

                print(
                    f"Estado: {estado}"
                )

                return False


            time.sleep(
                self.intervalo_verificacao
            )


    # =====================================================
    # OBTER POSIÇÃO ATUAL
    # =====================================================

    def obter_posicao_atual(
        self,
        eixo
    ):

        status = self.mks.ler_status()

        valor = status.get(
            eixo
        )


        if valor is None:

            print(
                f"ERRO: não foi possível ler {eixo}."
            )

            return None


        try:

            return float(
                valor
            )

        except (
            ValueError,
            TypeError
        ):

            print(
                f"ERRO: valor atual de {eixo} inválido:",
                valor
            )

            return None


    # =====================================================
    # GARANTIR X = 0 ANTES DE MOVER Y
    #
    # REGRA DE SEGURANÇA:
    # Y só pode se movimentar quando X estiver em 0.
    # =====================================================

    def garantir_x_zero_antes_y(self):

        x_atual = self.obter_posicao_atual(
            "X"
        )

        if x_atual is None:

            return False


        if x_atual == 0:

            print(
                "SEGURANÇA Y: X já está em 0."
            )

            return True


        print()
        print(
            "===================================="
        )

        print(
            " SEGURANÇA ANTES DO Y"
        )

        print(
            "===================================="
        )

        print(
            f"X atual: {x_atual}"
        )

        print(
            "X precisa estar em 0 antes de mover Y."
        )

        print(
            "Movendo X para 0..."
        )

        print(
            "===================================="
        )


        if not self.mover_x(
            0
        ):

            print(
                "ERRO: não foi possível colocar X em 0."
            )

            return False


        x_confirmacao = self.obter_posicao_atual(
            "X"
        )


        if x_confirmacao is None:

            return False


        if x_confirmacao != 0:

            print(
                f"ERRO DE SEGURANÇA: X ainda está em "
                f"{x_confirmacao}."
            )

            return False


        print(
            "X está em 0. Y liberado."
        )

        return True


    # =====================================================
    # OBTER AJUSTE Z
    # =====================================================

    def obter_ajuste_z(
        self,
        nome
    ):

        valor = (
            self.db.obter_configuracao_empilhadeira(
                nome
            )
        )


        if valor is None:

            print(
                f"ERRO: configuração não encontrada: {nome}"
            )

            return None


        try:

            valor = float(
                valor
            )

        except (
            ValueError,
            TypeError
        ):

            print(
                f"ERRO: configuração inválida: {nome}"
            )

            return None


        return valor


    # =====================================================
    # LEVANTAR PALLET
    #
    # Neste eixo:
    # aumentar Z = descer
    # diminuir Z = subir
    #
    # LEVANTAR = Z atual - Z_LEVANTAR
    # =====================================================

    def levantar_pallet(self):

        ajuste = self.obter_ajuste_z(
            "Z_LEVANTAR"
        )


        if ajuste is None:

            return False


        z_atual = self.obter_posicao_atual(
            "Z"
        )


        if z_atual is None:

            return False


        destino = (
            z_atual - ajuste
        )


        print()
        print(
            "===================================="
        )

        print(
            " LEVANTAR PALLET"
        )

        print(
            "===================================="
        )

        print(
            f"Z atual: {z_atual}"
        )

        print(
            f"Ajuste: -{ajuste}"
        )

        print(
            f"Z destino: {destino}"
        )

        print(
            "===================================="
        )


        return self.mover_z(
            destino
        )


    # =====================================================
    # APOIAR PALLET
    #
    # Neste eixo:
    # aumentar Z = descer
    # diminuir Z = subir
    #
    # APOIAR = Z atual + Z_APOIAR
    # =====================================================

    def apoiar_pallet(self):

        ajuste = self.obter_ajuste_z(
            "Z_APOIAR"
        )


        if ajuste is None:

            return False


        z_atual = self.obter_posicao_atual(
            "Z"
        )


        if z_atual is None:

            return False


        destino = (
            z_atual + ajuste
        )


        print()
        print(
            "===================================="
        )

        print(
            " APOIAR PALLET"
        )

        print(
            "===================================="
        )

        print(
            f"Z atual: {z_atual}"
        )

        print(
            f"Ajuste: +{ajuste}"
        )

        print(
            f"Z destino: {destino}"
        )

        print(
            "===================================="
        )


        return self.mover_z(
            destino
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


        x_atual = self.obter_posicao_atual(
            "X"
        )


        if x_atual is None:

            return False


        velocidade = self.obter_velocidade(
            "VELOCIDADE_X",
            self.velocidade_x
        )


        comando = (
            "G90\n"
            f"G1 X{x:g} F{velocidade:g}"
        )


        print(
            f"Velocidade X: {velocidade:g} mm/min"
        )


        if not self.enviar(
            comando
        ):

            return False


        return self.aguardar_posicao(
            "X",
            x,
            x_atual
        )


    # =====================================================
    # MOVER Y
    #
    # REGRA:
    # X precisa estar em 0 antes do movimento de Y.
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


        # -----------------------------------------
        # GARANTIR SEGURANÇA
        # -----------------------------------------

        if not self.garantir_x_zero_antes_y():

            return False


        y_atual = self.obter_posicao_atual(
            "Y"
        )


        if y_atual is None:

            return False


        velocidade = self.obter_velocidade(
            "VELOCIDADE_Y",
            self.velocidade_y
        )


        comando = (
            "G90\n"
            f"G1 Y{y:g} F{velocidade:g}"
        )


        print(
            f"Velocidade Y: {velocidade:g} mm/min"
        )


        if not self.enviar(
            comando
        ):

            return False


        return self.aguardar_posicao(
            "Y",
            y,
            y_atual
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


        z_atual = self.obter_posicao_atual(
            "Z"
        )


        if z_atual is None:

            return False


        velocidade = self.obter_velocidade(
            "VELOCIDADE_Z",
            self.velocidade_z
        )


        comando = (
            "G90\n"
            f"G1 Z{z:g} F{velocidade:g}"
        )


        print(
            f"Velocidade Z: {velocidade:g} mm/min"
        )


        if not self.enviar(
            comando
        ):

            return False


        return self.aguardar_posicao(
            "Z",
            z,
            z_atual
        )


    # =====================================================
    # MOVER XY
    #
    # PRIMEIRO GARANTE X = 0
    # DEPOIS Y
    # =====================================================

    def mover_xy(
        self,
        x,
        y
    ):

        if not self.garantir_x_zero_antes_y():

            return False


        if not self.mover_y(
            y
        ):

            return False


        if not self.mover_x(
            x
        ):

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
    #
    # REGRA DE SEGURANÇA:
    #
    # X = 0
    # ↓
    # Y da posição
    # ↓
    # X da posição
    # ↓
    # Z da posição
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
        # PRIMEIRO X = 0
        # -----------------------------------------

        if not self.mover_x(
            0
        ):

            return False


        # -----------------------------------------
        # DEPOIS Y
        # -----------------------------------------

        if not self.mover_y(
            posicao["Y"]
        ):

            return False


        # -----------------------------------------
        # DEPOIS X FINAL
        # -----------------------------------------

        if not self.mover_x(
            posicao["X"]
        ):

            return False


        # -----------------------------------------
        # POR ÚLTIMO Z
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
    #
    # REGRA DE SEGURANÇA:
    #
    # X = 0
    # ↓
    # Y da célula
    # ↓
    # X da célula
    # ↓
    # Z da célula
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
        # PRIMEIRO X = 0
        # -----------------------------------------

        if not self.mover_x(
            0
        ):

            return False


        # -----------------------------------------
        # DEPOIS Y
        # -----------------------------------------

        if not self.mover_y(
            coordenadas["Y"]
        ):

            return False


        # -----------------------------------------
        # DEPOIS X FINAL
        # -----------------------------------------

        if not self.mover_x(
            coordenadas["X"]
        ):

            return False


        # -----------------------------------------
        # POR ÚLTIMO Z
        # -----------------------------------------

        if not self.mover_z(
            coordenadas["Z"]
        ):

            return False


        return True


    # =====================================================
    # ACIONAR GARFO
    #
    # HIGH por 5,5 segundos.
    # =====================================================

    def acionar_garfo(self):

        if not self.conectado():

            return False


        print()
        print(
            "===================================="
        )

        print(
            " ACIONANDO GARFO"
        )

        print(
            "===================================="
        )


        if not self.enviar(
            "M3 S1000"
        ):

            return False


        print(
            "Mantendo TTL HIGH por 5,5 segundo..."
        )


        time.sleep(
            5.5
        )


        if not self.enviar(
            "M3 S0"
        ):

            return False


        print(
            "Garfo acionado."
        )


        return True


    # =====================================================
    # ARMAZENAR PALLET
    #
    # RECEBIMENTO
    # ↓
    # APOIAR
    # ↓
    # PEGAR
    # ↓
    # LEVANTAR
    # ↓
    # AJUSTAR GARFO
    # ↓
    # X = 0
    # ↓
    # Z TRANSPORTE
    # ↓
    # CÉLULA
    # ↓
    # SOLTAR
    # ↓
    # APOIAR
    # ↓
    # RECOLHER GARFO
    # ↓
    # Z TRANSPORTE
    # ↓
    # ZERO
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
            # 1. RECEBIMENTO
            # -----------------------------------------

            print(
                "ETAPA 1 - RECEBIMENTO"
            )


            if not self.mover_para_posicao_maquina(
                "RECEBIMENTO"
            ):

                return False


            # -----------------------------------------
            # 2. APOIAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 2 - APOIAR PALLET"
            )


            if not self.apoiar_pallet():

                return False


            # -----------------------------------------
            # 3. PEGAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 3 - PEGAR PALLET"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 4. LEVANTAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 4 - LEVANTAR PALLET"
            )


            if not self.levantar_pallet():

                return False


            # -----------------------------------------
            # 5. AJUSTAR GARFO
            # -----------------------------------------

            print(
                "ETAPA 5 - AJUSTAR GARFO"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 6. X SEGURO = 0
            # -----------------------------------------

            print(
                "ETAPA 6 - X SEGURO"
            )


            if not self.mover_x(
                0
            ):

                return False


            # -----------------------------------------
            # 7. Z TRANSPORTE
            # -----------------------------------------

            print(
                "ETAPA 7 - Z TRANSPORTE"
            )


            if not self.ir_para_z_transporte():

                return False


            # -----------------------------------------
            # 8. DESTINO
            # -----------------------------------------

            print(
                "ETAPA 8 - DESTINO"
            )


            if not self.mover_para_celula(
                destino
            ):

                return False


            # -----------------------------------------
            # 9. SOLTAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 9 - SOLTAR PALLET"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 10. APOIAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 10 - APOIAR PALLET"
            )


            if not self.apoiar_pallet():

                return False


            # -----------------------------------------
            # 11. RECOLHER GARFO
            # -----------------------------------------

            print(
                "ETAPA 11 - RECOLHER GARFO"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 12. Z TRANSPORTE
            # -----------------------------------------

            print(
                "ETAPA 12 - Z TRANSPORTE"
            )


            if not self.ir_para_z_transporte():

                return False


            # -----------------------------------------
            # 13. VOLTAR PARA ZERO
            # -----------------------------------------

            print(
                "ETAPA 13 - RETORNAR PARA ZERO"
            )


            if not self.mover_x(
                0
            ):

                return False


            if not self.mover_y(
                0
            ):

                return False


            if not self.mover_z(
                0
            ):

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
    # APOIAR
    # ↓
    # PEGAR
    # ↓
    # LEVANTAR
    # ↓
    # AJUSTAR GARFO
    # ↓
    # X = 0
    # ↓
    # Z TRANSPORTE
    # ↓
    # EXPEDIÇÃO
    # ↓
    # SOLTAR
    # ↓
    # APOIAR
    # ↓
    # RECOLHER GARFO
    # ↓
    # Z TRANSPORTE
    # ↓
    # ZERO
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
                "ETAPA 1 - IR PARA CÉLULA"
            )


            if not self.mover_para_celula(
                origem
            ):

                return False


            # -----------------------------------------
            # 2. APOIAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 2 - APOIAR PALLET"
            )


            if not self.apoiar_pallet():

                return False


            # -----------------------------------------
            # 3. PEGAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 3 - PEGAR PALLET"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 4. LEVANTAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 4 - LEVANTAR PALLET"
            )


            if not self.levantar_pallet():

                return False


            # -----------------------------------------
            # 5. AJUSTAR GARFO
            # -----------------------------------------

            print(
                "ETAPA 5 - AJUSTAR GARFO"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 6. X SEGURO = 0
            # -----------------------------------------

            print(
                "ETAPA 6 - X SEGURO"
            )


            if not self.mover_x(
                0
            ):

                return False


            # -----------------------------------------
            # 7. Z TRANSPORTE
            # -----------------------------------------

            print(
                "ETAPA 7 - Z TRANSPORTE"
            )


            if not self.ir_para_z_transporte():

                return False


            # -----------------------------------------
            # 8. EXPEDIÇÃO
            # -----------------------------------------

            print(
                "ETAPA 8 - EXPEDIÇÃO"
            )


            if not self.mover_para_posicao_maquina(
                "EXPEDICAO"
            ):

                return False


            # -----------------------------------------
            # 9. SOLTAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 9 - SOLTAR PALLET"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 10. APOIAR PALLET
            # -----------------------------------------

            print(
                "ETAPA 10 - APOIAR PALLET"
            )


            if not self.apoiar_pallet():

                return False


            # -----------------------------------------
            # 11. RECOLHER GARFO
            # -----------------------------------------

            print(
                "ETAPA 11 - RECOLHER GARFO"
            )


            if not self.acionar_garfo():

                return False


            # -----------------------------------------
            # 12. Z TRANSPORTE
            # -----------------------------------------

            print(
                "ETAPA 12 - Z TRANSPORTE"
            )


            if not self.ir_para_z_transporte():

                return False


            # -----------------------------------------
            # 13. VOLTAR PARA ZERO
            # -----------------------------------------

            print(
                "ETAPA 13 - RETORNAR PARA ZERO"
            )


            if not self.mover_x(
                0
            ):

                return False


            if not self.mover_y(
                0
            ):

                return False


            if not self.mover_z(
                0
            ):

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