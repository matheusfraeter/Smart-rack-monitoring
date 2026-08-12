import websocket
import time


IP = "192.168.4.1"
WS_URL = f"ws://{IP}:81"


print("=" * 60)
print("TESTE DE ENVIO - MESMO CANAL DO APLICATIVO")
print("=" * 60)

print()
print("Conectando em:")
print(WS_URL)

ws = websocket.WebSocket()

try:

    ws.connect(
        WS_URL,
        subprotocols=["arduino"],
        timeout=5
    )

    print()
    print("WEBSOCKET CONECTADO!")

    # =========================================
    # RECEBER IDENTIFICAÇÃO ESP3D
    # =========================================

    ws.settimeout(2)

    pronto = False

    inicio = time.time()

    while time.time() - inicio < 5:

        try:

            mensagem = ws.recv()

            print()
            print("<<< RECEBIDO >>>")
            print(repr(mensagem))

            if isinstance(mensagem, bytes):

                mensagem = mensagem.decode(
                    "utf-8",
                    errors="ignore"
                )

            if mensagem.startswith("ACTIVE_ID:"):

                pronto = True

                print()
                print("ESP3D PRONTO!")

                break

        except websocket.WebSocketTimeoutException:

            pass

    if not pronto:

        print()
        print("ESP3D NÃO FICOU PRONTO!")

    else:

        # =====================================
        # ENVIA G91
        # =====================================

        print()
        print("=" * 60)
        print("ENVIANDO:")
        print("G91")
        print("=" * 60)

        ws.send("G91")

        print("G91 ENVIADO!")

        time.sleep(0.5)

        # =====================================
        # ENVIA MOVIMENTO
        # =====================================

        print()
        print("=" * 60)
        print("ENVIANDO:")
        print("G1 X10 F1000")
        print("=" * 60)

        ws.send("G1 X10 F1000")

        print("MOVIMENTO ENVIADO!")

        # =====================================
        # AGUARDA RESPOSTA
        # =====================================

        ws.settimeout(2)

        inicio = time.time()

        while time.time() - inicio < 5:

            try:

                mensagem = ws.recv()

                print()
                print("<<< RESPOSTA >>>")
                print(repr(mensagem))

            except websocket.WebSocketTimeoutException:

                break


finally:

    print()
    print("Fechando WebSocket...")

    ws.close()

    print("FINALIZADO")