import datetime
import os
import struct
import sys
from base64 import b64decode

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


class Crypto:
    
    def __init__(self):
        self.path_privat_key = "priv_key"
        self.path_public_keys = "public_keys"
        self.RSA_size = 1024
        self.RSA_key = None
        self.session_key = None
        
        self.CONN_RSA_KEY = None
        
        self.progress = 0
        self.is_cryptoNow = False
        
    def create_ff(self, path, file_name="", mod='w') -> str:
        """Check if the full path to the file exists 
        and creates a path if it does not exist. Return full path.
        """
        full_path = os.path.join(path, file_name)
        if not os.path.exists(full_path):
            if not os.path.exists(path):
                os.makedirs(path)
            if file_name != "":
                with open(full_path, mod):
                    pass
            
        return full_path
    
    def set_path(self, path) -> None:
        self.path_privat_key = path
        
    def set_size_rsa(self, size) -> None:
        self.RSA_size = size
    
    def init_rsa_key(self, name) -> None:
        """Initialization RSA keys"""
        PRIV_PKEY_NAME = f"priv_key_{name}.pem"
        SIZE_RSA_KEY = self.RSA_size
        
        priv_path = self.path_privat_key
        
        if not os.path.exists(priv_path):
            os.makedirs(priv_path)
            
        full_priv_path = os.path.join(priv_path, PRIV_PKEY_NAME) 
        if not os.path.exists(full_priv_path):
            
            keyPair = RSA.generate(SIZE_RSA_KEY)
            privKeyPEM = keyPair.exportKey()
                
            with open(full_priv_path, "wb") as f:
                f.write(privKeyPEM)
                
            self.RSA_key = keyPair
        else:
            
            with open(full_priv_path, "rb") as f:
                priv_key = RSA.import_key(f.read())
            self.RSA_key = priv_key
            
        print("RSA key was generated")
        
    def save_conn_RSAkey(self, public_key) -> None:
        if not os.path.exists(self.path_public_keys):
            name_file = f"public_key.pem"
            full_priv_path = self.create_ff(self.path_public_keys, name_file, 'a+')
            with open(full_priv_path, "wb") as f:
                f.write(public_key)
        
    def set_session_key(self, key):
        self.session_key = key
        
    def get_public_key(self):
        return self.RSA_key.publickey().exportKey('PEM')
    
    def import_pub_key(self, key):
        return RSA.import_key(key)
    
    def encryptRSA(self, data, pub_key):
        cipher = PKCS1_OAEP.new(pub_key)
        return cipher.encrypt(data)
    
    def decryptRSA(self, data):
        decryptor = PKCS1_OAEP.new(self.RSA_key)
        return decryptor.decrypt(data)
            
    def generate_session_key(self, size=16) -> bytes:
        self.session_key = get_random_bytes(size)
        return self.session_key
    
    def get_random_bytes(self, size):
        return get_random_bytes(size)
    
    def encrypt_data(self, data:bytes, mod_AES=AES.MODE_ECB):
        key = self.session_key
        SIZE_BLOCK = 16
        
        if mod_AES == AES.MODE_ECB:
            encryptor = AES.new(key, mod_AES)
        else:
            iv = get_random_bytes(SIZE_BLOCK)
            encryptor = AES.new(key, mod_AES, iv)    
        
        modSize = len(data)%SIZE_BLOCK
        dif = SIZE_BLOCK - modSize
        data += (' '*dif).encode("utf-8")
        
        enc_data = encryptor.encrypt(data)
        
        if mod_AES == AES.MODE_ECB:
            enc_data = bytes([mod_AES]) + bytes([dif]) + enc_data
        else:
            enc_data = bytes([mod_AES]) + bytes([dif]) + iv + enc_data        

        return enc_data

    def decrypt_data(self, data: bytes):
        key = self.session_key
        iv = None
        SIZE_BLOCK = 16
        
        mod_AES = int.from_bytes(data[:1], "little")
        
        dif = int.from_bytes(data[1:2], "little")
        
        if mod_AES == AES.MODE_ECB:
            encryptor = AES.new(key, mod_AES)
            data = data[2:]
        else:
            iv = data[2:18]
            encryptor = AES.new(key, mod_AES, iv)
            data = data[18:]        
        
        dec_data = encryptor.decrypt(data)
        dec_data = dec_data[:-dif]
        
        return dec_data
    
    
    
    def encrypt_file(self, in_filename, out_filename=None, mod_AES=AES.MODE_ECB, chunksize=1024*1024) -> str:
        key = self.session_key
        SIZE_BLOCK = 16
        if not out_filename:
            out_filename = in_filename + '.enc'
            
        if mod_AES == AES.MODE_ECB:
            encryptor = AES.new(key, mod_AES)
        else:
            iv = get_random_bytes(SIZE_BLOCK)
            encryptor = AES.new(key, mod_AES, iv)
            
        filesize = os.path.getsize(in_filename)
        progress_now = 0
        self.is_cryptoNow = True

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                #outfile.write(struct.pack('<Q', filesize))
                outfile.write(bytes([mod_AES]))
                if mod_AES is not AES.MODE_ECB:
                    outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    progress_now += chunksize
                    self.progress = progress_now/filesize * 100
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += (' ' * (16 - len(chunk) % 16)).encode("utf-8")

                    outfile.write(encryptor.encrypt(chunk))
                    
        self.is_cryptoNow = False
        return out_filename
                    
                    
    def decrypt_file(self, in_filename, size, out_filename=None, chunksize=1024*1024) -> str:
        key = self.session_key
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]        
        self.is_cryptoNow = True
        with open(in_filename, 'rb') as infile:
            #origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            origsize = size
            mod = int.from_bytes(infile.read(1), "little")
            
            if mod == AES.MODE_ECB:
                decryptor = AES.new(key, mod)
            else:
                iv = infile.read(16)
                decryptor = AES.new(key, mod, iv)
            progress_now = 0
            with open(out_filename, 'wb') as outfile:
                while True:                    
                    chunk = infile.read(chunksize)
                    progress_now += chunksize
                    self.progress = progress_now/origsize * 100
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)
        self.is_cryptoNow = False
        return out_filename
