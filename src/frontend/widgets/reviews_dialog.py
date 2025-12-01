from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QListWidgetItem, QLabel

class ReviewsDialog(QDialog):
    def __init__(self, reviews):
        super().__init__()
        self.setWindowTitle("Reviews")
        layout = QVBoxLayout(self)

        if not reviews or len(reviews) == 0:
            layout.addWidget(QLabel("No reviews yet."))
            return

        list_widget = QListWidget()

        for r in reviews:
            date = r.get("created_at", "Unknown date")
            acct = r.get("account_id", "Anonymous")
            content = r.get("review_content", "")

            text = f"[{date}] User {acct}:\n{content}"

            item = QListWidgetItem(text)
            list_widget.addItem(item)

        layout.addWidget(list_widget)
