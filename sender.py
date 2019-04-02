"""
  ____                              _                   _ _
 / ___|_ __ _   _ _ __   ___     __| | ___  ___   _ __ (_) | ____ _
| |  _| '__| | | | '_ \ / _ \   / _` |/ _ \/ __| | '_ \| | |/ / _` |
| |_| | |  | |_| | |_) | (_) | | (_| | (_) \__ \ | |_) | |   < (_| |
 \____|_|   \__,_| .__/ \___/   \__,_|\___/|___/ | .__/|_|_|\_\__,_|
                 |_|                             |_|
"""

#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""

from socket import AF_INET, socket, SOCK_STREAM
from tkinter.filedialog import askopenfilename
from tkinter import *
import time



class Sender:

    def __init__(self, t):
        self.t = t

    def set_sleep_time(self, sleep):
        self.set_sleep_time = sleep

    def set_ip(self, ip):
        self.ip = ip
    
    def set_port(self, port):
        self.port = port
    
    def set_file(self):
        self.filename = askopenfilename()
        self.buffer = BUFFER
        sendFileButton.place(x=20, y=130)
    
    def sendFile(self):
        sock = socket(AF_INET, SOCK_STREAM)
        
        sock.connect((self.ip, self.port))
        file = open(self.filename, "rb")
        data = file.read()

        n = int(len(data)/self.buffer)

        numberPacketsInBytes = n.to_bytes(4, 'big')

        # i = 0
        # progressBar = self.t.progressBar(self.t, variable=i, maximum=numberPacketsInBytes)

        b = numberPacketsInBytes + self.getOnlyFileName().encode()
        # b = b + 
        print("B: " + str(b))
        print("FileName: " + self.getOnlyFileName())
        sock.sendto(b, (self.ip,self.port))
        for i in range(n+1):
            #Formando pacote de dados
            packet = data[i*self.buffer:(i+1)*self.buffer]
            
            sock.sendto(packet,(self.ip,self.port))
            #Tempo de espera de chegada do pacote
            # time.sleep(SLEEP_TIME)
                
        print("Fim do envio")

        file.close()
        sock.close()

    def getOnlyFileName(self):
        size = len(self.filename)
        i = size - 1
        while i > 0:
            if self.filename[i] == '/':
                newString = self.filename[i+1:size]
                newString = newString + '@'
                return newString
            i = i - 1
        return ''

    def partOfData(self, data, i):
        return (data[(i*self.buffer):self.buffer*(i+1)])

    def setIpButton(self):
        global e1
        global e2
        self.ip = e1.get()
        self.port = int(e2.get())
        e1.destroy()
        e2.destroy()
        setIpButton1.destroy()
        # print("FUNCIONOU")

def close():
    window.quit()


BUFFER = 20
SLEEP_TIME = 0.02
IP = "127.0.0.1"
PORT = 6061


window = Tk()

sender = Sender(window)
sender.set_ip(IP)
sender.set_port(PORT)
sender.set_sleep_time(SLEEP_TIME)

window.title("Troca de arquivos")
window.geometry("300x300")
selectFileButton = Button(window, text="Selecionar Arquivo", command=sender.set_file)
sendFileButton = Button(window, text="Enviar Arquivo", command=sender.sendFile)
closeButton = Button(window, text="Fechar", command=close)
#ENTRAD DO IP
e1 = Entry(window)
e2 = Entry(window)

e1.place(x=20, y=20)
e2.place(x=20, y=40)

e1.insert(END, IP)
e2.insert(END, str(PORT))
# e1.pack()
# e2.pack()

setIpButton1 = Button(window, text="Configurar conexao", command=sender.setIpButton)

e1.focus_set()


setIpButton1.place(x=20,y=60)
selectFileButton.place(x=20, y=100)
closeButton.place(x=20, y=200)

window.mainloop()