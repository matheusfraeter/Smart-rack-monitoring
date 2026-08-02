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

from ui.pages.dashboard import DashboardPage
from ui.pages.manual import ManualPage
from ui.pages.rack import RackPage
from ui.pages.history import HistoryPage
from ui.pages.settings import SettingsPage


class SmartRackGUI(QMainWindow):

    def __init__(self):

        super().__init__()

        # Comunicação com a MKS
        self.mks = MKSConnection()

        self.setWindowTitle("Smart Rack Monitoring")
        self.resize(1400, 850)

        self.criar_interface()

        # Conecta automaticamente
        self.conectar_mks()

    # =====================================
    # CONEXÃO
    # =====================================

    def conectar_mks(self):

        conectado = self.mks.conectar()

        if conectado:
            mensagem = "🟢 MKS DLC32 conectada"
        else:
            mensagem = "🔴 MKS DLC32 desconectada"

        print(mensagem)

        self.statusbar.showMessage(mensagem)

        self.dashboard.atualizar_status()

        if conectado:
            self.manual.status.setText("🟢 MKS DLC32 conectada")
        else:
            self.manual.status.setText("🔴 MKS DLC32 desconectada")

    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        principal = QWidget()
        self.setCentralWidget(principal)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # ==============================
        # PÁGINAS
        # ==============================

        self.paginas = QStackedWidget()

        self.dashboard = DashboardPage(self.mks)
        self.manual = ManualPage(self.mks)
        self.rack = RackPage()
        self.history = HistoryPage()
        self.settings = SettingsPage()

        paginas = [
            self.dashboard,
            self.manual,
            self.rack,
            self.history,
            self.settings
        ]

        for pagina in paginas:
            self.paginas.addWidget(pagina)

        # ==============================
        # MENU
        # ==============================

        menu = self.criar_menu()

        layout.addWidget(menu)

        # ==============================
        # ÁREA CENTRAL
        # ==============================

        area = QVBoxLayout()

        header = QLabel("SMART RACK MONITORING")
        header.setObjectName("header")

        area.addWidget(header)
        area.addWidget(self.paginas)

        layout.addLayout(area)

        principal.setLayout(layout)

        self.criar_statusbar()

            # =====================================
    # MENU LATERAL
    # =====================================

    def criar_menu(self):

        menu = QFrame()
        menu.setObjectName("sidebar")
        menu.setFixedWidth(230)

        layout = QVBoxLayout()

        titulo = QLabel("MENU")
        titulo.setObjectName("menuTitle")

        layout.addWidget(titulo)

        botoes = [

            "🏠 Dashboard",

            "🎮 Controle Manual",

            "📦 Rack",

            "📜 Histórico",

            "⚙ Configurações"

        ]

        for indice, texto in enumerate(botoes):

            botao = QPushButton(texto)

            botao.clicked.connect(

                lambda checked=False, i=indice:
                self.paginas.setCurrentIndex(i)

            )

            layout.addWidget(botao)

        layout.addStretch()

        menu.setLayout(layout)

        return menu

    # =====================================
    # STATUS BAR
    # =====================================

    def criar_statusbar(self):

        self.statusbar = QStatusBar()

        self.statusbar.showMessage(
            "Inicializando sistema..."
        )

        self.setStatusBar(
            self.statusbar
        )