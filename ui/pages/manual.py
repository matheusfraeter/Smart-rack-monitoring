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

from PySide6.QtCore import Qt

from movement import Movement



class ManualPage(QWidget):


    def __init__(self, mks):

        super().__init__()

        self.mks = mks

        self.movimento = Movement(
            mks
        )


        self.passo = 10


        self.criar_interface()



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



        # =====================================
        # TÍTULO
        # =====================================

        titulo = QLabel(
            "Controle Manual XYZ"
        )

        titulo.setObjectName(
            "title"
        )


        self.status = QLabel(
            ""
        )

        self.status.setObjectName(
            "offline"
        )



        # =====================================
        # CONTROLE DE PASSO
        # =====================================

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


        passo_box.addSpacing(
            20
        )


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



        # =====================================
        # CONTROLE XYZ
        # =====================================

        caixa = QFrame()

        caixa.setObjectName(
            "controlBox"
        )


        controles = QHBoxLayout(
            caixa
        )


        controles.setSpacing(
            60
        )


        controles.addStretch()



        # =====================================
        # MOVIMENTO XY
        # =====================================

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

        # =====================================
        # MOVIMENTO Z
        # =====================================

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



        controles.addSpacing(
            60
        )


        controles.addWidget(
            z_box
        )


        controles.addStretch()



        # =====================================
        # BOTÕES INFERIORES
        # =====================================

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


        stop.setMinimumHeight(
            50
        )


        continuar.setMinimumHeight(
            50
        )


        botoes.addWidget(
            stop
        )


        botoes.addWidget(
            continuar
        )



        # =====================================
        # EVENTOS
        # =====================================

        self.bt_mais.clicked.connect(
            self.aumentar_passo
        )


        self.bt_menos.clicked.connect(
            self.diminuir_passo
        )



        self.xp.clicked.connect(
            lambda:
            self.mover_x(
                self.passo
            )
        )


        self.xm.clicked.connect(
            lambda:
            self.mover_x(
                -self.passo
            )
        )


        self.yp.clicked.connect(
            lambda:
            self.mover_y(
                self.passo
            )
        )


        self.ym.clicked.connect(
            lambda:
            self.mover_y(
                -self.passo
            )
        )


        self.zp.clicked.connect(
            lambda:
            self.mover_z(
                self.passo
            )
        )


        self.zm.clicked.connect(
            lambda:
            self.mover_z(
                -self.passo
            )
        )


        stop.clicked.connect(
            self.stop
        )


        continuar.clicked.connect(
            self.reset
        )



        # =====================================
        # MONTAGEM FINAL
        # =====================================

        principal.addWidget(
            titulo
        )


        principal.addWidget(
            self.status
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



    # =====================================
    # CONTROLE DE PASSO
    # =====================================

    def aumentar_passo(self):

        if self.passo < 100:

            self.passo += 10

            self.passo_label.setText(
                f"{self.passo} mm"
            )



    def diminuir_passo(self):

        if self.passo > 10:

            self.passo -= 10

            self.passo_label.setText(
                f"{self.passo} mm"
            )



    # =====================================
    # STATUS
    # =====================================

    def atualizar_conexao(self, conectado):

        if conectado:

            self.status.setObjectName(
                "online"
            )

            self.status.setText(
                "MKS DLC32 conectada"
            )


        else:

            self.status.setObjectName(
                "offline"
            )

            self.status.setText(
                "MKS DLC32 desconectada"
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