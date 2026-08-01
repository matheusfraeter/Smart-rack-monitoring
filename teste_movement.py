from controllers.movement_controller import MovementController


movimento = MovementController()


resultado = movimento.criar_movimento(
    "A2",
    "C3"
)


print(resultado)