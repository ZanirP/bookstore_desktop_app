from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QListWidget, QListWidgetItem
)
from frontend.widgets.book_details_dialog import BookDetailsDialog
from frontend.widgets.cart_dialog import CartDialog
from PyQt5.QtCore import Qt
from frontend.api_client import api
from frontend.worker import Worker


class CustomerPage(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.search_input = None
        self.books_list = None
        
        self.main_window = main_window
        self.api = api
        self.pool = main_window.pool

        self.cart = []

        self.setup_ui()
        self.load_all_books()


    def setup_ui(self):
        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for a book...")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_clicked)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)

        self.books_list = QListWidget()
        self.books_list.itemClicked.connect(self.book_clicked)

        cart_btn = QPushButton("View Cart")
        cart_btn.clicked.connect(self.view_cart)

        layout.addLayout(search_layout)
        layout.addWidget(self.books_list)
        layout.addWidget(cart_btn)

        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)

    def load_all_books(self):
        worker = Worker(self.api.get_all_books)
        worker.signals.finished.connect(self.populate_books)
        self.pool.start(worker)

    def populate_books(self, books):
        self.books_list.clear()
        for book in books:
            item = QListWidgetItem(f"{book['title']} — {book['author']}")
            item.setData(Qt.UserRole, book)
            self.books_list.addItem(item)

    def search_clicked(self):
        query = self.search_input.text().strip()
        if query == "":
            self.load_all_books()
            return

        worker = Worker(self.api.search_books, query)
        worker.signals.finished.connect(self.populate_books)
        self.pool.start(worker)

    def book_clicked(self, item):
        book = item.data(Qt.UserRole)
        dialog = BookDetailsDialog(book, self)
        dialog.exec_()

    def view_cart(self):
        dlg = CartDialog(self)
        dlg.exec_()

    def logout(self):
        worker = Worker(self.api.logout)
        worker.signals.finished.connect(lambda _: self.main_window.logout())
        self.pool.start(worker)





