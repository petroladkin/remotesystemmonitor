import numpy
import pyqtgraph

from PyQt4 import QtGui, QtCore


class ParamInfoString(QtGui.QLabel):
    def __init__(self, parrent, settings, **kargs):
        QtGui.QLabel.__init__(self, settings['name'], parrent)

        self.__sufix = settings['name']
        self.__prefix = settings['valueType']
        self.__averageValue = settings['averageValue']
        self.__maxValue = settings['maxValue']
        self.__redLimit = None
        if 'redLimit' in settings.keys():
            self.__redLimit = settings['redLimit']
        self.__yellowLimit = None
        if 'yellowLimit' in settings.keys():
            self.__yellowLimit = settings['yellowLimit']
        self.__isCheckingValueLimit = (self.__redLimit != None) or (self.__yellowLimit != None)

        self.setAutoFillBackground(True)

        # self.__palette = QtGui.QPalette()
        # self.__normalBackgroud = self.__palette.color(QtGui.QPalette.Background)
        # self.__normalForeground = self.__palette.color(QtGui.QPalette.Foreground)

        # palette.setColor(QtGui.QPalette.Background, QtCore.Qt.red)
        # palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.green)
        # self.setPalette(palette)
        # # self.update()

        # palette = QtGui.QPalette()
        # palette.setColor(QtGui.QPalette.Background, QtCore.Qt.yellow)
        # palette.setColor(QtGui.QPalette.Foreground, QtCore.Qt.black)
        # self.setPalette(palette)
        # # self.update()

    def getType(self):
        return 'string'

    def setExt(self, ext):
        self.__sufix = '{0} ({1})'.format(self.__sufix, ext)
        self.setText(self.__sufix)

    def updateValues(self, values):
        if self.__averageValue:
            value = sum(values) / len(values)
        elif len(values) == 1:
            value = str(values[0])
        else:
            for val in values:
                value = '{0}{1}{2}'.format(value, '' if value == None else '/', val)
        self.setText('{0}: {1} {2}'.format(self.__sufix, value, self.__prefix))
        if self.__isCheckingValueLimit: self.__checkValueLimit(values)

    def __checkValueLimit(self, values):
        red = False
        yellow = False
        for val in values:
            yellow = self.__yellowLimit != None and self.__yellowLimit < val
            red = self.__yellowLimit != None and self.__yellowLimit < val
        if red:
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Background, QtCore.Qt.red)
            self.setPalette(palette)
        elif yellow:
            palette = QtGui.QPalette()
            palette.setColor(QtGui.QPalette.Background, QtCore.Qt.yellow)
            self.setPalette(palette)


class LogTimeDataAxis(pyqtgraph.AxisItem):
    def __init__(self, AxisRatio, AxisLenght):
        pyqtgraph.AxisItem.__init__(self, 'bottom')
        self._axisRatio = AxisRatio
        self._axisLenght = AxisLenght

    def tickStrings(self, value, scale, spacing):
        ret = []
        for x in value: ret.append(self.__time2humman((x - self._axisLenght) * self._axisRatio))
        return ret

    def __time2humman(self, t):
        t = abs(t)
        if t > 59:
            m, s = divmod(t, 60)
            if m > 59:
                h, m = divmod(m, 60)
                return '-{0:01}:{1:02}:{2:02}'.format(int(round(h)), int(round(m)), int(round(s)))
            else:
                return '-0:{0:02}:{1:02}'.format(int(round(m)), int(round(s)))     
        else:
            return '{0}0:00:{1:02}'.format('' if t == 0.0 else '-', int(round(t)))


class ParamInfoGraph(pyqtgraph.PlotWidget):
    def __init__(self, parrent, settings, **kargs):
        pyqtgraph.PlotWidget.__init__(self, parrent, axisItems={'bottom': LogTimeDataAxis(settings['updateCoef'], settings['buffer'])})

        self.__pli = self.getPlotItem()

        self.__pens = kargs['pens']
        self.__updatePeriod = kargs['updatePeriod']
        self.__title = settings['name']
        self.__bufferLenght = settings['buffer']
        self.__updateCoef = settings['updateCoef']
        self.__averageValue = settings['averageValue']
        self.__valueType = settings['valueType']

        self.__skipCount = self.__updateCoef + 1

        self.__pli.setTitle(self.__title)
        self.__pli.setLabel('left', self.__valueType)
        self.__pli.setLabel('bottom', 'Time (' + str() + ' s)')
        self.__pli.setYRange(0, settings['maxValue'])
        if settings['maxValue'] == 1:
            self.__pli.enableAutoScale()
        self.__pli.setXRange(0, self.__bufferLenght)

        self.__buffers = [list(numpy.zeros(self.__bufferLenght))]
        self.__pli.plot(self.__buffers[0], pen=self.__pens[0], clear=True)
        self.__setCurrentValue([0.0])

    def getType(self):
        return 'graph'

    def setExt(self, ext):
        self.__title = self.__title + ' (' + ext + ')'
        self.__pli.setTitle(self.__title)

    def updateValues(self, values):
        self.__setCurrentValue(values)
        self.__skipCount = self.__skipCount + 1
        if self.__skipCount > self.__updateCoef:
            self.__skipCount = 0
            if len(values) != len(self.__buffers):
                if len(values) < len(self.__buffers):
                    for i in range(len(self.__buffers) - len(values)):
                        self.__buffers.pop()
                else:
                    for i in range(len(values) - len(self.__buffers)):
                        self.__buffers.append(list(numpy.zeros(self.__bufferLenght)))
            for i in range(len(values)):
                self.__updateArray(self.__buffers[i], values[i])
                self.__pli.plot(self.__buffers[i], pen=self.__pens[i], clear=(i == 0))

    def __setCurrentValue(self, values):
        if self.__averageValue:
            value = sum(values) / len(values)
        elif len(values) == 1:
            value = str(values[0])
        else:
            value = str(values[0])
            for i in range(1, len(values)):
                value += '/' + str(values[i])
        self.__pli.setLabel('right', '{0} {1}'.format(value, self.__valueType))

    def __updateArray(self, arr, value):
        arr.pop(0)
        arr.append(value)


def ParamInfo(parrent, settings, **kargs):
    if settings['type'] == 'graph':
        return ParamInfoGraph(parrent, settings, **kargs)
    else:
        return ParamInfoString(parrent, settings, **kargs)
