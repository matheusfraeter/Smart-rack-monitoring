"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: movement_page.py
 Descrição...: Interface de controle de movimentações
=========================================================
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QGridLayout
)


from controllers.movement_controller import MovementController
from database import Database
from movement import Movement



class MovementPage(QWidget):


    def __init__(self, mks):

        super().__init__()


        # Comunicação com MKS
        self.movimento = Movement(mks)


        self.controller = MovementController()


        self.db = Database()


        self.id_movimento = None


        self.criar_interface()




    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        layout = QVBoxLayout()



        titulo = QLabel(
            "🚜 Controle de Movimentação"
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



        self.info = QLabel(
            "Nenhuma movimentação criada"
        )


        self.info.setStyleSheet(
            """
            font-size:18px;
            """
        )



        # ===============================
        # CONTROLE MANUAL
        # ===============================


        manual_titulo = QLabel(
            "Controle Manual dos Eixos"
        )


        manual_titulo.setStyleSheet(
            """
            font-size:20px;
            font-weight:bold;
            """
        )


        layout.addWidget(
            manual_titulo
        )



        grid = QGridLayout()



        xmais = QPushButton("X +")
        xmenos = QPushButton("X -")

        ymais = QPushButton("Y +")
        ymenos = QPushButton("Y -")

        zmais = QPushButton("Z +")
        zmenos = QPushButton("Z -")



        xmais.clicked.connect(
            lambda: self.movimento.mover_x(10)
        )


        xmenos.clicked.connect(
            lambda: self.movimento.mover_x(-10)
        )


        ymais.clicked.connect(
            lambda: self.movimento.mover_y(10)
        )


        ymenos.clicked.connect(
            lambda: self.movimento.mover_y(-10)
        )


        zmais.clicked.connect(
            lambda: self.movimento.mover_z(10)
        )


        zmenos.clicked.connect(
            lambda: self.movimento.mover_z(-10)
        )



        grid.addWidget(
            ymais,
            0,
            1
        )

        grid.addWidget(
            xmenos,
            1,
            0
        )

        grid.addWidget(
            xmais,
            1,
            2
        )

        grid.addWidget(
            ymenos,
            2,
            1
        )

        grid.addWidget(
            zmais,
            3,
            1
        )

        grid.addWidget(
            zmenos,
            4,
            1
        )



        layout.addLayout(
            grid
        )




        # ===============================
        # MOVIMENTO RACK
        # ===============================


        self.origem = QComboBox()

        self.destino = QComboBox()



        self.carregar_posicoes()



        linha_origem = QHBoxLayout()


        linha_origem.addWidget(
            QLabel("Origem:")
        )


        linha_origem.addWidget(
            self.origem
        )



        linha_destino = QHBoxLayout()


        linha_destino.addWidget(
            QLabel("Destino:")
        )


        linha_destino.addWidget(
            self.destino
        )



        criar = QPushButton(
            "📦 Criar Movimento"
        )


        criar.clicked.connect(
            self.criar_movimento
        )



        iniciar = QPushButton(
            "▶ Iniciar"
        )


        iniciar.clicked.connect(
            self.iniciar
        )



        finalizar = QPushButton(
            "✔ Finalizar"
        )


        finalizar.clicked.connect(
            self.finalizar
        )



        botoes = QHBoxLayout()


        botoes.addWidget(
            criar
        )


        botoes.addWidget(
            iniciar
        )


        botoes.addWidget(
            finalizar
        )



        # ===============================
        # HISTÓRICO
        # ===============================


        self.tabela = QTableWidget()


        self.tabela.setColumnCount(
            5
        )


        self.tabela.setHorizontalHeaderLabels(
            [
                "ID",
                "Data",
                "Origem",
                "Destino",
                "Status"
            ]
        )



        layout.addLayout(
            linha_origem
        )


        layout.addLayout(
            linha_destino
        )


        layout.addLayout(
            botoes
        )


        layout.addWidget(
            self.info
        )


        layout.addWidget(
            QLabel(
                "Últimas movimentações:"
            )
        )


        layout.addWidget(
            self.tabela
        )



        self.setLayout(
            layout
        )


        self.atualizar_tabela()




    # =====================================
    # POSIÇÕES
    # =====================================

    def carregar_posicoes(self):

        posicoes = self.db.listar_posicoes()


        for dados in posicoes:

            endereco = dados[0]


            self.origem.addItem(
                endereco
            )


            self.destino.addItem(
                endereco
            )




    # =====================================
    # CRIAR MOVIMENTO
    # =====================================

    def criar_movimento(self):

        resultado = self.controller.criar_movimento(
            self.origem.currentText(),
            self.destino.currentText()
        )


        if resultado["sucesso"]:

            movimentos = self.db.listar_movimentos()


            self.id_movimento = movimentos[0][0]


            self.info.setText(
                f"ID {self.id_movimento} criado"
            )


        else:

            QMessageBox.warning(
                self,
                "Erro",
                resultado["mensagem"]
            )


        self.atualizar_tabela()




    # =====================================
    # INICIAR
    # =====================================

    def iniciar(self):

        if self.id_movimento:

            self.controller.iniciar_movimento(
                self.id_movimento
            )


            self.info.setText(
                "Movimento iniciado"
            )


        self.atualizar_tabela()




    # =====================================
    # FINALIZAR
    # =====================================

    def finalizar(self):

        if self.id_movimento:

            self.controller.finalizar_movimento(
                self.id_movimento
            )


            self.info.setText(
                "Movimento finalizado"
            )


        self.atualizar_tabela()




    # =====================================
    # TABELA
    # =====================================

    def atualizar_tabela(self):

        movimentos = self.db.listar_movimentos()


        self.tabela.setRowCount(
            len(movimentos)
        )


        for linha, dados in enumerate(movimentos):

            for coluna, valor in enumerate(dados):

                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(
                        str(valor)
                    )
                )