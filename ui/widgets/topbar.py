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
    QVBoxLayout,
    QSizePolicy
)

from PySide6.QtCore import (
    QTimer,
    Qt
)


class TopBar(QFrame):

    def __init__(self, mks):

        super().__init__()

        self.mks = mks

        self.setObjectName(
            "topBar"
        )

        # =====================================
        # CRIAR INTERFACE
        # =====================================

        self.criar_interface()

        # =====================================
        # TIMER DE ATUALIZAÇÃO
        # =====================================

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.atualizar_status
        )

        self.timer.start(
            500
        )


    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        self.layout_principal = QVBoxLayout(
            self
        )

        self.layout_principal.setContentsMargins(
            15,
            10,
            15,
            10
        )

        self.layout_principal.setSpacing(
            8
        )

        # =====================================
        # CABEÇALHO
        # =====================================

        self.topo = QHBoxLayout()

        self.topo.setSpacing(
            10
        )

        self.titulo = QLabel(
            "SMART RACK MONITORING"
        )

        self.titulo.setObjectName(
            "topTitle"
        )

        self.titulo.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.conexao = QLabel(
            "DESCONECTADA"
        )

        self.conexao.setObjectName(
            "offline"
        )

        self.conexao.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Fixed
        )

        self.topo.addWidget(
            self.titulo
        )

        self.topo.addStretch()

        self.topo.addWidget(
            self.conexao
        )

        self.layout_principal.addLayout(
            self.topo
        )

        # =====================================
        # ÁREA INFERIOR
        # =====================================

        self.inferior = QHBoxLayout()

        self.inferior.setSpacing(
            8
        )

        # =====================================
        # CARDS
        # =====================================

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

        self.inferior.addWidget(
            self.card_estado,
            1
        )

        self.inferior.addWidget(
            self.card_x,
            1
        )

        self.inferior.addWidget(
            self.card_y,
            1
        )

        self.inferior.addWidget(
            self.card_z,
            1
        )

        # =====================================
        # BOTÃO CONECTAR
        # =====================================

        self.bt_conectar = QPushButton(
            "Conectar MKS"
        )

        self.bt_conectar.setObjectName(
            "topButton"
        )

        self.bt_conectar.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.inferior.addWidget(
            self.bt_conectar,
            1
        )

        self.layout_principal.addLayout(
            self.inferior
        )

        # =====================================
        # EVENTOS
        # =====================================

        self.bt_conectar.clicked.connect(
            self.conectar_mks
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

        card.setMinimumWidth(
            70
        )

        card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        layout = QVBoxLayout(
            card
        )

        layout.setContentsMargins(
            8,
            5,
            8,
            5
        )

        layout.setSpacing(
            1
        )

        label_titulo = QLabel(
            titulo
        )

        label_titulo.setObjectName(
            "topCardTitle"
        )

        label_titulo.setAlignment(
            Qt.AlignCenter
        )

        label_valor = QLabel(
            valor
        )

        label_valor.setObjectName(
            "topCardValue"
        )

        label_valor.setAlignment(
            Qt.AlignCenter
        )

        label_valor.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        layout.addWidget(
            label_titulo
        )

        layout.addWidget(
            label_valor
        )

        return card, label_valor


    # =====================================
    # REDIMENSIONAMENTO
    # =====================================

    def resizeEvent(
        self,
        event
    ):

        super().resizeEvent(
            event
        )

        self.adaptar_layout()


    # =====================================
    # ADAPTAR LAYOUT
    # =====================================

    def adaptar_layout(self):

        largura = self.width()

        # =====================================
        # TELA MUITO PEQUENA
        # =====================================

        if largura < 750:

            self.inferior.setSpacing(
                5
            )

            self.layout_principal.setContentsMargins(
                8,
                6,
                8,
                6
            )

            self.bt_conectar.setText(
                "Conectar"
                if not self.mks.conectado
                else "Conectada"
            )

        # =====================================
        # TELA MÉDIA
        # =====================================

        elif largura < 1000:

            self.inferior.setSpacing(
                6
            )

            self.layout_principal.setContentsMargins(
                10,
                8,
                10,
                8
            )

            self.bt_conectar.setText(
                "Conectar MKS"
                if not self.mks.conectado
                else "MKS Conectada"
            )

        # =====================================
        # TELA GRANDE
        # =====================================

        else:

            self.inferior.setSpacing(
                8
            )

            self.layout_principal.setContentsMargins(
                15,
                10,
                15,
                10
            )

            self.bt_conectar.setText(
                "Conectar MKS"
                if not self.mks.conectado
                else "MKS Conectada"
            )


    # =====================================
    # ATUALIZA VISUAL DA CONEXÃO
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

        # =====================================
        # FORÇAR ATUALIZAÇÃO DO QSS
        # =====================================

        self.conexao.style().unpolish(
            self.conexao
        )

        self.conexao.style().polish(
            self.conexao
        )

        self.conexao.update()

        self.adaptar_layout()


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