"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: sidebar.py
 Descrição...: Menu lateral da aplicação
=========================================================
"""

from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel,
    QPushButton
)

from PySide6.QtCore import Signal


class Sidebar(QFrame):

    paginaSelecionada = Signal(int)


    def __init__(self):

        super().__init__()


        self.setObjectName(
            "sidebar"
        )


        self.setFixedWidth(
            230
        )


        self.botoes = []


        self.criar_interface()



    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        layout = QVBoxLayout(
            self
        )


        layout.setContentsMargins(
            15,
            20,
            15,
            20
        )


        layout.setSpacing(
            10
        )


        titulo = QLabel(
            "SMART RACK"
        )


        titulo.setObjectName(
            "menuTitle"
        )


        layout.addWidget(
            titulo
        )


        # =============================
        # MENU
        # =============================


        self.criar_botao(
            layout,
            "Rack",
            0
        )


        self.criar_botao(
            layout,
            "Controle Manual",
            1
        )


        self.criar_botao(
            layout,
            "Histórico",
            2
        )


        self.criar_botao(
            layout,
            "Configurações",
            3
        )


        layout.addStretch()



    # =====================================
    # CRIAR BOTÃO
    # =====================================

    def criar_botao(
        self,
        layout,
        texto,
        indice
    ):


        botao = QPushButton(
            texto
        )


        botao.setObjectName(
            "menuButton"
        )


        botao.setMinimumHeight(
            45
        )


        botao.clicked.connect(
            lambda:
            self.selecionar(
                indice
            )
        )


        self.botoes.append(
            botao
        )


        layout.addWidget(
            botao
        )



    # =====================================
    # SELEÇÃO DO MENU
    # =====================================

    def selecionar(
        self,
        indice
    ):


        for i, botao in enumerate(
            self.botoes
        ):

            if i == indice:

                botao.setProperty(
                    "active",
                    True
                )

            else:

                botao.setProperty(
                    "active",
                    False
                )


            botao.style().unpolish(
                botao
            )

            botao.style().polish(
                botao
            )


        self.paginaSelecionada.emit(
            indice
        )