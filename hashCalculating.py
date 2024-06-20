import os
from tkinter import Tk, filedialog
import hashlib
import binascii
import json

def chooseDirectory():
    root = Tk()
    root.withdraw()
    
    directory = filedialog.askdirectory()
    
    return directory

directory = chooseDirectory()

def calculateHash(filePath):
    with open(filePath, 'rb') as file:
        hash_md5=hashlib.md5()
        hash_md5.update(file.read()) 
        return hash_md5.hexdigest()

def hashAllFiles(directory):
    writeFile=open(directory+"/hashes.json", "w")
    print(type(writeFile))
    data = ''
    for root, directories, files in os.walk(directory):
        for fileName in files:
            filePath = os.path.join(root, fileName)
            hashValue = calculateHash(filePath)
            data += f'{fileName}:{hashValue}\n'
    json.dump(data, writeFile)
    return(data)

if __name__ == "__main__":
    print(hashAllFiles(directory))
