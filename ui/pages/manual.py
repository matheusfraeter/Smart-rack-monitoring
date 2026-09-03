"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: manual.py
 Descrição...: Controle manual dos eixos XYZ
=========================================================
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame,
    QSizePolicy
)

from PySide6.QtCore import (
    Qt,
    QTimer
)

from movement import Movement


class ManualPage(QWidget):

    def __init__(self, mks):

        super().__init__()

        self.mks = mks

        self.movimento = Movement(
            self.mks
        )

        self.passo = 10

        # =================================================
        # CONTROLE DO GARFO
        # =================================================

        self.garfo_acionado = False

        self.timer_garfo = QTimer(
            self
        )

        self.timer_garfo.setSingleShot(
            True
        )

        self.timer_garfo.timeout.connect(
            self.desligar_garfo
        )

        # =================================================
        # TAMANHO DOS BOTÕES
        # =================================================

        self.tamanho_botao_xy = 50

        # =================================================
        # CRIAR INTERFACE
        # =================================================

        self.criar_interface()

    # =====================================================
    # INTERFACE
    # =====================================================

    def criar_interface(self):

        principal = QVBoxLayout(
            self
        )

        principal.setContentsMargins(
            10,
            8,
            10,
            8
        )

        principal.setSpacing(
            6
        )

        self.principal_layout = principal

        # =================================================
        # TÍTULO
        # =================================================

        titulo = QLabel(
            "Controle Manual XYZ"
        )

        titulo.setObjectName(
            "title"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Fixed
        )

        # =================================================
        # CONTROLE DE PASSO
        # =================================================

        self.passo_box = QHBoxLayout()

        self.passo_box.setSpacing(
            5
        )

        passo_texto = QLabel(
            "Deslocamento"
        )

        self.bt_menos = QPushButton(
            "-"
        )

        self.bt_mais = QPushButton(
            "+"
        )

        self.passo_label = QLabel(
            "10 mm"
        )

        self.passo_label.setAlignment(
            Qt.AlignCenter
        )

        self.bt_menos.setObjectName(
            "actionButton"
        )

        self.bt_mais.setObjectName(
            "actionButton"
        )

        self.passo_label.setMinimumWidth(
            52
        )

        self.passo_box.addWidget(
            passo_texto
        )

        self.passo_box.addSpacing(
            5
        )

        self.passo_box.addWidget(
            self.bt_menos
        )

        self.passo_box.addWidget(
            self.passo_label
        )

        self.passo_box.addWidget(
            self.bt_mais
        )

        self.passo_box.addStretch()

        # =================================================
        # CAIXA PRINCIPAL
        # =================================================

        self.caixa = QFrame()

        self.caixa.setObjectName(
            "controlBox"
        )

        self.controles = QHBoxLayout(
            self.caixa
        )

        self.controles.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.controles.setSpacing(
            8
        )

        # =================================================
        # XY
        # =================================================

        self.xy_box = QFrame()

        self.xy_box.setObjectName(
            "controlBox"
        )

        self.xy_layout = QVBoxLayout(
            self.xy_box
        )

        self.xy_layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.xy_layout.setSpacing(
            3
        )

        self.xy_layout.setAlignment(
            Qt.AlignCenter
        )

        xy_titulo = QLabel(
            "Movimento XY"
        )

        xy_titulo.setAlignment(
            Qt.AlignCenter
        )

        self.xy_layout.addWidget(
            xy_titulo
        )

        self.grid_xy = QGridLayout()

        self.grid_xy.setSpacing(
            3
        )

        self.grid_xy.setAlignment(
            Qt.AlignCenter
        )

        # =================================================
        # BOTÕES XY
        # =================================================

        self.xp = QPushButton(
            "X+"
        )

        self.xm = QPushButton(
            "X-"
        )

        self.ym = QPushButton(
            "Y-"
        )

        self.yp = QPushButton(
            "Y+"
        )

        for botao in (
            self.xp,
            self.xm,
            self.ym,
            self.yp
        ):

            botao.setObjectName(
                "actionButton"
            )

            botao.setSizePolicy(
                QSizePolicy.Fixed,
                QSizePolicy.Fixed
            )

        # -------------------------------------------------
        # DISPOSIÇÃO XY
        # -------------------------------------------------

        self.grid_xy.addWidget(
            self.xp,
            0,
            1,
            Qt.AlignCenter
        )

        self.grid_xy.addWidget(
            self.ym,
            1,
            0,
            Qt.AlignCenter
        )

        self.grid_xy.addWidget(
            self.yp,
            1,
            2,
            Qt.AlignCenter
        )

        self.grid_xy.addWidget(
            self.xm,
            2,
            1,
            Qt.AlignCenter
        )

        self.xy_layout.addLayout(
            self.grid_xy
        )

        # =================================================
        # Z
        # =================================================

        self.z_box = QFrame()

        self.z_box.setObjectName(
            "controlBox"
        )

        self.z_layout = QVBoxLayout(
            self.z_box
        )

        self.z_layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.z_layout.setSpacing(
            5
        )

        self.z_layout.setAlignment(
            Qt.AlignCenter
        )

        z_titulo = QLabel(
            "Movimento Z"
        )

        z_titulo.setAlignment(
            Qt.AlignCenter
        )

        self.z_layout.addWidget(
            z_titulo
        )

        # =================================================
        # BOTÕES Z
        # =================================================

        self.zp = QPushButton(
            "Z +"
        )

        self.zm = QPushButton(
            "Z -"
        )

        for botao in (
            self.zp,
            self.zm
        ):

            botao.setObjectName(
                "actionButton"
            )

            botao.setSizePolicy(
                QSizePolicy.Fixed,
                QSizePolicy.Fixed
            )

            self.z_layout.addWidget(
                botao,
                0,
                Qt.AlignCenter
            )

        # =================================================
        # GARFOS
        # =================================================

        self.garfo_box = QFrame()

        self.garfo_box.setObjectName(
            "controlBox"
        )

        self.garfo_layout = QVBoxLayout(
            self.garfo_box
        )

        self.garfo_layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.garfo_layout.setSpacing(
            5
        )

        self.garfo_layout.setAlignment(
            Qt.AlignCenter
        )

        garfo_titulo = QLabel(
            "Garfos"
        )

        garfo_titulo.setAlignment(
            Qt.AlignCenter
        )

        self.garfo_layout.addWidget(
            garfo_titulo
        )

        # =================================================
        # BOTÃO GARFO
        # =================================================

        self.bt_garfo = QPushButton(
            "ACIONAR\nGARFO"
        )

        self.bt_garfo.setObjectName(
            "actionButton"
        )

        self.bt_garfo.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        self.garfo_layout.addWidget(
            self.bt_garfo,
            0,
            Qt.AlignCenter
        )

        # =================================================
        # MONTAR OS TRÊS CONTROLES
        # =================================================

        self.controles.addWidget(
            self.xy_box,
            4
        )

        self.controles.addWidget(
            self.z_box,
            2
        )

        self.controles.addWidget(
            self.garfo_box,
            3
        )

        # =================================================
        # BOTÕES INFERIORES
        # =================================================

        self.botoes = QHBoxLayout()

        self.botoes.setSpacing(
            8
        )

        stop = QPushButton(
            "STOP"
        )

        continuar = QPushButton(
            "CONTINUAR"
        )

        stop.setObjectName(
            "actionButton"
        )

        continuar.setObjectName(
            "actionButton"
        )

        self.stop_button = stop
        self.continuar_button = continuar

        self.botoes.addWidget(
            stop
        )

        self.botoes.addWidget(
            continuar
        )

        # =================================================
        # EVENTOS
        # =================================================

        self.bt_mais.clicked.connect(
            self.aumentar_passo
        )

        self.bt_menos.clicked.connect(
            self.diminuir_passo
        )

        self.xp.clicked.connect(
            self.botao_x_mais
        )

        self.xm.clicked.connect(
            self.botao_x_menos
        )

        self.yp.clicked.connect(
            self.botao_y_mais
        )

        self.ym.clicked.connect(
            self.botao_y_menos
        )

        self.zp.clicked.connect(
            self.botao_z_mais
        )

        self.zm.clicked.connect(
            self.botao_z_menos
        )

        self.bt_garfo.clicked.connect(
            self.acionar_garfo
        )

        stop.clicked.connect(
            self.stop
        )

        continuar.clicked.connect(
            self.reset
        )

        # =================================================
        # MONTAGEM FINAL
        # =================================================

        principal.addWidget(
            titulo
        )

        principal.addLayout(
            self.passo_box
        )

        principal.addWidget(
            self.caixa,
            1
        )

        principal.addLayout(
            self.botoes
        )

        # =================================================
        # TAMANHO INICIAL
        # =================================================

        self.atualizar_tamanho_botoes()

    # =====================================================
    # REDIMENSIONAMENTO
    # =====================================================

    def resizeEvent(self, event):

        super().resizeEvent(
            event
        )

        self.atualizar_tamanho_botoes()

    # =====================================================
    # ATUALIZAR TAMANHOS
    # =====================================================

    def atualizar_tamanho_botoes(self):

        largura = self.width()
        altura = self.height()

        # =================================================
        # TAMANHO BASE DOS BOTÕES DE MOVIMENTO
        # =================================================

        tamanho_base = int(
            min(
                62,
                max(
                    46,
                    largura * 0.075
                )
            )
        )

        self.tamanho_botao_xy = tamanho_base

        # =================================================
        # BOTÕES XY
        # =================================================

        # Agora XY tem o mesmo formato dos botões Z:
        # retangular em vez de quadrado.

        largura_movimento = int(
            tamanho_base * 1.25
        )

        altura_movimento = int(
            tamanho_base * 0.80
        )

        for botao in (
            self.xp,
            self.xm,
            self.ym,
            self.yp
        ):

            botao.setFixedSize(
                largura_movimento,
                altura_movimento
            )

        # =================================================
        # BOTÕES Z
        # =================================================

        self.zp.setFixedSize(
            largura_movimento,
            altura_movimento
        )

        self.zm.setFixedSize(
            largura_movimento,
            altura_movimento
        )

        # =================================================
        # BOTÃO GARFO
        # =================================================

        largura_garfo = int(
            max(
                120,
                tamanho_base * 2.5
            )
        )

        altura_garfo = int(
            tamanho_base * 1.20
        )

        self.bt_garfo.setFixedSize(
            largura_garfo,
            altura_garfo
        )

        # =================================================
        # NÃO FORÇAR TAMANHO DOS BLOCOS
        # =================================================

        self.xy_box.setMinimumWidth(
            0
        )

        self.z_box.setMinimumWidth(
            0
        )

        self.garfo_box.setMinimumWidth(
            0
        )

        # =================================================
        # BOTÕES DE PASSO
        # =================================================

        tamanho_passo = int(
            max(
                32,
                min(
                    44,
                    largura * 0.043
                )
            )
        )

        self.bt_menos.setFixedSize(
            tamanho_passo,
            tamanho_passo
        )

        self.bt_mais.setFixedSize(
            tamanho_passo,
            tamanho_passo
        )

        # =================================================
        # STOP / CONTINUAR
        # =================================================

        altura_inferior = int(
            max(
                36,
                min(
                    46,
                    altura * 0.095
                )
            )
        )

        self.stop_button.setFixedHeight(
            altura_inferior
        )

        self.continuar_button.setFixedHeight(
            altura_inferior
        )

    # =====================================================
    # PASSO +
    # =====================================================

    def aumentar_passo(self):

        if self.passo < 100:

            self.passo += 10

            self.passo_label.setText(
                f"{self.passo} mm"
            )

            print(
                f"PASSO ALTERADO PARA: {self.passo} mm"
            )

    # =====================================================
    # PASSO -
    # =====================================================

    def diminuir_passo(self):

        if self.passo > 10:

            self.passo -= 10

            self.passo_label.setText(
                f"{self.passo} mm"
            )

            print(
                f"PASSO ALTERADO PARA: {self.passo} mm"
            )

    # =====================================================
    # BOTÃO X+
    # =====================================================

    def botao_x_mais(self):

        print()
        print(
            ">>> BOTÃO X+ PRESSIONADO"
        )

        print(
            f">>> PASSO: {self.passo} mm"
        )

        self.mover_x(
            self.passo
        )

    # =====================================================
    # BOTÃO X-
    # =====================================================

    def botao_x_menos(self):

        print()
        print(
            ">>> BOTÃO X- PRESSIONADO"
        )

        print(
            f">>> PASSO: {self.passo} mm"
        )

        self.mover_x(
            -self.passo
        )

    # =====================================================
    # BOTÃO Y+
    # =====================================================

    def botao_y_mais(self):

        print()
        print(
            ">>> BOTÃO Y+ PRESSIONADO"
        )

        print(
            f">>> PASSO: {self.passo} mm"
        )

        self.mover_y(
            self.passo
        )

    # =====================================================
    # BOTÃO Y-
    # =====================================================

    def botao_y_menos(self):

        print()
        print(
            ">>> BOTÃO Y- PRESSIONADO"
        )

        print(
            f">>> PASSO: {self.passo} mm"
        )

        self.mover_y(
            -self.passo
        )

    # =====================================================
    # BOTÃO Z+
    # =====================================================

    def botao_z_mais(self):

        print()
        print(
            ">>> BOTÃO Z+ PRESSIONADO"
        )

        print(
            f">>> PASSO: {self.passo} mm"
        )

        self.mover_z(
            self.passo
        )

    # =====================================================
    # BOTÃO Z-
    # =====================================================

    def botao_z_menos(self):

        print()
        print(
            ">>> BOTÃO Z- PRESSIONADO"
        )

        print(
            f">>> PASSO: {self.passo} mm"
        )

        self.mover_z(
            -self.passo
        )

    # =====================================================
    # MOVIMENTO X
    # =====================================================

    def mover_x(self, valor):

        print()
        print(
            ">>> MANUAL PAGE"
        )

        print(
            f">>> SOLICITADO X: {valor}"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        resultado = self.movimento.mover_x(
            valor
        )

        print(
            f">>> RESULTADO X: {resultado}"
        )

    # =====================================================
    # MOVIMENTO Y
    # =====================================================

    def mover_y(self, valor):

        print()
        print(
            ">>> MANUAL PAGE"
        )

        print(
            f">>> SOLICITADO Y: {valor}"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        resultado = self.movimento.mover_y(
            valor
        )

        print(
            f">>> RESULTADO Y: {resultado}"
        )

    # =====================================================
    # MOVIMENTO Z
    # =====================================================

    def mover_z(self, valor):

        print()
        print(
            ">>> MANUAL PAGE"
        )

        print(
            f">>> SOLICITADO Z: {valor}"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        resultado = self.movimento.mover_z(
            valor
        )

        print(
            f">>> RESULTADO Z: {resultado}"
        )

    # =====================================================
    # ACIONAR GARFO
    # =====================================================

    def acionar_garfo(self):

        print()
        print(
            ">>> BOTÃO ACIONAR GARFO PRESSIONADO"
        )

        if self.garfo_acionado:

            print(
                ">>> GARFO JÁ ESTÁ EM ACIONAMENTO"
            )

            return

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        print(
            ">>> ENVIANDO M3 S1000"
        )

        resultado = self.mks.enviar_comando(
            "M3 S1000"
        )

        if not resultado:

            print(
                ">>> FALHA AO LIGAR GARFO"
            )

            return

        self.garfo_acionado = True

        self.bt_garfo.setEnabled(
            False
        )

        self.bt_garfo.setText(
            "GARFO\nACIONADO"
        )

        print(
            ">>> TTL HIGH POR 1 SEGUNDO"
        )

        self.timer_garfo.start(
            1000
        )

    # =====================================================
    # DESLIGAR GARFO
    # =====================================================

    def desligar_garfo(self):

        print()
        print(
            ">>> TEMPO DO GARFO FINALIZADO"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA AO FINALIZAR GARFO"
            )

            self.garfo_acionado = False

            self.bt_garfo.setEnabled(
                True
            )

            self.bt_garfo.setText(
                "ACIONAR\nGARFO"
            )

            return

        print(
            ">>> ENVIANDO M3 S0"
        )

        resultado = self.mks.enviar_comando(
            "M3 S0"
        )

        print(
            f">>> RESULTADO GARFO: {resultado}"
        )

        self.garfo_acionado = False

        self.bt_garfo.setEnabled(
            True
        )

        self.bt_garfo.setText(
            "ACIONAR\nGARFO"
        )

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        print()
        print(
            ">>> STOP PRESSIONADO"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        if self.timer_garfo.isActive():

            self.timer_garfo.stop()

            print(
                ">>> TIMER DO GARFO CANCELADO"
            )

            self.mks.enviar_comando(
                "M3 S0"
            )

            self.garfo_acionado = False

            self.bt_garfo.setEnabled(
                True
            )

            self.bt_garfo.setText(
                "ACIONAR\nGARFO"
            )

        self.mks.enviar_comando(
            "!"
        )

    # =====================================================
    # CONTINUAR
    # =====================================================

    def reset(self):

        print()
        print(
            ">>> CONTINUAR PRESSIONADO"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        self.mks.enviar_comando(
            "~"
        )