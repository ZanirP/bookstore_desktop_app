from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
)

from frontend.api_client import api
from frontend.worker import Worker


class RegisterPage(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.pool = main_window.pool

        layout = QVBoxLayout()

        # Title
        title = QLabel("Create Account")
        title.setStyleSheet("font-size: 25px; font-weight: bold;")
        layout.addWidget(title)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: red;")
        layout.addWidget(self.status_label)

        # Submit button
        register_btn = QPushButton("Create Account")
        register_btn.clicked.connect(self.register_clicked)
        layout.addWidget(register_btn)

        # Back to login
        back_btn = QPushButton("Back to Login")
        back_btn.clicked.connect(self.back_to_login)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def back_to_login(self):
        self.main_window.go_to_login_page()

    def register_clicked(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not email or not password:
            self.status_label.setText("All fields are required.")
            return

        self.status_label.setText("Creating account...")

        worker = Worker(api.register, username, password, email)
        worker.signals.finished.connect(self.register_finished)
        worker.signals.error.connect(self.register_error)

        self.pool.start(worker)

    def register_error(self, msg):
        self.status_label.setText(f"Error: {msg}")

    def register_finished(self, result):
        if "error" in result:
            self.status_label.setText(f"Error: {result['error']}")
            return

        self.status_label.setStyleSheet("color: green;")
        self.status_label.setText("Account created successfully!")

        # After successful registration, go back to login automatically
        self.main_window.go_to_login_page()
