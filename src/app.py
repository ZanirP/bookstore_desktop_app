import sys
import threading

from backend import create_app
from PyQt5.QtWidgets import QApplication
from frontend.widgets.main_window import MainWindow


def run_backend():
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


def main():
    # --- Start Flask backend thread ---
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()

    # --- Start PyQt frontend ---
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(qt_app.exec_())


if __name__ == "__main__":
    main()
