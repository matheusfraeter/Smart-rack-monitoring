from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox,
    QGridLayout,
    QSpinBox
)

from communication import MKSConnection
from movement import Movement


class SmartRackGUI(QMainWindow):

    def __init__(self):
        super().__init__()

        self.mks = MKSConnection()
        self.movimento = Movement(self.mks)

        self.passo = 10

        self.setWindowTitle(
            "Smart Rack Monitoring"
        )

        self.resize(1200,700)

        self.criar_interface()



    def criar_interface(self):

        principal = QWidget()
        self.setCentralWidget(principal)


        layout_principal = QHBoxLayout()


        # MENU

        menu = QFrame()
        menu.setFixedWidth(220)

        menu_layout = QVBoxLayout()


        logo = QLabel(
            "SMART RACK"
        )

        logo.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)


        btn_conectar = QPushButton(
            "Conectar MKS DLC32"
        )

        btn_conectar.clicked.connect(
            self.conectar_mks
        )


        menu_layout.addWidget(logo)
        menu_layout.addWidget(btn_conectar)
        menu_layout.addStretch()

        menu.setLayout(menu_layout)



        # ÁREA PRINCIPAL

        area = QVBoxLayout()


        titulo = QLabel(
            "Painel de Controle da Empilhadeira"
        )

        titulo.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)


        self.status = QLabel(
            "🔴 MKS DLC32: Desconectada"
        )


        # PASSO

        passo_layout = QHBoxLayout()

        passo_label = QLabel(
            "Passo (mm):"
        )

        self.valor_passo = QSpinBox()

        self.valor_passo.setRange(
            1,100
        )

        self.valor_passo.setValue(
            10
        )


        passo_layout.addWidget(
            passo_label
        )

        passo_layout.addWidget(
            self.valor_passo
        )


        # CONTROLE XYZ

        controle = QLabel(
            "Controle Manual"
        )


        grid = QGridLayout()


        btn_ymais = QPushButton("Y +")
        btn_ymenos = QPushButton("Y -")

        btn_xmais = QPushButton("X +")
        btn_xmenos = QPushButton("X -")

        btn_zmais = QPushButton("Z +")
        btn_zmenos = QPushButton("Z -")

        btn_stop = QPushButton("🛑 EMERGÊNCIA STOP")

        btn_reset = QPushButton("▶ CONTINUAR")

        btn_stop.setMinimumSize(200,60)

        btn_reset.setMinimumSize(200,60)

        btn_stop.clicked.connect(
        self.emergencia_stop
        )


        btn_reset.clicked.connect(
        self.reset_maquina
        )


        btn_xmais.clicked.connect(
            lambda: self.mover_x(
                self.valor_passo.value()
            )
        )

        btn_xmenos.clicked.connect(
            lambda: self.mover_x(
                -self.valor_passo.value()
            )
        )


        btn_ymais.clicked.connect(
            lambda: self.mover_y(
                self.valor_passo.value()
            )
        )

        btn_ymenos.clicked.connect(
            lambda: self.mover_y(
                -self.valor_passo.value()
            )
        )


        btn_zmais.clicked.connect(
            lambda: self.mover_z(
                self.valor_passo.value()
            )
        )

        btn_zmenos.clicked.connect(
            lambda: self.mover_z(
                -self.valor_passo.value()
            )
        )


        grid.addWidget(btn_zmais,0,1)

        grid.addWidget(btn_ymenos,1,0)

        grid.addWidget(btn_xmais,1,1)

        grid.addWidget(btn_ymais,1,2)

        grid.addWidget(btn_zmenos,2,1)

        grid.addWidget(btn_xmenos,3,1)


        area.addWidget(titulo)

        area.addWidget(self.status)

        area.addLayout(passo_layout)

        area.addWidget(controle)

        area.addWidget(btn_stop)

        area.addWidget(btn_reset)

        area.addLayout(grid)

        layout_principal.addWidget(menu)

        layout_principal.addLayout(area)


        principal.setLayout(layout_principal)

    def conectar_mks(self):

        if self.mks.conectar():

            self.status.setText("🟢 MKS DLC32: Conectada")

        else:

            self.status.setText("🔴 MKS DLC32: Falha")



    def mover_x(self, valor):

        if not self.mks.conectado:
            QMessageBox.warning(
                self,
                "Erro",
                "MKS DLC32 desconectada"
            )
            return


        self.movimento.mover_x(valor)



    def mover_y(self, valor):

        if not self.mks.conectado:
            QMessageBox.warning(
                self,
                "Erro",
                "MKS DLC32 desconectada"
            )
            return


        self.movimento.mover_y(valor)



    def mover_z(self, valor):

        if not self.mks.conectado:
            QMessageBox.warning(
                self,
                "Erro",
                "MKS DLC32 desconectada"
            )
            return


        self.movimento.mover_z(valor)

    def emergencia_stop(self):

        self.mks.enviar_comando("!")

        self.status.setText("🔴 EMERGÊNCIA ATIVADA")



    def reset_maquina(self):

        self.mks.enviar_comando("~")

        self.status.setText("🟢 Máquina liberada")