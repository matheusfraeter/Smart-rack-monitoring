class Movement:

    def __init__(self, mks):
        self.mks = mks


    def mover_x(self, valor):

        comando = f"""
G91
G1 X{valor} F1000
"""

        self.mks.enviar_comando(comando)



    def mover_y(self, valor):

        comando = f"""
G91
G1 Y{valor} F1000
"""

        self.mks.enviar_comando(comando)



    def mover_z(self, valor):

        comando = f"""
G91
G1 Z{valor} F500
"""

        self.mks.enviar_comando(comando)