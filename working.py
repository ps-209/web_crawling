from typing import Optional
from PySide6.QtCore import *

import time

class Work(QThread):
    progress_updated = Signal(int)

    def __init__(self, num):
        super().__init__()
        self.num = num

    def run(self):
        for i in range(1,self.num+1):
            print(i)
            self.progress_updated.emit(i)
            self.sleep(1)
        self.quit()
        self.wait()
