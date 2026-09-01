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
    QFrame
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

        self.criar_interface()


    # =====================================================
    # INTERFACE
    # =====================================================

    def criar_interface(self):

        principal = QVBoxLayout(self)

        principal.setContentsMargins(
            20,
            20,
            20,
            20
        )

        principal.setSpacing(15)

        # =================================================
        # TÍTULO
        # =================================================

        titulo = QLabel(
            "Controle Manual XYZ"
        )

        titulo.setObjectName(
            "title"
        )

        # =================================================
        # CONTROLE DE PASSO
        # =================================================

        passo_box = QHBoxLayout()

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

        self.bt_menos.setMinimumSize(
            50,
            40
        )

        self.bt_mais.setMinimumSize(
            50,
            40
        )

        self.passo_label.setMinimumWidth(
            80
        )

        passo_box.addWidget(
            passo_texto
        )

        passo_box.addSpacing(20)

        passo_box.addWidget(
            self.bt_menos
        )

        passo_box.addWidget(
            self.passo_label
        )

        passo_box.addWidget(
            self.bt_mais
        )

        passo_box.addStretch()

        # =================================================
        # CAIXA PRINCIPAL
        # =================================================

        caixa = QFrame()

        caixa.setObjectName(
            "controlBox"
        )

        controles = QHBoxLayout(
            caixa
        )

        controles.setSpacing(60)

        controles.addStretch()

        # =================================================
        # XY
        # =================================================

        xy_box = QFrame()

        xy_box.setObjectName(
            "controlBox"
        )

        xy_layout = QVBoxLayout(
            xy_box
        )

        xy_titulo = QLabel(
            "Movimento XY"
        )

        xy_titulo.setAlignment(
            Qt.AlignCenter
        )

        xy_layout.addWidget(
            xy_titulo
        )

        grid = QGridLayout()

        self.xp = QPushButton(
            "↑\nX+"
        )

        self.xm = QPushButton(
            "↓\nX-"
        )

        self.ym = QPushButton(
            "←\nY-"
        )

        self.yp = QPushButton(
            "→\nY+"
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

            botao.setMinimumSize(
                90,
                90
            )

        grid.addWidget(
            self.xp,
            0,
            1
        )

        grid.addWidget(
            self.ym,
            1,
            0
        )

        grid.addWidget(
            self.yp,
            1,
            2
        )

        grid.addWidget(
            self.xm,
            2,
            1
        )

        xy_layout.addLayout(
            grid
        )

        controles.addWidget(
            xy_box
        )

        # =================================================
        # Z
        # =================================================

        z_box = QFrame()

        z_box.setObjectName(
            "controlBox"
        )

        z_layout = QVBoxLayout(
            z_box
        )

        z_titulo = QLabel(
            "Movimento Z"
        )

        z_titulo.setAlignment(
            Qt.AlignCenter
        )

        z_layout.addWidget(
            z_titulo
        )

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

            botao.setMinimumSize(
                100,
                70
            )

            z_layout.addWidget(
                botao
            )

        controles.addSpacing(60)

        controles.addWidget(
            z_box
        )

        # =================================================
        # CONTROLE DOS GARFOS
        # =================================================

        garfo_box = QFrame()

        garfo_box.setObjectName(
            "controlBox"
        )

        garfo_layout = QVBoxLayout(
            garfo_box
        )

        garfo_titulo = QLabel(
            "Garfos"
        )

        garfo_titulo.setAlignment(
            Qt.AlignCenter
        )

        garfo_layout.addWidget(
            garfo_titulo
        )

        self.bt_garfo = QPushButton(
            "ACIONAR GARFO"
        )

        self.bt_garfo.setObjectName(
            "actionButton"
        )

        self.bt_garfo.setMinimumSize(
            150,
            70
        )

        garfo_layout.addWidget(
            self.bt_garfo
        )

        controles.addSpacing(60)

        controles.addWidget(
            garfo_box
        )

        controles.addStretch()

        # =================================================
        # BOTÕES INFERIORES
        # =================================================

        botoes = QHBoxLayout()

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

        stop.setMinimumHeight(50)

        continuar.setMinimumHeight(50)

        botoes.addWidget(
            stop
        )

        botoes.addWidget(
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
        # MONTAGEM
        # =================================================

        principal.addWidget(
            titulo
        )

        principal.addLayout(
            passo_box
        )

        principal.addWidget(
            caixa
        )

        principal.addLayout(
            botoes
        )

        principal.addStretch()


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
        print(">>> BOTÃO X+ PRESSIONADO")
        print(f">>> PASSO: {self.passo} mm")

        self.mover_x(
            self.passo
        )


    # =====================================================
    # BOTÃO X-
    # =====================================================

    def botao_x_menos(self):

        print()
        print(">>> BOTÃO X- PRESSIONADO")
        print(f">>> PASSO: {self.passo} mm")

        self.mover_x(
            -self.passo
        )


    # =====================================================
    # BOTÃO Y+
    # =====================================================

    def botao_y_mais(self):

        print()
        print(">>> BOTÃO Y+ PRESSIONADO")
        print(f">>> PASSO: {self.passo} mm")

        self.mover_y(
            self.passo
        )


    # =====================================================
    # BOTÃO Y-
    # =====================================================

    def botao_y_menos(self):

        print()
        print(">>> BOTÃO Y- PRESSIONADO")
        print(f">>> PASSO: {self.passo} mm")

        self.mover_y(
            -self.passo
        )


    # =====================================================
    # BOTÃO Z+
    # =====================================================

    def botao_z_mais(self):

        print()
        print(">>> BOTÃO Z+ PRESSIONADO")
        print(f">>> PASSO: {self.passo} mm")

        self.mover_z(
            self.passo
        )


    # =====================================================
    # BOTÃO Z-
    # =====================================================

    def botao_z_menos(self):

        print()
        print(">>> BOTÃO Z- PRESSIONADO")
        print(f">>> PASSO: {self.passo} mm")

        self.mover_z(
            -self.passo
        )


    # =====================================================
    # MOVIMENTO X
    # =====================================================

    def mover_x(self, valor):

        print()
        print(">>> MANUAL PAGE")
        print(f">>> SOLICITADO X: {valor}")

        if not self.mks.conectado:

            print(">>> MKS DESCONECTADA")

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
        print(">>> MANUAL PAGE")
        print(f">>> SOLICITADO Y: {valor}")

        if not self.mks.conectado:

            print(">>> MKS DESCONECTADA")

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
        print(">>> MANUAL PAGE")
        print(f">>> SOLICITADO Z: {valor}")

        if not self.mks.conectado:

            print(">>> MKS DESCONECTADA")

            return

        resultado = self.movimento.mover_z(
            valor
        )

        print(
            f">>> RESULTADO Z: {resultado}"
        )


    # =====================================================
    # ACIONAR GARFO
    #
    # M3 S1000
    # ↓
    # HIGH POR 1 SEGUNDO
    # ↓
    # M3 S0
    #
    # QTimer mantém a interface responsiva.
    # =====================================================

    def acionar_garfo(self):

        print()
        print(">>> BOTÃO ACIONAR GARFO PRESSIONADO")

        # ---------------------------------------------
        # IMPEDIR NOVO ACIONAMENTO
        # ---------------------------------------------

        if self.garfo_acionado:

            print(
                ">>> GARFO JÁ ESTÁ EM ACIONAMENTO"
            )

            return

        # ---------------------------------------------
        # VERIFICAR CONEXÃO
        # ---------------------------------------------

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        # ---------------------------------------------
        # LIGAR TTL
        # ---------------------------------------------

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

        # ---------------------------------------------
        # ESTADO
        # ---------------------------------------------

        self.garfo_acionado = True

        self.bt_garfo.setEnabled(
            False
        )

        self.bt_garfo.setText(
            "GARFO ACIONADO"
        )

        # ---------------------------------------------
        # TIMER
        #
        # 1000 ms = 1 segundo de HIGH
        # ---------------------------------------------

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
                "ACIONAR GARFO"
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
            "ACIONAR GARFO"
        )


    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        print()
        print(">>> STOP PRESSIONADO")

        if not self.mks.conectado:

            print(">>> MKS DESCONECTADA")

            return

        # ---------------------------------------------
        # CANCELAR TIMER DO GARFO
        # ---------------------------------------------

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
                "ACIONAR GARFO"
            )

        # ---------------------------------------------
        # STOP DA MKS
        # ---------------------------------------------

        self.mks.enviar_comando(
            "!"
        )


    # =====================================================
    # CONTINUAR
    # =====================================================

    def reset(self):

        print()
        print(">>> CONTINUAR PRESSIONADO")

        if not self.mks.conectado:

            print(">>> MKS DESCONECTADA")

            return

        self.mks.enviar_comando(
            "~"
        )