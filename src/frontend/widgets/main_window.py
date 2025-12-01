from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

app = QApplication(sys.argv)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bookstore")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)


