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
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QStatusBar
)

from PySide6.QtCore import QTimer


from communication import MKSConnection

from ui.widgets.topbar import TopBar
from ui.widgets.sidebar import Sidebar

from ui.pages.rack import RackPage
from ui.pages.manual import ManualPage
from ui.pages.history import HistoryPage
from ui.pages.settings import SettingsPage



class SmartRackGUI(QMainWindow):


    def __init__(self):

        super().__init__()


        # Comunicação com a MKS

        self.mks = MKSConnection()



        self.setWindowTitle(
            "Smart Rack Monitoring"
        )


        self.resize(
            1200,
            700
        )


        self.setMinimumSize(
            1000,
            650
        )



        self.criar_interface()



        # =====================================
        # TENTA CONECTAR SEM BLOQUEAR A GUI
        # =====================================

        self.timer_conexao = QTimer()

        self.timer_conexao.setSingleShot(
            True
        )


        self.timer_conexao.timeout.connect(
            self.tentar_conexao
        )


        # espera a interface abrir

        self.timer_conexao.start(
            1500
        )



    # =====================================
    # TENTATIVA DE CONEXÃO
    # =====================================

    def tentar_conexao(self):

        self.topbar.conectar_mks()



    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):


        principal = QWidget()


        self.setCentralWidget(
            principal
        )



        # Layout principal horizontal
        # Sidebar | Conteúdo


        layout_principal = QHBoxLayout()


        layout_principal.setContentsMargins(
            0,
            0,
            0,
            0
        )


        layout_principal.setSpacing(
            0
        )



        # =====================================
        # MENU LATERAL
        # =====================================


        self.sidebar = Sidebar()


        layout_principal.addWidget(
            self.sidebar
        )



        # =====================================
        # ÁREA DE CONTEÚDO
        # =====================================


        conteudo = QVBoxLayout()


        conteudo.setContentsMargins(
            0,
            0,
            0,
            0
        )


        conteudo.setSpacing(
            0
        )



        # =====================================
        # TOP BAR
        # =====================================


        self.topbar = TopBar(
            self.mks
        )


        conteudo.addWidget(
            self.topbar
        )



        # =====================================
        # PÁGINAS
        # =====================================


        self.paginas = QStackedWidget()



        self.rack = RackPage()


        self.manual = ManualPage(
            self.mks
        )


        self.history = HistoryPage()


        self.settings = SettingsPage()



        self.paginas.addWidget(
            self.rack
        )


        self.paginas.addWidget(
            self.manual
        )


        self.paginas.addWidget(
            self.history
        )


        self.paginas.addWidget(
            self.settings
        )



        self.sidebar.paginaSelecionada.connect(
            self.paginas.setCurrentIndex
        )



        conteudo.addWidget(
            self.paginas,
            1
        )



        # Container área direita


        area_direita = QWidget()


        area_direita.setLayout(
            conteudo
        )



        layout_principal.addWidget(
            area_direita,
            1
        )



        principal.setLayout(
            layout_principal
        )



        self.criar_statusbar()



    # =====================================
    # STATUS BAR
    # =====================================

    def criar_statusbar(self):


        self.statusbar = QStatusBar()


        self.statusbar.showMessage(
            "Sistema inicializado."
        )


        self.setStatusBar(
            self.statusbar
        )