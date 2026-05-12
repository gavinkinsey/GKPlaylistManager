import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from gkplaylistmanager.application import Application
from gkplaylistmanager.ui.controllers.main_controller import MainController
from gkplaylistmanager.ui.main_window import MainWindow


def main():
    # Initialize the Application layer (no GUI dependencies)
    app_service = Application()
    
    # Create the controller bridge
    controller = MainController(app_service)
    
    # Initialize Qt application
    qt_app = QApplication(sys.argv)
    
    # Create and show the main window (thin UI layer)
    window = MainWindow(controller)
    
    # Initialize playlists from default location
    data_dir = Path.home() / ".gkplaylistmanager"
    data_dir.mkdir(exist_ok=True)
    data_file = data_dir / "playlists.json"
    
    controller.initialize_playlists(str(data_file))
    
    window.show()
    sys.exit(qt_app.exec_())


if __name__ == "__main__":
    main()

