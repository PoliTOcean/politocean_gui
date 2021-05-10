from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtQuick import QQuickView


class QLedIndicator(QWidget):
    def __init__(self, parent=None) -> None:
        QWidget.__init__(self, parent)

        self.viewer = QQuickView()
        self.viewer.setSource(QUrl("resources/LedIndicator.qml"))
        # self.viewer.rootContext().setContextProperty("LedIndicator", this)
        self.viewer.setResizeMode(QQuickView.SizeRootObjectToView)

        self.container = QWidget.createWindowContainer(self.viewer)
        self.container.setFocusPolicy(Qt.TabFocus)

        self.refreshPalette()

    def setTitle(self, title: str):
        self.viewer.rootObject().setProperty("indicatorTitle", title)

    def getIndicatorTitle(self):
        return self.viewer.rootObject().property("indicatorTitle")

    def setStatus(self, on: bool):
        self.viewer.rootObject().setProperty("isStatusOn", on)

    def getStatus(self):
        return self.viewer.rootObject().property("isStatusOn")

    def refreshPalette(self):
        p = self.palette()

        self.viewer.setColor(p.window().color())
        self.viewer.rootObject().setProperty("textColor", p.text().color())
        self.viewer.rootObject().setProperty("borderColor", p.text().color())

        backgroundColor = p.highlight().color()
        backgroundColor.setAlpha(90)
        self.viewer.rootObject().setProperty("backgroundColor", backgroundColor)

        titleColor = p.highlight().color()
        self.viewer.rootObject().setProperty("titleColor", titleColor)
