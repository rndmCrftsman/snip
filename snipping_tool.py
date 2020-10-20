import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui, Qt
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2

CONFIGPATH = os.path.join(os.path.expanduser('~'), ".config/snipping_tool/config.txt")

class MyMenu(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        def saveSettings():
            with open(CONFIGPATH, 'w') as f:
                f.writelines(self.savepath_textBox.text())
                f.writelines("\n")
                f.writelines(self.prefix_textBox.text())

        self.setWindowTitle("Snipping Tool Menu")
        layout = QtWidgets.QVBoxLayout()
        savepath_label = QtWidgets.QLabel("Path to save images to:")
        self.savepath_textBox = QtWidgets.QLineEdit()
        prefix_label = QtWidgets.QLabel("Prefixes for images:")
        self.prefix_textBox = QtWidgets.QLineEdit()
        with open(CONFIGPATH, 'r') as f:
            path = f.readline().rstrip()
            if(path != ''):
                self.savepath_textBox.setText(path)
            else:
                self.savepath_textBox.setText("Trash")
            prefix = f.readline().rstrip()
            if(prefix != ''):
                self.prefix_textBox.setText(prefix)
            else:
                self.prefix_textBox.setText("2_Trash")

        save_button = QtWidgets.QPushButton("Save")
        save_button.clicked.connect(saveSettings)
        layout.addWidget(savepath_label)
        layout.addWidget(self.savepath_textBox)
        layout.addWidget(prefix_label)
        layout.addWidget(self.prefix_textBox)
        layout.addWidget(save_button)
        self.setLayout(layout)
        self.show()

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        root = tk.Tk()
        self.selection_mode = True
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        print('Capture the screen...')
        self.show()

    def paintEvent(self, event):
        if(self.selection_mode):
            qp = QtGui.QPainter(self)
            qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
            # qp.setBrush(QtGui.QColor(128, 128, 255, 128))
            qp.setBrush(QtGui.QColor(128, 128, 255, 0))
            qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        if(self.selection_mode):
            self.begin = event.pos()
            self.end = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if(self.selection_mode):
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if(self.selection_mode):
            self.selection_mode = False
        else:
            return
        self.close()
        self.update()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        with open(CONFIGPATH, 'r') as f:
            default_path = f.readline().rstrip()
            prefix = f.readline().rstrip()
            
        self.img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        # img.save('capture.png')
        # img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)

        # Does not work because of headless opencv version (conflicts with PyQt and cv2 -> seem to have different Qt versions)
        # cv2.imshow('Captured Image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        def savePicture():
            path = self.path_textBox.text()
            name = self.name_textBox.text()
            filepath = os.path.join(path, name)
            print(filepath)
            self.img.save(filepath)
            self.close()

        def cancelSnip():
            self.close()
        
        layout = QtWidgets.QVBoxLayout()
        path_label = QtWidgets.QLabel("Path:")
        self.path_textBox = QtWidgets.QLineEdit()
        self.path_textBox.setText(default_path)
        name_label = QtWidgets.QLabel("Name:")
        self.name_textBox = QtWidgets.QLineEdit()
        self.name_textBox.setText(prefix)
        save_button = QtWidgets.QPushButton("Save Picture")
        save_button.clicked.connect(savePicture)
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(cancelSnip)
        layout.addWidget(path_label)
        layout.addWidget(self.path_textBox)
        layout.addWidget(name_label)
        layout.addWidget(self.name_textBox)
        layout.addWidget(save_button)
        layout.addWidget(cancel_button)
        self.setLayout(layout)
        hcenter = int(self.screen_width/2)
        if(self.screen_width > 3500):
            hcenter = int(hcenter/2)
        vcenter = int(self.screen_height/2)
        height = 250
        width = 400
        self.setGeometry(int(hcenter-width/2), int(vcenter-height/2), width, height)
        self.setWindowOpacity(1)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.ArrowCursor)
        )
        self.show()
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    if(len(sys.argv) >= 2):
        if(sys.argv[1] == "--settings"):
            window = MyMenu()
        else:
            print("use --setting to make changes to the paths or use no arg to use the snipping tool\n")
    else:
        window = MyWidget()
    window.show()
    app.aboutToQuit.connect(app.deleteLater)
    sys.exit(app.exec_())
