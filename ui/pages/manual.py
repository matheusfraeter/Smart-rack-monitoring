"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: manual.py
 Descrição...: Controle manual dos eixos XYZ
=========================================================
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGridLayout,
    QSpinBox, QFrame
)

from PySide6.QtCore import QTimer

from movement import Movement



class ManualPage(QWidget):

    def __init__(self, mks):

        super().__init__()

        self.mks = mks
        self.movimento = Movement(mks)

        self.criar_interface()

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_posicao)
        self.timer.start(1000)



    def criar_interface(self):

        self.setStyleSheet("""
            QWidget {
                background:#1e1e1e;
                color:white;
            }

            QPushButton {
                background:#333333;
                color:white;
                font-size:18px;
                font-weight:bold;
                border-radius:8px;
            }

            QPushButton:hover {
                background:#444444;
            }
        """)


        principal = QVBoxLayout(self)

        principal.setContentsMargins(
            20,20,20,20
        )

        principal.setSpacing(10)



        titulo = QLabel(
            "🎮 Controle Manual XYZ"
        )

        titulo.setStyleSheet(
            "font-size:26px;font-weight:bold;"
        )


        self.status = QLabel(
            "MKS DLC32: Aguardando conexão"
        )



        # =========================
        # POSIÇÃO
        # =========================

        pos_box = QFrame()

        pos_box.setMaximumHeight(140)

        pos_box.setStyleSheet("""
            QFrame{
                background:#252525;
                border-radius:12px;
            }
        """)


        pos_layout = QVBoxLayout(pos_box)


        titulo_pos = QLabel(
            "📍 Posição Atual"
        )

        titulo_pos.setStyleSheet(
            "font-size:18px;font-weight:bold;"
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
            titulo_pos
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



        # =========================
        # PASSO
        # =========================

        self.passo = QSpinBox()

        self.passo.setRange(
            1,
            100
        )

        self.passo.setValue(
            10
        )



        # =========================
        # CONTROLE XYZ
        # =========================


        caixa = QFrame()

        caixa.setMinimumHeight(
            250
        )


        caixa.setStyleSheet("""
            QFrame{
                background:#202020;
                border-radius:15px;
            }
        """)


        controles = QHBoxLayout(caixa)


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


        for b in [
            self.xp,
            self.xm,
            self.ym,
            self.yp
        ]:

            b.setMinimumSize(
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



        z_layout = QVBoxLayout()


        z_label = QLabel(
            "Eixo Z"
        )

        z_label.setStyleSheet(
            "font-size:18px;font-weight:bold;"
        )


        self.zp = QPushButton(
            "Z +"
        )

        self.zm = QPushButton(
            "Z -"
        )


        self.zp.setMinimumSize(
            90,
            45
        )

        self.zm.setMinimumSize(
            90,
            45
        )


        z_layout.addWidget(
            z_label
        )

        z_layout.addWidget(
            self.zp
        )

        z_layout.addWidget(
            self.zm
        )


        controles.addLayout(
            grid
        )

        controles.addSpacing(
            40
        )

        controles.addLayout(
            z_layout
        )



        # =========================
        # STOP
        # =========================


        botoes = QHBoxLayout()


        stop = QPushButton(
            "🛑 STOP"
        )


        continuar = QPushButton(
            "▶ CONTINUAR"
        )


        botoes.addWidget(
            stop
        )

        botoes.addWidget(
            continuar
        )



        # =========================
        # EVENTOS
        # =========================


        self.xp.clicked.connect(
            lambda:self.mover_x(self.passo.value())
        )

        self.xm.clicked.connect(
            lambda:self.mover_x(-self.passo.value())
        )

        self.yp.clicked.connect(
            lambda:self.mover_y(self.passo.value())
        )

        self.ym.clicked.connect(
            lambda:self.mover_y(-self.passo.value())
        )

        self.zp.clicked.connect(
            lambda:self.mover_z(self.passo.value())
        )

        self.zm.clicked.connect(
            lambda:self.mover_z(-self.passo.value())
        )


        stop.clicked.connect(
            self.stop
        )

        continuar.clicked.connect(
            self.reset
        )



        # =========================
        # MONTAGEM
        # =========================


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



    def atualizar_posicao(self):

        try:

            s = self.mks.ler_status()

            self.pos_x.setText(
                f"X: {s['X']:.3f} mm"
            )

            self.pos_y.setText(
                f"Y: {s['Y']:.3f} mm"
            )

            self.pos_z.setText(
                f"Z: {s['Z']:.3f} mm"
            )

        except Exception as erro:

            print(
                "Erro posição:",
                erro
            )



    def mover_x(self, valor):

        if self.mks.conectado:
            self.movimento.mover_x(valor)



    def mover_y(self, valor):

        if self.mks.conectado:
            self.movimento.mover_y(valor)



    def mover_z(self, valor):

        if self.mks.conectado:
            self.movimento.mover_z(valor)



    def stop(self):

        self.mks.enviar_comando("!")



    def reset(self):

        self.mks.enviar_comando("~")