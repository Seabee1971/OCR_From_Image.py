from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QPainter, QPen, QCursor, QBitmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget


class SnippingTool(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """Initialize the UI with a layout and a label to display screenshots."""
        self.layout = QVBoxLayout()
        self.label = QLabel('Screenshot will be displayed here')
        self.layout.addWidget(self.label)
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def startSnipping(self):
        """Start the snipping process after hiding the main window and adding a delay."""
        self.hide()
        QTimer.singleShot(1000, self.openSnippingWindow)

    def openSnippingWindow(self):
        """Open the snipping window, determining the current screen and setting the geometry to cover it."""
        self.snippingWindow = SnippingWindow(self)
        desktop = QApplication.desktop()
        current_screen = desktop.screenNumber(QCursor.pos())
        rect = desktop.screenGeometry(current_screen)
        self.snippingWindow.setGeometry(rect)
        self.snippingWindow.showFullScreen()

    def displayScreenshot(self, pixmap):
        """Display the captured screenshot and handle it in the OCRApp class."""
        self.label.setPixmap(pixmap)
        self.show()
        self.parent().handle_screenshot(pixmap)


class SnippingWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_screen = None
        self.start = None
        self.end = None
        self.initUI()

    def initUI(self):
        """Initialize the UI with a custom crosshair cursor."""
        self.setWindowTitle('Snipping Window')
        self.setWindowOpacity(0.3)
        cursor_pixmap = QBitmap(16, 16)
        cursor_pixmap.clear()
        cursor_painter = QPainter(cursor_pixmap)
        cursor_painter.drawLine(0, 8, 15, 8)
        cursor_painter.drawLine(8, 0, 8, 15)
        cursor_painter.end()
        self.setCursor(QCursor(cursor_pixmap, 8, 8))

    def paintEvent(self, event):
        """Draw a rectangle to indicate the area being selected for the screenshot."""
        if self.start:
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 1.5, Qt.SolidLine))
            painter.drawRect(QRect(self.start, self.end))

    def mousePressEvent(self, event):
        """Start the screenshot selection process when the mouse is pressed."""
        self.start = event.pos()
        self.end = self.start
        self.update()
        desktop = QApplication.desktop()
        self.current_screen = desktop.screenNumber(event.globalPos())

    def mouseMoveEvent(self, event):
        """Update the end point of the selection rectangle as the mouse moves."""
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        """End the screenshot selection process when the mouse is released, capturing the screenshot."""
        self.end = event.pos()
        self.close()
        self.captureScreenshot()

    def captureScreenshot(self):
        """Capture the screenshot of the selected area and display it in the SnippingTool window."""
        x1, y1 = min(self.start.x(), self.end.x()), min(self.start.y(), self.end.y())
        x2, y2 = max(self.start.x(), self.end.x()), max(self.start.y(), self.end.y())
        screen = QApplication.screens()[self.current_screen]
        rect = screen.geometry()
        x1 += rect.x()
        y1 += rect.y()
        x2 += rect.x()
        y2 += rect.y()
        pixmap = screen.grabWindow(QApplication.desktop().winId(), x1, y1, x2 - x1, y2 - y1)
        self.parent().displayScreenshot(pixmap)

    def showEvent(self, event):
        """Set the cursor to a cross cursor when the window is shown."""
        self.setCursor(QCursor(Qt.CrossCursor))
