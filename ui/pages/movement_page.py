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
    QTableWidgetItem
)


from controllers.movement_controller import MovementController
from database import Database



class MovementPage(QWidget):


    def __init__(self):

        super().__init__()


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



        self.info = QLabel(
            "Nenhuma movimentação criada"
        )


        self.info.setStyleSheet(
            """
            font-size:18px;
            """
        )



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



        layout.addWidget(
            titulo
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
    # CARREGAR POSIÇÕES
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
                f"ID: {self.id_movimento} | "
                f"{self.origem.currentText()} → "
                f"{self.destino.currentText()} | "
                f"Status: Aguardando"
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
                f"ID: {self.id_movimento} | "
                "Status: Em movimento"
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
                f"ID: {self.id_movimento} | "
                "Status: Concluído"
            )


        self.atualizar_tabela()



    # =====================================
    # ATUALIZAR TABELA
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