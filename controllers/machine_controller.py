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
        # Verifica pallet na origem
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
        # Verifica destino livre
        # ---------------------------------

        if self.db.verificar_posicao_livre(
            destino
        ) is False:


            return {

                "sucesso": False,

                "mensagem":
                f"Destino {destino} já possui pallet"

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
        # Verifica envio
        # ---------------------------------

        if isinstance(resultado, dict):


            if resultado.get("sucesso") is False:


                self.mission.cancelar_missao(
                    id_movimento
                )


                return {

                    "sucesso": False,

                    "mensagem":
                    "Erro ao enviar G-code",

                    "erro":
                    resultado

                }



        else:


            for linha in resultado:


                if linha.get("sucesso") is False:


                    self.mission.cancelar_missao(
                        id_movimento
                    )


                    return {

                        "sucesso": False,

                        "mensagem":
                        "Falha na comunicação FluidNC",

                        "erro":
                        linha

                    }



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


            "pallet":

            pallet,


            "gcode":

            codigo,


            "resultado":

            resultado

        }