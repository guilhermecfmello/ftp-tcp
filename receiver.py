"""
  ____                              _                   _ _
 / ___|_ __ _   _ _ __   ___     __| | ___  ___   _ __ (_) | ____ _
| |  _| '__| | | | '_ \ / _ \   / _` |/ _ \/ __| | '_ \| | |/ / _` |
| |_| | |  | |_| | |_) | (_) | | (_| | (_) \__ \ | |_) | |   < (_| |
 \____|_|   \__,_| .__/ \___/   \__,_|\___/|___/ | .__/|_|_|\_\__,_|
                 |_|                             |_|
"""

"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from client import Client
from tkinter.filedialog import askdirectory
from tkinter import *
import struct


class Receiver():

        def __init__(self, ip, port, buffer):
                self.ip = ip
                self.port = port
                self.buffer = buffer
                self.dir = "./"

        def setDirectory(self):
                self.dir = askdirectory()
                if len(self.dir) > 0:
                        receiveButton.place(x=100,y=100)

        def receiveFile(self):
                sock = socket(AF_INET, SOCK_STREAM)
                sock.bind(('',self.port))
                sock.listen(1)
                client, client_addres = sock.accept()
                print("%s:%s conectado." % client_addres)

                data = client.recv(FIRST_BUFFER)
                
                # Pegando o numero de pacotes
                b = data[0:4]
                n = struct.unpack(">I", bytearray(b))[0]
                print("Tamanho do primeiro pacote: " + str(len(data)))
                fileNameT = data[4:len(data)].decode('iso-8859-1')
                j = 0
                for c in fileNameT:
                        if c == '@':
                                break
                        j = j + 1
                fileName = fileNameT[0:j]


                dataWrite = []
                for i in range(n+1):
                        
                        data = client.recvfrom(BUFFER)
                        print("Recebido: " + str(data) + "I: " + str(i))
                        dataWrite.append(data)

                print("Fim recebimento")


                print("Gravando em "+ self.dir + "\nnome: " + fileName)
                file = open(self.dir+"/"+fileName,"wb")
                finalData = bytes(0)
                for data in dataWrite:
                        finalData = finalData + data[0]
                
                file.write(finalData)

                file.close()
                sock.close()
        
        def setIpButton(self):
                global e1
                global e2
                # self.ip = e1.get()
                self.port = int(e2.get())
                # e1.destroy()
                e2.destroy()
                setIpButton1.destroy() 


def close():
        window.quit()


BUFFER = 200
FIRST_BUFFER = 60
IP = "127.0.0.1"
PORT = 6061

receiver = Receiver(IP, PORT, BUFFER)

window = Tk()
window.title("Receiver")
window.geometry("300x300")
selectFileButton = Button(window, text="Selecionar diretorio", command=receiver.setDirectory)
closeButton = Button(window, text="Fechar", command=close)
receiveButton = Button(window, text="Iniciar FTP", command=receiver.receiveFile)

# e1 = Entry(window)
e2 = Entry(window)

# e1.place(x=20, y=20)
e2.place(x=20, y=40)

setIpButton1 = Button(window, text="Configurar conexao", command=receiver.setIpButton)

# e1.insert(END, IP)
e2.insert(END, str(PORT))
e2.focus()

receiveButton.place(x=20, y=100)
setIpButton1.place(x=20, y=60)
# selectFileButton.place(x=20, y=100)
closeButton.place(x=100, y=200)



window.mainloop()




