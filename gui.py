"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: gui.py
 Descrição...: Janela principal da aplicação
=========================================================
"""
from ui.pages.dashboard import DashboardPage
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QStackedWidget,
    QStatusBar
)

from PySide6.QtCore import Qt

from communication import MKSConnection
from theme import Theme


class SmartRackGUI(QMainWindow):

    def __init__(self):

        super().__init__()

        self.mks = MKSConnection()

        self.setWindowTitle(
            "Smart Rack Monitoring"
        )

        self.resize(
            1200,
            700
        )

        self.criar_interface()


    # =====================================================
    # INTERFACE PRINCIPAL
    # =====================================================

    def criar_interface(self):

        self.setStyleSheet(
            Theme.application()
        )


        principal = QWidget()

        self.setCentralWidget(
            principal
        )


        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )


        # MENU

        menu = self.criar_menu()

        layout.addWidget(
            menu
        )


        # AREA CENTRAL

        area = QVBoxLayout()


        header = QLabel(
            "🚜 SMART RACK MONITORING"
        )

        header.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            padding:15px;
        """)


        self.paginas = QStackedWidget()


        dashboard = DashboardPage()

        self.paginas.addWidget(
        dashboard
        )


        area.addWidget(
            header
        )

        area.addWidget(
            self.paginas
        )


        layout.addLayout(
            area
        )


        principal.setLayout(
            layout
        )


        self.criar_statusbar()



    # =====================================================
    # MENU LATERAL
    # =====================================================

    def criar_menu(self):

        menu = QFrame()

        menu.setFixedWidth(
            230
        )

        menu.setStyleSheet(
            Theme.sidebar()
        )


        layout = QVBoxLayout()


        titulo = QLabel(
            "MENU"
        )

        titulo.setStyleSheet("""
            font-size:18px;
            font-weight:bold;
            padding:20px;
        """)


        layout.addWidget(
            titulo
        )


        botoes = [

            "🏠 Dashboard",

            "🎮 Controle Manual",

            "📦 Rack",

            "🤖 Automação",

            "📜 Histórico",

            "🔧 Diagnóstico",

            "⚙ Configurações"

        ]


        for texto in botoes:

            botao = QPushButton(
                texto
            )

            botao.setStyleSheet(
                Theme.button()
            )


            layout.addWidget(
                botao
            )


        layout.addStretch()


        menu.setLayout(
            layout
        )


        return menu



    # =====================================================
    # STATUS BAR
    # =====================================================

    def criar_statusbar(self):

        status = QStatusBar()

        status.showMessage(
            "Sistema iniciado"
        )

        status.setStyleSheet(
            Theme.statusbar()
        )


        self.setStatusBar(
            status
        )