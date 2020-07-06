import sys
import os
import time
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide2.QtCore import QFile, QThread
from interface.ui_mainwindow import Ui_MainWindow
from communicator import Communicator

from Crypto.Cipher import AES

import threading

class UpdateInfo(QThread):
    def __init__(self, communicator):
        QThread.__init__(self)
        self.comm = communicator
        
    def __del__(self):
        self.wait()
        
    def _check_new_messages(self):
        if self.comm.new_content:
            list_content = self.comm.get_text_toshow()
            str_content = '\n'.join(i for i in list_content)
            self.ui.plainTextEdit.appendPlainText(str_content)
        
    def run(self):
        while True:
            self._check_new_messages()
        
        

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_Connect.clicked.connect(self.connect)
        self.ui.pushButton_StartListen.clicked.connect(self.init_communicator)
        self.communicator = None
        self.stop = False
        self.thread_update = threading.Thread(target=self.update)
        
        self.connect_updated = False
        self.if_send_file = False
        self.filename = None
        
        self.ui.pushButton_SendMessage.clicked.connect(self.send_message)
        self.ui.pushButton_BrowsFile.clicked.connect(self.brows_file)
        
        self.ui.progressBar.hide()
        self.ui.label.hide()
    
    def init_communicator(self):        
        port = self.ui.lineEdit_2.text()
        self.communicator = Communicator(int(port))
        self.communicator.start_listen()
        self.communicator.generateRSAkey(port)
        self.ui.lineEdit_3.setText(self.communicator.IP)
        self.ui.lineEdit_3.setReadOnly(True)
        
        self.thread_update.start()
        
    def connect(self):
        ip, port = self.ui.lineEdit.text().split(':')
        self.communicator.connect(ip, int(port))
    
    def update_conn_info(self):
        if not self.connect_updated:
            if self.communicator.connecting:
                conn_addr, conn_port = self.communicator.connecting_addr
                self.ui.lineEdit.setText(conn_addr + " " + str(conn_port))
                self.connect_updated = True
            else:
                self.connect_updated = False
                
    def add_message(self, message):
        self.ui.plainTextEdit.appendPlainText(message)
    
    def update(self):
        while not self.stop:
            
            if (self.if_send_file or 
                self.communicator.is_progressNow or 
                self.communicator.crypto.is_cryptoNow):
                self.ui.progressBar.show()
                self.ui.label.show()
                
                if self.communicator.is_progressNow:
                    self.ui.progressBar.setValue(self.communicator.procces_SRCD)
                
                if self.communicator.crypto.is_cryptoNow:
                    self.ui.progressBar.setValue(self.communicator.crypto.progress)
                
                if self.communicator.procces_SRCD >= 100.0:
                    self.filename = None
                    self.if_send_file = False
            else:
                self.ui.progressBar.setValue(0)
                self.ui.progressBar.hide()
                self.ui.label.hide()
                
            self.update_conn_info()
        
    def closeEvent(self, event):
        if self.communicator is not None:
            self.communicator.stop_listen = True
            self.communicator.socket_recv.close()
        self.stop = True
        
    def send_message(self):
        mod = None
        if self.ui.radioButton_ECB.isChecked():
            mod = AES.MODE_ECB
        elif self.ui.radioButton_CBC.isChecked():
            mod = AES.MODE_CBC
        elif self.ui.radioButton_CFB.isChecked():
            mod = AES.MODE_CFB
        elif self.ui.radioButton_OFB.isChecked():
            mod = AES.MODE_OFB
        
        content = self.ui.plainTextEdit_Message.toPlainText().strip(" ")
        if content is not None and len(content) > 0:
            self.ui.plainTextEdit_Message.clear()            
            self.communicator.send_text(content, mod)            
            self.ui.plainTextEdit.appendPlainText("me:\t" + content)
            
        if self.if_send_file:            
            self.communicator.send_file(self.filename, mod)
        
    def brows_file(self):
        fname, _ = QFileDialog.getOpenFileName(self)
        if fname != "":
            filename = os.path.split(fname)[1]
            self.filename = fname
            self.ui.label_sendFile.setText("Send file: " + filename)
            self.if_send_file = True
        else:
            self.filename = None
            self.ui.label_sendFile.setText("Send file: ")
            self.if_send_file = False
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())