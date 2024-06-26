import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QVBoxLayout
from PyQt5.QtCore import QDir
import hashCalculating
from hashCalculating import calculateHash, hashAllFiles

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle("Calculate MD5 Hash")

        self.directory_line_edit = QLineEdit()
        select_directory_button = QPushButton("Select Directory")
        calculate_hash_button = QPushButton("Calculate Hash")
        result_line_edit = QLineEdit()

        select_directory_button.clicked.connect(self.select_directory)
        calculate_hash_button.clicked.connect(self.calculate_hash)

        vbox = QVBoxLayout()
        vbox.addWidget(self.directory_line_edit)
        vbox.addWidget(select_directory_button)
        vbox.addWidget(calculate_hash_button)
        vbox.addWidget(result_line_edit)
        self.setLayout(vbox)

    def select_directory(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        if dialog.exec():
            self.directory_line_edit.setText(dialog.selectedFiles()[0])

    def calculate_hash(self):
        directory = str(Path(self.directory_line_edit.text()).resolve())
        try:
            hash_value = hashAllFiles(directory)
            self.result_line_edit.setText(hashValue)
        except Exception as e:
            print(f"Error calculating hash: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())