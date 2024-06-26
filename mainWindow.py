import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt5.QtCore import QDir
import hashlib

def selectDirectory(directoryLineEdit):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    if dialog.exec():
        directoryLineEdit.setText(dialog.selectedFiles()[0])

def calculateHash(directoryLineEdit, resultTextEdit, folderNameLineEdit, generalHashLineEdit):
    directory = str(Path(directoryLineEdit.text()).resolve())
    try:
        fileInfo = hashAllFiles(directory)
        resultTextEdit.clear()
        for file_name, info in fileInfo.items():
            resultTextEdit.append(f"Название: {file_name}\nРазмер: {info['size']} Байт\nХэш: {info['hash']}\n")
        
        generalHash = hashlib.md5()
        for file_name, info in sorted(fileInfo.items()):
            generalHash.update(file_name.encode('utf-8'))
            generalHash.update(str(info['size']).encode('utf-8'))
            generalHash.update(info['hash'].encode('utf-8'))
        
        folderNameLineEdit.setText(Path(directory).name)
        generalHashLineEdit.setText(generalHash.hexdigest())
    except Exception as e:
        print(f"Error calculating hash: {e}")

def hashAllFiles(directory):
    fileInfo = {}
    for path in Path(directory).rglob('*'):
        if path.is_file():
            hash_md5 = hashlib.md5()
            file_size = path.stat().st_size
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            fileInfo[path.name] = {
                'size': file_size,
                'hash': hash_md5.hexdigest()
            }
    return fileInfo

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 800, 400)
    window.setWindowTitle("Calculate MD5 Hash")

    directoryLineEdit = QLineEdit()
    selectDirectoryButton = QPushButton("Выберите директорию")
    calculateHashButton = QPushButton("Рассчитать хэш")
    resultTextEdit = QTextEdit()
    folderNameLineEdit = QLineEdit()
    generalHashLineEdit = QLineEdit()

    selectDirectoryButton.clicked.connect(lambda: selectDirectory(directoryLineEdit))
    calculateHashButton.clicked.connect(lambda: calculateHash(directoryLineEdit, resultTextEdit, folderNameLineEdit, generalHashLineEdit))

    vbox = QVBoxLayout()
    vbox.addWidget(directoryLineEdit)
    vbox.addWidget(selectDirectoryButton)
    vbox.addWidget(calculateHashButton)
    vbox.addWidget(resultTextEdit)

    hbox = QHBoxLayout()
    hbox.addWidget(QLineEdit("Папка:"))
    hbox.addWidget(folderNameLineEdit)
    hbox.addWidget(QLineEdit("Общий хэш:"))
    hbox.addWidget(generalHashLineEdit)

    vbox.addLayout(hbox)
    window.setLayout(vbox)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
