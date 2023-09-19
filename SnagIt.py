from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QBrush, QCursor, QBitmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget


class SnippingTool(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel('Screenshot will be displayed here')
        self.layout.addWidget(self.label)

        # self.snipBtn = QPushButton('Take Screenshot')
        # self.snipBtn.clicked.connect(self.startSnipping)
        # self.layout.addWidget(self.snipBtn)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def startSnipping(self):
        self.hide()
        # Add a delay to allow the user to move the cursor to the desired screen
        QTimer.singleShot(1000, self.openSnippingWindow)

    def openSnippingWindow(self):
        self.snippingWindow = SnippingWindow(self)

        # Get the screen number where the cursor is currently located
        desktop = QApplication.desktop()
        current_screen = desktop.screenNumber(QCursor.pos())

        # Get the geometry of the current screen
        rect = desktop.screenGeometry(current_screen)

        # Set the geometry of the snipping window to cover the current screen
        self.snippingWindow.setGeometry(rect)

        self.snippingWindow.showFullScreen()  # Use showFullScreen() to cover the entire screen
        self.snippingWindow.show()  # Use show() instead of showFullScreen()

    def displayScreenshot(self, pixmap):
        self.label.setPixmap(pixmap)
        self.show()
        self.parent().handle_screenshot(pixmap)  # Call the handle_screenshot method of the OCRApp class


class SnippingWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_screen = None
        self.start = None
        self.end = None

        self.setWindowTitle('Snipping Window')
        self.setWindowOpacity(0.3)
        # Set a custom crosshair cursor using a bitmap
        cursor_pixmap = QBitmap(16, 16)
        cursor_pixmap.clear()
        cursor_painter = QPainter(cursor_pixmap)
        cursor_painter.drawLine(0, 8, 15, 8)
        cursor_painter.drawLine(8, 0, 8, 15)
        cursor_painter.end()
        self.setCursor(QCursor(cursor_pixmap, 8, 8))

    def paintEvent(self, event):
        if self.start:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 1.5, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.red, Qt.DiagCrossPattern))
            painter.drawRect(QRect(self.start, self.end))

    def mousePressEvent(self, event):
        self.start = event.pos()
        self.end = self.start
        self.update()
        # Determine which screen the cursor is on
        desktop = QApplication.desktop()
        self.current_screen = desktop.screenNumber(event.globalPos())

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.close()

        x1 = min(self.start.x(), self.end.x())
        y1 = min(self.start.y(), self.end.y())
        x2 = max(self.start.x(), self.end.x())
        y2 = max(self.start.y(), self.end.y())

        screen = QApplication.screens()[self.current_screen]

        # Adjust the coordinates to be relative to the screen geometry
        rect = screen.geometry()
        x1 += rect.x()
        y1 += rect.y()
        x2 += rect.x()
        y2 += rect.y()

        # Capture the screenshot from the correct screen
        pixmap = screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2 - x1, y2 - y1)

        self.parent().displayScreenshot(pixmap)

    def showEvent(self, event):
        self.setCursor(QCursor(Qt.CrossCursor))

