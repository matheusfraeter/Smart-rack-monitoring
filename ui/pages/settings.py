"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: settings.py
 Descrição...: Configurações do sistema
=========================================================
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QDialog,
    QDialogButtonBox,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
)

from PySide6.QtCore import (
    Qt,
    QTimer
)

from PySide6.QtGui import (
    QGuiApplication
)


# =========================================================
# DIÁLOGO DE EDIÇÃO NUMÉRICA
# =========================================================

class EditValueDialog(QDialog):

    def __init__(
        self,
        valor,
        titulo,
        minimo,
        maximo,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle(
            titulo
        )

        self.setModal(
            True
        )

        self.setMinimumWidth(
            320
        )

        layout = QVBoxLayout(
            self
        )

        # =====================================
        # TÍTULO
        # =====================================

        label = QLabel(
            titulo
        )

        label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            label
        )

        # =====================================
        # CAMPO
        # =====================================

        self.campo = QLineEdit()

        self.campo.setAlignment(
            Qt.AlignCenter
        )

        self.campo.setInputMethodHints(
            Qt.ImhPreferNumbers
        )

        self.campo.setText(
            str(valor)
        )

        self.campo.selectAll()

        layout.addWidget(
            self.campo
        )

        # =====================================
        # BOTÕES
        # =====================================

        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        botoes.accepted.connect(
            self.validar
        )

        botoes.rejected.connect(
            self.reject
        )

        layout.addWidget(
            botoes
        )

        self.campo.returnPressed.connect(
            self.validar
        )

        # =====================================
        # LIMITES
        # =====================================

        self.minimo = minimo
        self.maximo = maximo

        # =====================================
        # FOCO
        # =====================================

        self.campo.setFocus()

        # =====================================
        # TECLADO VIRTUAL
        # =====================================

        QTimer.singleShot(
            200,
            self.abrir_teclado
        )

    # =====================================================
    # ABRIR TECLADO
    # =====================================================

    def abrir_teclado(self):

        try:

            QGuiApplication.inputMethod().show()

        except Exception:

            pass

    # =====================================================
    # VALIDAR
    # =====================================================

    def validar(self):

        texto = (
            self.campo.text()
            .strip()
            .replace(
                ",",
                "."
            )
        )

        if not texto:

            QMessageBox.warning(
                self,
                "Valor inválido",
                "Digite um valor."
            )

            self.campo.setFocus()

            return

        try:

            valor = float(
                texto
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Valor inválido",
                "Digite um número válido."
            )

            self.campo.setFocus()

            self.campo.selectAll()

            return

        if valor < self.minimo:

            QMessageBox.warning(
                self,
                "Valor inválido",
                f"O valor mínimo é {self.minimo}."
            )

            self.campo.setFocus()
            self.campo.selectAll()

            return

        if valor > self.maximo:

            QMessageBox.warning(
                self,
                "Valor inválido",
                f"O valor máximo é {self.maximo}."
            )

            self.campo.setFocus()
            self.campo.selectAll()

            return

        self.accept()

    # =====================================================
    # VALOR
    # =====================================================

    def valor(self):

        return float(
            self.campo.text()
            .strip()
            .replace(
                ",",
                "."
            )
        )


# =========================================================
# PÁGINA DE CONFIGURAÇÕES
# =========================================================

class SettingsPage(QWidget):

    def __init__(self):

        super().__init__()

        # =====================================
        # VALORES
        # =====================================

        self.valor_ip = "192.168.4.1"

        self.valor_velocidade = 1000

        self.valor_passo = 10

        # =====================================
        # CRIAR INTERFACE
        # =====================================

        self.criar_interface()

    # =====================================================
    # INTERFACE
    # =====================================================

    def criar_interface(self):

        # =====================================
        # LAYOUT EXTERNO
        # =====================================

        layout_externo = QVBoxLayout(
            self
        )

        layout_externo.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # =====================================
        # SCROLL
        # =====================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        self.scroll.setFrameShape(
            QScrollArea.NoFrame
        )

        # =====================================
        # CONTEÚDO
        # =====================================

        conteudo = QWidget()

        conteudo.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Minimum
        )

        layout = QVBoxLayout(
            conteudo
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        layout.setSpacing(
            12
        )

        # =====================================
        # TÍTULO
        # =====================================

        titulo = QLabel(
            "⚙ Configurações do Sistema"
        )

        titulo.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)

        # =====================================
        # IP
        # =====================================

        ip_label = QLabel(
            "IP da MKS DLC32:"
        )

        self.ip = QLineEdit(
            self.valor_ip
        )

        # =====================================
        # IP SOMENTE LEITURA
        # =====================================

        self.ip.setReadOnly(
            True
        )

        self.ip.setFocusPolicy(
            Qt.NoFocus
        )

        # =====================================
        # VELOCIDADE
        # =====================================

        velocidade_label = QLabel(
            "Velocidade padrão:"
        )

        self.velocidade = QPushButton(
            f"{self.valor_velocidade}"
        )

        self.velocidade.setObjectName(
            "actionButton"
        )

        self.velocidade.clicked.connect(
            self.editar_velocidade
        )

        # =====================================
        # PASSO
        # =====================================

        passo_label = QLabel(
            "Passo de movimento:"
        )

        self.passo = QPushButton(
            f"{self.valor_passo}"
        )

        self.passo.setObjectName(
            "actionButton"
        )

        self.passo.clicked.connect(
            self.editar_passo
        )

        # =====================================
        # SALVAR
        # =====================================

        salvar = QPushButton(
            "💾 Salvar Configurações"
        )

        salvar.clicked.connect(
            self.salvar_configuracoes
        )

        self.salvar = salvar

        # =====================================
        # MONTAGEM
        # =====================================

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            ip_label
        )

        layout.addWidget(
            self.ip
        )

        layout.addWidget(
            velocidade_label
        )

        layout.addWidget(
            self.velocidade
        )

        layout.addWidget(
            passo_label
        )

        layout.addWidget(
            self.passo
        )

        layout.addWidget(
            salvar
        )

        # =====================================
        # ESPAÇO FINAL
        # =====================================

        layout.addStretch()

        # =====================================
        # CONFIGURAR SCROLL
        # =====================================

        self.scroll.setWidget(
            conteudo
        )

        layout_externo.addWidget(
            self.scroll
        )

    # =====================================================
    # EDITAR VELOCIDADE
    # =====================================================

    def editar_velocidade(self):

        dialogo = EditValueDialog(
            valor=self.valor_velocidade,
            titulo="Alterar velocidade padrão",
            minimo=100,
            maximo=5000,
            parent=self
        )

        if dialogo.exec() != QDialog.Accepted:

            return

        self.valor_velocidade = int(
            dialogo.valor()
        )

        self.velocidade.setText(
            str(
                self.valor_velocidade
            )
        )

    # =====================================================
    # EDITAR PASSO
    # =====================================================

    def editar_passo(self):

        dialogo = EditValueDialog(
            valor=self.valor_passo,
            titulo="Alterar passo de movimento",
            minimo=1,
            maximo=100,
            parent=self
        )

        if dialogo.exec() != QDialog.Accepted:

            return

        self.valor_passo = int(
            dialogo.valor()
        )

        self.passo.setText(
            str(
                self.valor_passo
            )
        )

    # =====================================================
    # SALVAR
    # =====================================================

    def salvar_configuracoes(self):

        self.valor_ip = (
            self.ip.text()
            .strip()
        )

        QMessageBox.information(
            self,
            "Sucesso",
            "Configurações salvas com sucesso."
        )