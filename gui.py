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
from ui.pages.history import HistoryPage
from ui.pages.settings import SettingsPage




class SmartRackGUI(QMainWindow):


    def __init__(self):

        super().__init__()



        # =====================================
        # COMUNICAÇÃO MKS
        # =====================================

        self.mks = MKSConnection()



        self.setWindowTitle(
            "Smart Rack Monitoring"
        )


        self.resize(
            1400,
            850
        )



        self.criar_interface()



        # conecta automaticamente

        self.conectar_mks()




    # =====================================
    # CONEXÃO AUTOMÁTICA
    # =====================================

    def conectar_mks(self):


        conectado = self.mks.conectar()



        if conectado:


            mensagem = (
                "🟢 MKS DLC32 conectada"
            )


        else:


            mensagem = (
                "🔴 MKS DLC32 desconectada"
            )



        print(mensagem)



        if hasattr(
            self,
            "statusbar"
        ):


            self.statusbar.showMessage(
                mensagem
            )



        if hasattr(
            self,
            "dashboard"
        ):


            self.dashboard.atualizar_status()



        if hasattr(
            self,
            "manual"
        ):


            self.manual.status.setText(
                mensagem
            )





    # =====================================
    # INTERFACE
    # =====================================

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





        # =====================================
        # PÁGINAS
        # =====================================

        self.paginas = QStackedWidget()



        self.dashboard = DashboardPage(
            self.mks
        )



        self.manual = ManualPage(
            self.mks
        )



        paginas = [

            self.dashboard,

            self.manual,

            RackPage(),

            HistoryPage(),

            SettingsPage()

        ]



        for pagina in paginas:


            self.paginas.addWidget(
                pagina
            )






        # MENU

        menu = self.criar_menu()



        layout.addWidget(
            menu
        )





        # ÁREA CENTRAL


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





    # =====================================
    # MENU
    # =====================================

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

            "📜 Histórico",

            "⚙ Configurações"

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





    # =====================================
    # STATUS BAR
    # =====================================

    def criar_statusbar(self):


        self.statusbar = QStatusBar()



        self.statusbar.showMessage(
            "Inicializando sistema..."
        )



        self.statusbar.setStyleSheet(
            Theme.statusbar()
        )



        self.setStatusBar(
            self.statusbar
        )