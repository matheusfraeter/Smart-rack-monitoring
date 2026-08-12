"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: ui/widgets/topbar.py
 Descrição...: Barra superior com status da MKS DLC32
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

        self.setObjectName("topBar")

        self.criar_interface()

        # =====================================
        # TIMER DE ATUALIZAÇÃO
        # =====================================

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.atualizar_status
        )

        self.timer.start(500)


    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            20,
            12,
            20,
            12
        )

        layout.setSpacing(10)


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

        layout.addLayout(topo)


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


        # =====================================
        # BOTÃO CONECTAR
        # =====================================

        self.bt_conectar = QPushButton(
            "Conectar MKS"
        )

        self.bt_conectar.setObjectName(
            "topButton"
        )

        inferior.addWidget(
            self.bt_conectar
        )


        # =====================================
        # BOTÃO HOME
        # =====================================

        self.bt_home = QPushButton(
            "Zerar Eixos"
        )

        self.bt_home.setObjectName(
            "topButton"
        )

        self.bt_home.setEnabled(False)

        inferior.addWidget(
            self.bt_home
        )


        layout.addLayout(inferior)


        # =====================================
        # EVENTOS
        # =====================================

        self.bt_conectar.clicked.connect(
            self.conectar_mks
        )

        self.bt_home.clicked.connect(
            self.zerar_eixos
        )


    # =====================================
    # CRIAR MINI CARD
    # =====================================

    def criar_card(self, titulo, valor):

        card = QFrame()

        card.setObjectName(
            "topCard"
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            12,
            8,
            12,
            8
        )

        layout.setSpacing(2)


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
    # ATUALIZA VISUAL DA CONEXÃO
    # =====================================

    def atualizar_conexao_visual(self, conectado):

        if conectado:

            self.conexao.setObjectName(
                "online"
            )

            self.conexao.setText(
                "MKS CONECTADA"
            )

            self.bt_conectar.setText(
                "MKS Conectada"
            )

        else:

            self.conexao.setObjectName(
                "offline"
            )

            self.conexao.setText(
                "DESCONECTADA"
            )

            self.bt_conectar.setText(
                "Conectar MKS"
            )


        # Força atualização do QSS

        self.conexao.style().unpolish(
            self.conexao
        )

        self.conexao.style().polish(
            self.conexao
        )


        self.conexao.update()


    # =====================================
    # ATUALIZA STATUS
    # =====================================

    def atualizar_status(self):

        try:

            # =================================
            # SEM CONEXÃO
            # =================================

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


            # =================================
            # CONECTADO
            # =================================

            self.atualizar_conexao_visual(
                True
            )


            dados = self.mks.ler_status()


            if not dados:

                return


            # =================================
            # ESTADO
            # =================================

            estado = dados.get(
                "estado",
                "---"
            )


            self.estado.setText(
                estado.upper()
            )


            # =================================
            # POSIÇÕES
            # =================================

            self.x.setText(
                f'{dados.get("X", 0.0):.3f}'
            )


            self.y.setText(
                f'{dados.get("Y", 0.0):.3f}'
            )


            self.z.setText(
                f'{dados.get("Z", 0.0):.3f}'
            )


            # =================================
            # HOME
            # =================================

            self.bt_home.setEnabled(
                True
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

        # Já conectado
        if self.mks.conectado:

            self.atualizar_status()

            return


        conectado = self.mks.conectar()


        if conectado:

            self.atualizar_conexao_visual(
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


        self.bt_home.setEnabled(
            False
        )


        self.estado.setText(
            "HOMING"
        )


        sucesso = self.mks.zerar_eixos()


        if sucesso:

            self.estado.setText(
                "HOMING"
            )

        else:

            self.estado.setText(
                "ERRO"
            )


        # O estado real será atualizado
        # automaticamente pelo WebSocket.