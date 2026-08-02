from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)

from ui.widgets.card import InfoCard



class DashboardPage(QWidget):


    def __init__(self, mks):

        super().__init__()


        self.mks = mks


        self.criar_interface()




    def criar_interface(self):

        layout = QVBoxLayout()



        titulo = QLabel(
            "Dashboard"
        )


        titulo.setStyleSheet(
            """
            font-size:26px;
            font-weight:bold;
            """
        )


        layout.addWidget(
            titulo
        )



        # ===============================
        # LINHA SUPERIOR
        # ===============================


        linha1 = QHBoxLayout()



        self.maquina = InfoCard(
            "Máquina",
            "IDLE"
        )



        self.conexao = InfoCard(
            "MKS DLC32",
            "Verificando..."
        )



        self.estado = InfoCard(
            "Estado",
            "Pronto"
        )



        linha1.addWidget(
            self.maquina
        )


        linha1.addWidget(
            self.conexao
        )


        linha1.addWidget(
            self.estado
        )




        # ===============================
        # EIXOS
        # ===============================


        linha2 = QHBoxLayout()



        self.x = InfoCard(
            "Eixo X",
            "0 mm"
        )


        self.y = InfoCard(
            "Eixo Y",
            "0 mm"
        )


        self.z = InfoCard(
            "Eixo Z",
            "0 mm"
        )



        linha2.addWidget(
            self.x
        )


        linha2.addWidget(
            self.y
        )


        linha2.addWidget(
            self.z
        )




        layout.addLayout(
            linha1
        )


        layout.addLayout(
            linha2
        )



        self.setLayout(
            layout
        )



        # Atualiza estado inicial

        self.atualizar_status()




    # =====================================
    # ATUALIZA STATUS DA MKS
    # =====================================

    def atualizar_status(self):


        if self.mks.conectado:


            self.conexao.atualizar_valor(
                "🟢 Conectada"
            )


        else:


            self.conexao.atualizar_valor(
                "🔴 Desconectada"
            )