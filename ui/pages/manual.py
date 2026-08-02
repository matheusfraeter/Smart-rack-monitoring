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
    QLabel,
    QPushButton,
    QGridLayout,
    QSpinBox,
    QMessageBox
)


from movement import Movement




class ManualPage(QWidget):


    def __init__(
        self,
        mks
    ):

        super().__init__()


        self.mks = mks


        self.movimento = Movement(
            self.mks
        )


        self.criar_interface()




    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):


        layout = QVBoxLayout()



        titulo = QLabel(
            "🎮 Controle Manual"
        )


        titulo.setStyleSheet(
            """
            font-size:26px;
            font-weight:bold;
            """
        )



        self.status = QLabel(
            "MKS DLC32: Aguardando conexão"
        )



        self.passo = QSpinBox()


        self.passo.setRange(
            1,
            100
        )


        self.passo.setValue(
            10
        )




        controle = QGridLayout()



        btn_zmais = QPushButton(
            "Z +"
        )


        btn_zmenos = QPushButton(
            "Z -"
        )


        btn_xmais = QPushButton(
            "X +"
        )


        btn_xmenos = QPushButton(
            "X -"
        )


        btn_ymais = QPushButton(
            "Y +"
        )


        btn_ymenos = QPushButton(
            "Y -"
        )



        btn_stop = QPushButton(
            "🛑 STOP"
        )


        btn_reset = QPushButton(
            "▶ CONTINUAR"
        )



        botoes = [

            btn_zmais,
            btn_zmenos,
            btn_xmais,
            btn_xmenos,
            btn_ymais,
            btn_ymenos,
            btn_stop,
            btn_reset

        ]



        for botao in botoes:


            botao.setMinimumSize(
                120,
                50
            )




        # Movimento XYZ


        btn_xmais.clicked.connect(
            lambda:
            self.mover_x(
                self.passo.value()
            )
        )


        btn_xmenos.clicked.connect(
            lambda:
            self.mover_x(
                -self.passo.value()
            )
        )



        btn_ymais.clicked.connect(
            lambda:
            self.mover_y(
                self.passo.value()
            )
        )


        btn_ymenos.clicked.connect(
            lambda:
            self.mover_y(
                -self.passo.value()
            )
        )



        btn_zmais.clicked.connect(
            lambda:
            self.mover_z(
                self.passo.value()
            )
        )


        btn_zmenos.clicked.connect(
            lambda:
            self.mover_z(
                -self.passo.value()
            )
        )



        btn_stop.clicked.connect(
            self.stop
        )


        btn_reset.clicked.connect(
            self.reset
        )





        controle.addWidget(
            btn_zmais,
            0,
            1
        )


        controle.addWidget(
            btn_ymenos,
            1,
            0
        )


        controle.addWidget(
            btn_xmais,
            1,
            1
        )


        controle.addWidget(
            btn_ymais,
            1,
            2
        )


        controle.addWidget(
            btn_zmenos,
            2,
            1
        )


        controle.addWidget(
            btn_xmenos,
            3,
            1
        )


        controle.addWidget(
            btn_stop,
            4,
            0
        )


        controle.addWidget(
            btn_reset,
            4,
            2
        )




        layout.addWidget(
            titulo
        )


        layout.addWidget(
            self.status
        )


        layout.addWidget(
            QLabel(
                "Passo (mm)"
            )
        )


        layout.addWidget(
            self.passo
        )


        layout.addLayout(
            controle
        )



        self.setLayout(
            layout
        )




    # =====================================
    # MOVIMENTOS
    # =====================================


    def mover_x(
        self,
        valor
    ):

        if not self.mks.conectado:

            QMessageBox.warning(
                self,
                "Erro",
                "MKS DLC32 desconectada"
            )

            return


        self.movimento.mover_x(
            valor
        )



    def mover_y(
        self,
        valor
    ):


        if not self.mks.conectado:

            QMessageBox.warning(
                self,
                "Erro",
                "MKS DLC32 desconectada"
            )

            return


        self.movimento.mover_y(
            valor
        )



    def mover_z(
        self,
        valor
    ):


        if not self.mks.conectado:

            QMessageBox.warning(
                self,
                "Erro",
                "MKS DLC32 desconectada"
            )

            return


        self.movimento.mover_z(
            valor
        )




    # =====================================
    # CONTROLE MÁQUINA
    # =====================================


    def stop(self):

        self.mks.enviar_comando(
            "!"
        )



    def reset(self):

        self.mks.enviar_comando(
            "~"
        )