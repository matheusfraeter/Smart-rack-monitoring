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

    def mover_x(
        self,
        valor,
        velocidade=1000
    ):

        try:

            valor = float(
                valor
            )

        except (ValueError, TypeError):

            print(
                "ERRO: valor X inválido:",
                valor
            )

            return False

        try:

            velocidade = float(
                velocidade
            )

        except (ValueError, TypeError):

            print(
                "ERRO: velocidade X inválida:",
                velocidade
            )

            return False

        if velocidade <= 0:

            print(
                "ERRO: velocidade deve ser maior que zero."
            )

            return False

        comando = (
            f"G91\n"
            f"G1 X{valor:g} F{velocidade:g}"
        )

        print()
        print(
            "===================================="
        )
        print(
            " MOVIMENTO X"
        )
        print(
            "===================================="
        )
        print(
            "Valor:",
            valor
        )
        print(
            "Velocidade:",
            velocidade
        )
        print(
            "G-CODE:"
        )
        print(
            repr(comando)
        )
        print(
            "===================================="
        )

        return self.mks.enviar_comando(
            comando
        )

    # =====================================================
    # EIXO Y
    # =====================================================

    def mover_y(
        self,
        valor,
        velocidade=1000
    ):

        try:

            valor = float(
                valor
            )

        except (ValueError, TypeError):

            print(
                "ERRO: valor Y inválido:",
                valor
            )

            return False

        try:

            velocidade = float(
                velocidade
            )

        except (ValueError, TypeError):

            print(
                "ERRO: velocidade Y inválida:",
                velocidade
            )

            return False

        if velocidade <= 0:

            print(
                "ERRO: velocidade deve ser maior que zero."
            )

            return False

        comando = (
            f"G91\n"
            f"G1 Y{valor:g} F{velocidade:g}"
        )

        print()
        print(
            "===================================="
        )
        print(
            " MOVIMENTO Y"
        )
        print(
            "===================================="
        )
        print(
            "Valor:",
            valor
        )
        print(
            "Velocidade:",
            velocidade
        )
        print(
            "G-CODE:"
        )
        print(
            repr(comando)
        )
        print(
            "===================================="
        )

        return self.mks.enviar_comando(
            comando
        )

    # =====================================================
    # EIXO Z
    # =====================================================

    def mover_z(
        self,
        valor,
        velocidade=500
    ):

        try:

            valor = float(
                valor
            )

        except (ValueError, TypeError):

            print(
                "ERRO: valor Z inválido:",
                valor
            )

            return False

        try:

            velocidade = float(
                velocidade
            )

        except (ValueError, TypeError):

            print(
                "ERRO: velocidade Z inválida:",
                velocidade
            )

            return False

        if velocidade <= 0:

            print(
                "ERRO: velocidade deve ser maior que zero."
            )

            return False

        comando = (
            f"G91\n"
            f"G1 Z{valor:g} F{velocidade:g}"
        )

        print()
        print(
            "===================================="
        )
        print(
            " MOVIMENTO Z"
        )
        print(
            "===================================="
        )
        print(
            "Valor:",
            valor
        )
        print(
            "Velocidade:",
            velocidade
        )
        print(
            "G-CODE:"
        )
        print(
            repr(comando)
        )
        print(
            "===================================="
        )

        return self.mks.enviar_comando(
            comando
        )