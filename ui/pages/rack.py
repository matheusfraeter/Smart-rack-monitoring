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
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame,
    QScrollArea
)

from PySide6.QtCore import Qt

from controllers.rack_controller import RackController
from ui.widgets.pallet_dialog import PalletDialog
from ui.widgets.rack_action_dialog import RackActionDialog


class RackPage(QWidget):

    def __init__(self):

        super().__init__()

        self.controller = RackController()

        self.botoes = {}

        # ==========================
        # CONFIGURAÇÃO DO RACK
        # ==========================

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

        principal = QVBoxLayout(self)

        principal.setContentsMargins(
            20,
            20,
            20,
            20
        )

        principal.setSpacing(20)

        titulo = QLabel("📦 SMART RACK")
        titulo.setObjectName("title")

        self.selecionado = QLabel(
            "Nenhuma posição selecionada"
        )
        self.selecionado.setObjectName(
            "rackStatus"
        )

        principal.addWidget(titulo)
        principal.addWidget(self.selecionado)

        # ==========================
        # ÁREA COM ROLAGEM
        # ==========================

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

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

        self.atualizar_tela()

    # =================================================
    # CRIAR ESTANTE
    # =================================================

    def criar_estante(self, estante):

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

        # Cabeçalho das colunas

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

    def selecionar(self, endereco):

        dados = self.controller.buscar_posicao(
            endereco
        )

        if dados is None:
            return

        ocupado = dados[1]
        pallet = dados[2]

        # -------------------------
        # POSIÇÃO LIVRE
        # -------------------------

        if ocupado == 0:

            dialog = PalletDialog(
                endereco
            )

            if dialog.exec():

                codigo = dialog.obter_pallet()

                if codigo:

                    self.controller.armazenar_pallet(
                        endereco,
                        codigo
                    )

                    self.selecionado.setText(
                        f"Pallet {codigo} armazenado em {endereco}"
                    )

        # -------------------------
        # POSIÇÃO OCUPADA
        # -------------------------

        else:

            dialog = RackActionDialog(
                endereco,
                pallet
            )

            if dialog.exec():

                if dialog.remover:

                    self.controller.retirar_pallet(
                        endereco
                    )

                    self.selecionado.setText(
                        f"Posição {endereco} liberada"
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

            botao.setText("📦")

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

            botao.setText("")

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