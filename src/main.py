import sys

from PyQt6.QtWidgets import QApplication

from app.Controller import Controller


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec())
