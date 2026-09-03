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
    QPushButton,
    QSizePolicy
)

from PySide6.QtCore import (
    Qt,
    Signal
)


class Sidebar(QFrame):

    paginaSelecionada = Signal(int)


    def __init__(self):

        super().__init__()

        self.setObjectName(
            "sidebar"
        )

        # =====================================
        # LAYOUT RESPONSIVO
        # =====================================

        self.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Expanding
        )

        self.botoes = []

        self.criar_interface()


    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        self.layout = QVBoxLayout(
            self
        )

        self.layout.setContentsMargins(
            15,
            20,
            15,
            20
        )

        self.layout.setSpacing(
            10
        )

        # =====================================
        # TÍTULO
        # =====================================

        self.titulo = QLabel(
            "SMART RACK"
        )

        self.titulo.setObjectName(
            "menuTitle"
        )

        self.titulo.setAlignment(
            Qt.AlignCenter
        )

        self.titulo.setWordWrap(
            True
        )

        self.titulo.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        self.layout.addWidget(
            self.titulo
        )

        # =====================================
        # MENU
        # =====================================

        self.criar_botao(
            self.layout,
            "Rack",
            0
        )

        self.criar_botao(
            self.layout,
            "Controle Manual",
            1
        )

        self.criar_botao(
            self.layout,
            "Histórico",
            2
        )

        self.criar_botao(
            self.layout,
            "Coordenadas do Rack",
            3
        )

        self.criar_botao(
            self.layout,
            "Configurações",
            4
        )

        self.layout.addStretch()


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

        # =====================================
        # O BOTÃO OCUPA A LARGURA DISPONÍVEL
        # =====================================

        botao.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        botao.setMinimumHeight(
            40
        )

        botao.clicked.connect(
            lambda checked=False:
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

            botao.update()


        self.paginaSelecionada.emit(
            indice
        )