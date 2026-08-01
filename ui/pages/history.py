from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem
)


class HistoryPage(QWidget):

    def __init__(self):

        super().__init__()

        self.criar_interface()


    def criar_interface(self):

        layout = QVBoxLayout()


        titulo = QLabel(
            "📜 Histórico de Operações"
        )


        titulo.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)


        tabela = QTableWidget()


        tabela.setColumnCount(
            4
        )


        tabela.setHorizontalHeaderLabels(
            [
                "Data/Hora",
                "Origem",
                "Destino",
                "Status"
            ]
        )


        tabela.setRowCount(
            3
        )


        dados = [

            [
                "08:30",
                "A1",
                "C3",
                "Concluído"
            ],

            [
                "09:15",
                "B2",
                "D4",
                "Em andamento"
            ],

            [
                "10:00",
                "C1",
                "A4",
                "Aguardando"
            ]

        ]


        for linha, valores in enumerate(dados):

            for coluna, valor in enumerate(valores):

                tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(valor)
                )



        layout.addWidget(
            titulo
        )


        layout.addWidget(
            tabela
        )


        self.setLayout(
            layout
        )