"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: movement.py
 Descrição...: Controle dos movimentos XYZ
=========================================================
"""


class Movement:

    def __init__(self, mks):

        self.mks = mks

    # =====================================================
    # EIXO X
    # =====================================================

    def mover_x(self, valor):

        try:

            valor = float(valor)

        except (ValueError, TypeError):

            print("ERRO: valor X inválido:", valor)

            return False

        comando = f"G91\nG1 X{valor:g} F1000"

        print()
        print("====================================")
        print(" MOVIMENTO X")
        print("====================================")
        print("Valor:", valor)
        print("G-CODE:")
        print(repr(comando))
        print("====================================")

        return self.mks.enviar_comando(comando)

    # =====================================================
    # EIXO Y
    # =====================================================

    def mover_y(self, valor):

        try:

            valor = float(valor)

        except (ValueError, TypeError):

            print("ERRO: valor Y inválido:", valor)

            return False

        comando = f"G91\nG1 Y{valor:g} F1000"

        print()
        print("====================================")
        print(" MOVIMENTO Y")
        print("====================================")
        print("Valor:", valor)
        print("G-CODE:")
        print(repr(comando))
        print("====================================")

        return self.mks.enviar_comando(comando)

    # =====================================================
    # EIXO Z
    # =====================================================

    def mover_z(self, valor):

        try:

            valor = float(valor)

        except (ValueError, TypeError):

            print("ERRO: valor Z inválido:", valor)

            return False

        comando = f"G91\nG1 Z{valor:g} F500"

        print()
        print("====================================")
        print(" MOVIMENTO Z")
        print("====================================")
        print("Valor:", valor)
        print("G-CODE:")
        print(repr(comando))
        print("====================================")

        return self.mks.enviar_comando(comando)