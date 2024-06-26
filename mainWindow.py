import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QDir
import hashlib

def selectDirectory(directoryLineEdit):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    if dialog.exec():
        directoryLineEdit.setText(dialog.selectedFiles()[0])

def calculateHash(directoryLineEdit, resultTextEdit):
    directory = str(Path(directoryLineEdit.text()).resolve())
    try:
        file_info = hashAllFiles(directory)
        resultTextEdit.clear()
        for file_name, info in file_info.items():
            resultTextEdit.append(f"File: {file_name}\nSize: {info['size']} bytes\nHash: {info['hash']}\n")
    except Exception as e:
        print(f"Error calculating hash: {e}")

def hashAllFiles(directory):
    file_info = {}
    for path in Path(directory).rglob('*'):
        if path.is_file():
            hash_md5 = hashlib.md5()
            file_size = path.stat().st_size
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            file_info[path.name] = {
                'size': file_size,
                'hash': hash_md5.hexdigest()
            }
    return file_info

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 600, 400)
    window.setWindowTitle("Calculate MD5 Hash")

    directoryLineEdit = QLineEdit()
    selectDirectory_button = QPushButton("Select Directory")
    calculateHash_button = QPushButton("Calculate Hash")
    resultTextEdit = QTextEdit()

    selectDirectory_button.clicked.connect(lambda: selectDirectory(directoryLineEdit))
    calculateHash_button.clicked.connect(lambda: calculateHash(directoryLineEdit, resultTextEdit))

    vbox = QVBoxLayout()
    vbox.addWidget(directoryLineEdit)
    vbox.addWidget(selectDirectory_button)
    vbox.addWidget(calculateHash_button)
    vbox.addWidget(resultTextEdit)
    window.setLayout(vbox)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
