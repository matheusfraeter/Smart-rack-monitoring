"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: rack.py
 Descrição...: Visualização e controle do Rack
=========================================================
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame,
    QScrollArea,
    QMessageBox
)

from PySide6.QtCore import (
    Qt,
    QThread,
    Signal
)

from controllers.rack_controller import RackController

from ui.widgets.pallet_dialog import PalletDialog
from ui.widgets.rack_action_dialog import RackActionDialog


# =========================================================
# WORKER DE OPERAÇÃO AUTOMÁTICA
# =========================================================

class RackWorker(QThread):

    concluido = Signal(
        bool,
        str
    )

    def __init__(
        self,
        controller,
        operacao,
        endereco,
        pallet=None
    ):

        super().__init__()

        self.controller = controller

        self.operacao = operacao

        self.endereco = endereco

        self.pallet = pallet


    # =====================================================
    # EXECUTAR
    # =====================================================

    def run(self):

        try:

            # ---------------------------------------------
            # ARMAZENAMENTO
            # ---------------------------------------------

            if self.operacao == "armazenar":

                sucesso = (
                    self.controller.armazenar_pallet(
                        self.endereco,
                        self.pallet
                    )
                )

                if sucesso:

                    self.concluido.emit(
                        True,
                        (
                            f"Pallet {self.pallet} "
                            f"armazenado em {self.endereco}."
                        )
                    )

                else:

                    self.concluido.emit(
                        False,
                        (
                            "Falha no armazenamento. "
                            "A posição não foi alterada."
                        )
                    )

                return


            # ---------------------------------------------
            # RETIRADA
            # ---------------------------------------------

            if self.operacao == "retirar":

                sucesso = (
                    self.controller.retirar_pallet(
                        self.endereco
                    )
                )

                if sucesso:

                    self.concluido.emit(
                        True,
                        (
                            f"Pallet {self.pallet} "
                            f"retirado de {self.endereco} "
                            "e enviado para expedição."
                        )
                    )

                else:

                    self.concluido.emit(
                        False,
                        (
                            "Falha na retirada. "
                            "A posição não foi alterada."
                        )
                    )

                return


            self.concluido.emit(
                False,
                "Operação desconhecida."
            )


        except Exception as erro:

            print()
            print(
                "ERRO NO WORKER DO RACK:"
            )

            print(
                erro
            )

            self.concluido.emit(
                False,
                (
                    "Erro durante a operação: "
                    f"{erro}"
                )
            )


# =========================================================
# PÁGINA DO RACK
# =========================================================

class RackPage(QWidget):

    def __init__(
        self,
        mks
    ):

        super().__init__()

        # =====================================
        # COMUNICAÇÃO
        # =====================================

        self.mks = mks

        # =====================================
        # CONTROLLER
        # =====================================

        self.controller = RackController(
            self.mks
        )

        # =====================================
        # BOTÕES DO RACK
        # =====================================

        self.botoes = {}

        # =====================================
        # OPERAÇÃO EM ANDAMENTO
        # =====================================

        self.operacao_em_andamento = False

        self.worker = None

        # =====================================
        # CONFIGURAÇÃO DO RACK
        # =====================================

        self.estantes = [
            "A",
            "B"
        ]

        self.niveis = 3

        self.colunas = 4

        self.criar_interface()


    # =================================================
    # INTERFACE
    # =================================================

    def criar_interface(self):

        principal = QVBoxLayout(
            self
        )

        principal.setContentsMargins(
            20,
            20,
            20,
            20
        )

        principal.setSpacing(
            15
        )

        # =====================================
        # TÍTULO
        # =====================================

        titulo = QLabel(
            "SMART RACK"
        )

        titulo.setObjectName(
            "title"
        )

        self.selecionado = QLabel(
            "Selecione uma posição."
        )

        self.selecionado.setObjectName(
            "rackStatus"
        )

        principal.addWidget(
            titulo
        )

        principal.addWidget(
            self.selecionado
        )

        # =====================================
        # PAINEL DE OPERAÇÃO
        # =====================================

        self.operacao_box = QFrame()

        self.operacao_box.setObjectName(
            "controlBox"
        )

        operacao_layout = QHBoxLayout(
            self.operacao_box
        )

        self.pallet_label = QLabel(
            "Pallet: ---"
        )

        self.posicao_label = QLabel(
            "Posição: ---"
        )

        operacao_layout.addWidget(
            self.pallet_label
        )

        operacao_layout.addSpacing(
            30
        )

        operacao_layout.addWidget(
            self.posicao_label
        )

        operacao_layout.addStretch()

        principal.addWidget(
            self.operacao_box
        )

        # =====================================
        # ÁREA COM ROLAGEM
        # =====================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.NoFrame
        )

        conteudo = QWidget()

        self.layout_racks = QVBoxLayout(
            conteudo
        )

        self.layout_racks.setSpacing(
            30
        )

        for estante in self.estantes:

            frame = self.criar_estante(
                estante
            )

            self.layout_racks.addWidget(
                frame
            )

        self.layout_racks.addStretch()

        scroll.setWidget(
            conteudo
        )

        principal.addWidget(
            scroll
        )

        # =====================================
        # ATUALIZAR
        # =====================================

        self.atualizar_tela()


    # =================================================
    # CRIAR ESTANTE
    # =================================================

    def criar_estante(
        self,
        estante
    ):

        frame = QFrame()

        frame.setObjectName(
            "rackFrame"
        )

        layout = QVBoxLayout(
            frame
        )

        titulo = QLabel(
            f"ESTANTE {estante}"
        )

        titulo.setObjectName(
            "rackTitle"
        )

        layout.addWidget(
            titulo
        )

        grade = QGridLayout()

        grade.setSpacing(
            10
        )

        # =====================================
        # CABEÇALHO DAS COLUNAS
        # =====================================

        for coluna in range(
            1,
            self.colunas + 1
        ):

            label = QLabel(
                str(coluna)
            )

            label.setObjectName(
                "rackLabel"
            )

            label.setAlignment(
                Qt.AlignCenter
            )

            grade.addWidget(
                label,
                0,
                coluna
            )

        linha = 1

        # =====================================
        # CÉLULAS
        # =====================================

        for nivel in range(
            self.niveis,
            0,
            -1
        ):

            nivel_label = QLabel(
                f"Nível {nivel}"
            )

            nivel_label.setObjectName(
                "rackLabel"
            )

            grade.addWidget(
                nivel_label,
                linha,
                0
            )

            for coluna in range(
                1,
                self.colunas + 1
            ):

                endereco = (
                    f"{estante}"
                    f"{nivel}"
                    f"{coluna}"
                )

                botao = QPushButton()

                botao.setMinimumSize(
                    90,
                    70
                )

                botao.clicked.connect(
                    lambda checked=False,
                    e=endereco:
                    self.selecionar(e)
                )

                self.botoes[endereco] = botao

                grade.addWidget(
                    botao,
                    linha,
                    coluna
                )

            linha += 1

        layout.addLayout(
            grade
        )

        return frame


    # =================================================
    # SELECIONAR POSIÇÃO
    # =================================================

    def selecionar(
        self,
        endereco
    ):

        # =====================================
        # NÃO PERMITIR NOVA OPERAÇÃO
        # DURANTE UMA OPERAÇÃO AUTOMÁTICA
        # =====================================

        if self.operacao_em_andamento:

            QMessageBox.information(
                self,
                "Operação em andamento",
                "Aguarde a operação atual terminar."
            )

            return


        dados = self.controller.buscar_posicao(
            endereco
        )

        if dados is None:

            QMessageBox.warning(
                self,
                "Erro",
                f"A posição {endereco} não foi encontrada."
            )

            return

        ocupado = dados[1]

        pallet = dados[2]

        # =====================================
        # MOSTRAR SELEÇÃO
        # =====================================

        self.posicao_label.setText(
            f"Posição: {endereco}"
        )

        # =====================================
        # POSIÇÃO OCUPADA
        # =====================================

        if ocupado:

            self.pallet_label.setText(
                f"Pallet: {pallet}"
            )

            self.selecionado.setText(
                f"Pallet {pallet} localizado em {endereco}."
            )

            self.confirmar_retirada(
                endereco,
                pallet
            )

            return

        # =====================================
        # POSIÇÃO VAZIA
        # =====================================

        self.pallet_label.setText(
            "Pallet: ---"
        )

        self.selecionado.setText(
            f"Posição {endereco} disponível."
        )

        self.confirmar_armazenamento(
            endereco
        )


    # =================================================
    # CONFIRMAR ARMAZENAMENTO
    # =================================================

    def confirmar_armazenamento(
        self,
        endereco
    ):

        dialog = PalletDialog(
            endereco
        )

        if not dialog.exec():

            return

        codigo = dialog.obter_pallet()

        if not codigo:

            return

        resposta = QMessageBox.question(
            self,
            "Confirmar armazenamento",
            (
                f"Pallet: {codigo}\n\n"
                f"Destino: {endereco}\n\n"
                "Deseja iniciar o armazenamento?"
            ),
            QMessageBox.Yes |
            QMessageBox.No,
            QMessageBox.No
        )

        if resposta != QMessageBox.Yes:

            return

        # =====================================
        # INICIAR OPERAÇÃO
        # =====================================

        self.iniciar_operacao(
            operacao="armazenar",
            endereco=endereco,
            pallet=codigo
        )


    # =================================================
    # CONFIRMAR RETIRADA
    # =================================================

    def confirmar_retirada(
        self,
        endereco,
        pallet
    ):

        resposta = QMessageBox.question(
            self,
            "Retirar pallet",
            (
                f"Pallet: {pallet}\n\n"
                f"Origem: {endereco}\n"
                "Destino: EXPEDIÇÃO\n\n"
                "Deseja iniciar a retirada?"
            ),
            QMessageBox.Yes |
            QMessageBox.No,
            QMessageBox.No
        )

        if resposta != QMessageBox.Yes:

            return

        # =====================================
        # INICIAR OPERAÇÃO
        # =====================================

        self.iniciar_operacao(
            operacao="retirar",
            endereco=endereco,
            pallet=pallet
        )


    # =================================================
    # INICIAR OPERAÇÃO
    # =================================================

    def iniciar_operacao(
        self,
        operacao,
        endereco,
        pallet=None
    ):

        if self.operacao_em_andamento:

            return

        if not self.mks.conectado:

            QMessageBox.warning(
                self,
                "MKS desconectada",
                "Conecte a MKS antes de iniciar a operação."
            )

            return

        self.operacao_em_andamento = True

        # =====================================
        # DESABILITAR RACK
        # =====================================

        self.definir_rack_habilitado(
            False
        )

        # =====================================
        # MENSAGEM
        # =====================================

        if operacao == "armazenar":

            self.selecionado.setText(
                f"Armazenando pallet {pallet} "
                f"em {endereco}..."
            )

        else:

            self.selecionado.setText(
                f"Retirando pallet {pallet} "
                f"de {endereco}..."
            )

        # =====================================
        # CRIAR WORKER
        # =====================================

        self.worker = RackWorker(
            self.controller,
            operacao,
            endereco,
            pallet
        )

        self.worker.concluido.connect(
            self.operacao_concluida
        )

        self.worker.finished.connect(
            self.worker_finalizado
        )

        self.worker.start()


    # =================================================
    # OPERAÇÃO CONCLUÍDA
    # =================================================

    def operacao_concluida(
        self,
        sucesso,
        mensagem
    ):

        self.selecionado.setText(
            mensagem
        )

        # -------------------------------------
        # ATUALIZAR VISUAL
        # -------------------------------------

        self.atualizar_tela()


    # =================================================
    # WORKER FINALIZADO
    # =================================================

    def worker_finalizado(self):

        self.operacao_em_andamento = False

        self.definir_rack_habilitado(
            True
        )

        self.worker = None

        self.atualizar_tela()


    # =================================================
    # HABILITAR / DESABILITAR RACK
    # =================================================

    def definir_rack_habilitado(
        self,
        habilitado
    ):

        for botao in self.botoes.values():

            botao.setEnabled(
                habilitado
            )


    # =================================================
    # ATUALIZAR TELA
    # =================================================

    def atualizar_tela(self):

        posicoes = self.controller.listar_posicoes()

        for endereco, ocupado, pallet in posicoes:

            if endereco in self.botoes:

                self.atualizar_cor(
                    self.botoes[endereco],
                    ocupado
                )


    # =================================================
    # ATUALIZAR COR DOS BOTÕES
    # =================================================

    def atualizar_cor(
        self,
        botao,
        ocupado
    ):

        if ocupado:

            botao.setText(
                "📦"
            )

            botao.setStyleSheet("""
                QPushButton{

                    background-color:#DC2626;

                    color:white;

                    font-size:28px;

                    font-weight:bold;

                    border:none;

                    border-radius:10px;

                }

                QPushButton:hover{

                    background-color:#EF4444;

                }
            """)

        else:

            botao.setText(
                ""
            )

            botao.setStyleSheet("""
                QPushButton{

                    background-color:#16A34A;

                    border:none;

                    border-radius:10px;

                }

                QPushButton:hover{

                    background-color:#22C55E;

                }
            """)


    # =================================================
    # FINALIZAÇÃO DA PÁGINA
    # =================================================

    def closeEvent(
        self,
        event
    ):

        if (
            self.worker is not None
            and self.worker.isRunning()
        ):

            QMessageBox.warning(
                self,
                "Operação em andamento",
                "Finalize a operação antes de fechar o aplicativo."
            )

            event.ignore()

            return

        event.accept()