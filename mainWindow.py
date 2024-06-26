import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QTextEdit, QHBoxLayout, QComboBox
from PyQt5.QtCore import QDir
import hashlib
import zlib

def selectDirectory(directoryLineEdit):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    if dialog.exec():
        directoryLineEdit.setText(dialog.selectedFiles()[0])

def calculateHash(directoryLineEdit, resultTextEdit, folderNameLineEdit, generalHashLineEdit, algorithmCombo):
    directory = str(Path(directoryLineEdit.text()).resolve())
    selectedAlgorithm = algorithmCombo.currentText()
    try:
        fileInfo = hashAllFiles(directory, selectedAlgorithm)
        resultTextEdit.clear()
        for filePath, info in fileInfo.items():
            resultTextEdit.append(f"Файл: {filePath}\nРазмер: {info['size']} байт\nХэш: {info['hash']}\n")
        
        generalHash = hashlib.md5()
        for filePath, info in sorted(fileInfo.items()):
            generalHash.update(filePath.encode('utf-8'))
            generalHash.update(str(info['size']).encode('utf-8'))
            generalHash.update(info['hash'].encode('utf-8'))
        
        folderNameLineEdit.setText(Path(directory).name)
        generalHashLineEdit.setText(generalHash.hexdigest())
    except Exception as e:
        print(f"Error calculating hash: {e}")

def hashAllFiles(directory, algorithm):
    fileInfo = {}
    for path in Path(directory).rglob('*'):
        if path.is_file():
            fileSize = path.stat().st_size
            relativePath = path.relative_to(directory)
            if algorithm == "CRC32":
                hashValue = calculateCrc32(path)
            elif algorithm == "SHA-256":
                hashValue = calculateSha256(path)
            else:
                hashValue = calculateMd5(path)
            fileInfo[str(relativePath)] = {
                'size': fileSize,
                'hash': hashValue
            }
    return fileInfo

def calculateCrc32(filePath):
    crc32 = 0
    with open(filePath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            crc32 = zlib.crc32(chunk, crc32)
    return format(crc32 & 0xFFFFFFFF, '08x')

def calculateMd5(filePath):
    hashMd5 = hashlib.md5()
    with open(filePath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashMd5.update(chunk)
    return hashMd5.hexdigest()

def calculateSha256(filePath):
    hashSha256 = hashlib.sha256()
    with open(filePath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hashSha256.update(chunk)
    return hashSha256.hexdigest()

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setGeometry(100, 100, 600, 400)
    window.setWindowTitle("Calculate Hash")

    directoryLineEdit = QLineEdit()
    selectDirectoryButton = QPushButton("Выберите директорию")
    calculateHashButton = QPushButton("Рассчитать хэш")
    resultTextEdit = QTextEdit()
    folderNameLineEdit = QLineEdit()
    generalHashLineEdit = QLineEdit()
    algorithmCombo = QComboBox()
    algorithmCombo.addItems(["MD5", "CRC32", "SHA-256"])

    selectDirectoryButton.clicked.connect(lambda: selectDirectory(directoryLineEdit))
    calculateHashButton.clicked.connect(lambda: calculateHash(directoryLineEdit, resultTextEdit, folderNameLineEdit, generalHashLineEdit, algorithmCombo))

    vbox = QVBoxLayout()
    vbox.addWidget(directoryLineEdit)
    vbox.addWidget(selectDirectoryButton)
    vbox.addWidget(algorithmCombo)
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
