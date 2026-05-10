from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GK Playlist Manager")
        central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to GKPlaylistManager!"))
        central.setLayout(layout)
        self.setCentralWidget(central)
