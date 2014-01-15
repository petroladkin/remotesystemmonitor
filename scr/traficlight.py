from PyQt4 import QtSvg, QtCore


class TraficLight(QtSvg.QSvgWidget):
    def __init__(self, parent=None):
        QtSvg.QSvgWidget.__init__(self, parent)
        self.LightColorRed = 0
        self.LightColorYellow = 1
        self.LightColorGreen = 2
        self._ratio = 1.0
        self._minHeight = 60
        self._height = self._minHeight * 2
        self._maxHeight = self._minHeight * 4
        self._lightColor = -1
        self.updateSize()

    def resizeEvent(self, event):
        newWidth = self.widthForHeight(self.height())
        newPos = self.pos().x() + (self.width() - newWidth) / 2
        self.resize(newWidth, self.height())
        self.move(QtCore.QPoint(newPos, self.pos().y()))
        self.updateGeometry()

    def widthForHeight(self, h):
        return int(float(h) / self._ratio)

    def sizeHint(self):
        return QtCore.QSize(self.widthForHeight(self.height()), self.height())

    def setLightColor(self, lc):
        if lc == self._lightColor:
            return

        if lc == self.LightColorRed:
            fileName = "./res/svg/traffic_light_red.svg"
        elif lc == self.LightColorYellow:
            fileName = "./res/svg/traffic_light_yellow.svg"
        elif lc == self.LightColorGreen:
            fileName = "./res/svg/traffic_light_green.svg"
        else:
            return
        self._lightColor = lc

        svgr = QtSvg.QSvgRenderer(fileName)
        self._ratio = float(svgr.defaultSize().height()) / float(svgr.defaultSize().width())

        self.load(fileName)
        self.updateSize()

    def updateSize(self):
        self.setMinimumSize(self.widthForHeight(self._minHeight), self._minHeight)
        self.setMaximumSize(self.widthForHeight(self._maxHeight), self._maxHeight)
        self.updateGeometry()
