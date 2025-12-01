from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import QThreadPool
from widgets.login_page import LoginPage
from widgets.customer_page import CustomerPage
import sys

app = QApplication(sys.argv)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bookstore")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.pool = QThreadPool.globalInstance()

        self.login_page = LoginPage(self)
        self.stack.addWidget(self.login_page)

        self.customer_page = CustomerPage(self)
        self.stack.addWidget(self.customer_page)

        self.showMaximized()
        self.go_to_login_page()

    def go_to_login_page(self):
        self.stack.setCurrentWidget(self.login_page)

    def go_to_manager_page(self):
        self.stack.setCurrentWidget(self.login_page)

    def go_to_customer_page(self):
        self.stack.setCurrentWidget(self.customer_page)



