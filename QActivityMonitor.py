import custom_types as t

from datetime import datetime

from PyQt5.QtCore import QObject, QTime
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QTextCursor


class QActivityMonitor(QObject):
    def __init__(self, textEdit: QTextEdit, parent=None) -> None:
        super(QObject, self).__init__(parent)
        self.__textEdit = textEdit
        self.autoscroll = True

    def display(self, msg: str, type: t.Message):
        time = datetime.now().strftime("%H:%M:%S")
        msg = f"({time}) {type.name}: {msg}"

        self.__textEdit.append(msg)
        if (self.autoscroll):
            cursor = self.__textEdit.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.__textEdit.setTextCursor(cursor)

    def clear(self):
        self.__textEdit.clear()
