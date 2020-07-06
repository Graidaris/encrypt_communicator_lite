import socket
import pickle
import os
import threading
from cryptography import Crypto
import time

class Communicator:
    
    def __init__(self, port:int):
        self.HOST_NAME = socket.gethostname()
        self.IP = socket.gethostbyname(self.HOST_NAME)
        self.PORT = port
        self._stop = False
        
        self.stop_listen = False
        
        self.BUFFER_SIZE = 4096
        self.BUFFER_SIZE_FILE = 64000
        
        self.socket_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_recv.bind((self.IP, self.PORT))
        print(f"BIND: {(self.IP, self.PORT)}")
        
        self.lock = threading.Lock()
        self.connecting = False
        self.connecting_addr = None
        
        self.new_content = False
        
        self.crypto = Crypto()
        self.thread_listen = threading.Thread(target=self._listen)
        
        self.texttoshow = []
        
        self.procces_SRCD = 0
        self.is_progressNow = False
        
    def add_text_toshow(self, text):
        with self.lock:
            self.texttoshow.append(text)
            self.new_content = True
        
    def get_text_toshow(self):
        with self.lock:
            text = self.texttoshow.copy()
            self.texttoshow = []
            self.new_content = False
            return text
        
    def _generateRSAkey(self, name):
        self.add_text_toshow("Wait to RSA key")
        self.crypto.init_rsa_key(name)
        self.add_text_toshow("RSA key has been import")
        
    def generateRSAkey(self, name):
        threading._start_new_thread(self._generateRSAkey, (name, ))   
        
    def _rec_message(self, data):
        pass
    
    def _rec_file(self, conn, filename, size):
        FOLDER_SAVE_FILE = "Downloads"
        rand = self.crypto.get_random_bytes(100)
        if not os.path.exists(FOLDER_SAVE_FILE):
            os.makedirs(FOLDER_SAVE_FILE)
        
        path = os.path.join(FOLDER_SAVE_FILE, filename)
        
        conn.sendall(rand)
        
        progress_now = 0
        self.procces_SRCD = 0
        self.is_progressNow = True
        with open(path, "wb") as f:
            
            data = conn.recv(self.BUFFER_SIZE_FILE)
            while data:
                progress_now += self.BUFFER_SIZE_FILE
                self.procces_SRCD = progress_now/size * 100
                f.write(data)
                data = conn.recv(self.BUFFER_SIZE_FILE)
                
        self.procces_SRCD = 0
        self.is_progressNow = False
        self.crypto.decrypt_file(path, size)        
        os.remove(path)
        self.add_text_toshow(f"File {filename} has been receive")
        
    def _rec_connect(self, conn:socket, public_key, addr):
        self.crypto.save_conn_RSAkey(public_key)
        session_key = self.crypto.generate_session_key()
        public_key = self.crypto.import_pub_key(public_key)
        enc_session_key = self.crypto.encryptRSA(session_key, public_key)        
        conn.sendall(enc_session_key)
        
        self.connecting = True
        self.connecting_addr = addr
        time.sleep(2)
        self.add_text_toshow(f"{addr[0]}:{addr[1]} was connected")
        
        
    def _receive(self, conn:socket, addr:str):
        try:
            data = conn.recv(self.BUFFER_SIZE)
            if not self.connecting:
                info = pickle.loads(data)
                
                if info["TYPE"] == "CONNECT":
                    public_key = info["DATA"]
                    addr = (addr[0], info["LOCPORT"])
                    threading._start_new_thread(self._rec_connect, (conn,public_key,addr, ))
            else:
                dec_data = self.crypto.decrypt_data(data)
                info = pickle.loads(dec_data)
                
                if info["TYPE"] == "MESSAGE":
                    self.add_text_toshow(f"{addr[0]}: " + info["DATA"])
                elif info["TYPE"] == "FILE":
                    threading._start_new_thread(self._rec_file, (conn,info["NAME"],info["SIZE"], ))
            
        except OSError as e:
            pass
        
        
    def _listen(self):
        print()
        self.add_text_toshow("START LISTEN")
        while not self.stop_listen:
            try:
                conn, addr = self.socket_recv.accept()
                threading._start_new_thread(self._receive, (conn,addr,))
            except OSError as e:
                pass
    
    
    def _send_file(self, path, mod):
        BIG_FILE = 100.0 #MB
        FOLDER = "enc"
        
        if not os.path.exists(FOLDER):
            os.makedirs(FOLDER)
        
        filename = os.path.split(path)[1]
        filesize = os.path.getsize(path)
        path_to_enc_file = os.path.join(FOLDER, filename + ".enc")
        
        
        self.crypto.encrypt_file(path, path_to_enc_file, mod)
        
        d = {"TYPE":"FILE", "NAME":filename + ".enc", "SIZE":filesize}
        d_bytes = pickle.dumps(d)
        d_enc = self.crypto.encrypt_data(d_bytes)
        
        send_data_size = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
            ss.connect(self.connecting_addr)
            ss.sendall(d_enc)
            ss.recv(self.BUFFER_SIZE)
            self.is_progressNow = True
            with open(path_to_enc_file, "rb") as f:
                data = f.read(self.BUFFER_SIZE_FILE)
                while data:
                    send_data_size += self.BUFFER_SIZE_FILE
                    self.procces_SRCD = send_data_size/filesize * 100
                    ss.sendall(data)
                    data = f.read(self.BUFFER_SIZE_FILE)
            
            
        os.remove(path_to_enc_file)
        self.procces_SRCD = 0
        self.is_progressNow = False
        
        time.sleep(2)
        self.add_text_toshow(f"File {filename} has been send")
        
            
    def send_file(self, path, mod):
        threading._start_new_thread(self._send_file, (path,mod,))
        
    def _send_text(self, message, mod):    
        d = {"TYPE":"MESSAGE", "DATA":message}
        d_bytes = pickle.dumps(d)
        d_enc = self.crypto.encrypt_data(d_bytes, mod)
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
            ss.connect(self.connecting_addr)
            ss.sendall(d_enc)
    
    def send_text(self, message, mod):
        threading._start_new_thread(self._send_text, (message, mod, ))
        
    def start_listen(self):
        self.socket_recv.listen(1)
        self.thread_listen.start()
    
    def wait_RSA_key(self):
        while self.crypto.RSA_key is None:
            pass
    
    
    
    def _connect(self, addr:str, port:int):
        self.wait_RSA_key()
        
        RSA = self.crypto.get_public_key()
        d = {"TYPE":"CONNECT", "DATA":RSA, "LOCPORT":self.PORT}
        print(f"TRY CONNECT{(addr, port)}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss:
            ss.connect((addr, port))
            ss.sendall(pickle.dumps(d))
            
            enc_session_key = ss.recv(self.BUFFER_SIZE)
            dec_session_key = self.crypto.decryptRSA(enc_session_key)
            self.crypto.set_session_key(dec_session_key)
            
        self.connecting = True
        self.connecting_addr = (addr, port)
        
        self.add_text_toshow(f"{addr}:{port} was connected")
            # while not self._stop:
            #     ss.sendall(pickle.dumps(d))
            #     ss.settimeout(30)
            #     try:
            #         data = ss.recv(self.BUFFER_SIZE)
            #         self.is_connecting = True
            #     except OSError as e:
            #         self.is_connecting = False
    

        
    def connect(self, ip:str, port:int) -> None:
        threading._start_new_thread(self._connect, (ip, port,))  