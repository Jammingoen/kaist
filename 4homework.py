import sys
import cv2
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import*
import threading
from PyQt5 import QtGui

#웹캠화면보여주기
def run():
    global state
    
    
    fourcc = cv2.VideoWriter_fourcc(*'H264')
    record = False

    while True:
        #웹캠정보읽기
        ret, image = camera.read()

        height, width = image.shape[:2]
        image = cv2.flip(image, 1)

        #현재시각정보 저장하기
        now = datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S") 

        if state == 1:

            qt_image = QImage(image.data, 
                            width, 
                            height, 
                            image.strides[0], 
                            QImage.Format_BGR888)
            pixmap = QPixmap.fromImage(qt_image)
            img_cap = image
            temp_state = state
            webcam.setPixmap(pixmap)
            

        elif state == -1:
            #원하는 파일경로에 이미지 파일 저장
            cv2.imwrite('C:/Users/p0109/Desktop/카이스트 사이버/3차시/사진, 영상 저장/' + str(now) + '.png', image)
            temp_state = state     
            
            #녹화기능 추가
        elif state == -2:
            record = True
            video = cv2.VideoWriter( 'C:/Users/p0109/Desktop/카이스트 사이버/3차시/사진, 영상 저장/' + str(now) + '.mp4', fourcc, 20.0, (width, height))
            temp_state = state

        elif state == -3:
            print("--- Record End ---")
            record = False
            video.release()
            temp_state = state
        
        elif state == 2:
            qt_image, img_cap = blackwhite_filter(image)
            pixmap = QPixmap.fromImage(qt_image)
            webcam.setPixmap(pixmap)
            temp_state = state

        elif state == 3:
            qt_image, img_cap = canny_filter(image)
            pixmap = QPixmap.fromImage(qt_image)
            webcam.setPixmap(pixmap)

        elif state == 4:
            qt_image, img_cap = sketch_filter(image)
            pixmap = QPixmap.fromImage(qt_image)
            webcam.setPixmap(pixmap)

        elif state == 5:
            qt_image, img_cap = colorinversion_filter(image)
            pixmap = QPixmap.fromImage(qt_image)
            webcam.setPixmap(pixmap)


        if record == True:
            print("--- Recording~ ---")
            
            video.write(image)
    
#흑백필터
def blackwhite_filter(image):
    height, width = image.shape[:2]
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    qt_image = QtGui.QImage(img_gray.data, width, height, img_gray.strides[0], QtGui.QImage.Format_Grayscale8)
    img_cap = img_gray

    return qt_image, img_cap

#흑백 스케치 필터
def canny_filter(image):
    height, width = image.shape[:2]
    img_canny = cv2.Canny(image, 50, 100)
    img_bwsketch = 255 - img_canny

    qt_image = QtGui.QImage(img_bwsketch.data, width, height, img_bwsketch.strides[0], QtGui.QImage.Format_Grayscale8)

    img_cap = img_bwsketch

    return qt_image, img_cap

#스케치 필터
def sketch_filter(image):
    height, width = image.shape[:2]
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    img_gray = cv2.GaussianBlur(img_gray, (9,9), 8)
    edges = cv2.Laplacian(img_gray, -1, None, 5)
    ret, sketch = cv2.threshold(edges, 70, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    sketch = cv2.erode(sketch, kernel)
    sketch = cv2.medianBlur(sketch, 5)
    img_sketch = cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)
    img_paint = cv2.blur(image, (10,10)) 
    img_paint = cv2.bitwise_and(img_sketch, img_paint)

    qt_image = QtGui.QImage(img_paint.data, width, height, img_paint.strides[0], QtGui.QImage.Format_BGR888)

    img_cap = img_paint

    return qt_image, img_cap

#색반전 필터
def colorinversion_filter(image):
    height, width = image.shape[:2]
    img_inversion = 255 - image
   
    qt_image = QtGui.QImage(img_inversion.data, width, height, img_inversion.strides[0], QtGui.QImage.Format_BGR888)

    img_cap = img_inversion

    return qt_image, img_cap

# camera_function 함수
def camera_function(mode):
    global state
    

    #capture mode
    if mode == -1:
        state = 1   

    #record on mode
    elif mode == -2:
        state = -2
    
    #record off mode
    elif mode == -3:
        state = -3

    elif mode == 1:
        state = 1
    
    # black-filter mode
    elif mode == 2:
        state = 2

    # black-sketch-filter mode
    elif mode == 3:
        state =3

    # sketch-filter mode
    elif mode == 4:
        state = 4

    # 색반전 mode
    elif mode == 5:
        state = 5

# QWidget을 상속받아 애플리케이션의 틀 만들기
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        #threading 모듈로 스레드 지정
        thread = threading.Thread(target = run)
        thread.daemon = True
        thread.start()

        self.makeUI()

    def makeUI(self):
        # 창의 위치와 크기로 사용될 변수 (조절 가능)
        self.wtop = 200
        self.wleft = 500
        self.wwidth = 800
        self.wheight = 600

        # 창의 제목 정하기
        self.setWindowTitle("나만의 필터 카메라")

        # 창의 위치 및 크기 정하기
        self.setGeometry(self.wleft, self.wtop, self.wwidth, self.wheight)

        # 웹캠 자리가 업로드될 공간 만들기
        #self.label = QLabel("여기에 웹캠 화면이 업로드됩니다.", self)

        # 버튼 만들기
        self.btn_start  = QPushButton("전원버튼", self)
        self.btn0 =       QPushButton("기본필터", self)
        self.btn1 =       QPushButton("흑백", self)
        self.btn2 =       QPushButton("흑백 스캐치", self)
        self.btn3 =       QPushButton("컬러 스캐치", self)
        self.btn4 =       QPushButton("색반전", self)
        self.btn5 =       QPushButton("왜곡2", self)
        self.btn6 =       QPushButton("마스크1", self)
        self.btn7 =       QPushButton("마스크2", self)
        self.btn_cap =    QPushButton("사진촬영", self)
        self.btn_ron =    QPushButton("영상촬영 ON", self)
        self.btn_roff =   QPushButton("영산촬영 OFF", self)

        #버튼과 camera_function() 함수 connect
        self.btn_cap.clicked.connect(lambda: camera_function(-1))
        self.btn_ron.clicked.connect(lambda: camera_function(-2))
        self.btn_roff.clicked.connect(lambda: camera_function(-3))
        self.btn0.clicked.connect(lambda: camera_function(1))
        self.btn1.clicked.connect(lambda: camera_function(2))
        self.btn2.clicked.connect(lambda: camera_function(3))
        self.btn3.clicked.connect(lambda: camera_function(4))
        self.btn4.clicked.connect(lambda: camera_function(5))


        # 버튼의 위치 지정 (수직 박스 레이아웃 이용)
        # QVBoxLayout1 객체 만들기
        vbox1 = QVBoxLayout()

        # QVBoxLayout에 위젯 등록하기
        vbox1.addWidget(self.btn_start)
        vbox1.addWidget(self.btn0)
        vbox1.addWidget(self.btn1)
        vbox1.addWidget(self.btn2)
        vbox1.addWidget(self.btn3)
        vbox1.addWidget(self.btn4)
        vbox1.addWidget(self.btn5)
        vbox1.addWidget(self.btn6)
        vbox1.addWidget(self.btn7)
        vbox1.addWidget(self.btn_cap)
        vbox1.addWidget(self.btn_ron)
        vbox1.addWidget(self.btn_roff)

        # QVBoxLayout1을 위젯화시키기
        widget1 = QWidget()
        widget1.setLayout(vbox1)

        # QHBoxLayout1 객체 만들기
        hbox1 = QHBoxLayout()

        # QHBoxLayout1에 위젯 등록하기
        # label 등록 (실제 웹캠화면으로 대체)
        #hbox1.addWidget(self.label, stretch=5)
        #hbox1.addWidget(widget1, stretch=1)
        
        #애플리 케이션 틀에 전달
        hbox1.addWidget(webcam, stretch= 5)
        hbox1.addWidget(widget1, stretch= 1)

        #QHBoxLayout1을 위젯화 시키기
        widget2 = QWidget()
        widget2.setLayout(hbox1)

        #QHBoxLayout2 객체만들기
        hbox2 = QHBoxLayout()

        #QHBoxLayout2 에 위젯등록하기
        hbox2.addWidget(self.btn_cap)
        hbox2.addWidget(self.btn_ron)
        hbox2.addWidget(self.btn_roff)

        #QHBoxLayout2응 위젯화 시키기
        widget3 = QWidget()
        widget3.setLayout(hbox2)

        #QVboxLayout2 객체만들기
        vbox2 = QVBoxLayout()

        #QVBoxLayout2에 위젯 등록하기
        vbox2.addWidget(widget2)
        vbox2.addWidget(widget3)

        #전체창을 지정한 layout을 기반으로 배치
        self.setLayout(vbox2)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    #웹캠연결
    webcam = QLabel()
    camera = cv2.VideoCapture(0)
    state = 1

    # MainWindow 객체 불러오기
    main_window = MainWindow()
    
    # 창 표시
    main_window.show()
    sys.exit(app.exec_())
