import threading, socket, CommandHandler
class CarSocket(threading.Thread):
    """description of class"""
    
    #def __init__(self,  parent=None ,sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
    #    threading.Thread.__init__(self)
        
    #    self.sock = sock
    #    if parent is None:
    #        raise SyntaxError("no Parent")
    #    self.parent = parent
    
    def __init__(self, parent=None):
        threading.Thread.__init__(self)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if parent is None:
            raise SyntaxError("no Parent")
        self.parent = parent
    def connect(self,host,port):
        self.sock.connect((host,port))

    def hostServerSocket(self, hostname = socket.gethostname, port =25566):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((hostname,port))
        serverSocket.listen(5)
        temp = serverSocket.accept()
        print(temp)
        
        self.sock = temp[0]


    def recive(self, MSGLEN = 3):
        MSGLEN = 3
        chunks = []
        recvd = []
        rec_bytes = 0
        while rec_bytes < MSGLEN:
            chunk = recb = self.sock.recv(min(MSGLEN - rec_bytes, 2048))
            if chunk ==b'':
                raise RuntimeError("socket is down")
            chunks.append(chunk)
            recvd.append(int(recb.decode(),10))

            rec_bytes = rec_bytes + len(chunk)

        return b''.join(chunks)

    def recivePack(self, MSGLEN = 14):
        rec_bytes = self.sock.recv(MSGLEN)
        if (rec_bytes ==b''):
            self.parent.dict=CommandHandler.blankDict()
            self.parent.stop()
            raise RuntimeError("socket is down")
        text = rec_bytes.decode()
        text.replace("\r\n","")
        pack = text.split(" ")
        #print(pack)
        packedInts = [int(pack[0]),int(pack[1]),int(pack[2])]
        return packedInts

    def sendPack(self,pack):
        text = str(pack[0])
        for i in range(1,3):
            text = text + " " + str(pack[i])
        text = text + "\r\n"
        sentBytes = self.sock.send(text.encode())
        return sentBytes

    def myrecive(self,MSGLEN = 3):
        chunks = []
        rec_bytes = 0
        while rec_bytes < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - rec_bytes, 2048))
            if chunk ==b'':
                raise RuntimeError("socket is down")
            chunks.append(chunk)
            rec_bytes = rec_bytes + len(chunk)
        return b''.join(chunks)
    
    def mysend(self, msg , MSGLEN =3):
        print(msg)
        print(msg[0].bit_length())  
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(str(msg[totalsent]).encode())
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent
    def send(self, msg = [], MSGLEN =None):
        for b in msg:
            sent = self.sock.send(msg[b])
            if sent == 0:
                raise RuntimeError("socket connection broken")

    def run(self):
        self.running = True
        while self.running:
            rb = self.recivePack()
            rd = CommandHandler.getAsDict(rb)
            print(rb)
            if CommandHandler.validDict(rd):
                self.parent.dict = rd
            else:
                self.parent.dict = CommandHandler.blankDict
                print("faulty Dict, replaced with blank")
    def dc(self):
        self.sock.send("d".encode())
        print("disconnected")
    def __del__(self):
        self.sock.send("d".encode())
        self.parent.dict = CommandHandler.blankDict
        print("disconnected")
