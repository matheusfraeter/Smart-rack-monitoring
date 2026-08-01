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
    QMessageBox
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



        self.status = QLabel(
            "Nenhuma movimentação criada"
        )


        self.status.setStyleSheet(
            """
            font-size:18px;
            """
        )



        self.origem = QComboBox()

        self.destino = QComboBox()



        self.carregar_posicoes()



        botao_criar = QPushButton(
            "Criar Movimento"
        )


        botao_criar.clicked.connect(
            self.criar_movimento
        )



        botao_iniciar = QPushButton(
            "▶ Iniciar"
        )


        botao_iniciar.clicked.connect(
            self.iniciar
        )



        botao_finalizar = QPushButton(
            "✔ Finalizar"
        )


        botao_finalizar.clicked.connect(
            self.finalizar
        )



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



        botoes = QHBoxLayout()

        botoes.addWidget(
            botao_criar
        )

        botoes.addWidget(
            botao_iniciar
        )

        botoes.addWidget(
            botao_finalizar
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
            self.status
        )


        self.setLayout(
            layout
        )



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


            self.status.setText(
                "Movimento criado: Aguardando"
            )


        else:

            QMessageBox.warning(
                self,
                "Erro",
                resultado["mensagem"]
            )



    # =====================================
    # INICIAR
    # =====================================

    def iniciar(self):

        if self.id_movimento:


            self.controller.iniciar_movimento(
                self.id_movimento
            )


            self.status.setText(
                "Status: Em movimento"
            )



    # =====================================
    # FINALIZAR
    # =====================================

    def finalizar(self):

        if self.id_movimento:


            self.controller.finalizar_movimento(
                self.id_movimento
            )


            self.status.setText(
                "Status: Concluído"
            )