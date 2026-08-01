from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout
)


class RackPage(QWidget):

    def __init__(self):

        super().__init__()

        self.criar_interface()


    def criar_interface(self):

        layout = QVBoxLayout()


        titulo = QLabel(
            "📦 Mapa do Rack"
        )


        titulo.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)


        self.selecionado = QLabel(
            "Nenhuma posição selecionada"
        )


        self.selecionado.setStyleSheet("""
            font-size:18px;
        """)



        grade = QGridLayout()


        linhas = [
            "A",
            "B",
            "C",
            "D"
        ]


        colunas = 4



        for linha, letra in enumerate(linhas):

            for coluna in range(1, colunas + 1):

                endereco = f"{letra}{coluna}"


                botao = QPushButton(
                    endereco
                )


                botao.setMinimumSize(
                    80,
                    60
                )


                botao.clicked.connect(
                    lambda checked=False, e=endereco:
                    self.selecionar(e)
                )


                grade.addWidget(
                    botao,
                    linha,
                    coluna-1
                )



        layout.addWidget(
            titulo
        )


        layout.addWidget(
            self.selecionado
        )


        layout.addLayout(
            grade
        )


        self.setLayout(
            layout
        )



    def selecionar(self, endereco):

        self.selecionado.setText(
            f"Posição selecionada: {endereco}"
        )