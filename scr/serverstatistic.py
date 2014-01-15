import numpy
import pyqtgraph

from traficlight import TraficLight
from paraminfo import ParamInfo

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot


class ServerStatistic(QtGui.QFrame):
    def __init__(self, parent, settings):
        QtGui.QFrame.__init__(self, parent)

        # base configure
        self.__updatePeriod = settings['updatePeriod']

        # root frame
        self.setFrameStyle(QtGui.QFrame.StyledPanel)
        hboxRoot = QtGui.QHBoxLayout(self)

        # icon frame
        vboxIcon = QtGui.QVBoxLayout()
        hboxRoot.addLayout(vboxIcon, 0)

        serverName = QtGui.QLabel(settings['name'], self)
        serverName.setMinimumWidth(140)
        vboxIcon.addWidget(serverName, 0, QtCore.Qt.AlignHCenter)

        self.__traficLight = TraficLight(self)
        self.__traficLight.setLightColor(0)
        vboxIcon.addWidget(self.__traficLight, 1, QtCore.Qt.AlignHCenter)

        vboxIcon.addStretch(1)

        # info frame
        vboxGrapth = QtGui.QVBoxLayout()
        hboxRoot.addLayout(vboxGrapth, 1)

        # info/status
        hboxServerInfo = QtGui.QHBoxLayout()
        vboxGrapth.addLayout(hboxServerInfo)

        self.__serverInfo = QtGui.QLabel('{0}:{1}'.format(settings['connection']['host'], settings['connection']['port']), self)
        hboxServerInfo.addWidget(self.__serverInfo, 0, QtCore.Qt.AlignLeft)

        self.__serverStatus = QtGui.QLabel('', self)
        hboxServerInfo.addWidget(self.__serverStatus, 0, QtCore.Qt.AlignRight)

        # params info
        self.__pens = [(0,0,255), (0,255,0), (255,0,0), (255,0,255)]

        self.__keys = []
        self.__values = {}
        for val in settings['view']['values']:
            self.__keys.append(val['key'])
            self.__values[val['key']] = ParamInfo(self, val, pens=self.__pens, updatePeriod=self.__updatePeriod)

        # add param to panel
        stringCout = 0
        graphCount = 0
        for val in self.__values.values():
            if val.getType() == 'graph':
                graphCount += 1
            else:
                stringCout += 1

        # param layouts
        if stringCout > 0:
            hboxStringInfo = QtGui.QHBoxLayout()
            if settings['view']['stringInfoPosition'] == 'top':
                vboxGrapth.addLayout(hboxStringInfo)
        if graphCount > 0:
            if settings['view']['graphInfoType'] == 'horizontal':
                boxGrapthInfo = QtGui.QHBoxLayout()
                vboxGrapth.addLayout(boxGrapthInfo, 1)
            elif settings['view']['graphInfoType'] == 'vertical':
                boxGrapthInfo = QtGui.QVBoxLayout()
                vboxGrapth.addLayout(boxGrapthInfo, 1)
            else:
                boxGrapthInfo = QtGui.QGridLayout()
                vboxGrapth.addLayout(boxGrapthInfo, 1)
        if stringCout > 0:
            if settings['view']['stringInfoPosition'] == 'bottom':
                vboxGrapth.addLayout(hboxStringInfo)

        # add param to layouts
        gridIndex = 0
        for val in self.__values.values():
            if val.getType() == 'graph':
                if settings['view']['graphInfoType'] == 'grid':
                    y, x = divmod(gridIndex, 2)
                    boxGrapthInfo.addWidget(val, x, y)
                    gridIndex += 1
                else:
                    boxGrapthInfo.addWidget(val)
            else:
                hboxStringInfo.addWidget(val)

        self.__yellowTimer = QtCore.QTimer(self)
        self.__yellowTimer.setInterval(self.__updatePeriod * 1000 * 2)
        self.connect(self.__yellowTimer, QtCore.SIGNAL('timeout()'), self, QtCore.SLOT('yellowAlarm()'))

        self.__redTimer = QtCore.QTimer(self)
        self.__redTimer.setInterval(self.__updatePeriod * 1000 * 5)
        self.connect(self.__redTimer, QtCore.SIGNAL('timeout()'), self, QtCore.SLOT('redAlarm()'))

    def setExts(self, **kargs):
        self.__traficLight.setLightColor(1)
        for key in self.__keys:
            name = '{0}_ext_name'.format(key)
            if name in kargs.keys():
                self.__values[key].setExt(kargs[name])

    def updateData(self, **kargs):
        self.__yellowTimer.stop()
        self.__yellowTimer.start()

        self.__redTimer.stop()
        self.__redTimer.start()

        self.__traficLight.setLightColor(2)

        for key in self.__keys:
            if key in kargs.keys():
                self.__values[key].updateValues(kargs[key])

        val = ''
        if 'server_date' in kargs.keys():
            val = '{0}Server date: {1}'.format(val, kargs['server_date'])
        if 'server_uptime' in kargs.keys():
            val = '{0}{1}server uptime: {2}'.format(val, '' if len(val) == 0 else '  ', kargs['server_uptime'])
        self.__serverStatus.setText(val)

    @pyqtSlot()
    def yellowAlarm(self):
        self.__yellowTimer.stop()
        self.__traficLight.setLightColor(1)

    @pyqtSlot()
    def redAlarm(self):
        self.__redTimer.stop()
        self.__traficLight.setLightColor(0)

