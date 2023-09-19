import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QCursor, QBitmap
from PyQt5.QtCore import Qt, QRect
from PIL import ImageGrab

class SnippingTool(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        print("SnippingWindow __init__ called")  # Debug print statement
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        self.label = QLabel('Screenshot will be displayed here')
        self.layout.addWidget(self.label)

        self.snipBtn = QPushButton('Take Screenshot')
        self.snipBtn.clicked.connect(self.startSnipping)
        self.layout.addWidget(self.snipBtn)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def startSnipping(self):
        self.hide()
        self.snippingWindow = SnippingWindow(self)
        self.snippingWindow.showFullScreen()  # Use showFullScreen() to cover the entire screen
        self.snippingWindow.show()  # Use show() instead of showFullScreen()

    def displayScreenshot(self, pixmap):
        self.label.setPixmap(pixmap)
        self.show()
        self.parent().handle_screenshot(pixmap)  # Call the handle_screenshot method of the OCRApp class


class SnippingWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.start = None
        self.end = None

        self.setWindowTitle('Snipping Window')
        self.setWindowOpacity(0.3)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setStyleSheet("background-color: rgba(100, 100, 100, 100);")  # Set a semi-transparent background color

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

        # Get the screen number that the snipping window is on
        screen_number = QApplication.desktop().screenNumber(self)

        # Get the screen object for the correct screen
        screen = QApplication.screens()[screen_number]

        # Capture the screenshot from the correct screen
        pixmap = screen.grabWindow(0, x1, y1, x2 - x1, y2 - y1)
        self.parent().displayScreenshot(pixmap)

    def showEvent(self, event):
        self.setCursor(QCursor(Qt.CrossCursor))
        print("SnippingWindow showEvent called")  # Debug print statement

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = SnippingTool()
#     ex.show()
#     sys.exit(app.exec_())
