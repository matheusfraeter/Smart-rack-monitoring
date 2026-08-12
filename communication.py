"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: communication.py
 Descrição...:
     - HTTP  -> envio de comandos
     - HTTP  -> solicita status
     - WS    -> recebe status do FluidNC
=========================================================
"""

import requests
import websocket
import threading
import time


class MKSConnection:

    def __init__(self):

        self.ip = "192.168.4.1"

        self.http_url = f"http://{self.ip}"
        self.ws_url = f"ws://{self.ip}:81"

        # =====================================
        # CONEXÃO
        # =====================================

        self.conectado = False
        self.running = False

        # =====================================
        # WEBSOCKET
        # =====================================

        self.ws = None
        self.thread = None

        # =====================================
        # ESP3D
        # =====================================

        self.active_id = None
        self.esp3d_pronto = False

        # =====================================
        # STATUS
        # =====================================

        self.status = {
            "estado": "Desconectada",
            "X": 0.0,
            "Y": 0.0,
            "Z": 0.0
        }

        self.ultima_resposta = ""

        # =====================================
        # LOCKS
        # =====================================

        self.status_lock = threading.Lock()
        self.ws_lock = threading.Lock()

        # =====================================
        # CONTROLE
        # =====================================

        self.ultimo_status = 0


    # =========================================
    # CONECTAR
    # =========================================

    def conectar(self):

        if self.conectado:
            return True

        try:

            print()
            print("=" * 60)
            print(" CONECTANDO MKS DLC32")
            print("=" * 60)

            # ---------------------------------
            # TESTE HTTP
            # ---------------------------------

            resposta = requests.get(
                self.http_url,
                timeout=3
            )

            if resposta.status_code != 200:

                print(
                    "HTTP não respondeu:",
                    resposta.status_code
                )

                return False

            print("HTTP OK")

            # ---------------------------------
            # WEBSOCKET
            # ---------------------------------

            self.ws = websocket.WebSocket()

            self.ws.connect(
                self.ws_url,
                subprotocols=["arduino"],
                timeout=5
            )

            print(
                "WebSocket conectado!"
            )

            self.conectado = True
            self.running = True

            self.esp3d_pronto = False
            self.active_id = None

            with self.status_lock:

                self.status["estado"] = "Conectada"

            # ---------------------------------
            # THREAD
            # ---------------------------------

            self.thread = threading.Thread(
                target=self._loop_websocket,
                daemon=True
            )

            self.thread.start()

            return True

        except Exception as erro:

            print()
            print("Erro ao conectar:")
            print(erro)

            self._desconectar_interno()

            return False


    # =========================================
    # LOOP WEBSOCKET
    # =========================================

    def _loop_websocket(self):

        while self.running:

            try:

                if self.ws is None:

                    time.sleep(0.5)
                    continue

                # ---------------------------------
                # RECEBER
                # ---------------------------------

                self.ws.settimeout(0.2)

                try:

                    mensagem = self.ws.recv()

                    if mensagem:

                        self._processar_mensagem(
                            mensagem
                        )

                except websocket.WebSocketTimeoutException:

                    pass

                # ---------------------------------
                # SOLICITAR STATUS
                # ---------------------------------

                agora = time.time()

                if (
                    agora - self.ultimo_status
                    >= 1.0
                ):

                    self._solicitar_status()

                    self.ultimo_status = agora

                time.sleep(0.01)

            except Exception as erro:

                print()
                print(
                    "Erro no WebSocket:"
                )
                print(erro)

                time.sleep(0.5)


    # =========================================
    # SOLICITAR STATUS
    # =========================================

    def _solicitar_status(self):

        try:

            resposta = requests.get(
                f"{self.http_url}/command",
                params={
                    "plain": "?"
                },
                timeout=2
            )

            if resposta.status_code != 200:

                print(
                    "Erro solicitando status:",
                    resposta.status_code
                )

        except Exception as erro:

            print(
                "Erro HTTP status:",
                erro
            )


    # =========================================
    # PROCESSAR MENSAGEM
    # =========================================

    def _processar_mensagem(self, mensagem):

        try:

            if isinstance(
                mensagem,
                bytes
            ):

                mensagem = mensagem.decode(
                    "utf-8",
                    errors="ignore"
                )

            mensagem = mensagem.strip()

            if not mensagem:
                return

            print()
            print("<<< STATUS WEBSOCKET >>>")
            print(repr(mensagem))

            self.ultima_resposta = mensagem

            # =================================
            # STATUS FLUIDNC
            # =================================

            if mensagem.startswith("<"):

                self._processar_status(
                    mensagem
                )

                return

            # =================================
            # CURRENT ID
            # =================================

            if mensagem.startswith(
                "CURRENT_ID:"
            ):

                return

            # =================================
            # ACTIVE ID
            # =================================

            if mensagem.startswith(
                "ACTIVE_ID:"
            ):

                try:

                    self.active_id = int(
                        mensagem.split(
                            ":",
                            1
                        )[1]
                    )

                except Exception:

                    self.active_id = None

                self.esp3d_pronto = True

                print(
                    "ESP3D pronto. ACTIVE_ID:",
                    self.active_id
                )

                return

            # =================================
            # PING
            # =================================

            if mensagem.startswith(
                "PING:"
            ):

                return

        except Exception as erro:

            print(
                "Erro processando mensagem:",
                erro
            )


    # =========================================
    # PROCESSAR STATUS
    # =========================================

    def _processar_status(self, mensagem):

        try:

            # ---------------------------------
            # LIMPA CRLF
            # ---------------------------------

            mensagem = mensagem.strip()

            # ---------------------------------
            # REMOVE < >
            # ---------------------------------

            if mensagem.startswith("<"):

                mensagem = mensagem[1:]

            if mensagem.endswith(">"):

                mensagem = mensagem[:-1]

            # ---------------------------------
            # SEPARA CAMPOS
            # ---------------------------------

            partes = mensagem.split("|")

            if not partes:

                return

            # ---------------------------------
            # ESTADO
            # ---------------------------------

            estado = partes[0].strip()

            x = None
            y = None
            z = None

            # ---------------------------------
            # PROCURA MPos
            # ---------------------------------

            for parte in partes:

                parte = parte.strip()

                if parte.startswith("MPos:"):

                    texto_posicao = parte[
                        5:
                    ]

                    valores = (
                        texto_posicao.split(",")
                    )

                    if len(valores) >= 3:

                        try:

                            x = float(
                                valores[0]
                            )

                            y = float(
                                valores[1]
                            )

                            z = float(
                                valores[2]
                            )

                        except ValueError:

                            print(
                                "MPos inválido:",
                                texto_posicao
                            )

                    break

            # ---------------------------------
            # ATUALIZA STATUS
            # ---------------------------------

            with self.status_lock:

                self.status["estado"] = estado

                if x is not None:
                    self.status["X"] = x

                if y is not None:
                    self.status["Y"] = y

                if z is not None:
                    self.status["Z"] = z

            # ---------------------------------
            # DEBUG
            # ---------------------------------

            if (
                x is not None
                and y is not None
                and z is not None
            ):

                print(
                    "POSIÇÃO ATUALIZADA:"
                )

                print(
                    f"Estado: {estado}"
                )

                print(
                    f"X: {x:.3f}"
                )

                print(
                    f"Y: {y:.3f}"
                )

                print(
                    f"Z: {z:.3f}"
                )

        except Exception as erro:

            print(
                "Erro interpretando MPos:"
            )

            print(erro)


    # =========================================
    # ENVIAR COMANDO
    # =========================================

    def enviar_comando(
        self,
        comando
    ):

        if isinstance(
            comando,
            bool
        ):

            print(
                "ERRO: comando booleano:",
                comando
            )

            return False

        if comando is None:

            return False

        comando = str(
            comando
        ).strip()

        if not comando:

            return False

        if not self.conectado:

            print(
                "MKS desconectada"
            )

            return False

        try:

            print()
            print("=" * 60)
            print(" ENVIANDO COMANDO VIA HTTP")
            print("=" * 60)

            print(
                "G-code:",
                repr(comando)
            )

            resposta = requests.post(

                f"{self.http_url}/command",

                data=comando,

                timeout=5

            )

            self.ultima_resposta = (
                resposta.text
            )

            print(
                "HTTP:",
                resposta.status_code
            )

            print(
                "Resposta:",
                repr(resposta.text)
            )

            if resposta.status_code != 200:

                return False

            return True

        except Exception as erro:

            print(
                "Erro comando:",
                erro
            )

            return False


    # =========================================
    # HOME
    # =========================================

    def zerar_eixos(self):

        return self.enviar_comando(
            "$H"
        )


    # =========================================
    # DESCONECTAR
    # =========================================

    def desconectar(self):

        print(
            "Desconectando MKS..."
        )

        self.running = False
        self.conectado = False

        self._fechar_websocket()

        with self.status_lock:

            self.status["estado"] = (
                "Desconectada"
            )


    # =========================================
    # FECHAR WEBSOCKET
    # =========================================

    def _fechar_websocket(self):

        try:

            if self.ws:

                self.ws.close()

        except Exception:

            pass

        self.ws = None
        self.esp3d_pronto = False


    # =========================================
    # DESCONECTAR INTERNO
    # =========================================

    def _desconectar_interno(self):

        self.running = False
        self.conectado = False
        self.esp3d_pronto = False

        self._fechar_websocket()

        with self.status_lock:

            self.status["estado"] = (
                "Desconectada"
            )


    # =========================================
    # LER STATUS
    # =========================================

    def ler_status(self):

        with self.status_lock:

            return self.status.copy()