from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

from frontend.api_client import api
from frontend.worker import Worker


class LoginPage(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.pool = main_window.pool

        layout = QVBoxLayout()
        self.title = QLabel("Login")
        self.title.setStyleSheet("font-size: 25px; font-weight:bold; background-color:white")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.status_label = QLabel("Status")
        self.status_label.setStyleSheet("color:red;")

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_clicked)

        self.signup_button = QPushButton("Create Account")
        self.signup_button.clicked.connect(self.register_clicked)

        layout.addWidget(self.title)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def login_clicked(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self.status_label.setText("Missing Username or Password")
            return

        self.status_label.setStyleSheet("Logging in...")

        worker = Worker(api.login, username, password)
        worker.signals.finished.connect(self.finished_clicked)
        worker.signals.error.connect(self.error_clicked)
        self.pool.start(worker)


    def error_clicked(self, message):
        self.status_label.setText(f"Error {message}")

    def finished_clicked(self, result):
        if "error" in result:
            self.status_label.setText("Error")
            return

        api.token = result["token"]
        role = result.get("role")

        if role == "customer":
            self.main_window.go_to_customer_page()
        elif role == "manager":
            self.main_window.go_to_manager_page()
        else:
            self.status_label.setText("Error: you are not assigned a role")

    def register_clicked(self):
        self.main_window.go_to_register_page()



