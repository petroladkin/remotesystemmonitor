import sys
import json

from PyQt4 import QtGui, QtCore, QtSvg
from PyQt4.QtCore import pyqtSlot

from serverstatistic import ServerStatistic
from serverstatisticworker import ServerStatisticWorker


class AppWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        all_settings = json.loads(open('./data/settings.json', 'r').read())

        vbox = QtGui.QVBoxLayout(self)

        self.__sstw = []
        for settings in all_settings:
            ss = ServerStatistic(self, settings)
            sstw = ServerStatisticWorker(self, settings, ss)
            sstw.start()
            self.__sstw.append(sstw)
            vbox.addWidget(ss, 1)

        statusbar = QtGui.QStatusBar(self)
        statusbar.showMessage('PhoneCrypt Monitor   created by Petro Ladkin   (c)   2014')
        vbox.addWidget(statusbar)

        quit = QtGui.QPushButton('Close', statusbar)
        self.connect(quit, QtCore.SIGNAL('clicked()'), self, QtCore.SLOT('quit()'))
        statusbar.addPermanentWidget(quit)

    @pyqtSlot()
    def quit(self):
        for th in self.__sstw:
            th.stop()
        self.close()


###############################################################################
#
# main
#
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    widget = AppWidget()
    if len(sys.argv) > 1 and sys.argv[1] == '--fullscreen':
        widget.showFullScreen()
    else:
        widget.show()

    sys.exit(app.exec_())
