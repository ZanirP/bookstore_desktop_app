from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
from worker import Worker

class CartDialog(QDialog):

    def __init__(self, customer_page):
        super().__init__()
        self.page = customer_page
        self.api = customer_page.api
        self.pool = customer_page.pool
        self.setWindowTitle("Cart")

        layout = QVBoxLayout(self)

        self.list = QListWidget()
        for book in self.page.cart:
            self.list.addItem(f"{book['title']} - {book['action']} ${book['price']}")

        checkout_btn = QPushButton("Checkout")
        checkout_btn.clicked.connect(self.checkout)

        layout.addWidget(self.list)
        layout.addWidget(checkout_btn)

    def checkout(self):
        items = [
            {"book_id": book["book_id"], "type": book['action']}
            for book in self.page.cart
        ]
        worker = Worker(self.api.checkout, items)
        worker.signals.finished.connect(self.checkout_done)
        self.pool.start(worker)

    def checkout_done(self, result):
        # after checkout, clear cart
        if "error" in result:
            print("Checkout error:", result)
            return
        self.page.cart.clear()
        self.accept()
