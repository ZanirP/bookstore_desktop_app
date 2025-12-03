from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import QThreadPool
from frontend.widgets.login_page import LoginPage
from frontend.widgets.customer_page import CustomerPage
from frontend.widgets.manager_page import ManagerPage
from frontend.widgets.register_page import RegisterPage
from frontend.api_client import api
import sys

app = QApplication(sys.argv)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bookstore")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.pool = QThreadPool.globalInstance()

        # Only create login page
        self.login_page = LoginPage(self)
        self.stack.addWidget(self.login_page)

        self.customer_page = None
        self.manager_page = None

        self.register_page = RegisterPage(self)
        self.stack.addWidget(self.register_page)

        self.showMaximized()
        self.go_to_login_page()

    def go_to_login_page(self):
        self.stack.setCurrentWidget(self.login_page)

    def go_to_customer_page(self):
        if self.customer_page is None:
            self.customer_page = CustomerPage(self)
            self.stack.addWidget(self.customer_page)

        self.stack.setCurrentWidget(self.customer_page)

    def go_to_manager_page(self):
        if self.manager_page is None:
            self.manager_page = ManagerPage(self)
            self.stack.addWidget(self.manager_page)

        self.stack.setCurrentWidget(self.manager_page)

    def go_to_register_page(self):
        self.stack.setCurrentWidget(self.register_page)

    def logout(self):
        api.token = None
        self.go_to_login_page()

    def closeEvent(self, event):
        try:
            if api.token:  # only call backend if logged in
                api.logout()
            api.token = None
        except:
            pass  # ignore network errors on exit

        event.accept()  # let the window close






