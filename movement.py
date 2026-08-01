class Movement:


    def __init__(self, mks):

        self.mks = mks



    def mover_x(self, distancia):

        comando = (
            "G91\n"
            f"G1 X{distancia} F1000"
        )

        return self.mks.enviar_comando(comando)



    def mover_y(self, distancia):

        comando = (
            "G91\n"
            f"G1 Y{distancia} F1000"
        )

        return self.mks.enviar_comando(comando)



    def mover_z(self, distancia):

        comando = (
            "G91\n"
            f"G1 Z{distancia} F500"
        )

        return self.mks.enviar_comando(comando)