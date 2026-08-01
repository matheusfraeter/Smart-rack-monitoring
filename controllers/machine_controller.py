"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: machine_controller.py
 Descrição...: Controle da execução das missões na máquina
=========================================================
"""


from controllers.mission_controller import MissionController
from modules.gcode_generator import GCodeGenerator
from modules.fluidnc_sender import FluidNCSender



class MachineController:


    def __init__(self):

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


        # Busca próxima tarefa

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
        # Atualiza status
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
        # Finaliza missão
        # ---------------------------------

        self.mission.finalizar_missao(
            id_movimento
        )



        return {

            "sucesso": True,

            "origem":
            origem,

            "destino":
            destino,

            "gcode":
            codigo,

            "resultado":
            resultado

        }