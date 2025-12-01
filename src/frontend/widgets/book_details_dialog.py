from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QHBoxLayout

class BookDetailsDialog(QDialog):

    def __init__(self, book, customer_page):
        super().__init__()
        self.book = book
        self.customer_page = customer_page

        self.setWindowTitle(book["title"])
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(f"Title: {book['title']}"))
        layout.addWidget(QLabel(f"Author: {book['author']}"))
        layout.addWidget(QLabel(f"Price Buy: ${book['price_buy']}"))
        layout.addWidget(QLabel(f"Price Rent: ${book['price_rent']}"))
        synopsis_label = QLabel(f"Synopsis:\n{book['synopsis']}")
        synopsis_label.setWordWrap(True)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(synopsis_label)

        layout.addWidget(scroll_area)

        btn_layout = QHBoxLayout()

        buy_btn = QPushButton("Buy")
        buy_btn.clicked.connect(self.buy_clicked)
        btn_layout.addWidget(buy_btn)

        rent_btn = QPushButton("Rent")
        rent_btn.clicked.connect(self.rent_clicked)
        btn_layout.addWidget(rent_btn)

        reviews_btn = QPushButton("Show Reviews")
        reviews_btn.clicked.connect(self.show_reviews)
        btn_layout.addWidget(reviews_btn)

        layout.addLayout(btn_layout)

    def buy_clicked(self):
        item = {
            "book_id": self.book["id"],
            "title": self.book["title"],
            "price": self.book["price_buy"],
            "action": "buy"
        }
        self.customer_page.cart.append(item)
        self.accept()

    def rent_clicked(self):
        item = {
            "book_id": self.book["id"],
            "title": self.book["title"],
            "price": self.book["price_rent"],
            "action": "rent"
        }
        self.customer_page.cart.append(item)
        self.accept()

    def show_reviews(self):
        worker = Worker(api.get_reviews, self.book["id"])
        worker.signals.finished.connect(self.open_reviews_dialog)
        self.page.pool.start(worker)

    def open_reviews_dialog(self, reviews):
        dlg = ReviewsDialog(reviews)
        dlg.exec_()
