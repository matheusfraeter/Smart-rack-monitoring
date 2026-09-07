"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: manual.py
 Descrição...: Controle manual dos eixos XYZ
=========================================================
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame,
    QSizePolicy,
    QDialog,
    QLineEdit,
    QDialogButtonBox,
    QMessageBox,
    QScrollArea
)

from PySide6.QtCore import (
    Qt,
    QTimer
)

from PySide6.QtGui import (
    QGuiApplication
)

from movement import Movement
from database import Database


# =========================================================
# DIÁLOGO DE EDIÇÃO
# =========================================================

class EditValueDialog(QDialog):

    def __init__(
        self,
        valor,
        titulo,
        minimo,
        maximo,
        decimais,
        unidade,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.minimo = minimo
        self.maximo = maximo
        self.decimais = decimais
        self.unidade = unidade

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
            f"{float(valor):.{decimais}f}"
        )

        self.campo.selectAll()

        layout.addWidget(
            self.campo
        )

        # =====================================
        # UNIDADE
        # =====================================

        if unidade:

            unidade_label = QLabel(
                unidade
            )

            unidade_label.setAlignment(
                Qt.AlignCenter
            )

            layout.addWidget(
                unidade_label
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
    # TECLADO VIRTUAL
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
                (
                    f"O valor mínimo permitido é "
                    f"{self.minimo}."
                )
            )

            self.campo.setFocus()
            self.campo.selectAll()

            return

        if valor > self.maximo:

            QMessageBox.warning(
                self,
                "Valor inválido",
                (
                    f"O valor máximo permitido é "
                    f"{self.maximo}."
                )
            )

            self.campo.setFocus()
            self.campo.selectAll()

            return

        self.accept()

    # =====================================================
    # VALOR
    # =====================================================

    def valor(self):

        texto = (
            self.campo.text()
            .strip()
            .replace(
                ",",
                "."
            )
        )

        return float(
            texto
        )


# =========================================================
# PÁGINA MANUAL
# =========================================================

class ManualPage(QWidget):

    def __init__(
        self,
        mks
    ):

        super().__init__()

        self.mks = mks

        # =================================================
        # MOVIMENTO
        # =================================================

        self.movimento = Movement(
            self.mks
        )

        # =================================================
        # BANCO
        # =================================================

        self.db = Database()

        # =================================================
        # DESLOCAMENTO PADRÃO
        # =================================================

        self.passo = 10.0

        # =================================================
        # VELOCIDADE PADRÃO
        # =================================================

        self.velocidade = 1000.0

        # =================================================
        # CONTROLE DO GARFO
        # =================================================

        self.garfo_acionado = False

        self.timer_garfo = QTimer(
            self
        )

        self.timer_garfo.setSingleShot(
            True
        )

        self.timer_garfo.timeout.connect(
            self.desligar_garfo
        )

        # =================================================
        # TAMANHO DOS BOTÕES
        # =================================================

        self.tamanho_botao_xy = 50

        # =================================================
        # CRIAR INTERFACE
        # =================================================

        self.criar_interface()

    # =====================================================
    # INTERFACE
    # =====================================================

    def criar_interface(self):

        layout_externo = QVBoxLayout(
            self
        )

        layout_externo.setContentsMargins(
            0,
            0,
            0,
            0
        )

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        scroll.setFrameShape(
            QScrollArea.NoFrame
        )

        conteudo = QWidget()

        conteudo.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Minimum
        )

        principal = QVBoxLayout(
            conteudo
        )

        principal.setContentsMargins(
            10,
            8,
            10,
            8
        )

        principal.setSpacing(
            6
        )

        self.principal_layout = principal

        titulo = QLabel(
            "Controle Manual XYZ"
        )

        titulo.setObjectName(
            "title"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Fixed
        )

        self.passo_box = QHBoxLayout()

        self.passo_box.setSpacing(
            6
        )

        passo_texto = QLabel(
            "Deslocamento"
        )

        self.passo_button = QPushButton(
            f"{self.passo:.2f} mm"
        )

        self.passo_button.setObjectName(
            "actionButton"
        )

        self.passo_button.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        self.passo_button.setMinimumWidth(
            110
        )

        self.passo_button.setFixedHeight(
            40
        )

        self.passo_button.clicked.connect(
            self.editar_passo
        )

        velocidade_texto = QLabel(
            "Velocidade"
        )

        self.velocidade_button = QPushButton(
            f"{self.velocidade:.0f} mm/min"
        )

        self.velocidade_button.setObjectName(
            "actionButton"
        )

        self.velocidade_button.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        self.velocidade_button.setMinimumWidth(
            125
        )

        self.velocidade_button.setFixedHeight(
            40
        )

        self.velocidade_button.clicked.connect(
            self.editar_velocidade
        )

        self.passo_box.addWidget(
            passo_texto
        )

        self.passo_box.addSpacing(
            4
        )

        self.passo_box.addWidget(
            self.passo_button
        )

        self.passo_box.addSpacing(
            12
        )

        self.passo_box.addWidget(
            velocidade_texto
        )

        self.passo_box.addSpacing(
            4
        )

        self.passo_box.addWidget(
            self.velocidade_button
        )

        self.passo_box.addStretch()

        self.caixa = QFrame()

        self.caixa.setObjectName(
            "controlBox"
        )

        self.controles = QHBoxLayout(
            self.caixa
        )

        self.controles.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.controles.setSpacing(
            8
        )

        self.xy_box = QFrame()

        self.xy_box.setObjectName(
            "controlBox"
        )

        self.xy_layout = QVBoxLayout(
            self.xy_box
        )

        self.xy_layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.xy_layout.setSpacing(
            3
        )

        self.xy_layout.setAlignment(
            Qt.AlignCenter
        )

        xy_titulo = QLabel(
            "Movimento XY"
        )

        xy_titulo.setAlignment(
            Qt.AlignCenter
        )

        self.xy_layout.addWidget(
            xy_titulo
        )

        self.grid_xy = QGridLayout()

        self.grid_xy.setSpacing(
            3
        )

        self.grid_xy.setAlignment(
            Qt.AlignCenter
        )

        self.xp = QPushButton(
            "X+"
        )

        self.xm = QPushButton(
            "X-"
        )

        self.ym = QPushButton(
            "Y-"
        )

        self.yp = QPushButton(
            "Y+"
        )

        for botao in (
            self.xp,
            self.xm,
            self.ym,
            self.yp
        ):

            botao.setObjectName(
                "actionButton"
            )

            botao.setSizePolicy(
                QSizePolicy.Fixed,
                QSizePolicy.Fixed
            )

        self.grid_xy.addWidget(
            self.xp,
            0,
            1,
            Qt.AlignCenter
        )

        self.grid_xy.addWidget(
            self.ym,
            1,
            0,
            Qt.AlignCenter
        )

        self.grid_xy.addWidget(
            self.yp,
            1,
            2,
            Qt.AlignCenter
        )

        self.grid_xy.addWidget(
            self.xm,
            2,
            1,
            Qt.AlignCenter
        )

        self.xy_layout.addLayout(
            self.grid_xy
        )

        self.z_box = QFrame()

        self.z_box.setObjectName(
            "controlBox"
        )

        self.z_layout = QVBoxLayout(
            self.z_box
        )

        self.z_layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.z_layout.setSpacing(
            5
        )

        self.z_layout.setAlignment(
            Qt.AlignCenter
        )

        z_titulo = QLabel(
            "Movimento Z"
        )

        z_titulo.setAlignment(
            Qt.AlignCenter
        )

        self.z_layout.addWidget(
            z_titulo
        )

        self.zp = QPushButton(
            "Z +"
        )

        self.zm = QPushButton(
            "Z -"
        )

        for botao in (
            self.zp,
            self.zm
        ):

            botao.setObjectName(
                "actionButton"
            )

            botao.setSizePolicy(
                QSizePolicy.Fixed,
                QSizePolicy.Fixed
            )

            self.z_layout.addWidget(
                botao,
                0,
                Qt.AlignCenter
            )

        self.garfo_box = QFrame()

        self.garfo_box.setObjectName(
            "controlBox"
        )

        self.garfo_layout = QVBoxLayout(
            self.garfo_box
        )

        self.garfo_layout.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.garfo_layout.setSpacing(
            5
        )

        self.garfo_layout.setAlignment(
            Qt.AlignCenter
        )

        garfo_titulo = QLabel(
            "Garfos"
        )

        garfo_titulo.setAlignment(
            Qt.AlignCenter
        )

        self.garfo_layout.addWidget(
            garfo_titulo
        )

        self.bt_garfo = QPushButton(
            "ACIONAR\nGARFO"
        )

        self.bt_garfo.setObjectName(
            "actionButton"
        )

        self.bt_garfo.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        self.garfo_layout.addWidget(
            self.bt_garfo,
            0,
            Qt.AlignCenter
        )

        self.controles.addWidget(
            self.xy_box,
            4
        )

        self.controles.addWidget(
            self.z_box,
            2
        )

        self.controles.addWidget(
            self.garfo_box,
            3
        )

        self.botoes = QHBoxLayout()

        self.botoes.setSpacing(
            8
        )

        stop = QPushButton(
            "STOP"
        )

        continuar = QPushButton(
            "CONTINUAR"
        )

        stop.setObjectName(
            "actionButton"
        )

        continuar.setObjectName(
            "actionButton"
        )

        self.stop_button = stop
        self.continuar_button = continuar

        self.botoes.addWidget(
            stop
        )

        self.botoes.addWidget(
            continuar
        )

        self.xp.clicked.connect(
            self.botao_x_mais
        )

        self.xm.clicked.connect(
            self.botao_x_menos
        )

        self.yp.clicked.connect(
            self.botao_y_mais
        )

        self.ym.clicked.connect(
            self.botao_y_menos
        )

        self.zp.clicked.connect(
            self.botao_z_mais
        )

        self.zm.clicked.connect(
            self.botao_z_menos
        )

        self.bt_garfo.clicked.connect(
            self.acionar_garfo
        )

        stop.clicked.connect(
            self.stop
        )

        continuar.clicked.connect(
            self.reset
        )

        principal.addWidget(
            titulo
        )

        principal.addLayout(
            self.passo_box
        )

        principal.addWidget(
            self.caixa,
            1
        )

        principal.addLayout(
            self.botoes
        )

        principal.addStretch()

        scroll.setWidget(
            conteudo
        )

        layout_externo.addWidget(
            scroll
        )

        self.atualizar_tamanho_botoes()

    # =====================================================
    # EDITAR DESLOCAMENTO
    # =====================================================

    def editar_passo(self):

        dialogo = EditValueDialog(
            valor=self.passo,
            titulo="Alterar deslocamento",
            minimo=0.01,
            maximo=1000.0,
            decimais=2,
            unidade="mm",
            parent=self
        )

        if dialogo.exec() != QDialog.Accepted:

            return

        self.alterar_passo(
            dialogo.valor()
        )

    # =====================================================
    # EDITAR VELOCIDADE
    # =====================================================

    def editar_velocidade(self):

        dialogo = EditValueDialog(
            valor=self.velocidade,
            titulo="Alterar velocidade",
            minimo=1.0,
            maximo=10000.0,
            decimais=0,
            unidade="mm/min",
            parent=self
        )

        if dialogo.exec() != QDialog.Accepted:

            return

        self.alterar_velocidade(
            dialogo.valor()
        )

    # =====================================================
    # ALTERAR DESLOCAMENTO
    # =====================================================

    def alterar_passo(
        self,
        valor
    ):

        self.passo = float(
            valor
        )

        self.passo_button.setText(
            f"{self.passo:.2f} mm"
        )

        print(
            f"DESLOCAMENTO ALTERADO PARA: "
            f"{self.passo:g} mm"
        )

    # =====================================================
    # ALTERAR VELOCIDADE
    # =====================================================

    def alterar_velocidade(
        self,
        valor
    ):

        self.velocidade = float(
            valor
        )

        self.velocidade_button.setText(
            f"{self.velocidade:.0f} mm/min"
        )

        print(
            f"VELOCIDADE ALTERADA PARA: "
            f"{self.velocidade:.0f} mm/min"
        )

    # =====================================================
    # REDIMENSIONAMENTO
    # =====================================================

    def resizeEvent(
        self,
        event
    ):

        super().resizeEvent(
            event
        )

        self.atualizar_tamanho_botoes()

    # =====================================================
    # ATUALIZAR TAMANHOS
    # =====================================================

    def atualizar_tamanho_botoes(self):

        largura = self.width()
        altura = self.height()

        tamanho_base = int(
            min(
                62,
                max(
                    46,
                    largura * 0.075
                )
            )
        )

        self.tamanho_botao_xy = tamanho_base

        largura_movimento = int(
            tamanho_base * 1.25
        )

        altura_movimento = int(
            tamanho_base * 0.80
        )

        for botao in (
            self.xp,
            self.xm,
            self.ym,
            self.yp
        ):

            botao.setFixedSize(
                largura_movimento,
                altura_movimento
            )

        self.zp.setFixedSize(
            largura_movimento,
            altura_movimento
        )

        self.zm.setFixedSize(
            largura_movimento,
            altura_movimento
        )

        largura_garfo = int(
            max(
                120,
                tamanho_base * 2.5
            )
        )

        altura_garfo = int(
            tamanho_base * 1.20
        )

        self.bt_garfo.setFixedSize(
            largura_garfo,
            altura_garfo
        )

        self.xy_box.setMinimumWidth(
            0
        )

        self.z_box.setMinimumWidth(
            0
        )

        self.garfo_box.setMinimumWidth(
            0
        )

        self.passo_button.setFixedHeight(
            40
        )

        self.velocidade_button.setFixedHeight(
            40
        )

        altura_inferior = int(
            max(
                36,
                min(
                    46,
                    altura * 0.095
                )
            )
        )

        self.stop_button.setFixedHeight(
            altura_inferior
        )

        self.continuar_button.setFixedHeight(
            altura_inferior
        )

    # =====================================================
    # OBTER LIMITES DO EIXO
    # =====================================================

    def obter_limites_eixo(
        self,
        eixo
    ):

        eixo = str(
            eixo
        ).upper()

        try:

            limites = (
                self.db.obter_limite_eixo(
                    eixo
                )
            )

        except Exception as erro:

            print(
                f">>> ERRO AO OBTER LIMITES DO EIXO "
                f"{eixo}: {erro}"
            )

            return None

        if limites is None:

            print(
                f">>> LIMITES DO EIXO {eixo} "
                f"NÃO ENCONTRADOS"
            )

            return None

        try:

            minimo = float(
                limites["minimo"]
            )

            maximo = float(
                limites["maximo"]
            )

        except (
            TypeError,
            ValueError,
            KeyError
        ):

            print(
                f">>> LIMITES DO EIXO {eixo} INVÁLIDOS"
            )

            return None

        if minimo >= maximo:

            print(
                f">>> ERRO: LIMITE MÍNIMO DO EIXO "
                f"{eixo} >= LIMITE MÁXIMO"
            )

            return None

        return (
            minimo,
            maximo
        )

    # =====================================================
    # OBTER POSIÇÃO ATUAL
    # =====================================================

    def obter_posicao_atual(
        self,
        eixo
    ):

        try:

            status = self.mks.ler_status()

        except Exception as erro:

            print(
                f">>> ERRO AO LER STATUS DA MKS: {erro}"
            )

            return None

        if not isinstance(
            status,
            dict
        ):

            print(
                ">>> STATUS DA MKS INVÁLIDO"
            )

            return None

        try:

            posicao = float(
                status.get(
                    eixo.upper()
                )
            )

        except (
            TypeError,
            ValueError
        ):

            print(
                f">>> POSIÇÃO DO EIXO {eixo} "
                f"INDISPONÍVEL"
            )

            return None

        return posicao

    # =====================================================
    # VERIFICAR LIMITES
    # =====================================================

    def verificar_limites(
        self,
        eixo,
        deslocamento
    ):

        eixo = str(
            eixo
        ).upper()

        limites = self.obter_limites_eixo(
            eixo
        )

        if limites is None:

            QMessageBox.warning(
                self,
                "Limites indisponíveis",
                (
                    f"Não foi possível obter os limites "
                    f"do eixo {eixo}."
                )
            )

            return False

        minimo, maximo = limites

        posicao_atual = self.obter_posicao_atual(
            eixo
        )

        if posicao_atual is None:

            QMessageBox.warning(
                self,
                "Posição indisponível",
                (
                    f"Não foi possível obter a posição "
                    f"atual do eixo {eixo}."
                )
            )

            return False

        deslocamento = float(
            deslocamento
        )

        posicao_destino = (
            posicao_atual
            +
            deslocamento
        )

        print()
        print(
            f">>> VERIFICAÇÃO DE LIMITE - EIXO {eixo}"
        )

        print(
            f">>> POSIÇÃO ATUAL: "
            f"{posicao_atual:.3f} mm"
        )

        print(
            f">>> DESLOCAMENTO: "
            f"{deslocamento:.3f} mm"
        )

        print(
            f">>> DESTINO: "
            f"{posicao_destino:.3f} mm"
        )

        print(
            f">>> MÍNIMO: "
            f"{minimo:.3f} mm"
        )

        print(
            f">>> MÁXIMO: "
            f"{maximo:.3f} mm"
        )

        # ---------------------------------------------
        # ABAIXO DO MÍNIMO
        # ---------------------------------------------

        if posicao_destino < minimo:

            print(
                f">>> MOVIMENTO BLOQUEADO"
            )

            print(
                f">>> DESTINO ABAIXO DO MÍNIMO"
            )

            QMessageBox.warning(
                self,
                f"Limite mínimo do eixo {eixo}",
                (
                    f"O movimento foi bloqueado.\n\n"
                    f"Posição atual: "
                    f"{posicao_atual:.3f} mm\n"
                    f"Deslocamento: "
                    f"{deslocamento:.3f} mm\n"
                    f"Destino: "
                    f"{posicao_destino:.3f} mm\n"
                    f"Limite mínimo: "
                    f"{minimo:.3f} mm"
                )
            )

            return False

        # ---------------------------------------------
        # ACIMA DO MÁXIMO
        # ---------------------------------------------

        if posicao_destino > maximo:

            print(
                f">>> MOVIMENTO BLOQUEADO"
            )

            print(
                f">>> DESTINO ACIMA DO MÁXIMO"
            )

            QMessageBox.warning(
                self,
                f"Limite máximo do eixo {eixo}",
                (
                    f"O movimento foi bloqueado.\n\n"
                    f"Posição atual: "
                    f"{posicao_atual:.3f} mm\n"
                    f"Deslocamento: "
                    f"{deslocamento:.3f} mm\n"
                    f"Destino: "
                    f"{posicao_destino:.3f} mm\n"
                    f"Limite máximo: "
                    f"{maximo:.3f} mm"
                )
            )

            return False

        # ---------------------------------------------
        # MOVIMENTO DENTRO DOS LIMITES
        # ---------------------------------------------

        print(
            ">>> MOVIMENTO DENTRO DOS LIMITES"
        )

        return True

    # =====================================================
    # BOTÃO X+
    # =====================================================

    def botao_x_mais(self):

        print()
        print(
            ">>> BOTÃO X+ PRESSIONADO"
        )

        print(
            f">>> DESLOCAMENTO: {self.passo:g} mm"
        )

        print(
            f">>> VELOCIDADE: {self.velocidade:.0f} mm/min"
        )

        self.mover_x(
            self.passo
        )

    # =====================================================
    # BOTÃO X-
    # =====================================================

    def botao_x_menos(self):

        print()
        print(
            ">>> BOTÃO X- PRESSIONADO"
        )

        print(
            f">>> DESLOCAMENTO: {self.passo:g} mm"
        )

        print(
            f">>> VELOCIDADE: {self.velocidade:.0f} mm/min"
        )

        self.mover_x(
            -self.passo
        )

    # =====================================================
    # BOTÃO Y+
    # =====================================================

    def botao_y_mais(self):

        print()
        print(
            ">>> BOTÃO Y+ PRESSIONADO"
        )

        print(
            f">>> DESLOCAMENTO: {self.passo:g} mm"
        )

        print(
            f">>> VELOCIDADE: {self.velocidade:.0f} mm/min"
        )

        self.mover_y(
            self.passo
        )

    # =====================================================
    # BOTÃO Y-
    # =====================================================

    def botao_y_menos(self):

        print()
        print(
            ">>> BOTÃO Y- PRESSIONADO"
        )

        print(
            f">>> DESLOCAMENTO: {self.passo:g} mm"
        )

        print(
            f">>> VELOCIDADE: {self.velocidade:.0f} mm/min"
        )

        self.mover_y(
            -self.passo
        )

    # =====================================================
    # BOTÃO Z+
    # =====================================================

    def botao_z_mais(self):

        print()
        print(
            ">>> BOTÃO Z+ PRESSIONADO"
        )

        print(
            f">>> DESLOCAMENTO: {self.passo:g} mm"
        )

        print(
            f">>> VELOCIDADE: {self.velocidade:.0f} mm/min"
        )

        self.mover_z(
            self.passo
        )

    # =====================================================
    # BOTÃO Z-
    # =====================================================

    def botao_z_menos(self):

        print()
        print(
            ">>> BOTÃO Z- PRESSIONADO"
        )

        print(
            f">>> DESLOCAMENTO: {self.passo:g} mm"
        )

        print(
            f">>> VELOCIDADE: {self.velocidade:.0f} mm/min"
        )

        self.mover_z(
            -self.passo
        )

    # =====================================================
    # MOVIMENTO X
    # =====================================================

    def mover_x(
        self,
        valor
    ):

        print()
        print(
            ">>> MANUAL PAGE"
        )

        print(
            f">>> SOLICITADO X: {valor}"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        # ---------------------------------------------
        # VERIFICAR LIMITES
        # ---------------------------------------------

        if not self.verificar_limites(
            "X",
            valor
        ):

            return

        # ---------------------------------------------
        # EXECUTAR
        # ---------------------------------------------

        resultado = self.movimento.mover_x(
            valor,
            self.velocidade
        )

        print(
            f">>> RESULTADO X: {resultado}"
        )

    # =====================================================
    # MOVIMENTO Y
    # =====================================================

    def mover_y(
        self,
        valor
    ):

        print()
        print(
            ">>> MANUAL PAGE"
        )

        print(
            f">>> SOLICITADO Y: {valor}"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        # ---------------------------------------------
        # VERIFICAR LIMITES
        # ---------------------------------------------

        if not self.verificar_limites(
            "Y",
            valor
        ):

            return

        # ---------------------------------------------
        # EXECUTAR
        # ---------------------------------------------

        resultado = self.movimento.mover_y(
            valor,
            self.velocidade
        )

        print(
            f">>> RESULTADO Y: {resultado}"
        )

    # =====================================================
    # MOVIMENTO Z
    # =====================================================

    def mover_z(
        self,
        valor
    ):

        print()
        print(
            ">>> MANUAL PAGE"
        )

        print(
            f">>> SOLICITADO Z: {valor}"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        # ---------------------------------------------
        # VERIFICAR LIMITES
        # ---------------------------------------------

        if not self.verificar_limites(
            "Z",
            valor
        ):

            return

        # ---------------------------------------------
        # EXECUTAR
        # ---------------------------------------------

        resultado = self.movimento.mover_z(
            valor,
            self.velocidade
        )

        print(
            f">>> RESULTADO Z: {resultado}"
        )

    # =====================================================
    # ACIONAR GARFO
    # =====================================================

    def acionar_garfo(self):

        print()
        print(
            ">>> BOTÃO ACIONAR GARFO PRESSIONADO"
        )

        if self.garfo_acionado:

            print(
                ">>> GARFO JÁ ESTÁ EM ACIONAMENTO"
            )

            return

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        print(
            ">>> ENVIANDO M3 S1000"
        )

        resultado = self.mks.enviar_comando(
            "M3 S1000"
        )

        if not resultado:

            print(
                ">>> FALHA AO LIGAR GARFO"
            )

            return

        self.garfo_acionado = True

        self.bt_garfo.setEnabled(
            False
        )

        self.bt_garfo.setText(
            "GARFO\nACIONADO"
        )

        print(
            ">>> TTL HIGH POR 1 SEGUNDO"
        )

        self.timer_garfo.start(
            1000
        )

    # =====================================================
    # DESLIGAR GARFO
    # =====================================================

    def desligar_garfo(self):

        print()
        print(
            ">>> TEMPO DO GARFO FINALIZADO"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA AO FINALIZAR GARFO"
            )

            self.garfo_acionado = False

            self.bt_garfo.setEnabled(
                True
            )

            self.bt_garfo.setText(
                "ACIONAR\nGARFO"
            )

            return

        print(
            ">>> ENVIANDO M3 S0"
        )

        resultado = self.mks.enviar_comando(
            "M3 S0"
        )

        print(
            f">>> RESULTADO GARFO: {resultado}"
        )

        self.garfo_acionado = False

        self.bt_garfo.setEnabled(
            True
        )

        self.bt_garfo.setText(
            "ACIONAR\nGARFO"
        )

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        print()
        print(
            ">>> STOP PRESSIONADO"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        if self.timer_garfo.isActive():

            self.timer_garfo.stop()

            print(
                ">>> TIMER DO GARFO CANCELADO"
            )

            self.mks.enviar_comando(
                "M3 S0"
            )

            self.garfo_acionado = False

            self.bt_garfo.setEnabled(
                True
            )

            self.bt_garfo.setText(
                "ACIONAR\nGARFO"
            )

        self.mks.enviar_comando(
            "!"
        )

    # =====================================================
    # CONTINUAR
    # =====================================================

    def reset(self):

        print()
        print(
            ">>> CONTINUAR PRESSIONADO"
        )

        if not self.mks.conectado:

            print(
                ">>> MKS DESCONECTADA"
            )

            return

        self.mks.enviar_comando(
            "~"
        )