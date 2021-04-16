from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
import sys, time, cv2


class Clicker_App(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('clicker.ui', self)

        self.thread = {}
        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)

    def start(self):
        self.thread[1] = ThreadClass(parent=None, index=1)
        self.thread[1].start()
        self.thread[1].any_signal.connect(self.my_function)
        self.btn_start.setEnabled(False)

    def stop(self):
        self.thread[1].stop()
        self.btn_start.setEnabled(True)

    def my_function(self, counter):
        cnt = counter
        index = self.sender().index
        if index == 1:
            self.progressBar.setValue(cnt)


class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True

    def run(self):
        print('Starting thread...', self.index)
        mainWindow.ui.progressBar.setRange(0, int(mainWindow.ui.line_htm.text()))
        cnt = 0
        while (True):
            cnt += 1
            if cnt == int(mainWindow.ui.line_htm.text()): cnt = 0
            time.sleep(0.01)
            self.any_signal.emit(cnt)

    def stop(self):
        self.is_running = False
        print('Stopping thread...', self.index)
        self.terminate()


app = QtWidgets.QApplication(sys.argv)
mainWindow = Clicker_App()
mainWindow.show()
sys.exit(app.exec_())
