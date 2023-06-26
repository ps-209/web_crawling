import sys, asyncio
from typing import Optional
import PySide6.QtCore
import PySide6.QtGui
from PySide6.QtWidgets import *
from t1_dev_ui import Ui_MainWindow
from working import Work
from threading import Thread
import time

class Main_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_window,self).__init__()
        self.work_thread = None
        
        self.setupUi(self)
        self.photo_button.clicked.connect(self.img_search)
        self.text_button.clicked.connect(self.text)

    def SD(self): #버튼 비활성화
        self.search_button.setDisabled(True)
        self.text_button.setDisabled(True)
        self.photo_button.setDisabled(True)
        self.keyword_edit.setDisabled(True)
        self.directory_edit.setDisabled(True)

    def SE(self): #버튼 활성화
        self.search_button.setEnabled(True)
        self.text_button.setEnabled(True)
        self.photo_button.setEnabled(True)
        self.keyword_edit.setEnabled(True)
        self.directory_edit.setEnabled(True)
        
    def image(self): #이미지
        self.SD()
        thread = Thread(target=self.img_search)
        thread.start()

    def img_search(self):
        self.SD()
        num = 10
        self.progressBar.setMaximum(num)

        self.work_thread = Work(num)
        self.work_thread.progress_updated.connect(self.update_progress)
        self.work_thread.finished.connect(self.SE)
        self.work_thread.start()
    
    def update_progress(self,value):
        self.progressBar.setValue(value)

    def closeEvent(self, event):
        if self.work_thread and self.work_thread.isRunning():
            self.work_thread.quit()
            self.work_thread.wait()
        event.accept()

    def text(self): #텍스트
        self.SD()
        thread = Thread(target=self.txt_search)
        thread.start()
    
    def txt_search(self):
        
        self.SE()

    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Main_window()
    window.show()

    app.exec()

#새로운 스레드에서 함수를 시작하지 않으면 함수가 끝날 때까지 GUI가 멈추기 때문에
#thread 사용으로 새로운 함수를 시작하도록 함