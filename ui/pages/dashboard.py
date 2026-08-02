"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: dashboard.py
 Descrição...: Dashboard com status real da MKS DLC32
=========================================================
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel
)

from PySide6.QtCore import QTimer

from ui.widgets.card import InfoCard



class DashboardPage(QWidget):

    def __init__(self, mks):

        super().__init__()

        self.mks = mks

        self.criar_interface()


        # Atualização automática

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.atualizar_status
        )

        self.timer.start(1000)



    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        layout = QVBoxLayout(self)


        layout.setSpacing(20)


        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )



        # =====================================
        # TÍTULO
        # =====================================


        titulo = QLabel(
            "Dashboard"
        )

        titulo.setObjectName(
            "title"
        )


        layout.addWidget(
            titulo
        )



        # =====================================
        # STATUS PRINCIPAL
        # =====================================


        linha1 = QHBoxLayout()


        linha1.setSpacing(
            20
        )



        self.maquina = InfoCard(
            "🏭 Máquina",
            "IDLE"
        )


        self.conexao = InfoCard(
            "📡 MKS DLC32",
            "Verificando..."
        )


        self.estado = InfoCard(
            "⚙ Estado",
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



        layout.addLayout(
            linha1
        )



        # =====================================
        # EIXOS
        # =====================================


        linha2 = QHBoxLayout()


        linha2.setSpacing(
            20
        )



        self.x = InfoCard(
            "↔ Eixo X",
            "0.000 mm"
        )


        self.y = InfoCard(
            "↕ Eixo Y",
            "0.000 mm"
        )


        self.z = InfoCard(
            "⬆ Eixo Z",
            "0.000 mm"
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
            linha2
        )



        layout.addStretch()



    # =====================================
    # ATUALIZA STATUS DA MKS
    # =====================================

    def atualizar_status(self):

        try:


            if self.mks.conectado:


                self.conexao.atualizar_valor(
                    "🟢 Conectada"
                )


            else:


                self.conexao.atualizar_valor(
                    "🔴 Desconectada"
                )


                return



            dados = self.mks.ler_status()



            if not dados:

                return



            estado = dados["estado"]



            # Estado da máquina

            self.maquina.atualizar_valor(
                estado
            )



            if estado == "IDLE":


                self.estado.atualizar_valor(
                    "Pronto"
                )


            elif estado == "MOVENDO":


                self.estado.atualizar_valor(
                    "Executando"
                )


            else:


                self.estado.atualizar_valor(
                    estado
                )



            # Posição dos eixos


            self.x.atualizar_valor(
                f'{dados["X"]:.3f} mm'
            )


            self.y.atualizar_valor(
                f'{dados["Y"]:.3f} mm'
            )


            self.z.atualizar_valor(
                f'{dados["Z"]:.3f} mm'
            )



        except Exception as erro:


            print(
                "Erro dashboard:",
                erro
            )