import time
import random
import jsonrpclib

from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot


class ServerStatisticWorker(QtCore.QTimer):
    def __init__(self, parent, settings, serverStatistic):
        QtCore.QTimer.__init__(self, parent)

        self.__serverHost = settings['connection']['host']
        self.__serverPort = settings['connection']['port']
        self.__serverUser = settings['connection']['user']
        self.__serverPassword = settings['connection']['password']

        self.__updatePeriod = settings['updatePeriod']

        self.__serverStatistic = serverStatistic

        self.__keys = []
        for val in settings['view']['values']:
            self.__keys.append(val['key'])

        self.setInterval(self.__updatePeriod * 1000)
        self.connect(self, QtCore.SIGNAL('timeout()'), self, QtCore.SLOT('run()'))

    def start(self):
        QtCore.QTimer.singleShot(100, self, QtCore.SLOT('init()'));

    def __getStatistic(self, level):
        server = jsonrpclib.Server('http://{0}:{1}'.format(self.__serverHost, self.__serverPort), user=self.__serverUser, password=self.__serverPassword)
        return server.server_get_statistic(level)

    @pyqtSlot()
    def init(self):
        try:
            res = self.__getStatistic('global')
            self.__serverStatistic.setExts(**res)
            self.run()
            QtCore.QTimer.start(self)
        except Exception, exc:
            QtCore.QTimer.singleShot(500, self, QtCore.SLOT('init()'));

    @pyqtSlot()
    def run(self):
        try:
            res = self.__getStatistic('local')
            self.__serverStatistic.updateData(**res)
        except Exception, exc:
            pass
