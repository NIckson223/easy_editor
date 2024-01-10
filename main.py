from PyQt5.QtWidgets import (
                    QWidget, QApplication, QPushButton,QLabel,
                    QHBoxLayout, QVBoxLayout, QListWidget, QFileDialog
                    )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import (Image, ImageFilter, ImageEnhance)
from PIL.ImageFilter import (SHARPEN, BLUR)
import os

app=QApplication([])
main_win=QWidget()
main_win.setWindowTitle('EasyEditor')
main_win.resize(700,500)

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

btn_dir=QPushButton('Папка')
btn_left = QPushButton("Вліво")
btn_right = QPushButton("Вправо")
btn_flip = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")
list_files = QListWidget()

col1.addWidget(btn_dir)
col1.addWidget(list_files)
lb_image=QLabel('Картинка')

col2.addWidget(lb_image)
row_tools  = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)
col2.addLayout(row_tools)

row.addLayout(col1,20)
row.addLayout(col2,80)
main_win.setLayout(row)
main_win.show()

workdir=''
def filter(files, ext):
    result = []
    for file in files:
        for e in ext:
            if file.endswith(e):
                result.append(file)
    return result


def chooseWorkdir():
    global workdir
    workdir=QFileDialog.getExistingDirectory()

def showFileList():
    extension = ['.jpg','.bmp','.gif','.png','.jpeg']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extension)
    list_files.clear()
    for file in filenames:
        list_files.addItem(file)

class ImageProcessor():
    def __init__(self):
        self.filename = None
        self.dir = None
        self.image = None
        self.save_dir = 'modified/'

    def loadImage(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)

    def saveImage(self):
        path = os.path.join(os.getcwd(), self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(os.getcwd(),self.save_dir,self.filename)
        self.showImage(image_path)

    def do_mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(os.getcwd(), self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image=self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(os.getcwd(), self.save_dir, self.filename)
        self.showImage(image_path)

    def do_sharpen(self):
        self.image=self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(os.getcwd(), self.save_dir, self.filename)
        self.showImage(image_path)

    def showImage(self,path):
        lb_image.hide()
        pixmap = QPixmap(path)
        w,h = lb_image.width(), lb_image.height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmap)
        lb_image.show()


def showChosenImage():
    if list_files.currentRow()>=0:
        filename = list_files.currentItem().text()
        workimage.loadImage(workdir,filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)


workimage = ImageProcessor()
list_files.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_dir.clicked.connect(showFileList)
btn_flip.clicked.connect(workimage.do_mirror)
btn_sharp.clicked.connect(workimage.do_sharpen)
app.exec_()