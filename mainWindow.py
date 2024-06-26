
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QVBoxLayout
from PyQt5.QtCore import QDir
import hashlib

def select_directory(directory_line_edit):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    if dialog.exec():
        directory_line_edit.setText(dialog.selectedFiles()[0])

def calculate_hash(directory_line_edit, result_line_edit):
    directory = str(Path(directory_line_edit.text()).resolve())
    try:
        hash_value = hash_all_files(directory)
        result_line_edit.setText(hash_value)
    except Exception as e:
        print(f"Error calculating hash: {e}")

def hash_all_files(directory):
    hash_md5 = hashlib.md5()
    for path in Path(directory).rglob('*'):
        if path.is_file():
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 400, 300)
    window.setWindowTitle("Calculate MD5 Hash")

    directory_line_edit = QLineEdit()
    select_directory_button = QPushButton("Select Directory")
    calculate_hash_button = QPushButton("Calculate Hash")
    result_line_edit = QLineEdit()

    select_directory_button.clicked.connect(lambda: select_directory(directory_line_edit))
    calculate_hash_button.clicked.connect(lambda: calculate_hash(directory_line_edit, result_line_edit))

    vbox = QVBoxLayout()
    vbox.addWidget(directory_line_edit)
    vbox.addWidget(select_directory_button)
    vbox.addWidget(calculate_hash_button)
    vbox.addWidget(result_line_edit)
    window.setLayout(vbox)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

