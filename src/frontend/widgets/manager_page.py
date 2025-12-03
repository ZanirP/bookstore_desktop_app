from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QLabel, QTabWidget, QTextEdit
)
from PyQt5.QtCore import Qt
from frontend.worker import Worker
from frontend.api_client import api


class ManagerPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.pool = main_window.pool
        self.api = api

        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        # Tabs
        self.orders_tab = self.build_orders_tab()
        self.add_book_tab = self.build_add_book_tab()
        self.edit_book_tab = self.build_edit_book_tab()

        tabs.addTab(self.orders_tab, "Orders")
        tabs.addTab(self.add_book_tab, "Add Book")
        tabs.addTab(self.edit_book_tab, "Edit Book")

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)

        layout = self.layout()  # already created in your file

        layout.addWidget(tabs)
        layout.addWidget(logout_btn)

        # Load orders immediately
        self.load_orders()

    def build_orders_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels(
            ["Order ID", "Account ID", "Total Cost", "Status", "Created"]
        )
        layout.addWidget(self.orders_table)

        # Button row
        btn_row = QHBoxLayout()
        self.btn_mark_paid = QPushButton("Mark as Paid")
        self.btn_mark_paid.clicked.connect(self.mark_paid)
        btn_row.addWidget(self.btn_mark_paid)

        layout.addLayout(btn_row)
        return widget


    def load_orders(self):
        worker = Worker(self.api.get_all_orders)
        worker.signals.finished.connect(self.populate_orders)
        self.pool.start(worker)

    def populate_orders(self, orders):
        self.orders_table.setRowCount(len(orders))
        for row, o in enumerate(orders):
            self.orders_table.setItem(row, 0, QTableWidgetItem(str(o["order_id"])))
            self.orders_table.setItem(row, 1, QTableWidgetItem(str(o["account_id"])))
            self.orders_table.setItem(row, 2, QTableWidgetItem(str(o["total_cost"])))
            self.orders_table.setItem(row, 3, QTableWidgetItem(o["payment_status"]))
            self.orders_table.setItem(row, 4, QTableWidgetItem(o["created_at"]))


    def mark_paid(self):
        row = self.orders_table.currentRow()
        if row < 0:
            return

        order_id = self.orders_table.item(row, 0).text()

        worker = Worker(self.api.update_order_status, order_id, "Paid")
        worker.signals.finished.connect(lambda _: self.load_orders())
        self.pool.start(worker)


    def build_add_book_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.in_title = QLineEdit()
        self.in_author = QLineEdit()
        self.in_price_buy = QLineEdit()
        self.in_price_rent = QLineEdit()
        self.in_genres = QLineEdit()
        self.in_synopsis = QTextEdit()

        layout.addWidget(QLabel("Title"))
        layout.addWidget(self.in_title)

        layout.addWidget(QLabel("Author"))
        layout.addWidget(self.in_author)

        layout.addWidget(QLabel("Price Buy"))
        layout.addWidget(self.in_price_buy)

        layout.addWidget(QLabel("Price Rent"))
        layout.addWidget(self.in_price_rent)

        layout.addWidget(QLabel("Genres (comma separated)"))
        layout.addWidget(self.in_genres)

        layout.addWidget(QLabel("Synopsis"))
        layout.addWidget(self.in_synopsis)

        btn = QPushButton("Add Book")
        btn.clicked.connect(self.submit_new_book)
        layout.addWidget(btn)

        return widget


    def submit_new_book(self):
        data = {
            "title": self.in_title.text(),
            "author": self.in_author.text(),
            "price_buy": float(self.in_price_buy.text()),
            "price_rent": float(self.in_price_rent.text()),
            "genres": [g.strip() for g in self.in_genres.text().split(",")],
            "synopsis": self.in_synopsis.toPlainText()
        }

        worker = Worker(self.api.add_book, data)
        worker.signals.finished.connect(lambda _: self.clear_add_book_form())
        self.pool.start(worker)

    def clear_add_book_form(self):
        self.in_title.clear()
        self.in_author.clear()
        self.in_price_buy.clear()
        self.in_price_rent.clear()
        self.in_genres.clear()
        self.in_synopsis.clear()


    def build_edit_book_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Search bar
        self.search_edit_input = QLineEdit()
        self.search_edit_input.setPlaceholderText("Search by title")
        btn = QPushButton("Search")
        btn.clicked.connect(self.search_edit_book)

        layout.addWidget(self.search_edit_input)
        layout.addWidget(btn)

        # Editable fields
        self.up_title = QLineEdit()
        self.up_author = QLineEdit()
        self.up_price_buy = QLineEdit()
        self.up_price_rent = QLineEdit()
        self.up_synopsis = QTextEdit()

        layout.addWidget(QLabel("Title"))
        layout.addWidget(self.up_title)

        layout.addWidget(QLabel("Author"))
        layout.addWidget(self.up_author)

        layout.addWidget(QLabel("Price Buy"))
        layout.addWidget(self.up_price_buy)

        layout.addWidget(QLabel("Price Rent"))
        layout.addWidget(self.up_price_rent)

        layout.addWidget(QLabel("Synopsis"))
        layout.addWidget(self.up_synopsis)

        update_btn = QPushButton("Save Changes")
        update_btn.clicked.connect(self.update_book)
        layout.addWidget(update_btn)

        self.current_book_id = None
        return widget


    def search_edit_book(self):
        query = self.search_edit_input.text()

        worker = Worker(self.api.search_books, query)
        worker.signals.finished.connect(self.fill_edit_form)
        self.pool.start(worker)

    def fill_edit_form(self, books):
        if not books:
            return

        book = books[0]
        self.current_book_id = book["id"]

        self.up_title.setText(book["title"])
        self.up_author.setText(book["author"])
        self.up_price_buy.setText(str(book["price_buy"]))
        self.up_price_rent.setText(str(book["price_rent"]))
        self.up_synopsis.setText(book["synopsis"])

    def update_book(self):
        if not self.current_book_id:
            return

        data = {
            "title": self.up_title.text(),
            "author": self.up_author.text(),
            "price_buy": float(self.up_price_buy.text()),
            "price_rent": float(self.up_price_rent.text()),
            "synopsis": self.up_synopsis.toPlainText(),
        }

        worker = Worker(self.api.update_book, self.current_book_id, data)
        worker.signals.finished.connect(lambda _: print("Updated"))
        self.pool.start(worker)

    def logout(self):
        worker = Worker(self.api.logout)
        worker.signals.finished.connect(lambda _: self.main_window.logout())
        self.pool.start(worker)

