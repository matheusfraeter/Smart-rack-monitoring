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
            self.mks
        )

        self.passo = 10

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

        self.status = QLabel(
            "MKS DLC32 desconectada"
        )

        self.status.setObjectName(
            "offline"
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
    # STATUS
    # =====================================================

    def atualizar_conexao(
        self,
        conectado
    ):

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

        self.status.style().unpolish(
            self.status
        )

        self.status.style().polish(
            self.status
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

            self.atualizar_conexao(
                False
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
        print(">>> MANUAL PAGE")
        print(f">>> SOLICITADO Y: {valor}")

        if not self.mks.conectado:

            print(">>> MKS DESCONECTADA")

            self.atualizar_conexao(
                False
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
        print(">>> MANUAL PAGE")
        print(f">>> SOLICITADO Z: {valor}")

        if not self.mks.conectado:

            print(">>> MKS DESCONECTADA")

            self.atualizar_conexao(
                False
            )

            return

        resultado = self.movimento.mover_z(
            valor
        )

        print(
            f">>> RESULTADO Z: {resultado}"
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