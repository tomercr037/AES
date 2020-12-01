from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time


class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        aes = self.encrypt(plaintext, self.key)
        with open(file_name + ".aes", 'wb') as fo:
            fo.write(aes)
        os.remove(file_name)

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

    def getAllFiles(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dirs = []
        for dirName, subdirList, fileList in os.walk(dir_path):
            for fname in fileList:
                if (fname != 'en.py' and fname != 'hola.txt.aes'):
                    dirs.append(dirName + "\\" + fname)
        return dirs

    def encrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.encrypt_file(file_name)

    def decrypt_all_files(self):
        dirs = self.getAllFiles()
        for file_name in dirs:
            self.decrypt_file(file_name)


key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
aes = Encryptor(key)
clear = lambda: os.system('cls')

if os.path.isfile('hola.txt.aes'):
    while True:
        password = str(input("Introdusca contrasena: "))
        aes.decrypt_file("hola.txt.aes")
        p = ''
        with open("hola.txt", "r") as f:
            p = f.readlines()
        if p[0] == password:
            aes.encrypt_file("hola.txt")
            break

    while True:
        clear()
        choice = int(input(
            "1. Presione '1' para cifrar el archivo.\n2. Presione '2' para decifrar el archivo.\n3. Presione '3' para cifrar todos los archivos en el directorio.\n4. Presione '4' para descifrar todos los archivos en el directorio.\n5. Presione '5' para salir.\n"))
        clear()
        if choice == 1:
            aes.encrypt_file(str(input("Ingrese el nombre del archivo para cifrar: ")))
        elif choice == 2:
            aes.decrypt_file(str(input("Ingrese el nombre del archivo para descifrar: ")))
        elif choice == 3:
            aes.encrypt_all_files()
        elif choice == 4:
            aes.decrypt_all_files()
        elif choice == 5:
            exit()
        else:
            print("Seleccione una opción válida!")

else:
    while True:
        clear()
        password = str(input("Ingrese una contraseña que se utilizará para el descifrado: "))
        repassword = str(input("Confirme contrasena: "))
        if password == repassword:
            break
        else:
            print("Las contraseñas no coinciden!")
    f = open("hola.txt", "w+")
    f.write(password)
    f.close()
    aes.encrypt_file("hola.txt")
    print("Reinicia el programa para completar la configuración")
    time.sleep(15)
