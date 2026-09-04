"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: rack.py
 Descrição...: Visualização e controle do Rack
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
    QScrollArea,
    QMessageBox,
    QSizePolicy,
    QApplication
)

from PySide6.QtCore import (
    Qt,
    QThread,
    Signal,
    QEvent,
    QPoint
)

from controllers.rack_controller import RackController

from ui.widgets.pallet_dialog import PalletDialog
from ui.widgets.rack_action_dialog import RackActionDialog


# =========================================================
# WORKER DE OPERAÇÃO AUTOMÁTICA
# =========================================================

class RackWorker(QThread):

    concluido = Signal(
        bool,
        str
    )

    def __init__(
        self,
        controller,
        operacao,
        endereco,
        pallet=None
    ):

        super().__init__()

        self.controller = controller
        self.operacao = operacao
        self.endereco = endereco
        self.pallet = pallet

    # =====================================================
    # EXECUTAR
    # =====================================================

    def run(self):

        try:

            # ---------------------------------------------
            # ARMAZENAMENTO
            # ---------------------------------------------

            if self.operacao == "armazenar":

                sucesso = (
                    self.controller.armazenar_pallet(
                        self.endereco,
                        self.pallet
                    )
                )

                if sucesso:

                    self.concluido.emit(
                        True,
                        (
                            f"Pallet {self.pallet} "
                            f"armazenado em {self.endereco}."
                        )
                    )

                else:

                    self.concluido.emit(
                        False,
                        (
                            "Falha no armazenamento. "
                            "A posição não foi alterada."
                        )
                    )

                return

            # ---------------------------------------------
            # RETIRADA
            # ---------------------------------------------

            if self.operacao == "retirar":

                sucesso = (
                    self.controller.retirar_pallet(
                        self.endereco
                    )
                )

                if sucesso:

                    self.concluido.emit(
                        True,
                        (
                            f"Pallet {self.pallet} "
                            f"retirado de {self.endereco} "
                            "e enviado para expedição."
                        )
                    )

                else:

                    self.concluido.emit(
                        False,
                        (
                            "Falha na retirada. "
                            "A posição não foi alterada."
                        )
                    )

                return

            self.concluido.emit(
                False,
                "Operação desconhecida."
            )

        except Exception as erro:

            print()
            print(
                "ERRO NO WORKER DO RACK:"
            )

            print(
                erro
            )

            self.concluido.emit(
                False,
                (
                    "Erro durante a operação: "
                    f"{erro}"
                )
            )


# =========================================================
# PÁGINA DO RACK
# =========================================================

class RackPage(QWidget):

    def __init__(
        self,
        mks
    ):

        super().__init__()

        # =====================================
        # COMUNICAÇÃO
        # =====================================

        self.mks = mks

        # =====================================
        # CONTROLLER
        # =====================================

        self.controller = RackController(
            self.mks
        )

        # =====================================
        # BOTÕES DO RACK
        # =====================================

        self.botoes = {}

        # =====================================
        # OPERAÇÃO EM ANDAMENTO
        # =====================================

        self.operacao_em_andamento = False

        self.worker = None

        # =====================================
        # CONFIGURAÇÃO DO RACK
        # =====================================

        self.estantes = [
            "A",
            "B"
        ]

        self.niveis = 3

        # AGORA SÃO SOMENTE 2 COLUNAS
        self.colunas = 2

        # =====================================
        # REFERÊNCIAS DAS GRADES
        # =====================================

        self.grades = []

        # =====================================
        # TAMANHO ATUAL DAS CÉLULAS
        # =====================================

        self.tamanho_celula = 90
        self.altura_celula = 55

        # =====================================
        # CONTROLE DO TOQUE / ARRASTO
        # =====================================

        self._touch_ativo = False
        self._touch_arrastando = False

        self._touch_posicao_inicial = QPoint()
        self._touch_posicao_anterior = QPoint()

        self._touch_scroll_inicial = 0

        # Distância mínima para considerar
        # que o dedo começou a arrastar.
        self._touch_limite_arrasto = 12

        # Endereço da célula onde começou
        # o toque/clique.
        self._endereco_touch = None

        # =====================================
        # CRIAR INTERFACE
        # =====================================

        self.criar_interface()

        # =====================================
        # EVENT FILTER GLOBAL
        # =====================================

        app = QApplication.instance()

        if app is not None:

            app.installEventFilter(
                self
            )

    # =================================================
    # INTERFACE
    # =================================================

    def criar_interface(self):

        principal = QVBoxLayout(
            self
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

        # =====================================
        # TÍTULO
        # =====================================

        titulo = QLabel(
            "SMART RACK"
        )

        titulo.setObjectName(
            "title"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        principal.addWidget(
            titulo
        )

        # =====================================
        # ÁREA COM ROLAGEM
        # =====================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        # =====================================
        # CONTEÚDO
        # =====================================

        self.conteudo = QWidget()

        self.conteudo.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        # =====================================
        # AS ESTANTES AGORA FICAM LADO A LADO
        # =====================================

        self.layout_racks = QHBoxLayout(
            self.conteudo
        )

        self.layout_racks.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.layout_racks.setSpacing(
            12
        )

        # =====================================
        # CRIAR ESTANTES
        # =====================================

        for estante in self.estantes:

            frame = self.criar_estante(
                estante
            )

            self.layout_racks.addWidget(
                frame,
                1
            )

        self.layout_racks.addStretch(
            0
        )

        self.scroll.setWidget(
            self.conteudo
        )

        principal.addWidget(
            self.scroll,
            1
        )

        # =====================================
        # ATUALIZAR
        # =====================================

        self.atualizar_tela()

        # =====================================
        # AJUSTAR TAMANHOS
        # =====================================

        self.atualizar_tamanho_rack()

    # =================================================
    # ENCONTRAR ENDEREÇO SOB O TOQUE
    # =================================================

    def encontrar_endereco(
        self,
        ponto_global
    ):

        for endereco, botao in self.botoes.items():

            if not botao.isVisible():

                continue

            topo_esquerdo = (
                botao.mapToGlobal(
                    QPoint(0, 0)
                )
            )

            largura = botao.width()
            altura = botao.height()

            if (
                topo_esquerdo.x()
                <= ponto_global.x()
                <= topo_esquerdo.x() + largura
                and
                topo_esquerdo.y()
                <= ponto_global.y()
                <= topo_esquerdo.y() + altura
            ):

                return endereco

        return None

    # =================================================
    # INICIAR TOUCH
    # =================================================

    def iniciar_touch(
        self,
        ponto_global
    ):

        self._touch_ativo = True

        self._touch_arrastando = False

        self._touch_posicao_inicial = (
            ponto_global
        )

        self._touch_posicao_anterior = (
            ponto_global
        )

        self._touch_scroll_inicial = (
            self.scroll.verticalScrollBar().value()
        )

        self._endereco_touch = (
            self.encontrar_endereco(
                ponto_global
            )
        )

    # =================================================
    # MOVER TOUCH
    # =================================================

    def mover_touch(
        self,
        ponto_global
    ):

        if not self._touch_ativo:

            return False

        deslocamento_y = (
            ponto_global.y()
            - self._touch_posicao_inicial.y()
        )

        # =====================================
        # DETECTAR INÍCIO DO ARRASTO
        # =====================================

        if not self._touch_arrastando:

            distancia = (
                ponto_global
                - self._touch_posicao_inicial
            ).manhattanLength()

            if distancia >= self._touch_limite_arrasto:

                self._touch_arrastando = True

        # =====================================
        # ROLAR
        # =====================================

        if self._touch_arrastando:

            barra = (
                self.scroll.verticalScrollBar()
            )

            novo_valor = (
                self._touch_scroll_inicial
                - deslocamento_y
            )

            novo_valor = max(
                barra.minimum(),
                min(
                    barra.maximum(),
                    int(novo_valor)
                )
            )

            barra.setValue(
                novo_valor
            )

            self._touch_posicao_anterior = (
                ponto_global
            )

            return True

        return False

    # =================================================
    # FINALIZAR TOUCH
    # =================================================

    def finalizar_touch(self):

        if not self._touch_ativo:

            return False, None

        foi_arrasto = (
            self._touch_arrastando
        )

        endereco = (
            self._endereco_touch
        )

        self._touch_ativo = False
        self._touch_arrastando = False
        self._endereco_touch = None

        return foi_arrasto, endereco

    # =================================================
    # EVENT FILTER
    # =================================================

    def eventFilter(
        self,
        obj,
        event
    ):

        # =====================================
        # SOMENTE A PÁGINA VISÍVEL
        # =====================================

        if not self.isVisible():

            return super().eventFilter(
                obj,
                event
            )

        # =====================================
        # IGNORAR EVENTOS ENQUANTO UM
        # DIÁLOGO MODAL ESTIVER ABERTO
        # =====================================

        if QApplication.activeModalWidget() is not None:

            return super().eventFilter(
                obj,
                event
            )

        # =====================================
        # MOUSE PRESS
        # =====================================

        if (
            event.type()
            == QEvent.MouseButtonPress
            and event.button()
            == Qt.LeftButton
        ):

            if not hasattr(
                event,
                "globalPosition"
            ):

                return super().eventFilter(
                    obj,
                    event
                )

            ponto_global = (
                event.globalPosition().toPoint()
            )

            # ---------------------------------
            # SOMENTE QUANDO O TOQUE ESTÁ
            # DENTRO DA ÁREA DE ROLAGEM
            # ---------------------------------

            viewport = (
                self.scroll.viewport()
            )

            viewport_top_left = (
                viewport.mapToGlobal(
                    QPoint(0, 0)
                )
            )

            viewport_rect = viewport.rect()

            viewport_rect.moveTopLeft(
                viewport_top_left
            )

            if viewport_rect.contains(
                ponto_global
            ):

                self.iniciar_touch(
                    ponto_global
                )

            return super().eventFilter(
                obj,
                event
            )

        # =====================================
        # MOUSE MOVE
        # =====================================

        if (
            event.type()
            == QEvent.MouseMove
            and self._touch_ativo
        ):

            if not hasattr(
                event,
                "globalPosition"
            ):

                return super().eventFilter(
                    obj,
                    event
                )

            ponto_global = (
                event.globalPosition().toPoint()
            )

            if self.mover_touch(
                ponto_global
            ):

                event.accept()

                return True

            return super().eventFilter(
                obj,
                event
            )

        # =====================================
        # MOUSE RELEASE
        # =====================================

        if (
            event.type()
            == QEvent.MouseButtonRelease
            and event.button()
            == Qt.LeftButton
        ):

            if not self._touch_ativo:

                return super().eventFilter(
                    obj,
                    event
                )

            foi_arrasto, endereco = (
                self.finalizar_touch()
            )

            # ---------------------------------
            # FOI ARRASTO
            # ---------------------------------

            if foi_arrasto:

                event.accept()

                return True

            # ---------------------------------
            # FOI TOQUE RÁPIDO
            # ---------------------------------

            if endereco is not None:

                self.selecionar(
                    endereco
                )

                event.accept()

                return True

            return super().eventFilter(
                obj,
                event
            )

        return super().eventFilter(
            obj,
            event
        )

    # =================================================
    # CRIAR ESTANTE
    # =================================================

    def criar_estante(
        self,
        estante
    ):

        frame = QFrame()

        frame.setObjectName(
            "rackFrame"
        )

        frame.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred
        )

        layout = QVBoxLayout(
            frame
        )

        layout.setContentsMargins(
            6,
            6,
            6,
            6
        )

        layout.setSpacing(
            5
        )

        titulo = QLabel(
            f"ESTANTE {estante}"
        )

        titulo.setObjectName(
            "rackTitle"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            titulo
        )

        grade = QGridLayout()

        grade.setHorizontalSpacing(
            6
        )

        grade.setVerticalSpacing(
            6
        )

        # =====================================
        # CABEÇALHO DAS COLUNAS
        # =====================================

        for coluna in range(
            1,
            self.colunas + 1
        ):

            label = QLabel(
                str(coluna)
            )

            label.setObjectName(
                "rackLabel"
            )

            label.setAlignment(
                Qt.AlignCenter
            )

            label.setSizePolicy(
                QSizePolicy.Fixed,
                QSizePolicy.Fixed
            )

            grade.addWidget(
                label,
                0,
                coluna
            )

        # =====================================
        # NÍVEIS
        # =====================================

        linha = 1

        for nivel in range(
            self.niveis,
            0,
            -1
        ):

            nivel_label = QLabel(
                f"Nível {nivel}"
            )

            nivel_label.setObjectName(
                "rackLabel"
            )

            nivel_label.setAlignment(
                Qt.AlignCenter
            )

            nivel_label.setSizePolicy(
                QSizePolicy.Fixed,
                QSizePolicy.Fixed
            )

            grade.addWidget(
                nivel_label,
                linha,
                0
            )

            # =================================
            # CÉLULAS
            # =================================

            for coluna in range(
                1,
                self.colunas + 1
            ):

                endereco = (
                    f"{estante}"
                    f"{nivel}"
                    f"{coluna}"
                )

                botao = QPushButton()

                botao.setObjectName(
                    "rackButton"
                )

                botao.setSizePolicy(
                    QSizePolicy.Fixed,
                    QSizePolicy.Fixed
                )

                # O clique é tratado pelo eventFilter.
                # Não conectar o clicked diretamente,
                # para evitar conflito com o touch/scroll.

                self.botoes[endereco] = botao

                grade.addWidget(
                    botao,
                    linha,
                    coluna
                )

            linha += 1

        # =====================================
        # EXPANSÃO DAS COLUNAS
        # =====================================

        grade.setColumnStretch(
            0,
            0
        )

        for coluna in range(
            1,
            self.colunas + 1
        ):

            grade.setColumnStretch(
                coluna,
                0
            )

        layout.addLayout(
            grade
        )

        self.grades.append(
            grade
        )

        return frame

    # =================================================
    # REDIMENSIONAMENTO
    # =================================================

    def resizeEvent(
        self,
        event
    ):

        super().resizeEvent(
            event
        )

        self.atualizar_tamanho_rack()

    # =================================================
    # CALCULAR TAMANHO DO RACK
    # =================================================

    def atualizar_tamanho_rack(self):

        if not hasattr(
            self,
            "scroll"
        ):

            return

        largura_disponivel = (
            self.scroll.viewport().width()
        )

        if largura_disponivel <= 0:

            return

        # =====================================
        # AGORA SÃO DUAS ESTANTES LADO A LADO
        # =====================================

        quantidade_estantes = len(
            self.estantes
        )

        margem = 30

        espaco_entre_estantes = 12

        largura_util = (
            largura_disponivel
            - margem
            - espaco_entre_estantes
        )

        largura_estante = (
            largura_util
            / quantidade_estantes
        )

        # =====================================
        # LARGURA DO RÓTULO "NÍVEL"
        # =====================================

        largura_nivel = 65

        # =====================================
        # ESPAÇAMENTOS
        # =====================================

        espacamento = 6

        total_espacamento = (
            espacamento * 3
        )

        # =====================================
        # LARGURA DISPONÍVEL PARA CÉLULAS
        # =====================================

        largura_disponivel_celulas = (
            largura_estante
            - largura_nivel
            - total_espacamento
        )

        tamanho = int(
            largura_disponivel_celulas
            / self.colunas
        )

        # =====================================
        # LIMITES DA LARGURA
        # =====================================

        tamanho = max(
            48,
            min(
                110,
                tamanho
            )
        )

        # =====================================
        # ALTURA
        # =====================================

        altura = int(
            tamanho * 0.62
        )

        altura = max(
            34,
            min(
                68,
                altura
            )
        )

        self.tamanho_celula = tamanho
        self.altura_celula = altura

        # =====================================
        # APLICAR NAS CÉLULAS
        # =====================================

        for botao in self.botoes.values():

            botao.setFixedSize(
                tamanho,
                altura
            )

        # =====================================
        # TAMANHO DOS CABEÇALHOS
        # =====================================

        for grade in self.grades:

            # ---------------------------------
            # LABELS DAS COLUNAS
            # ---------------------------------

            for coluna in range(
                1,
                self.colunas + 1
            ):

                item = grade.itemAtPosition(
                    0,
                    coluna
                )

                if item is not None:

                    widget = item.widget()

                    if widget is not None:

                        widget.setFixedSize(
                            tamanho,
                            24
                        )

            # ---------------------------------
            # LABELS DOS NÍVEIS
            # ---------------------------------

            for linha in range(
                1,
                self.niveis + 1
            ):

                item = grade.itemAtPosition(
                    linha,
                    0
                )

                if item is not None:

                    widget = item.widget()

                    if widget is not None:

                        widget.setFixedSize(
                            largura_nivel,
                            altura
                        )

    # =================================================
    # SELECIONAR POSIÇÃO
    # =================================================

    def selecionar(
        self,
        endereco
    ):

        if self.operacao_em_andamento:

            QMessageBox.information(
                self,
                "Operação em andamento",
                "Aguarde a operação atual terminar."
            )

            return

        dados = self.controller.buscar_posicao(
            endereco
        )

        if dados is None:

            QMessageBox.warning(
                self,
                "Erro",
                f"A posição {endereco} não foi encontrada."
            )

            return

        ocupado = dados[1]

        pallet = dados[2]

        # =====================================
        # POSIÇÃO OCUPADA
        # =====================================

        if ocupado:

            self.confirmar_retirada(
                endereco,
                pallet
            )

            return

        # =====================================
        # POSIÇÃO LIVRE
        # =====================================

        self.confirmar_armazenamento(
            endereco
        )

    # =================================================
    # CONFIRMAR ARMAZENAMENTO
    # =================================================

    def confirmar_armazenamento(
        self,
        endereco
    ):

        dialog = PalletDialog(
            endereco
        )

        if not dialog.exec():

            return

        codigo = dialog.obter_pallet()

        if not codigo:

            return

        resposta = QMessageBox.question(
            self,
            "Confirmar armazenamento",
            (
                f"Pallet: {codigo}\n\n"
                f"Destino: {endereco}\n\n"
                "Deseja iniciar o armazenamento?"
            ),
            QMessageBox.Yes |
            QMessageBox.No,
            QMessageBox.No
        )

        if resposta != QMessageBox.Yes:

            return

        self.iniciar_operacao(
            operacao="armazenar",
            endereco=endereco,
            pallet=codigo
        )

    # =================================================
    # CONFIRMAR RETIRADA
    # =================================================

    def confirmar_retirada(
        self,
        endereco,
        pallet
    ):

        resposta = QMessageBox.question(
            self,
            "Retirar pallet",
            (
                f"Pallet: {pallet}\n\n"
                f"Origem: {endereco}\n"
                "Destino: EXPEDIÇÃO\n\n"
                "Deseja iniciar a retirada?"
            ),
            QMessageBox.Yes |
            QMessageBox.No,
            QMessageBox.No
        )

        if resposta != QMessageBox.Yes:

            return

        self.iniciar_operacao(
            operacao="retirar",
            endereco=endereco,
            pallet=pallet
        )

    # =================================================
    # INICIAR OPERAÇÃO
    # =================================================

    def iniciar_operacao(
        self,
        operacao,
        endereco,
        pallet=None
    ):

        if self.operacao_em_andamento:

            return

        if not self.mks.conectado:

            QMessageBox.warning(
                self,
                "MKS desconectada",
                "Conecte a MKS antes de iniciar a operação."
            )

            return

        self.operacao_em_andamento = True

        self.definir_rack_habilitado(
            False
        )

        self.worker = RackWorker(
            self.controller,
            operacao,
            endereco,
            pallet
        )

        self.worker.concluido.connect(
            self.operacao_concluida
        )

        self.worker.finished.connect(
            self.worker_finalizado
        )

        self.worker.start()

    # =================================================
    # OPERAÇÃO CONCLUÍDA
    # =================================================

    def operacao_concluida(
        self,
        sucesso,
        mensagem
    ):

        print(
            mensagem
        )

        self.atualizar_tela()

    # =================================================
    # WORKER FINALIZADO
    # =================================================

    def worker_finalizado(
        self
    ):

        self.operacao_em_andamento = False

        self.definir_rack_habilitado(
            True
        )

        self.worker = None

        self.atualizar_tela()

    # =================================================
    # HABILITAR / DESABILITAR
    # =================================================

    def definir_rack_habilitado(
        self,
        habilitado
    ):

        for botao in self.botoes.values():

            botao.setEnabled(
                habilitado
            )

    # =================================================
    # ATUALIZAR TELA
    # =================================================

    def atualizar_tela(self):

        posicoes = self.controller.listar_posicoes()

        for endereco, ocupado, pallet in posicoes:

            if endereco in self.botoes:

                self.atualizar_cor(
                    self.botoes[endereco],
                    ocupado
                )

    # =================================================
    # ATUALIZAR COR DOS BOTÕES
    # =================================================

    def atualizar_cor(
        self,
        botao,
        ocupado
    ):

        if ocupado:

            botao.setText(
                "📦"
            )

            botao.setStyleSheet("""
                QPushButton{

                    background-color:#DC2626;

                    color:white;

                    font-size:28px;

                    font-weight:bold;

                    border:none;

                    border-radius:10px;

                }

                QPushButton:hover{

                    background-color:#EF4444;

                }
            """)

        else:

            botao.setText(
                ""
            )

            botao.setStyleSheet("""
                QPushButton{

                    background-color:#16A34A;

                    border:none;

                    border-radius:10px;

                }

                QPushButton:hover{

                    background-color:#22C55E;

                }
            """)

    # =================================================
    # FINALIZAÇÃO DA PÁGINA
    # =================================================

    def closeEvent(
        self,
        event
    ):

        if (
            self.worker is not None
            and self.worker.isRunning()
        ):

            QMessageBox.warning(
                self,
                "Operação em andamento",
                "Finalize a operação antes de fechar o aplicativo."
            )

            event.ignore()

            return

        event.accept()