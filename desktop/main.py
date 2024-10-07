import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
)


class FinanceTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Personal Finance Tracker - Login")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel("Login", self)
        self.layout.addWidget(self.label)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.layout.addWidget(self.email_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.login)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        response = requests.post(
            "http://127.0.0.1:5000/login", json={"email": email, "password": password}
        )

        if response.status_code == 200:
            self.label.setText("Login successful!")
            self.load_transactions()
        else:
            self.label.setText("Login failed.")

    def load_transactions(self):
        # Clear the current UI
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.setWindowTitle("Personal Finance Tracker - Transactions")

        self.label = QLabel("Your Transactions:", self)
        self.layout.addWidget(self.label)

        # Fetch transactions
        response = requests.get("http://127.0.0.1:5000/transactions")
        transactions = response.json()

        # Display transactions in a table
        self.transaction_table = QTableWidget(self)
        self.transaction_table.setRowCount(len(transactions))
        self.transaction_table.setColumnCount(2)
        self.transaction_table.setHorizontalHeaderLabels(["Description", "Amount"])

        for row, transaction in enumerate(transactions):
            self.transaction_table.setItem(
                row, 0, QTableWidgetItem(transaction["description"])
            )
            self.transaction_table.setItem(
                row, 1, QTableWidgetItem(str(transaction["amount"]))
            )

        self.layout.addWidget(self.transaction_table)

        self.logout_button = QPushButton("Logout", self)
        self.layout.addWidget(self.logout_button)
        self.logout_button.clicked.connect(self.logout)

    def logout(self):
        response = requests.post("http://127.0.0.1:5000/logout")
        if response.status_code == 200:
            self.label.setText("Logged out successfully!")
            self.initUI()  # Reset to login UI


def main():
    app = QApplication(sys.argv)
    window = FinanceTrackerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
