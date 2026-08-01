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


from communication import MKSConnection
from theme import Theme


from ui.pages.dashboard import DashboardPage
from ui.pages.manual import ManualPage
from ui.pages.rack import RackPage
from ui.pages.automation import AutomationPage
from ui.pages.history import HistoryPage
from ui.pages.diagnostics import DiagnosticsPage
from ui.pages.settings import SettingsPage
from ui.pages.movement_page import MovementPage
from ui.pages.mission_queue import MissionQueuePage



class SmartRackGUI(QMainWindow):


    def __init__(self):

        super().__init__()


        self.mks = MKSConnection()


        self.setWindowTitle(
            "Smart Rack Monitoring"
        )


        self.resize(
            1400,
            850
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

        history = HistoryPage()

        diagnostics = DiagnosticsPage()

        settings = SettingsPage()

        movement = MovementPage()

        mission_queue = MissionQueuePage()



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


        self.paginas.addWidget(
            history
        )


        self.paginas.addWidget(
            diagnostics
        )


        self.paginas.addWidget(
            settings
        )


        self.paginas.addWidget(
            movement
        )


        self.paginas.addWidget(
            mission_queue
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


        header.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            padding:15px;
            """
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


        titulo.setStyleSheet(
            """
            font-size:18px;
            font-weight:bold;
            padding:20px;
            """
        )


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

            "⚙ Configurações",

            "🚜 Movimentação",

            "📋 Fila de Missões"

        ]



        for indice, texto in enumerate(botoes):


            botao = QPushButton(
                texto
            )


            botao.setStyleSheet(
                Theme.button()
            )



            botao.clicked.connect(
                lambda checked=False, i=indice:
                self.paginas.setCurrentIndex(i)
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