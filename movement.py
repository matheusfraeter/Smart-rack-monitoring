"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: movement.py
 Descrição...: Movimentação manual dos eixos
=========================================================
"""


class Movement:

    def __init__(self, mks):
        self.mks = mks

    # =====================================
    # EIXO X
    # =====================================

    def mover_x(self, valor):

        comando = f"""
G91
G1 X{valor} F1000
"""

        if self.mks.enviar_comando(comando):

            self.mks.status["X"] += valor
            self.mks.status["estado"] = "MOVENDO"

            return True

        return False

    # =====================================
    # EIXO Y
    # =====================================

    def mover_y(self, valor):

        comando = f"""
G91
G1 Y{valor} F1000
"""

        if self.mks.enviar_comando(comando):

            self.mks.status["Y"] += valor
            self.mks.status["estado"] = "MOVENDO"

            return True

        return False

    # =====================================
    # EIXO Z
    # =====================================

    def mover_z(self, valor):

        comando = f"""
G91
G1 Z{valor} F500
"""

        if self.mks.enviar_comando(comando):

            self.mks.status["Z"] += valor
            self.mks.status["estado"] = "MOVENDO"

            return True

        return False