import requests
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
)


class FinanceTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Personal Finance Tracker - Login")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Login", self)
        layout.addWidget(self.label)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.login)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        response = requests.post(
            "http://127.0.0.1:5000/login", json={"email": email, "password": password}
        )
        if response.status_code == 200:
            self.label.setText("Login successful!")
        else:
            self.label.setText("Login failed.")
