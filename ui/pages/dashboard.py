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
    QLabel,
    QPushButton
)

from PySide6.QtCore import QTimer

from ui.widgets.card import InfoCard



class DashboardPage(QWidget):


    def __init__(self, mks, manual):

        super().__init__()

        self.mks = mks
        self.manual = manual

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
        # STATUS
        # =====================================

        linha1 = QHBoxLayout()


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



        # =====================================
        # BOTÕES
        # =====================================

        linha3 = QHBoxLayout()



        self.botao_conectar = QPushButton(
            "🔌 Conectar MKS"
        )


        self.botao_home = QPushButton(
            "🏠 Zerar Eixos"
        )



        self.botao_conectar.setMinimumHeight(
            50
        )


        self.botao_home.setMinimumHeight(
            50
        )



        linha3.addWidget(
            self.botao_conectar
        )


        linha3.addWidget(
            self.botao_home
        )



        layout.addLayout(
            linha3
        )



        self.botao_conectar.clicked.connect(
            self.conectar_mks
        )


        self.botao_home.clicked.connect(
            self.zerar_eixos
        )



        layout.addStretch()







    # =====================================
    # ATUALIZA STATUS
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

                self.manual.atualizar_conexao(
                  False
                )


                self.maquina.atualizar_valor(
                    "Desligada"
                )


                self.estado.atualizar_valor(
                    "Sem conexão"
                )


                return





            dados = self.mks.ler_status()



            if not dados:

                return





            estado = dados["estado"]





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


            elif estado == "ZERO":


                self.estado.atualizar_valor(
                    "Eixos zerados"
                )


            else:


                self.estado.atualizar_valor(
                    estado
                )





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







    # =====================================
    # CONECTAR MKS
    # =====================================

    def conectar_mks(self):


        conectado = self.mks.conectar()



        if conectado:


            self.conexao.atualizar_valor(
                "🟢 Conectada"
            )

            self.manual.atualizar_conexao(
             True
            )


            # Atualiza todos os mostradores imediatamente

            self.atualizar_status()



        else:


            self.conexao.atualizar_valor(
                "🔴 Desconectada"
            )

            self.manual.atualizar_conexao(
              False
            )

            self.maquina.atualizar_valor(
                "Desligada"
            )


            self.estado.atualizar_valor(
                "Sem conexão"
            )







    # =====================================
    # ZERAR EIXOS
    # =====================================

    def zerar_eixos(self):


        if not self.mks.conectado:


            self.estado.atualizar_valor(
                "Sem conexão"
            )


            return





        sucesso = self.mks.zerar_eixos()





        if sucesso:


            self.estado.atualizar_valor(
                "Eixos zerados"
            )


            self.atualizar_status()



        else:


            self.estado.atualizar_valor(
                "Erro HOME"
            )