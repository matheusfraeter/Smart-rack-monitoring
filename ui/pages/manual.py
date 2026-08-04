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
    QSpinBox,
    QFrame
)

from PySide6.QtCore import QTimer

from movement import Movement



class ManualPage(QWidget):


    def __init__(self, mks):

        super().__init__()

        self.mks = mks

        self.movimento = Movement(
            mks
        )

        self.criar_interface()


        self.timer = QTimer()

        self.timer.timeout.connect(
            self.atualizar_posicao
        )

        self.timer.start(
            1000
        )



    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        principal = QVBoxLayout(
            self
        )

        principal.setContentsMargins(
            20,
            20,
            20,
            20
        )

        principal.setSpacing(
            15
        )


        # Título

        titulo = QLabel(
            "🎮 Controle Manual XYZ"
        )

        titulo.setObjectName(
            "title"
        )


        self.status = QLabel(
            "MKS DLC32: Aguardando conexão"
        )

        self.status.setObjectName(
            "offline"
        )



        # =====================================
        # POSIÇÃO ATUAL
        # =====================================

        pos_box = QFrame()

        pos_box.setObjectName(
            "infoCard"
        )


        pos_layout = QVBoxLayout(
            pos_box
        )


        pos_layout.addWidget(
            QLabel("📍 Posição Atual")
        )


        self.pos_x = QLabel(
            "X: 0.000 mm"
        )

        self.pos_y = QLabel(
            "Y: 0.000 mm"
        )

        self.pos_z = QLabel(
            "Z: 0.000 mm"
        )


        pos_layout.addWidget(
            self.pos_x
        )

        pos_layout.addWidget(
            self.pos_y
        )

        pos_layout.addWidget(
            self.pos_z
        )



        # =====================================
        # PASSO
        # =====================================

        self.passo = QSpinBox()

        self.passo.setRange(
            1,
            100
        )

        self.passo.setValue(
            10
        )



        # =====================================
        # CONTROLES XYZ
        # =====================================

        caixa = QFrame()

        caixa.setObjectName(
            "controlBox"
        )


        controles = QHBoxLayout(
            caixa
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
                100,
                70
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



        # Eixo Z

        zlayout = QVBoxLayout()


        zlayout.addWidget(
            QLabel("Eixo Z")
        )


        self.zp = QPushButton(
            "Z +"
        )

        self.zm = QPushButton(
            "Z -"
        )


        self.zp.setObjectName(
            "actionButton"
        )

        self.zm.setObjectName(
            "actionButton"
        )


        zlayout.addWidget(
            self.zp
        )

        zlayout.addWidget(
            self.zm
        )



        controles.addLayout(
            grid
        )

        controles.addSpacing(
            40
        )

        controles.addLayout(
            zlayout
        )



        # =====================================
        # BOTÕES INFERIORES
        # =====================================

        botoes = QHBoxLayout()


        home = QPushButton(
            "🏠 ZERAR EIXOS"
        )

        stop = QPushButton(
            "🛑 STOP"
        )

        continuar = QPushButton(
            "▶ CONTINUAR"
        )


        for botao in (
            home,
            stop,
            continuar
        ):

            botao.setObjectName(
                "actionButton"
            )

            botao.setMinimumHeight(
                50
            )

            botoes.addWidget(
                botao
            )



        # =====================================
        # EVENTOS
        # =====================================

        self.xp.clicked.connect(
            lambda:
            self.mover_x(
                self.passo.value()
            )
        )


        self.xm.clicked.connect(
            lambda:
            self.mover_x(
                -self.passo.value()
            )
        )


        self.yp.clicked.connect(
            lambda:
            self.mover_y(
                self.passo.value()
            )
        )


        self.ym.clicked.connect(
            lambda:
            self.mover_y(
                -self.passo.value()
            )
        )


        self.zp.clicked.connect(
            lambda:
            self.mover_z(
                self.passo.value()
            )
        )


        self.zm.clicked.connect(
            lambda:
            self.mover_z(
                -self.passo.value()
            )
        )


        home.clicked.connect(
            self.zerar_eixos
        )


        stop.clicked.connect(
            self.stop
        )


        continuar.clicked.connect(
            self.reset
        )



        # Montagem

        principal.addWidget(
            titulo
        )

        principal.addWidget(
            self.status
        )

        principal.addWidget(
            pos_box
        )

        principal.addWidget(
            QLabel("Passo (mm)")
        )

        principal.addWidget(
            self.passo
        )

        principal.addWidget(
            caixa
        )

        principal.addLayout(
            botoes
        )

        principal.addStretch()



    # =====================================
    # STATUS
    # =====================================

    def atualizar_conexao(self, conectado):

        if conectado:

            self.status.setObjectName(
                "online"
            )

            self.status.setText(
                "🟢 MKS DLC32 conectada"
            )

        else:

            self.status.setObjectName(
                "offline"
            )

            self.status.setText(
                "🔴 MKS DLC32 desconectada"
            )



    # =====================================
    # POSIÇÃO
    # =====================================

    def atualizar_posicao(self):

        if not self.mks.conectado:
            return


        s = self.mks.ler_status()


        if s:

            self.pos_x.setText(
                f"X: {s['X']:.3f} mm"
            )

            self.pos_y.setText(
                f"Y: {s['Y']:.3f} mm"
            )

            self.pos_z.setText(
                f"Z: {s['Z']:.3f} mm"
            )



    # =====================================
    # MOVIMENTO
    # =====================================

    def mover_x(self, valor):

        if self.mks.conectado:

            self.movimento.mover_x(
                valor
            )


    def mover_y(self, valor):

        if self.mks.conectado:

            self.movimento.mover_y(
                valor
            )


    def mover_z(self, valor):

        if self.mks.conectado:

            self.movimento.mover_z(
                valor
            )



    # =====================================
    # HOME
    # =====================================

    def zerar_eixos(self):

        if not self.mks.conectado:

            self.status.setText(
                "🔴 MKS DLC32 desconectada"
            )

            return


        if self.mks.zerar_eixos():

            self.status.setText(
                "🟢 Eixos zerados"
            )

        else:

            self.status.setText(
                "🔴 Falha ao zerar eixos"
            )



    # =====================================
    # COMANDOS
    # =====================================

    def stop(self):

        self.mks.enviar_comando(
            "!"
        )


    def reset(self):

        self.mks.enviar_comando(
            "~"
        )