"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: gui.py
 Descrição...: Janela principal da aplicação
=========================================================
"""


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

from ui.pages.dashboard import DashboardPage
from ui.pages.manual import ManualPage
from ui.pages.rack import RackPage
from ui.pages.automation import AutomationPage



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


        # =================================================
        # PÁGINAS
        # =================================================

        self.paginas = QStackedWidget()


        dashboard = DashboardPage()

        manual = ManualPage()

        rack = RackPage()

        automation = AutomationPage()


        self.paginas.addWidget(
            dashboard
        )


        self.paginas.addWidget(
            manual
        )

        self.paginas.addWidget(
        rack
        )

        self.paginas.addWidget(
        automation
            )



        # =================================================
        # MENU
        # =================================================

        menu = self.criar_menu()


        layout.addWidget(
            menu
        )



        # =================================================
        # ÁREA CENTRAL
        # =================================================

        area = QVBoxLayout()


        header = QLabel(
            "🚜 SMART RACK MONITORING"
        )


        header.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            padding:15px;
        """)



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



        for indice, texto in enumerate(botoes):


            botao = QPushButton(
                texto
            )


            botao.setStyleSheet(
                Theme.button()
            )



            if indice == 0:

                botao.clicked.connect(
                    lambda: self.paginas.setCurrentIndex(0)
                )



            elif indice == 1:

                botao.clicked.connect(
                    lambda: self.paginas.setCurrentIndex(1)
                )

            elif indice == 2:

                botao.clicked.connect(
                   lambda: self.paginas.setCurrentIndex(2)
                )
            
            elif indice == 3:

                botao.clicked.connect(
                   lambda: self.paginas.setCurrentIndex(3)
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
    # BARRA DE STATUS
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