import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt5.QtCore import QDir
import hashlib

def select_directory(directory_line_edit):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.DirectoryOnly)
    if dialog.exec():
        directory_line_edit.setText(dialog.selectedFiles()[0])

def calculate_hash(directory_line_edit, result_text_edit, folder_name_line_edit, general_hash_line_edit):
    directory = str(Path(directory_line_edit.text()).resolve())
    try:
        file_info = hash_all_files(directory)
        result_text_edit.clear()
        for file_name, info in file_info.items():
            result_text_edit.append(f"Название: {file_name}\nРазмер: {info['size']} Байт\nХэш: {info['hash']}\n")
        
        general_hash = hashlib.md5()
        for file_name, info in sorted(file_info.items()):
            general_hash.update(file_name.encode('utf-8'))
            general_hash.update(str(info['size']).encode('utf-8'))
            general_hash.update(info['hash'].encode('utf-8'))
        
        folder_name_line_edit.setText(Path(directory).name)
        general_hash_line_edit.setText(general_hash.hexdigest())
    except Exception as e:
        print(f"Error calculating hash: {e}")

def hash_all_files(directory):
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
    window.setGeometry(100, 100, 800, 400)
    window.setWindowTitle("Calculate MD5 Hash")

    directory_line_edit = QLineEdit()
    select_directory_button = QPushButton("Выберите директорию")
    calculate_hash_button = QPushButton("Рассчитать хэш")
    result_text_edit = QTextEdit()
    folder_name_line_edit = QLineEdit()
    general_hash_line_edit = QLineEdit()

    select_directory_button.clicked.connect(lambda: select_directory(directory_line_edit))
    calculate_hash_button.clicked.connect(lambda: calculate_hash(directory_line_edit, result_text_edit, folder_name_line_edit, general_hash_line_edit))

    vbox = QVBoxLayout()
    vbox.addWidget(directory_line_edit)
    vbox.addWidget(select_directory_button)
    vbox.addWidget(calculate_hash_button)
    vbox.addWidget(result_text_edit)

    hbox = QHBoxLayout()
    hbox.addWidget(QLineEdit("Папка:"))
    hbox.addWidget(folder_name_line_edit)
    hbox.addWidget(QLineEdit("Общий хэш:"))
    hbox.addWidget(general_hash_line_edit)

    vbox.addLayout(hbox)
    window.setLayout(vbox)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
