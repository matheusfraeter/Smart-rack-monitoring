"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: machine_controller.py
 Descrição...: Controle da execução das missões na máquina
=========================================================
"""


from database import Database

from controllers.mission_controller import MissionController

from modules.gcode_generator import GCodeGenerator

from modules.fluidnc_sender import FluidNCSender




class MachineController:


    def __init__(self):

        self.db = Database()

        self.mission = MissionController()

        self.gcode = GCodeGenerator()

        self.fluidnc = FluidNCSender()



    # =====================================
    # TESTAR MÁQUINA
    # =====================================

    def testar_maquina(self):

        return self.fluidnc.testar_conexao()



    # =====================================
    # EXECUTAR PRÓXIMA MISSÃO
    # =====================================

    def executar_proxima_missao(self):


        movimento = self.mission.proxima_missao()



        if movimento is None:

            return {

                "sucesso": False,

                "mensagem":
                "Nenhuma missão pendente"

            }



        id_movimento = movimento[0]

        origem = movimento[1]

        destino = movimento[2]



        # ---------------------------------
        # Busca pallet
        # ---------------------------------

        pallet = self.db.verificar_pallet(
            origem
        )



        if pallet is None:

            return {

                "sucesso": False,

                "mensagem":
                f"Sem pallet em {origem}"

            }



        # ---------------------------------
        # Inicia missão
        # ---------------------------------

        self.mission.iniciar_missao(
            id_movimento
        )



        # ---------------------------------
        # Gera G-code
        # ---------------------------------

        codigo = self.gcode.gerar_movimentacao(
            origem,
            destino
        )



        # ---------------------------------
        # Envia para FluidNC
        # ---------------------------------

        resultado = self.fluidnc.enviar_programa(
            codigo
        )



        # ---------------------------------
        # Atualiza rack
        # ---------------------------------

        self.db.liberar_posicao(
            origem
        )


        self.db.ocupar_posicao(
            destino,
            pallet
        )



        # ---------------------------------
        # Finaliza missão
        # ---------------------------------

        self.mission.finalizar_missao(
            id_movimento
        )



        return {


            "sucesso": True,


            "mensagem":

            f"Pallet {pallet} movido de {origem} para {destino}",


            "origem":

            origem,


            "destino":

            destino,


            "gcode":

            codigo,


            "resultado":

            resultado

        }