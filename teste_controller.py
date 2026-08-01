from controllers.rack_controller import RackController


controller = RackController()


dados = controller.listar_posicoes()


for item in dados:

    print(item)