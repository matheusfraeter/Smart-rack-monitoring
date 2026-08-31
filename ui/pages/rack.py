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

from PySide6.QtCore import Qt

from controllers.rack_controller import RackController

from ui.widgets.pallet_dialog import PalletDialog
from ui.widgets.rack_action_dialog import RackActionDialog


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
        # EXECUTAR EMPILHADEIRA
        # =====================================

        self.selecionado.setText(
            f"Armazenando pallet {codigo} em {endereco}..."
        )

        sucesso = self.controller.armazenar_pallet(
            endereco,
            codigo
        )

        # =====================================
        # RESULTADO
        # =====================================

        if sucesso:

            self.selecionado.setText(
                f"Pallet {codigo} armazenado em {endereco}."
            )

            self.pallet_label.setText(
                f"Pallet: {codigo}"
            )

        else:

            self.selecionado.setText(
                "Falha no armazenamento. "
                "A posição não foi alterada."
            )

        self.atualizar_tela()


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
        # EXECUTAR EMPILHADEIRA
        # =====================================

        self.selecionado.setText(
            f"Retirando pallet {pallet} de {endereco}..."
        )

        sucesso = self.controller.retirar_pallet(
            endereco
        )

        # =====================================
        # RESULTADO
        # =====================================

        if sucesso:

            self.selecionado.setText(
                f"Pallet {pallet} retirado de {endereco} "
                "e enviado para expedição."
            )

            self.pallet_label.setText(
                "Pallet: ---"
            )

        else:

            self.selecionado.setText(
                "Falha na retirada. "
                "A posição não foi alterada."
            )

        self.atualizar_tela()


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