"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: topbar.py
 Descrição...: Barra superior da aplicação
=========================================================
"""

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout
)

from PySide6.QtCore import QTimer



class TopBar(QFrame):

    def __init__(self, mks):

        super().__init__()

        self.mks = mks

        self.setObjectName(
            "topBar"
        )

        self.criar_interface()


        self.timer = QTimer()

        self.timer.timeout.connect(
            self.atualizar_status
        )

        self.timer.start(
            1000
        )



    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        layout = QVBoxLayout(
            self
        )


        layout.setContentsMargins(
            20,
            12,
            20,
            12
        )


        layout.setSpacing(
            10
        )



        # =====================================
        # CABEÇALHO
        # =====================================

        topo = QHBoxLayout()


        self.titulo = QLabel(
            "SMART RACK MONITORING"
        )

        self.titulo.setObjectName(
            "topTitle"
        )


        self.conexao = QLabel(
            "DESCONECTADA"
        )

        self.conexao.setObjectName(
            "offline"
        )


        topo.addWidget(
            self.titulo
        )


        topo.addStretch()


        topo.addWidget(
            self.conexao
        )


        layout.addLayout(
            topo
        )



        # =====================================
        # CARDS + BOTÕES
        # =====================================

        inferior = QHBoxLayout()



        self.card_estado, self.estado = self.criar_card(
            "Estado",
            "---"
        )


        self.card_x, self.x = self.criar_card(
            "Eixo X",
            "0.000"
        )


        self.card_y, self.y = self.criar_card(
            "Eixo Y",
            "0.000"
        )


        self.card_z, self.z = self.criar_card(
            "Eixo Z",
            "0.000"
        )



        inferior.addWidget(
            self.card_estado
        )

        inferior.addWidget(
            self.card_x
        )

        inferior.addWidget(
            self.card_y
        )

        inferior.addWidget(
            self.card_z
        )



        inferior.addStretch()



        self.bt_conectar = QPushButton(
            "Conectar MKS"
        )

        self.bt_conectar.setObjectName(
            "topButton"
        )



        self.bt_home = QPushButton(
            "Zerar Eixos"
        )

        self.bt_home.setObjectName(
            "topButton"
        )


        self.bt_home.setEnabled(
            False
        )



        inferior.addWidget(
            self.bt_conectar
        )


        inferior.addWidget(
            self.bt_home
        )



        layout.addLayout(
            inferior
        )



        self.bt_conectar.clicked.connect(
            self.conectar_mks
        )


        self.bt_home.clicked.connect(
            self.zerar_eixos
        )



    # =====================================
    # CRIAR MINI CARD
    # =====================================

    def criar_card(
        self,
        titulo,
        valor
    ):

        card = QFrame()

        card.setObjectName(
            "topCard"
        )


        layout = QVBoxLayout(
            card
        )


        label_titulo = QLabel(
            titulo
        )

        label_titulo.setObjectName(
            "topCardTitle"
        )



        label_valor = QLabel(
            valor
        )

        label_valor.setObjectName(
            "topCardValue"
        )



        layout.addWidget(
            label_titulo
        )


        layout.addWidget(
            label_valor
        )



        return card, label_valor



    # =====================================
    # ATUALIZA COR DA CONEXÃO
    # =====================================

    def atualizar_conexao_visual(
        self,
        conectado
    ):

        if conectado:

            self.conexao.setObjectName(
                "online"
            )

            self.conexao.setText(
                "MKS CONECTADA"
            )


        else:

            self.conexao.setObjectName(
                "offline"
            )

            self.conexao.setText(
                "DESCONECTADA"
            )



        self.conexao.style().unpolish(
            self.conexao
        )

        self.conexao.style().polish(
            self.conexao
        )



    # =====================================
    # ATUALIZA STATUS
    # =====================================

    def atualizar_status(self):

        try:

            if not self.mks.conectado:


                self.atualizar_conexao_visual(
                    False
                )


                self.estado.setText(
                    "---"
                )

                self.x.setText(
                    "0.000"
                )

                self.y.setText(
                    "0.000"
                )

                self.z.setText(
                    "0.000"
                )


                self.bt_home.setEnabled(
                    False
                )


                return



            self.atualizar_conexao_visual(
                True
            )


            self.bt_home.setEnabled(
                True
            )



            dados = self.mks.ler_status()



            if not dados:

                return



            self.estado.setText(
                dados["estado"]
            )


            self.x.setText(
                f'{dados["X"]:.3f}'
            )


            self.y.setText(
                f'{dados["Y"]:.3f}'
            )


            self.z.setText(
                f'{dados["Z"]:.3f}'
            )



        except Exception as erro:

            print(
                "Erro TopBar:",
                erro
            )



    # =====================================
    # CONECTAR
    # =====================================

    def conectar_mks(self):

        conectado = self.mks.conectar()



        if conectado:


            self.atualizar_conexao_visual(
                True
            )


            self.bt_home.setEnabled(
                True
            )


            self.atualizar_status()



        else:


            self.atualizar_conexao_visual(
                False
            )


            self.bt_home.setEnabled(
                False
            )



    # =====================================
    # HOME
    # =====================================

    def zerar_eixos(self):

        if not self.mks.conectado:

            return



        sucesso = self.mks.zerar_eixos()



        if sucesso:


            self.estado.setText(
                "HOME"
            )


        else:


            self.estado.setText(
                "ERRO"
            )