from PySide6.QtWidgets import QApplication
from ui.pages.mission_queue import MissionQueuePage
import sys


app = QApplication(sys.argv)

janela = MissionQueuePage()

janela.show()

sys.exit(app.exec())