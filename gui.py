"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: gui.py
 Descrição...: Janela principal da aplicação
=========================================================
"""

from PySide6.QtWidgets import (
    QApplication,
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
from ui.pages.coordinates import CoordinatesPage
from ui.pages.settings import SettingsPage


class SmartRackGUI(QMainWindow):

    # =================================================
    # PROPORÇÃO DA JANELA
    # =================================================

    PROPORCAO_LARGURA = 800
    PROPORCAO_ALTURA = 480

    def __init__(self):

        super().__init__()

        # Indica que a janela está sendo redimensionada
        # internamente para manter a proporção.
        self._ajustando_tamanho = False

        # =====================================
        # COMUNICAÇÃO COM A MKS
        # =====================================

        self.mks = MKSConnection()

        # =====================================
        # CONFIGURAÇÃO DA JANELA
        # =====================================

        self.setWindowTitle(
            "Smart Rack Monitoring"
        )

        # =====================================
        # TAMANHO MÍNIMO
        # =====================================

        self.setMinimumSize(
            self.PROPORCAO_LARGURA,
            self.PROPORCAO_ALTURA
        )

        # =====================================
        # CRIAR INTERFACE
        # =====================================

        self.criar_interface()

        # =====================================
        # TAMANHO INICIAL
        # =====================================

        self.ajustar_tamanho_inicial()

        # =====================================
        # TENTA CONECTAR APÓS ABRIR A GUI
        # =====================================

        self.timer_conexao = QTimer()

        self.timer_conexao.setSingleShot(
            True
        )

        self.timer_conexao.timeout.connect(
            self.tentar_conexao
        )

        self.timer_conexao.start(
            1500
        )

    # =================================================
    # TAMANHO INICIAL
    # =================================================

    def ajustar_tamanho_inicial(self):

        tela = QApplication.primaryScreen()

        if tela is None:

            self.resize(
                self.PROPORCAO_LARGURA,
                self.PROPORCAO_ALTURA
            )

            return

        area = tela.availableGeometry()

        largura_tela = area.width()
        altura_tela = area.height()

        # =====================================
        # USAR 800x480 COMO MODELO
        # =====================================

        proporcao = (
            self.PROPORCAO_LARGURA /
            self.PROPORCAO_ALTURA
        )

        # -------------------------------------
        # TENTAR OCUPAR O MÁXIMO POSSÍVEL
        # SEM PERDER A PROPORÇÃO
        # -------------------------------------

        largura = largura_tela
        altura = int(largura / proporcao)

        # Caso a altura calculada ultrapasse
        # a tela, limitar pela altura.

        if altura > altura_tela:

            altura = altura_tela
            largura = int(
                altura * proporcao
            )

        # =====================================
        # GARANTIR O TAMANHO MÍNIMO
        # =====================================

        largura = max(
            self.PROPORCAO_LARGURA,
            largura
        )

        altura = max(
            self.PROPORCAO_ALTURA,
            altura
        )

        # =====================================
        # EVITAR PASSAR DA TELA
        # =====================================

        if largura > largura_tela:

            largura = largura_tela
            altura = int(
                largura / proporcao
            )

        if altura > altura_tela:

            altura = altura_tela
            largura = int(
                altura * proporcao
            )

        # =====================================
        # REDIMENSIONAR
        # =====================================

        self.resize(
            largura,
            altura
        )

        # =====================================
        # CENTRALIZAR
        # =====================================

        x = (
            area.left()
            + (largura_tela - largura) // 2
        )

        y = (
            area.top()
            + (altura_tela - altura) // 2
        )

        self.move(
            x,
            y
        )

    # =================================================
    # MANTER PROPORÇÃO 800x480
    # =================================================

    def resizeEvent(self, event):

        # Evita loop de resizeEvent
        if self._ajustando_tamanho:

            super().resizeEvent(event)

            return

        self._ajustando_tamanho = True

        largura = self.width()
        altura = self.height()

        proporcao = (
            self.PROPORCAO_LARGURA /
            self.PROPORCAO_ALTURA
        )

        # =====================================
        # DESCOBRIR QUAL DIMENSÃO FOI ALTERADA
        # =====================================

        # Usa a largura como referência
        # e calcula a altura proporcional.

        nova_altura = int(
            largura / proporcao
        )

        # =====================================
        # GARANTIR ALTURA MÍNIMA
        # =====================================

        if nova_altura < self.PROPORCAO_ALTURA:

            nova_altura = self.PROPORCAO_ALTURA

            nova_largura = int(
                nova_altura * proporcao
            )

        else:

            nova_largura = largura

        # =====================================
        # AJUSTAR TAMANHO
        # =====================================

        if (
            nova_largura != largura
            or nova_altura != altura
        ):

            self.resize(
                nova_largura,
                nova_altura
            )

        self._ajustando_tamanho = False

        super().resizeEvent(event)

    # =================================================
    # TENTATIVA DE CONEXÃO
    # =================================================

    def tentar_conexao(self):

        self.topbar.conectar_mks()

    # =================================================
    # INTERFACE
    # =================================================

    def criar_interface(self):

        principal = QWidget()

        self.setCentralWidget(
            principal
        )

        # =====================================
        # LAYOUT PRINCIPAL
        #
        # Sidebar | Conteúdo
        # =====================================

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
        # ÁREA DIREITA
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

        # -------------------------------------
        # 0 - RACK
        # -------------------------------------

        self.rack = RackPage(
            self.mks
        )

        self.paginas.addWidget(
            self.rack
        )

        # -------------------------------------
        # 1 - CONTROLE MANUAL
        # -------------------------------------

        self.manual = ManualPage(
            self.mks
        )

        self.paginas.addWidget(
            self.manual
        )

        # -------------------------------------
        # 2 - HISTÓRICO
        # -------------------------------------

        self.history = HistoryPage()

        self.paginas.addWidget(
            self.history
        )

        # -------------------------------------
        # 3 - COORDENADAS
        # -------------------------------------

        self.coordinates = CoordinatesPage()

        self.paginas.addWidget(
            self.coordinates
        )

        # -------------------------------------
        # 4 - CONFIGURAÇÕES
        # -------------------------------------

        self.settings = SettingsPage()

        self.paginas.addWidget(
            self.settings
        )

        # =====================================
        # TROCA DE PÁGINAS
        # =====================================

        self.sidebar.paginaSelecionada.connect(
            self.paginas.setCurrentIndex
        )

        conteudo.addWidget(
            self.paginas,
            1
        )

        # =====================================
        # CONTAINER DIREITO
        # =====================================

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

        # =====================================
        # STATUS BAR
        # =====================================

        self.criar_statusbar()

    # =================================================
    # STATUS BAR
    # =================================================

    def criar_statusbar(self):

        self.statusbar = QStatusBar()

        self.statusbar.showMessage(
            "Sistema inicializado."
        )

        self.setStatusBar(
            self.statusbar
        )