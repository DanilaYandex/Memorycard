#подключаем библеотеки
import os
from PyQt5.QtWidgets import QApplication,QWidget,QFileDialog,QLabel,QPushButton,QListWidget,QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image
from PIL.ImageQt import ImageQt
from PIL import ImageFilter
from PIL.ImageFilter import(
    BLUR,CONTOUR,DETAIL,EDGE_ENHANCE,EDGE_ENHANCE_MORE,
    EMBOSS,FIND_EDGES,SMOOTH,SMOOTH_MORE,SHARPEN,
    GaussianBlur,UnsharpMask
)

app = QApplication([])#создаем приложение
win = QWidget()#создаем окно
win.resize(700, 400)#задаем размеры
win.setWindowTitle('Easy Editor')#задаем название приложения
btn_dir = QPushButton("Папка")#название кнопки
lb_image=QLabel('Картинка')#место под картинку
lw_files=QListWidget()#создаем лист

btn_left=QPushButton('Лево')#кнопка влево
btn_right=QPushButton('Право')#кнопка вправо
btn_zer=QPushButton('Зеркало')#кнопка зеркало
btn_rez=QPushButton('Резкость')#кнопка резкости
btn_brwh=QPushButton('Ч/Б')#кнопка ч/б

row=QHBoxLayout()#создаем оснавную линию
col1=QVBoxLayout()#добавляем линию
col2=QVBoxLayout()#добавляем линию
col1.addWidget(btn_dir)#добавляем виджет
col1.addWidget(lw_files)#добавляем виджет
col2.addWidget(lb_image,95)#добавляем виджет
row_tools=QHBoxLayout()#создаем линию
row_tools.addWidget(btn_left)#добавляем виджет
row_tools.addWidget(btn_right)#добавляем виджет
row_tools.addWidget(btn_zer)#добавляем виджет
row_tools.addWidget(btn_rez)#добавляем виджет
row_tools.addWidget(btn_brwh)#добавляем виджет
col2.addLayout(row_tools)#добавляем на линию

row.addLayout(col1,20)#добавляем линию
row.addLayout(col2,80)#добавляем линию
win.setLayout(row)#меняем оснавную линию

win.show()#показываем окно

workdir=''

def filter(files,extensions):#создаем фильтры
    result=[]#создаем результат
    for filename in files:#условие
        for ext in extensions:#усолвие
            if filename.endswith(ext):#условие
                result.append(filename)#добавляем в конец списка
    return result#возвращаем результат

def chooseWorkdir():#создаем функцию
    global workdir#делаем переменную глобальной
    workdir=QFileDialog.getExistingDirectory()#проверяем

def showFilenamesList():#создаем функцию
    extensions=['.jpg','.jpeg','.png','.gif','.bmp']#создаем переменную с стандартными форматами
    chooseWorkdir()
    filenames=filter(os.listdir(workdir),extensions)#название файла
    lw_files.clear()#чистим
    for filename in filenames:#условие
        lw_files.addItem(filename)#добавляем
    
btn_dir.clicked.connect(showFilenamesList)#подключаем кнопку

class ImageProcessor():#создаем класс
    def __init__(self):#функция инит
        self.image=None#картинка по умолчанию нет
        self.dir=None#по умолчанию нет
        self.filename=None#по умолчанию нет
        self.save_dir='Modified/'#по умолчанию
    def loadImage(self, filename):#функцию загрузки изображения
        self.filename = filename#название файла
        image_path = os.path.join(workdir, filename)#проверяем
        self.image = Image.open(image_path)#открываем
    def do_bw(self):#функция ч/б
        self.image = self.image.convert("L")#делаем фото черно белым
        self.saveImage()#сохраняем
        image_path = os.path.join(workdir, self.save_dir, self.filename)#проверяем
        self.showImage(image_path)#показываем
    def do_left(self):#функция поворота
        self.image=self.image.transpose(Image.ROTATE_90)#поворот фото на лево
        self.saveImage()#сохраняем фото
        image_path = os.path.join(workdir, self.save_dir, self.filename)#проверяем
        self.showImage(image_path)#показываем
    def do_right(self):#создаем функцию поворота
        self.image=self.image.transpose(Image.ROTATE_270)#поворот фото на право
        self.saveImage()#сохраняем
        image_path = os.path.join(workdir, self.save_dir, self.filename)#проверяем
        self.showImage(image_path)#показываем
    def do_flip(self):#функция флипа фото
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)#флипаем фото
        self.saveImage()#сохраняем
        image_path = os.path.join(workdir, self.save_dir, self.filename)#проверяем
        self.showImage(image_path)#показываем
    def do_sharpen(self):#функция резкости
        self.image=self.image.filter(SHARPEN)#делаем фото резкой
        self.saveImage()#сохраняем фото
        image_path=os.path.join(workdir, self.save_dir, self.filename)#проверяем
        self.showImage(image_path)#показываем
    def saveImage(self):#функция сохранения фото
        ''' сохраняет копию файла в подпапке '''
        path = os.path.join(workdir, self.save_dir)#проверяем
        if not(os.path.exists(path) or os.path.isdir(path)):#условие
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)#
        self.image.save(image_path)#сохраняем фото


    def showImage(self, path):#функция показа фото
        lb_image.hide()#показываем
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)#
        lb_image.setPixmap(pixmapimage)#
        lb_image.show()#показываем

def showChosenImage():#функция
    if lw_files.currentRow() >= 0:#условия
        filename = lw_files.currentItem().text()#название фото
        workimage.loadImage(filename)#загружаем 
        image_path = os.path.join(workdir, workimage.filename)#проверяем
        workimage.showImage(image_path)#показываем

workimage=ImageProcessor()
lw_files.currentRowChanged.connect(showChosenImage)#подключаем
btn_brwh.clicked.connect(workimage.do_bw)#подключаем
btn_left.clicked.connect(workimage.do_left)#подключаем
btn_right.clicked.connect(workimage.do_right)#подключаем
btn_rez.clicked.connect(workimage.do_sharpen)#подключаем
btn_zer.clicked.connect(workimage.do_flip)#подключаем
app.exec()#запускаем приложение