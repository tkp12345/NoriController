from PyQt5.Qt3DExtras import QTorusMesh, QPhongMaterial, Qt3DWindow, QExtrudedTextMesh, QFirstPersonCameraController
from PyQt5.Qt3DRender import QPointLight, QMesh
from PyQt5.Qt3DCore import QTransform, QEntity
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QVector3D, QQuaternion, QIcon, QFont, QPalette, QImage, QPen, QPainter, QPixmap, QMovie
from PyQt5.QtCore import *
from qrangeslider import QRangeSlider
from noriController import *
import multiprocessing
#from gyroinput import GyroKeyInput
#import sys
from NORIDB import *
#import threading
#from time import sleep


class BlueData(QObject):   # pyqtSignal을 connect후 emit()하여 이벤트를 발동시킨다.
    blue_connecting = False
    blue_Mac = None
    blue_port = None
    blue_check = pyqtSignal()
    blue_check2 = pyqtSignal(str, str)
    def __init__(self):
        super().__init__()


class WiFiData(QObject):
    wifi_connecting = False
    wifi_list = None
    wifi_check = pyqtSignal(list)
    def __init__(self):
        super().__init__()


class GyroData:
    gyro_connecting = False
    gyro_rpy = None


class IRCameraData:
    ir_color =[]
    ir_image = None
    ir_connecting = False
    ir_text = None
"""
class IRCameraData(multiprocessing.Process):
    ir_image = None
    ir_connecting = False
    ir_text = None
"""

class CustomDBValue:
    custom_id = -1
    gyro_page = -1   # 0 == Pitch, 1 == Roll, 2 == Yaw
    gyro_id = -1
    btn_index = -1
    camera_id = -1


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()
        self.blue_siganl = threading.Thread(target=self.blue_start_thread)
        self.blue_siganl.start()

    def blue_start_thread(self):  # 블루투스가 연결되면 메인화면으로 이동
        self.blue = BlueData()
        self.blue.blue_check.connect(self.go_norimain_window)
        while True:
            if self.blue.blue_connecting:
                self.blue.blue_check.emit()
                break
            else:
                sleep(2)

    def initUI(self):
        self.menu_bar()  # 메뉴바 생성
        self.toolbar_create()  # 툴바 생성
        self.back_image()  # 배경화면 이미지 생성

        self.central_widget = QStackedWidget()  # 스택 위젯 생성(화면전환)
        self.setCentralWidget(self.central_widget)  # 메인화면 설정

        # 블루투스 연결 화면 생성, 추가
        bluetooth_connecting = BluetoothConnectingWindow()
        self.central_widget.addWidget(bluetooth_connecting)


        # 메인 화면 생성, 추가
        self.go_norimain_window_widget = NoriMainWindow()
        self.central_widget.addWidget(self.go_norimain_window_widget)  # 위젯 추가

        # 커스텀 화면 생성, 추가
        #self.go_custom_window_widget = CustomWindow()
        #self.central_widget.addWidget(self.go_custom_window_widget)

        # 세팅 화면 생성, 추가
        self.go_setting_window_widget = SettingWindow()
        self.central_widget.addWidget(self.go_setting_window_widget)  # 위젯 추가

        self.setWindowTitle('Nori Controller')
        self.resize(1280, 768)  # 화면 사이즈
        self.show()

        self.setStyleSheet("""
            QMenuBar {
                background: transparent;
                color: white;  
                border-top: 1px solid #000;
                font-size: 17px;
            }
            QMenuBar::item:hover {
                background: black;
            }

            QToolBar {
                background-color: #1E3269;
                border-bottom: 1px solid transparent;
                font-size: 17px;   
                color: rgb(255,255,255);          
            }
            QToolButton { /* all types of tool button */
                color: rgb(255,255,255);
                padding: 15px;
                font-size: 19px;             
            }

            QLabel{
                background-color: black;
                border: 2px solid #444444;
                color: rgb(255,255,255);
                font-size: 17px;
            }
            QGroupBox {          
                font-size: 18px;
                color: rgb(255,255,255);     
                border-radius: 10px;     
                background-color: black;                       
                border: 1px solid #444444;
            }
            QGroupBox::title {
                margin-top: 10px;
                margin-left: 10px;
                background-color: transparent
            }
            QRadioButton {
                color: rgb(255,255,255);       
                font-size: 20px;
                background-color: #444444;
            }
            QRadioButton::indicator {
                margin: 200px;          
                background-color: transparent;
            }                  
            QRadioButton::indicator:checked {
                background-color: rgb(0,116,188);
            }
            QPushButton{
                color: rgb(255,255,255);       
                background-color: #444444;
            }
            QPushButton:pressed {
                background-color: rgb(0,116,188);
            }
            QPushButton::menu-indicator {
                background-color: transparent;        
            }
            QLineEdit{
                border: 2px solid #444444;
                background-color: black;
                color: rgb(255,255,255);
                font-size: 17px;
            }
            QComboBox{
                font-size: 17px; 
                border: 2px solid #444444;
                background-color: black;
                color: rgb(255,255,255);         
                padding: auto;
            }     
            QComboBox QAbstractItemView {
                font-size: 17px; 
                background-color: black;
                color: rgb(255,255,255);
                selection-background-color: #444444;
            }
            QScrollBar {
                border: none;
                background-color: transparent;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle{
                border-radius: 4px;
                border: 0px solid #666;
                background-color: #666;
                min-height: 25px;
            }
            QScrollBar::add-line{
                width: 0px; 
                height: 0px;
            }
            QScrollBar::sub-line{
                width: 0px; 
                height: 0px;
            }
            QScrollBar::add-page{
                background-color: transparent;
            }
            QScrollBar::sub-page{
                background-color: transparent;
            }
    
            QMenu {
                font-size: 15px;        
                color: white;
                background-color: #333;
                border: 1px solid #666;
            }
            QMenu::item {
                padding-left: 15px;
                width: 130px;
                height: 50px;
                font-size: 17px;
            }     
            QMenu::item:selected  {
                color: rgb(0,116,188);
                background-color: #444444;
            }       
            QTreeWidget{
                outline: 0;
                font-size: 17px;                        
                color: white;
                border: 1px solid transparent;
                background-color: black;
            }
            QTreeWidget::item { 
                height: 50px;
            }
            QTreeWidget::item:selected {
                color: white;
                background-color: rgb(0,116,188);     
            }
            QTreeWidget::item:hover {
                
            }   
         """)


    def back_image(self):
        palette = QPalette()  # 배경 이미지
        palette.setColor(QPalette.Window, QColor(40, 40, 40))
        #palette.setBrush(QPalette.Background, QBrush(QPixmap('images/background.jpg')\
         #                                           .scaled(1920, 768, Qt.KeepAspectRatioByExpanding)))
        #Qt.KeepAspectRatio, IgnoreAspectRatio, KeepAspectRatioByExpanding
        self.setPalette(palette)

    def toolbar_create(self):
        self.toolbar1 = self.addToolBar('menu')
        self.toolbar1.addAction('환영합니다.')

        self.toolbar2 = self.addToolBar('menu')
        self.toolbar2.addAction('커스텀 생성')
        self.toolbar2.addAction('커스텀 삭제')

        self.toolbar3 = self.addToolBar('menu')
        buttonAction = self.toolbar3.addAction('버튼')
        gyroAction = self.toolbar3.addAction('기울기')
        cameraAction = self.toolbar3.addAction('IR 카메라')
        buttonAction.triggered.connect(self.go_setting_button)
        gyroAction.triggered.connect(self.go_setting_gyro)
        cameraAction.triggered.connect(self.go_setting_ircamera)

        self.toolbar1.hide()
        self.toolbar2.hide()
        self.toolbar3.hide()

    def toolbar_norimain(self):  # 각 메뉴마다 툴바 변경하기!!
        self.toolbar2.hide()
        self.toolbar3.hide()
        self.toolbar1.show()
        #self.toolbar1 = self.addToolBar('menu')

    def toolbar_custom(self):  # 각 메뉴마다 툴바 변경하기!!
        self.toolbar1.hide()
        self.toolbar3.hide()
        self.toolbar2.show()

    def toolbar_setting(self):  # 각 메뉴마다 툴바 변경하기!!
        self.toolbar1.hide()
        self.toolbar2.hide()
        self.toolbar3.show()

    def menu_bar(self):
        menu = self.menuBar()
        noriAction = menu.addAction('NORI')
        noriAction.triggered.connect(self.go_norimain_window)
        #profileAction = menu.addAction('커스텀')
        #profileAction.triggered.connect(self.go_custom_window)
        settingAction = menu.addAction('설정')
        settingAction.triggered.connect(self.go_setting_window)

    def go_norimain_window(self):
        self.toolbar_norimain()
        self.go_norimain_window_widget.db_select_all_favorites()
        self.central_widget.setCurrentWidget(self.go_norimain_window_widget)  # 위젯 적용

    def go_custom_window(self):
        self.toolbar_custom()
        self.central_widget.setCurrentWidget(self.go_custom_window_widget)  # 위젯 적용

    def go_setting_window(self):
        self.toolbar_setting()
        self.central_widget.setCurrentWidget(self.go_setting_window_widget)  # 위젯 적용

    def go_setting_button(self):  # 설정에서 버튼, 기울기, IR 카메라를 선택하면 바뀌는 위젯
        self.go_setting_window_widget.stk_w.setCurrentIndex(0)
        self.go_setting_window_widget.page_num = 0
        self.go_setting_window_widget.explain_text.setText('버튼의 입력칸을 선택하고 입력창에서 동작할 키를 입력해주세요.')

    def go_setting_gyro(self):
        self.go_setting_window_widget.stk_w.setCurrentIndex(1)
        self.go_setting_window_widget.page_num = 1
        self.go_setting_window_widget.explain_text.setText('1. 기울기 Roll, Pitch, Yaw 중에 하나를 선택해주세요.\n\n'
                                                               '2. 슬라이드를 움직여 최소, 최대 범위를 설정해주세요.\n\n'
                                                               '3. 이 범위안에서 동작할 키를 입력해주세요.\n\n'
                                                               '4. 3D 모델 보기를 통해 컨트롤러의 움직임을 보며'
                                                               '설정을 하면 도움이 됩니다.')
    def go_setting_ircamera(self):
        self.go_setting_window_widget.stk_w.setCurrentIndex(2)
        self.go_setting_window_widget.page_num = 2
        self.go_setting_window_widget.explain_text.setText('1. 마우스 왼쪽 클릭으로 파란 사각형을 생성하여 '
                                                           '영상에서 인식할 범위를 만들어주세요.\n\n'
                                                            '2. 이 사각형 안에서 동작할 키를 입력해주세요.\n\n'
                                                           '3. 마우스 오른쪽 클릭으로 사각형을 삭제할 수 있습니다.')

class BluetoothConnectingWindow(QWidget):  # 블루투스 연결 화면
    def __init__(self, parent=None):
        super(BluetoothConnectingWindow, self).__init__(parent)
        layout = QVBoxLayout()  # 박스 레이아웃 생성
        layout.addSpacing(100)
        spin = QLabel()
        spin.setFixedHeight(200)
        spin.setAlignment(Qt.AlignCenter)
        movie = QMovie("images/loader.gif")
        movie.setScaledSize(QSize(200, 200))
        spin.setMovie(movie)
        movie.start()
        layout.addWidget(spin)

        self.label = QLabel('기기를 찾는중입니다. 잠시만 기다려주세요.', self)
        self.label.setFixedHeight(50)
        self.label.setAlignment(Qt.AlignCenter)  # 중앙에 위치
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.setStyleSheet("""
            QLabel{
                color: white;
                font-size: 35px;
                font-weight: bold;
                border: 1px solid transparent;
                background-color: transparent;
            }
        """)


class NoriMainWindow(QWidget):  # 메인 화면
    # self.label = QLabel('커스텀 즐겨찾기\n기기정보', self)
    # self.label.setAlignment(Qt.AlignCenter)  # 중앙에 위치
    def __init__(self, parent=None):
        super(NoriMainWindow, self).__init__(parent)

        self.v_box = QVBoxLayout()
        self.v_box2 = QVBoxLayout()
        self.v_box3 = QVBoxLayout()
        self.v_box4 = QVBoxLayout()
        self.h_box = QHBoxLayout()
        self.h_box2 = QHBoxLayout()

        self.v_box.addSpacing(20)
        self.v_box2.addSpacing(30)
        self.v_box3.addSpacing(30)

        self.favorites_group = QGroupBox('즐겨찾기')
        self.device_group = QGroupBox('기기정보')

        self.favorites_tree_widget = self.add_tree_widget(self.v_box)
        self.favorites_tree_widget.itemClicked.connect(self.selected_item)
        self.favorites_group.setLayout(self.v_box)
        self.favorites_group.setFixedWidth(400)

        self.bluetooth_group = DeviceInformation('', self.v_box2, 0)
        self.bluetooth_group_information = DeviceInformation('블루투스 정보', self.v_box2, 1)
        self.wifi_group = DeviceInformation('', self.v_box3, 2)
        self.wifi_group_information = DeviceInformation('와이파이 정보', self.v_box3, 3)

        self.h_box2.addSpacing(10)
        self.h_box2.addLayout(self.v_box2)
        self.h_box2.addSpacing(10)
        self.h_box2.addLayout(self.v_box3)
        self.h_box2.addSpacing(10)
        self.device_group.setLayout(self.h_box2)

        self.menu()
        self.db_select_all_favorites()

        self.h_box.addSpacing(40)
        self.h_box.addWidget(self.favorites_group)
        self.h_box.addSpacing(40)
        self.h_box.addWidget(self.device_group)
        #self.h_box.addLayout(self.h_box2)
        self.h_box.addSpacing(40)

        self.v_box4.addSpacing(20)
        self.v_box4.addLayout(self.h_box)
        self.v_box4.addSpacing(20)
        self.setLayout(self.v_box4)
        self.setStyleSheet("""
            QTreeWidget:item{
                height: 50px;
            }
        """)

    def selected_item(self):
        self.select_item = self.favorites_tree_widget.selectedItems()[0]
        self.item_index = self.favorites_tree_widget.indexFromItem(self.select_item)

    def selected_item_button(self, item):
        self.select_item = item
        self.item_index = self.favorites_tree_widget.indexFromItem(self.select_item, 0)

    def db_select_all_favorites(self):
        # DB 연결
        favorites_list = Favorites.select_Favorites()
        custom_list = Setting.select_Setting(self)
        
        self.favorites_tree_widget.clear()
        for i in favorites_list:
            for j in custom_list:
                if i[0] == j[0]:
                    self.add_favorites(j[1])

    def add_favorites(self, name):
        widgets = FavoritesWidget()
        widgets.button.setMenu(self.pop_menu)

        item = QTreeWidgetItem(self.favorites_tree_widget)
        item.setText(0, '  '+name)
        self.favorites_tree_widget.setItemWidget(item, 1, widgets.button)

        widgets.button.clicked.connect(lambda: self.selected_item_button(item))

    def delete_favorites(self):
        try:
            index = self.item_index.row()
            self.favorites_tree_widget.takeTopLevelItem(index)
    
            # DB 연결
            custom_id = Favorites.select_Favorites()[index][0]
            Favorites.delete_Favorites(custom_id)
        except:
            print('삭제오류')
    
    def execute_favorites(self):
        index = self.item_index.row()
        custom_id = Favorites.select_Favorites()[index][0]
        print('선택한 즐겨찾기의 기본키를 넘겨주기', custom_id)
        try:
            #self.gyro_input = GyroKeyInput(custom_id, GyroData)
            #self.gyro_input.start()
            #self.key_input = keyInput(custom_id)
            #self.camera_input.start()
            self.camera_input = CamerakeyInput(custom_id, IRCameraData)
            self.camera_input.start()



        except:
            print('즐겨찾기 실행 오류')

    def end_favorites(self):
        self.gyro_input.stop()
        #self.camera_input.stop()
        print('끝내기')

    def add_tree_widget(self, box):
        tree_widget = QTreeWidget()
        tree_widget.setFixedSize(300, 550)
        tree_widget.setHeaderHidden(True)
        tree_widget.setRootIsDecorated(False)
        tree_widget.setColumnCount(2)
        tree_widget.setColumnWidth(0, 220)
        tree_widget.setColumnWidth(1, 50)
        box.addSpacing(30)
        box.addWidget(tree_widget, alignment=Qt.AlignCenter)
        box.addStretch(1)
        tree_widget.setStyleSheet("""
            font-size: 25px;
            font-weight: bold;
        """)
        return tree_widget

    def menu(self):
        self.pop_menu = QMenu(self)
        self.execute_action = QAction('실행', self)
        self.execute_action.triggered.connect(self.execute_favorites)
        self.pop_menu.addAction(self.execute_action)

        self.end_action = QAction('종료', self)
        self.end_action.triggered.connect(self.end_favorites)
        self.pop_menu.addAction(self.end_action)

        self.delete_action = QAction('즐겨찾기 삭제', self)
        self.delete_action.triggered.connect(self.delete_favorites)
        self.pop_menu.addAction(self.delete_action)


class DeviceInformation(QGroupBox):
    def __init__(self, name, layout, num):
        super(DeviceInformation, self).__init__()
        self.setTitle(name)
        self.setFixedSize(300, 250)
        layout.addWidget(self)
        box = QVBoxLayout()
        box.addSpacing(20)
        self.start_thread(num, box)
        self.setLayout(box)
        self.setStyleSheet("""
            QGroupBox{
                background-color: rgb(15, 15, 15);
                border-color: rgb(15, 15, 15);
            }
        """)

    def start_thread(self, num, box):
        if num == 0:
            widget = QLabel()
            widget.setAlignment(Qt.AlignCenter)  # 중앙에 위치
            widget.setStyleSheet("""
                border-color: transparent;
                background-color: transparent;
            """)
            image = QPixmap('images/bluetooth_off.png')
            image = image.scaled(150, 150)
            widget.setPixmap(image)
            box.addWidget(widget)

            widget2 = QLabel('Bluetooth')
            widget2.setAlignment(Qt.AlignCenter)
            widget2.setStyleSheet("""
                border-color: transparent;
                background-color: transparent;
            """)
            box.addWidget(widget2)

            tmep = threading.Thread(target=self.blue_state_thread, args=(widget, widget2))
            tmep.start()
        elif num == 1:
            self.blue_text_widget = QTextBrowser()
            self.blue_text_widget.setAlignment(Qt.AlignCenter)
            self.blue_text_widget.append('\n\n\n블루투스를 연결해주세요.')
            self.blue_text_widget.setStyleSheet("""
                color: white;
                font-size: 20px;
                border: 1px solid transparent;
                background-color: transparent;
     
            """)
            box.addSpacing(10)
            box.addWidget(self.blue_text_widget)

            tmep = threading.Thread(target=self.blue_information_thread)
            tmep.start()
        elif num == 2:
            widget = QLabel()
            widget.setAlignment(Qt.AlignCenter)  # 중앙에 위치
            widget.setStyleSheet("""
                border-color: transparent;
                background-color: transparent;
            """)
            image = QPixmap('images/wifi_off.png')
            image = image.scaled(150, 150)
            widget.setPixmap(image)
            box.addWidget(widget)

            widget2 = QLabel('WiFi')
            widget2.setAlignment(Qt.AlignCenter)
            widget2.setStyleSheet("""
                border-color: transparent;
                background-color: transparent;
            """)
            box.addWidget(widget2)

            tmep = threading.Thread(target=self.wifi_state_thread, args=(widget, widget2))
            tmep.start()

        elif num == 3:
            self.wifi_text_widget = QTextBrowser()
            self.wifi_text_widget.setAlignment(Qt.AlignCenter)
            self.wifi_text_widget.append('\n\n\nWiFi를 연결해주세요.')
            self.wifi_text_widget.setStyleSheet("""
                color: white;
                font-size: 20px;
                border: 1px solid transparent;
                background-color: transparent;
            """)
            box.addSpacing(10)
            box.addWidget(self.wifi_text_widget)

            tmep = threading.Thread(target=self.wifi_information_thread)
            tmep.start()

    def blue_state_thread(self, widget, widget2):
        while True:
            if BlueData.blue_connecting:
                image = QPixmap('images/bluetooth_on.png')
                image = image.scaled(150, 150)
                widget.setPixmap(image)

                widget2.setText(BlueData.blue_Mac)
                break
            else:
                sleep(2)

    def wifi_state_thread(self, widget, widget2):
        while True:
            if WiFiData.wifi_connecting:
                image = QPixmap('images/wifi_on.png')
                image = image.scaled(150, 150)
                widget.setPixmap(image)

                widget2.setText(WiFiData.wifi_list[0])
                break
            else:
                sleep(2)

    def blue_information_thread(self):
        blue = BlueData()
        blue.blue_check2.connect(self.blue_text_update)
        while True:
            if BlueData.blue_connecting:
                text1 = blue.blue_Mac
                text2 = blue.blue_port
                blue.blue_check2.emit(text1, text2)
                break
            else:
                sleep(2)

    def blue_text_update(self, text1, text2):
        self.blue_text_widget.clear()
        self.blue_text_widget.setAlignment(Qt.AlignCenter)
        text = '\n\n블루투스 주소\n' + text1 + '\n' + text2 + '번 port에서 연결중'
        self.blue_text_widget.append(text)

    def wifi_information_thread(self):
        wifi = WiFiData()
        wifi.wifi_check.connect(self.wifi_text_update)
        while True:
            if WiFiData.wifi_connecting:
                text = wifi.wifi_list
                wifi.wifi_check.emit(text)
                break
            else:
                sleep(2)

    def wifi_text_update(self, text):
        self.wifi_text_widget.clear()
        self.wifi_text_widget.setAlignment(Qt.AlignCenter)

        del text[0]
        self.wifi_text_widget.append('연결 가능한 WiFi SSID\n')
        for i in text:
            temp = 'SSID: ' + i
            self.wifi_text_widget.append(temp)


class FavoritesWidget(QWidget):
    def __init__(self, parent=None):
        super(FavoritesWidget, self).__init__(parent=parent)

        btn = SettingAddDelete()
        self.button = btn.menu_image()
        #self.button.setFixedHeight(50)
        self.button.setStyleSheet("""
            margin: 10px;
            background-color: transparent;
        """)
        self.button.setIconSize(QSize(30, 50))
        self.button.mousePressEvent = self.mousePressEvent

    def mousePressEvent(self, event):
        try:
            if event.type() == QEvent.MouseButtonPress:
                self.button.clicked.emit(True)
                QPushButton.mousePressEvent(self.button, event)
                event.accept()
        except:
            print('오류')


class CustomWindow(QWidget):  # 커스텀 생성 화면
    def __init__(self, parent=None):
        super(CustomWindow, self).__init__(parent)
        self.label = QLabel('커스텀 관리', self)
        self.label.setStyleSheet('color:white')
        self.label.setAlignment(Qt.AlignCenter)  # 중앙에 위치
        font = self.label.font()  # 폰트 생성
        font.setBold(True)
        font.setPointSize(20)
        self.label.setFont(font)  # 폰트 적용

        layout = QVBoxLayout()  # 박스 레이아웃 생성
        layout.addWidget(self.label)  # 레이아웃에 라벨 배치
        self.setLayout(layout)


class SettingWindow(QWidget):  # 키 세팅 화면
    page_num = 0
    def __init__(self, parent=None):
        super(SettingWindow, self).__init__(parent)
        self.stk_w = QStackedWidget(self)
        self.init_widget()

    def custom_clicked(self):
        print('test')

    def init_widget(self):
        self.setWindowTitle("키설정")
        self.input_setting()
        self.explain()

        h_box = QHBoxLayout()
        v_box = QVBoxLayout()
        v_box2 = QVBoxLayout()

        self.setting_custom = SettingCustom()
        self.setting_button = SettingButton()
        self.setting_gyro = SettingGyro()
        self.setting_ircamera = SettingIRCamera()

        self.setting_custom.tree_widget.itemSelectionChanged.connect(lambda: self.setting_button.custom_selected_btn(self.setting_custom.tree_widget))
        self.setting_custom.tree_widget.itemSelectionChanged.connect(self.setting_gyro.custom_selected_gyro)
        self.setting_custom.tree_widget.itemSelectionChanged.connect(lambda: self.setting_ircamera.custom_selected_ircamera(self.setting_custom.tree_widget))
        self.setting_custom.add_custom_btn.clicked.connect(self.setting_gyro.custom_add_gyro)
        self.setting_custom.delete_action.triggered.connect(self.setting_gyro.custom_delete_gyro)
        self.setting_custom.add_custom_btn.clicked.connect(self.setting_ircamera.custom_add_ircamera)
        self.setting_custom.delete_action.triggered.connect(self.setting_ircamera.custom_delete_ircamera)

        self.stk_w.addWidget(self.setting_button)
        self.stk_w.addWidget(self.setting_gyro)
        self.stk_w.addWidget(self.setting_ircamera)

        v_box2.addWidget(self.keyinsert)
        v_box2.addSpacing(10)
        v_box2.addWidget(self.example)

        h_box.addSpacing(10)
        h_box.addWidget(self.setting_custom, alignment=Qt.AlignLeft)

        h_box.addSpacing(10)
        #h_box.addWidget(scroll)
        h_box.addWidget(self.stk_w)
        h_box.addSpacing(10)
        h_box.addLayout(v_box2)
        #h_box.addWidget(self.example, alignment=Qt.AlignBottom)
        #h_box.addWidget(self.keyinsert, alignment=Qt.AlignTop)
        h_box.addSpacing(10)

        v_box.addSpacing(10)
        v_box.addLayout(h_box)
        v_box.addSpacing(10)
        self.setLayout(v_box)

        # 수정 필요(속도가 너무 느려짐)
        #input_check = threading.Thread(target=self.input_check)
        #input_check.start()
        
    def input_check(self):  # 입력 칸에 선택한 값을 보여줌
        while True:
            try:
                if self.page_num == 0:  # 버튼
                    self.input_name = self.setting_button
                elif self.page_num == 1:  # 자이로
                    self.input_name = self.setting_gyro
                elif self.page_num == 2:  # IR 카메라
                    self.input_name = self.setting_ircamera

                n = self.input_name.radioBtn.pos()
                sleep(0.2)
                if n != self.input_name.radioBtn.pos():  # 다른 라디오버튼을 누를 때마다
                    self.qle.setText('')
                    self.cb.setCurrentIndex(-1)
                    if self.input_name.radioBtn.text() in self.cb_item:  # 입력된 버튼에 마우스 버튼이 있으면
                        self.cb.setCurrentText(self.input_name.radioBtn.text())   # 콤보박스에 선택된 마우스 버튼이 보이게
                    elif self.input_name.radioBtn.text() == '입력':
                        continue
                    else:
                        self.qle.setText(self.input_name.radioBtn.text())
            except:
                pass

    def explain(self):   # 설정 설명문
        self.example = QGroupBox()
        #self.example.setFixedHeight(200)
        self.example.setFixedWidth(200)
        v_box = QVBoxLayout()
        self.example.setLayout(v_box)
        self.example.setTitle('설정 방법')

        self.explain_text = QTextBrowser()
        self.explain_text.append('버튼의 입력칸을 클릭하고 입력창에서 마우스 또는 키보드로 설정해주세요.')
        self.explain_text.setStyleSheet("""
                                border: 1px solid black;
                                color: white;
                                font-size: 17px;
                                background-color: black;
                            """)
        #self.explain_text.setFixedWidth(130)
        v_box.addSpacing(40)
        v_box.addWidget(self.explain_text)
        #v_box.addStretch(1)

    def input_setting(self):  # 설정 입력
        self.keyinsert = QGroupBox()
        v_box = QVBoxLayout()
        h_box = QHBoxLayout()
        self.keyinsert.setFixedHeight(270)
        self.keyinsert.setFixedWidth(200)
        self.keyinsert.setLayout(v_box)
        self.keyinsert.setTitle("입력")

        self.cb_item = ['왼쪽 클릭', '오른쪽 클릭', '스크롤 클릭', '위로 이동', '아래로 이동', '좌측으로 이동', '우측으로 이동']
        self.cb = QComboBox(self)
        self.cb.setPlaceholderText(' ')

        for i in self.cb_item:
            self.cb.addItem(i)
        self.cb.setFixedSize(180, 30)
        self.cb.setView(QListView())
        self.cb.activated[str].connect(self.mouse_on_changed)
        for i in range(len(self.cb_item)):
            self.cb.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

        self.qle = QLineEdit(self)
        #self.qle.focusNextPrevChild(True)
        #regex = QRegExp("[a-z-A-Z]{1}")
        #validator = QRegExpValidator(regex)
        #self.qle.setValidator(validator)
        self.qle.setFixedSize(180, 30)
        self.qle.setAlignment(Qt.AlignCenter)
        # self.qle.textEdited[str].connect(self.keyborad_on_changed)
        #self.focusNextPrevChild(False)

        self.qle.keyPressEvent = self.keyborad_on_changed_press
        self.qle.keyReleaseEvent = self.keyborad_on_changed_release

        self.key_count = 0

        label1 = QLabel('마우스')
        label1.setFixedSize(180, 30)
        label2 = QLabel('키보드')
        label2.setFixedSize(180, 30)
        label1.setAlignment(Qt.AlignCenter)
        label2.setAlignment(Qt.AlignCenter)

        v_box.addSpacing(50)
        v_box.addWidget(label1, alignment=Qt.AlignCenter)
        v_box.addWidget(self.cb, alignment=Qt.AlignCenter)
        v_box.addSpacing(30)
        v_box.addWidget(label2, alignment=Qt.AlignCenter)
        v_box.addWidget(self.qle, alignment=Qt.AlignCenter)
        v_box.addStretch(1)

        #h_box.addLayout(v_box)
        #h_box.addStretch(1)

    def mouse_on_changed(self, text):
        try:
            if self.page_num == 0:  # 버튼 설정
                self.setting_button.radioBtn.setText(text)
                self.update_btn_input(text)

            elif self.page_num == 1:  # 기울기 설정
                self.setting_gyro.radioBtn.setText(text)
                self.update_gyro_input(text)

            elif self.page_num == 2:  # 카메라 설정
                self.setting_ircamera.radioBtn.setText(text)
                self.update_camera_input(text)
            self.qle.setText('')
        except:
            print('마우스 입력 오류')

    def keyborad_on_changed_press(self, e):
        try:
            def print_key():
                vk_key = False
                # 딕셔너리에 있는 가상키인 경우 실행
                if e.nativeVirtualKey() in KeyList.key_code_dic:
                    vk_key = True
                    return KeyList.key_code_dic[e.nativeVirtualKey()]

                # 딕셔너리에 없는 키라면 실행
                elif not vk_key:
                    return chr(e.key())

            # 중복으로 입력되는걸 막음
            if not e.isAutoRepeat():
                if self.key_count == 0:  # 한 단어만 입력하는 경우
                    self.qle.setText(print_key())
                elif self.key_count == 1:  # 두 단어를 같이 입력한 경우
                    if '+' in self.qle.text():
                        self.qle.setText(self.qle.text().split('+')[1]+'+'+print_key())
                    else:
                        self.qle.setText(self.qle.text()+'+'+print_key())
                elif self.key_count == 2:  # 두 단어를 연속으로 같이 입력한 경우
                    self.qle.setText(self.qle.text().split('+')[1]+'+'+print_key())

                # 입력한 text를 선택한 입력칸에 setText
                text = self.qle.text()
                if self.page_num == 0:  # 버튼 설정
                    self.setting_button.radioBtn.setText(text)
                elif self.page_num == 1:  # 기울기 설정
                    self.setting_gyro.radioBtn.setText(text)
                elif self.page_num == 2:  # 카메라 설정
                    self.setting_ircamera.radioBtn.setText(text)
                self.cb.setCurrentIndex(-1)

                # 입력할 수 있는 단어를 2개로 제한
                self.key_count += 1
                if self.key_count == 3:
                    self.key_count = 1

        except:
            print('키 프레스 오류')

    def keyborad_on_changed_release(self, e):
        try:
            if not e.isAutoRepeat():
                # 키를 놓았을 때 입력한 단어수를 초기화
                self.key_count = 0
                
                # 입력한 키를 DB에 update
                text = self.qle.text()
                if self.page_num == 0:  # 버튼 설정
                    self.update_btn_input(text)

                elif self.page_num == 1:  # 기울기 설정
                    self.update_gyro_input(text)

                elif self.page_num == 2:  # 카메라 설정
                    self.update_camera_input(text)

        except:
            print('키 릴리즈 오류')

    """
    def keyborad_on_changed(self, text):
        try:
            text = text.upper()
            if self.page_num == 0:  # 버튼 설정
                self.setting_button.radioBtn.setText(text)
                self.update_btn_input(text)

            elif self.page_num == 1:  # 기울기 설정
                self.setting_gyro.radioBtn.setText(text)
                self.update_gyro_input(text)

            elif self.page_num == 2:  # 카메라 설정
                self.setting_ircamera.radioBtn.setText(text)
                self.update_camera_input(text)
            self.qle.setText(text)
            self.cb.setCurrentIndex(-1)
        except:
            print('키보드 입력 오류')
    """

    def update_btn_input(self, text):
        if CustomDBValue.btn_index == 0:
            ButtonDB.update_ButtonA(CustomDBValue.custom_id, text)
        elif CustomDBValue.btn_index == 1:
            ButtonDB.update_ButtonB(CustomDBValue.custom_id, text)
        elif CustomDBValue.btn_index == 2:
            ButtonDB.update_ButtonX(CustomDBValue.custom_id, text)
        elif CustomDBValue.btn_index == 3:
            ButtonDB.update_ButtonY(CustomDBValue.custom_id, text)

    def update_gyro_input(self, text):
        if CustomDBValue.gyro_page == 0:
            RollDB.update_Roll_input(CustomDBValue.custom_id, CustomDBValue.gyro_id, text)
        elif CustomDBValue.gyro_page == 1:
            PitchDB.update_Pitch_input(CustomDBValue.custom_id, CustomDBValue.gyro_id, text)
        elif CustomDBValue.gyro_page == 2:
            YawDB.update_Yaw_input(CustomDBValue.custom_id, CustomDBValue.gyro_id, text)

    def update_camera_input(self, text):
        Camera.update_Camera_input(CustomDBValue.custom_id, CustomDBValue.camera_id, text)



class SettingCustom(QGroupBox):
    def __init__(self, parent=None):
        super(SettingCustom, self).__init__(parent=parent)
        self.setTitle("커스텀")
        self.setFixedWidth(200)

        self.menu()  # 메뉴 생성

        # 트리 위젯 생성
        self.tree_widget = QTreeWidget()
        #self.tree_widget.setFixedHeight(590)
        #self.tree_widget.itemSelectionChanged.connect(self.selected_item)
        self.tree_widget.itemDoubleClicked.connect(self.double_click)
        self.tree_widget.itemClicked.connect(self.selected_item)
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setRootIsDecorated(False)
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setColumnWidth(0, 140)
        self.tree_widget.setColumnWidth(1, 20)
        self.tree_widget.setStyleSheet("""font-weight: bold;""")
        # 플러스 버튼 생성
        self.custom_stack_select = SettingAddDelete()
        self.add_custom_btn = self.custom_stack_select.add_image()
        self.add_custom_btn.setIconSize(QSize(20, 20))
        self.add_custom_btn.clicked.connect(self.add_widget)  # 이벤트 연결

        # DB에 있는 커스텀 생성
        custom_list = Setting.select_Setting(self)
        for index, name in custom_list:
            self.select_custom(name)

        v_box = QVBoxLayout()
        v_box2 = QVBoxLayout()
        h_box = QHBoxLayout()

        v_box.addWidget(self.tree_widget)

        h_box.addSpacing(150)
        h_box.addWidget(self.add_custom_btn)
        h_box.addStretch(1)

        v_box2.addLayout(h_box)
        v_box2.addLayout(v_box)
        #v_box2.addStretch(1)
        
        self.setLayout(v_box2)

    """
    def selected_item(self):
        self.select_item = self.tree_widget.selectedItems()[0]
        self.item_index = self.tree_widget.indexFromItem(self.select_item, 0)
        print(self.item_index.row(), CustomDBValue.custom_id)

    """

    # 트리 위젯을 클릭했을 때 선택된 아이템 구하기
    def selected_item(self):
        self.select_item = self.tree_widget.selectedItems()[0]
        self.item_index = self.tree_widget.indexFromItem(self.select_item, 0)

        # 현재 선택한 tree widget 의 custom_id를 클래스 변수에 담기
        CustomDBValue.custom_id = Setting.select_Setting(self)[self.item_index.row()][0]

    # 버튼을 클릭했을 때 선택된 아이템 구하기
    def selected_item_button(self, item):
        self.select_item = item
        self.item_index = self.tree_widget.indexFromItem(self.select_item, 0)

        # 현재 선택한 tree widget 의 custom_id를 클래스 변수에 담기
        CustomDBValue.custom_id = Setting.select_Setting(self)[self.item_index.row()][0]

    # 커스텀 이름을 더블 클릭하면 이름을 수정할 수 있는 LienEdit 생성
    def double_click(self):
        self.name = QLineEdit()
        self.name.setStyleSheet(""" margin: 10px; """)
        self.tree_widget.setItemWidget(self.select_item, 0, self.name)
        self.name.setText(self.select_item.text(0))
        self.name.selectAll()
        self.select_item.setText(0, ' ')
        self.name.focusOutEvent = self.update_name_focus_out
        self.name.returnPressed.connect(self.update_name_enter)

    # 텍스트편집을 벗어날 때 이벤트 실행
    def update_name_focus_out(self, event):
        if event.type() == QEvent.FocusOut:
            name = self.name.text()
            self.tree_widget.removeItemWidget(self.select_item, 0)
            self.select_item.setText(0, name)

            # DB 연결
            Setting.update_Setting_name(CustomDBValue.custom_id, name)

    # 텍스트 편집에서 엔터를 누르면 이벤트 실행
    def update_name_enter(self):
        name = self.name.text()  # db에 저장하기
        self.tree_widget.removeItemWidget(self.select_item, 0)
        self.select_item.setText(0, name)

        # DB 연결
        Setting.update_Setting_name(CustomDBValue.custom_id, name)

    # 커스텀 생성
    def add_widget(self):
        try:
            # 현재 DB에 저장돼 있는 마지막 Custom_id 를 가져옴
            custom_id = Setting.select_Setting(self)[-1][0] + 1  # 생성된 커스텀이 없는 경우 오류 발생
            self.select_custom('Custom')
            # DB 연결
            Setting.insert_Setting(custom_id, 'Custom')
            ButtonDB.insert_Button(custom_id, '입력', '입력', '입력', '입력')
        except:  # 생성된 커스텀이 없는 경우
            self.select_custom('Custom')
            # DB 연결
            Setting.insert_Setting(0, 'Custom')
            ButtonDB.insert_Button(0, '입력', '입력', '입력', '입력')

    # 커스텀 삭제
    def delete_widget(self):
        try:
            index = self.item_index.row()
            custom_index = Setting.select_Setting(self)[index][0]
            self.tree_widget.takeTopLevelItem(index)
            self.tree_widget.clearSelection()
            # DB 연결
            Setting.delete_Setting(custom_index)
        except:
            print('삭제 오류')

    # DB에 있는 커스텀 출력
    def select_custom(self, name):
        temp = CustomWidget()
        temp.button.setMenu(self.pop_menu)

        # tree widget 에 추가할 item 설정
        item = QTreeWidgetItem(self.tree_widget)
        item.setText(0, name)
        self.tree_widget.setItemWidget(item, 1, temp.button)

        # 메뉴 버튼을 클릭했을 때 위젯의 인덱스 번호를 알 수 있게 설정
        temp.button.clicked.connect(lambda: self.selected_item_button(item))

    # DB에 즐겨찾기 추가
    def insert_favorites(self):
        try:
            Favorites.insert_Favorites(CustomDBValue.custom_id)
        except:
            print('즐겨찾기 오류')
        
    # 버튼을 클릭했을 때 출력되는 메뉴 생성
    def menu(self):
        self.pop_menu = QMenu(self)
        self.favorites_action = QAction('즐겨찾기 추가', self)
        self.favorites_action.triggered.connect(self.insert_favorites)
        self.pop_menu.addAction(self.favorites_action)

        self.delete_action = QAction('삭제', self)
        self.delete_action.triggered.connect(self.delete_widget)
        self.pop_menu.addAction(self.delete_action)


class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super(CustomWidget, self).__init__(parent=parent)

        custom_btn = SettingAddDelete()
        self.button = custom_btn.menu_image()
        self.button.setStyleSheet("""
            margin: 10px;
            background-color: transparent;
        """)
        self.button.setIconSize(QSize(20, 20))
        self.button.mousePressEvent = self.mousePressEvent

    # 버튼에 클릭 이벤트를 실행했을 때 메뉴가 나오게 함
    def mousePressEvent(self, event):
        try:
            if event.type() == QEvent.MouseButtonPress:
                self.button.clicked.emit(True)
                QPushButton.mousePressEvent(self.button, event)
                event.accept()
        except:
            print('오류')


class StWidgetForm(QGroupBox):  # 버튼, 기울기, IR카메라 설정 베이스
    def __init__(self):
        QGroupBox.__init__(self)
        #self.setFixedHeight(270)
        self.h_box = QHBoxLayout()
        self.h_box2 = QHBoxLayout()
        self.v_box = QVBoxLayout()
        self.v_box2 = QVBoxLayout()
        self.v_box3 = QVBoxLayout()
        self.v_box4 = QVBoxLayout()

        self.tree_widget = QTreeWidget()
        self.tree_widget.setFixedWidth(300)
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setRootIsDecorated(False)
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setVisible(False)

class SettingButton(StWidgetForm):  # 키설정 버튼
    def __init__(self):
        super(SettingButton, self).__init__()

        self.setTitle("버튼")
        self.btn_name = ['A', 'B', 'X', 'Y']

        self.btn_tree_widget = self.tree_widget
        self.btn_list = []
        self.btn_group = QButtonGroup()

        for i in self.btn_name:
            self.add_button(i)

        self.choose_message = QLabel('커스텀을 선택해주세요.')
        self.choose_message.setStyleSheet("""
            font: 30px;
            background-color: transparent;
            border-color: transparent;
        """)

        self.h_box.addSpacing(70)
        self.h_box.addWidget(self.btn_tree_widget)
        self.h_box.addStretch(1)

        self.v_box.addWidget(self.choose_message, alignment=Qt.AlignCenter)
        self.v_box.addSpacing(70)
        self.v_box.addLayout(self.h_box)

        self.setLayout(self.v_box)
        self.setStyleSheet("""
            QLabel {
                background-color: rgb(0,116,188);
                border-radius: 25px;
                border-color: rgb(0,116,188);
                font-weight: bold;
            }
            QTreeWidget::item:selected {
                background-color: transparent;
            }
            QTreeWidget::item:hover {
                background-color: transparent;
            }
            QTreeWidget::item { 
                height: 120px;
            }
        """)

    def radio_button_clicked(self, item):
        self.radioBtn = self.sender()
        self.select_item = item
        self.item_index = self.btn_tree_widget.indexFromItem(self.select_item, 0)
        CustomDBValue.btn_index = self.item_index.row()

    def db_select_all_button(self, custom_id):
        button_list = ButtonDB.select_Button()

        for i in button_list:
            if custom_id == i[0]:
                for j in range(4):
                    self.btn_list[j].setText(i[j + 1])

    def custom_selected_btn(self, tree_widget):
        self.deselected_btn()
        item = tree_widget.currentItem()
        index = tree_widget.indexFromItem(item)
        custom_id = Setting.select_Setting(self)[index.row()][0]

        self.db_select_all_button(custom_id)

        self.choose_message.setVisible(False)
        self.btn_tree_widget.setVisible(True)

    def add_button(self, btn_name):
        i = QLabel(btn_name)
        i.setFixedSize(50, 50)
        i.setAlignment(Qt.AlignCenter)
        j = QRadioButton('입력')
        j.setFixedSize(200, 50)

        item = QTreeWidgetItem(self.btn_tree_widget)
        self.btn_tree_widget.setItemWidget(item, 0, i)
        self.btn_tree_widget.setItemWidget(item, 1, j)
        j.toggled.connect(lambda: self.radio_button_clicked(item))
        self.btn_group.addButton(j)
        self.btn_list.append(j)

    def deselected_btn(self):
        self.btn_group.setExclusive(False)
        for i in range(4):
            self.btn_list[i].setChecked(False)
        self.btn_group.setExclusive(True)

class SettingGyro(StWidgetForm):   # 키설정 기울기
    def __init__(self):
        super(SettingGyro, self).__init__()
        self.setTitle("기울기")
        self.gyro_select = QGroupBox()
        self.gyro_insert = QGroupBox()

        self.gyro_dic_roll = {}
        self.gyro_dic_pitch = {}
        self.gyro_dic_yaw = {}

        self.gyro_tree_widget = {}

        #self.create_tree_widget()
        self.db_select_all_gyro()

        self.gyro_list = ['Roll', 'Pitch', 'Yaw']
        self.unselected = []
        #self.h_box.addSpacing(10)
        self.select_gyro_group = QButtonGroup()
        for i in self.gyro_list:
            i = QRadioButton(i)
            i.toggled.connect(self.current_gyro_clicked)
            i.setFixedSize(120, 40)
            i.setStyleSheet("""                                                    
                font-size: 24px;
                padding-left: 15px;
            """)
            self.select_gyro_group.addButton(i)
            self.unselected.append(i)
            self.h_box.addWidget(i)
            self.h_box.addSpacing(20)

        gyro_3D_view_btn = QPushButton('3D 모델 보기')
        gyro_3D_view_btn.setFixedSize(160, 43)
        gyro_3D_view_btn.setStyleSheet("""                                                    
            font-size: 22px;
        """)
        gyro_3D_view_btn.clicked.connect(self.gyro_3D_view_clicked)
        self.h_box.addWidget(gyro_3D_view_btn)

        self.gyro_image = SettingAddDelete()
        btn_add = self.gyro_image.add_image()
        btn_delete = self.gyro_image.delete_image()
        btn_add.clicked.connect(self.add_widget)
        btn_delete.clicked.connect(self.delete_widget)

        self.h_box.addSpacing(20)
        self.h_box.addWidget(btn_add)
        self.h_box.addSpacing(20)
        self.h_box.addWidget(btn_delete)
        self.h_box.addStretch(1)
        self.gyro_select.setLayout(self.h_box)

        self.gyro_insert.setLayout(self.v_box2)

        self.choose_message = QLabel('커스텀과 Pitch, Roll, Yaw 중 하나를 선택해주세요.')
        self.choose_message.setFixedHeight(460)
        self.choose_message.setStyleSheet("""
            font: 30px;
            border-color: transparent;
        """)

        self.v_box.addSpacing(20)
        self.v_box.addWidget(self.gyro_select)
        self.v_box.addSpacing(10)
        self.v_box.addWidget(self.choose_message, alignment=Qt.AlignCenter)
        self.v_box.addWidget(self.gyro_insert)
        #self.v_box3.addLayout(self.v_box)
        #self.v_box3.addWidget(self.choose_message, alignment=Qt.AlignCenter)
        #self.v_box3.addWidget(self.gyro_insert)
        #self.v_box3.addStretch(1)

        self.setLayout(self.v_box)
        self.gyro_select.setStyleSheet("""
            border-color: transparent;
        """)
        self.gyro_insert.setStyleSheet("""
            border-color: transparent;
            QLabel{                      
                border-color: transparent;                         
            }
        """)

    def gyro_3D_view_clicked(self):
        Gyro3DView()

    # Pitch, Roll, Yaw 중 어느게 선택됐는지 확인
    def current_gyro_clicked(self):
        try:
            radio_gyro = self.sender()
            self.choose_message.setVisible(False)
            cumstom_id = CustomDBValue.custom_id

            if radio_gyro.isChecked():
                for index, value in enumerate(self.gyro_list):
                    if value == radio_gyro.text():
                        self.gyro_tree_widget[cumstom_id][index].setVisible(True)
                        self.gyro_page = index
                        CustomDBValue.gyro_page = index
                        #self.v_box2.addWidget(self.gyro_tree_widget[index])
                    else:
                        self.gyro_tree_widget[cumstom_id][index].setVisible(False)
        except:
            self.choose_message.setVisible(True)

    def radio_button_clicked(self, item):
        self.radioBtn = self.sender()
        custom_id = CustomDBValue.custom_id
        index = self.gyro_page
        self.select_item = item
        self.item_index = self.gyro_tree_widget[custom_id][index].indexFromItem(self.select_item, 0)

        # 선택된 인덱스 저장
        CustomDBValue.gyro_id = self.item_index.row()

    # 슬라이더의 최소값  최대값 변경 시 DB에 이 값들을 업데이트 함
    def update_gyro_slider(self, pos, rs_index, item, rs):
        custom_id = CustomDBValue.custom_id
        index = self.gyro_page
        self.select_item = item
        self.item_index = self.gyro_tree_widget[custom_id][index].indexFromItem(self.select_item, 0)
        gyro_id = self.item_index.row()

        if index == 0:  # Roll
            if rs_index == 1:
                RollDB.update_Roll_min(custom_id, gyro_id, rs.getRange()[0])
            elif rs_index == 2:
                RollDB.update_Roll_max(custom_id, gyro_id, rs.getRange()[1])
        elif index == 1:  # Pitch
            if rs_index == 1:  # 최소
                PitchDB.update_Pitch_min(custom_id, gyro_id, rs.getRange()[0])
            elif rs_index == 2:  # 최대
                PitchDB.update_Pitch_max(custom_id, gyro_id, rs.getRange()[1])
        elif index == 2:  # Yaw
            if rs_index == 1:
                YawDB.update_Yaw_min(custom_id, gyro_id, rs.getRange()[0])
            elif rs_index == 2:
                YawDB.update_Yaw_max(custom_id, gyro_id, rs.getRange()[1])

    def add_widget(self):  # 키 설정 추가
        try:
            custom_id = CustomDBValue.custom_id
            index = self.gyro_page
            roll, pitch, yaw = self.gyro_dic_roll[custom_id], self.gyro_dic_pitch[custom_id], self.gyro_dic_yaw[custom_id]
            tree_widget = self.gyro_tree_widget[custom_id]
            # Pitch, Roll, Yaw 중 하나를 선택했다면
            if index == 0:
                roll.append(GyroWidgets())
                gyro_id = len(roll) - 1
                self.add_gyro(roll[-1], tree_widget[0], -90, 90, '입력')
                # DB 연결
                RollDB.insert_Roll(custom_id, gyro_id, -90, 90, '입력')

            elif index == 1:
                pitch.append(GyroWidgets())
                gyro_id = len(pitch) - 1
                self.add_gyro(pitch[-1], tree_widget[1], -90, 90, '입력')
                # DB 연결
                PitchDB.insert_Pitch(custom_id, gyro_id, -90, 90, '입력')

            elif index == 2:
                yaw.append(GyroWidgets())
                gyro_id = len(yaw) - 1
                self.add_gyro(yaw[-1], tree_widget[2], -90, 90, '입력')
                # DB 연결
                YawDB.insert_Yaw(custom_id, gyro_id, -90, 90, '입력')

        except:  # 에러 메시지
            pass
            #msg = QMessageBox()
            #msg.setIcon(QMessageBox.Critical)
            #msg.setText('Custom 을 선택 후 Pitch, Roll, Yaw 중 하나를 선택해주세요.')
            #msg.setWindowTitle("Error")
            #msg.exec_()

    def delete_widget(self):  # 키 설정 삭제
        try:
            custom_id = CustomDBValue.custom_id
            index = self.gyro_page
            roll, pitch, yaw = self.gyro_dic_roll[custom_id], self.gyro_dic_pitch[custom_id], self.gyro_dic_yaw[custom_id]
            tree_widget = self.gyro_tree_widget[custom_id]

            if index == 0 and len(roll) > 0:
                roll_id = len(roll) - 1
                tree_widget[0].takeTopLevelItem(roll_id)
                roll.pop()
                # DB 연결
                RollDB.delete_Roll(custom_id, roll_id)

            elif index == 1 and len(pitch) > 0:
                pitch_id = len(pitch) - 1
                tree_widget[1].takeTopLevelItem(pitch_id)
                pitch.pop()
                # DB 연결
                PitchDB.delete_Pitch(custom_id, pitch_id)

            elif index == 2 and len(yaw) > 0:
                yaw_id = len(yaw) - 1
                tree_widget[2].takeTopLevelItem(yaw_id)
                yaw.pop()
                # DB 연결
                YawDB.delete_Yaw(custom_id, yaw_id)

        except:  # 에러 메시지
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Pitch, Roll, Yaw 중 하나를 선택해주세요.')
            msg.setWindowTitle("Error")
            msg.exec_()

    def add_gyro(self, widgets, tree, min, max, input):
        item = QTreeWidgetItem(tree)
        tree.setItemWidget(item, 0, widgets.rs)
        tree.setItemWidget(item, 1, widgets.radio)

        #self.gyro_tree_widget[index].addTopLevelItem(item)

        widgets.rs.setRange(min, max)
        widgets.radio.setText(input)

        widgets.radio.toggled.connect(lambda: self.radio_button_clicked(item))  # 이벤트 연결
        widgets.rs._splitter.splitterMoved.connect(lambda pos, index: self.update_gyro_slider(pos, index, item, widgets.rs))

    def db_select_all_gyro(self):
        roll_list = RollDB.select_Roll()
        pitch_list = PitchDB.select_Pitch()
        yaw_list = YawDB.select_Yaw()
        custom_list = Setting.select_Setting(self)

        # db에 있는 커스텀의 수 만큼 반복하여 자이로 위젯을 딕셔너리에 삽입함
        for custom_id, name in custom_list:
            # key 값에 리스트 삽입
            self.gyro_dic_roll[custom_id] = []
            self.gyro_tree_widget[custom_id] = []
            self.gyro_dic_pitch[custom_id] = []
            self.gyro_dic_yaw[custom_id] = []

            for i in range(3):  # tree widget 생성
                self.gyro_tree_widget[custom_id].append(self.add_tree_widget())
            # tree_widget[0] == Pitch, tree_widget[1] == Roll, tree_widget[2] == Yaw
            tree_widget = self.gyro_tree_widget[custom_id]

            num = 0
            for i in roll_list:
                if custom_id == i[0]:
                    widgets = GyroWidgets()
                    widgets.rs.show()
                    self.gyro_dic_roll[custom_id].append(widgets)
                    self.add_gyro(self.gyro_dic_roll[custom_id][num], tree_widget[0], i[2], i[3], i[4])
                    num += 1

            num = 0
            for i in pitch_list:
                if custom_id == i[0]:   # db에 저장된 기본키가 custom id인 자이로 값의 수만큼 자이로 위젯을 생성
                    widgets = GyroWidgets()
                    widgets.rs.show()
                    self.gyro_dic_pitch[custom_id].append(widgets)
                    self.add_gyro(self.gyro_dic_pitch[custom_id][num], tree_widget[1], i[2], i[3], i[4])
                    num += 1

            num = 0
            for i in yaw_list:
                if custom_id == i[0]:
                    widgets = GyroWidgets()
                    widgets.rs.show()
                    self.gyro_dic_yaw[custom_id].append(widgets)
                    self.add_gyro(self.gyro_dic_yaw[custom_id][num], tree_widget[2], i[2], i[3], i[4])
                    num += 1

    def custom_selected_gyro(self):  # 커스텀이 선택되면 실행
        try:
            # Pitch, Roll, Yaw 버튼 체크 풀기
            self.select_gyro_group.setExclusive(False)
            for i in range(3):
                self.unselected[i].setChecked(False)
            self.select_gyro_group.setExclusive(True)
            
            # 커스텀을 선택했을 때 자이로 설정대신 메시지가 출력되게 함
            for key in self.gyro_tree_widget.keys():
                tree_widget = self.gyro_tree_widget[key]
                #if key == custom_id:
                    #self.choose_message.setVisible(True)
                for i in range(3):
                    tree_widget[i].setVisible(False)
            self.choose_message.setVisible(True)
        except:
            print('커스텀 선택 오류')

    def custom_add_gyro(self):
        custom_id = Setting.select_Setting(self)[-1][0]
        self.gyro_dic_roll[custom_id] = []
        self.gyro_tree_widget[custom_id] = []
        self.gyro_dic_pitch[custom_id] = []
        self.gyro_dic_yaw[custom_id] = []
        for i in range(3):  # tree widget 생성
            self.gyro_tree_widget[custom_id].append(self.add_tree_widget())

    def custom_delete_gyro(self):
        custom_id = CustomDBValue.custom_id
        del self.gyro_tree_widget[custom_id]
        del self.gyro_dic_roll[custom_id]
        del self.gyro_dic_pitch[custom_id]
        del self.gyro_dic_yaw[custom_id]

    def add_tree_widget(self):
        tree_widget = QTreeWidget()
        tree_widget.setHeaderHidden(True)
        tree_widget.setRootIsDecorated(False)
        tree_widget.setColumnCount(2)
        tree_widget.setColumnWidth(0, 610)
        tree_widget.setColumnWidth(1, 150)
        self.v_box2.addWidget(tree_widget)
        tree_widget.setVisible(False)
        tree_widget.setStyleSheet("""
                        QTreeWidget::item:selected {
                            background-color: transparent;
                        }
                        QTreeWidget::item:hover {
                            background-color: transparent;
                        }
                        QTreeWidget::item { 
                            height: 65px;
                        }
                    """)
        return tree_widget

class GyroWidgets(QWidget):
    def __init__(self, parent=None):
        super(GyroWidgets, self).__init__(parent=parent)

        self.rs = QRangeSlider()
        self.rs.setFixedSize(580, 40)
        self.rs.setStyleSheet("""
            border-radius: 0px;
            margin-right: -20px;
        """)
        self.rs.setBackgroundStyle('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #555, stop:1 #333);')
        self.rs.handle.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgb(0,96,168), stop:1 rgb(0,116,188));')
        self.radio = QRadioButton('입력')
        self.radio.setFixedSize(140, 40)


class Gyro3DView(QDialog):
    def __init__(self, parent=None):
        super(Gyro3DView, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 200, 650, 400)
        self.setWindowTitle("3D 모델")
        self.setStyleSheet("""background-color: #222222;""")
        self.view = Qt3DWindow()
        #self.view.defaultFrameGraph().setClearColor(QColor(0x4d4d4f))
        self.view.defaultFrameGraph().setClearColor(QColor(34, 34, 34))
        container = QWidget.createWindowContainer(self.view)
        screenSize = self.view.screen().size()
        container.setMinimumSize(400, 200)
        container.setMaximumSize(screenSize)

        vbox = QVBoxLayout()
        vbox.addWidget(container, 1)
        self.setLayout(vbox)

        # 루트 엔티티
        self.rootEntity = QEntity()

        self.camera()
        self.light()
        self.gyro_model()
        self.text()

        self.view.setRootEntity(self.rootEntity)

        receive_gyro = threading.Thread(target=self.receive_gyro_data_thread)
        receive_gyro.start()

        self.show()
        #self.exec_()

    def camera(self):
        # 카메라 설정
        self.cameraEntity = self.view.camera()
        self.cameraEntity.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
        self.cameraEntity.setPosition(QVector3D(0, -30, 0))
        self.cameraEntity.setUpVector(QVector3D(0, 0, 0))
        self.cameraEntity.setViewCenter(QVector3D(0, 2, 0))

        # 카메라 컨트롤
        camController = QFirstPersonCameraController(self.rootEntity)
        camController.setCamera(self.cameraEntity)

    def light(self):
        lightEntity = QEntity(self.rootEntity)
        light = QPointLight(lightEntity)
        light.setColor(Qt.white)
        light.setIntensity(1)
        lightEntity.addComponent(light)
        lightTransform = QTransform(lightEntity)
        lightTransform.setTranslation(self.cameraEntity.position())
        lightEntity.addComponent(lightTransform)

    def text(self):
        text = QEntity(self.rootEntity)

        textTransform = QTransform()
        textTransform.setScale(1)
        textTransform.setRotationX(90)
        textTransform.setTranslation(QVector3D(-8, -15, -4))
        self.textMesh = QExtrudedTextMesh()
        self.textMesh.setDepth(0.2)
        font = QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(16)

        self.textMesh.setFont(font)
        self.textMesh.setText('자이로 센서를 연결해주세요.')
        textMaterial = QPhongMaterial(self.rootEntity)
        textMaterial.setDiffuse(QColor(0, 116, 188))

        text.addComponent(self.textMesh)
        text.addComponent(textMaterial)
        text.addComponent(textTransform)

    def gyro_model(self):
        # 3D 모델 설정
        gyroEntity = QEntity(self.rootEntity)

        mesh = QMesh()
        mesh.setSource(QUrl.fromLocalFile("images/robot.obj"))

        material = QPhongMaterial(self.rootEntity)

        self.transform = QTransform()  # import 충돌이 일어나면 오류가 발생함.
        self.transform.setScale(0.4)
        self.rotation = QQuaternion()
        gyroEntity.addComponent(mesh)
        gyroEntity.addComponent(material)
        gyroEntity.addComponent(self.transform)

    def receive_gyro_data_thread(self):
        while True:
            if GyroData.gyro_connecting:
                rpy = GyroData.gyro_rpy
                self.textMesh.setText('     Roll: ' + str(round(rpy[0] )) + '  Pitch: ' + str(round(rpy[1] )) + '  Yaw: ' + str(round(rpy[2] )))
                #self.rotation = self.rotation.fromEulerAngles(rpy[0], rpy[1], rpy[2])
                #self.transform.setRotation(self.rotation)
                self.transform.setRotationX(rpy[0])
                self.transform.setRotationY(rpy[1])
                self.transform.setRotationZ(rpy[2])
            sleep(0.001)

class SettingIRCamera(StWidgetForm):  # 키설정 IR카메라
    def __init__(self):
        super(SettingIRCamera, self).__init__()
        self.setTitle("IR 카메라")

        self.ir_tree_widget = {}
        self.ircamera_dic = {}
        self.rect_dic = {}

        self.ir_video = QLabel()  # 카메라 영상
        #self.ir_video.setVisible(False)
        self.ir_video.setStyleSheet("""
            border-color: black;
        """)

        self.ircamera = threading.Thread(target=self.ircamera_thread)
        self.ircamera.start()

        self.db_select_all_camera()

        #self.v_box2.addWidget(self.ir_tree_widget)

        self.v_box3.addSpacing(50)
        self.v_box3.addLayout(self.v_box2)
        #self.v_box3.addStretch(1)

        self.choose_message = QLabel('커스텀을 선택해주세요.')
        self.choose_message.setStyleSheet("""
                    font: 30px;
                    padding-top: 220%;
                    padding-bottom: 220%;
                    border-color: transparent;
                """)

        self.v_box.addSpacing(50)
        self.v_box.addWidget(self.ir_video)
        #self.v_box.addWidget(self.choose_message, alignment=Qt.AlignCenter)
        self.v_box.addStretch(1)

        self.h_box.addSpacing(10)
        #self.h_box.addWidget(self.choose_message, alignment=Qt.AlignCenter)
        self.h_box.addLayout(self.v_box)
        self.h_box.addSpacing(10)
        self.h_box.addLayout(self.v_box3)
        #self.h_box.addSpacing(10)
        self.h_box.addStretch(1)

        self.v_box4.addWidget(self.choose_message, alignment=Qt.AlignCenter)
        self.v_box4.addLayout(self.h_box)
        self.setLayout(self.v_box4)

        self.begin = QPoint()  # 생성할 사각형의 시작 좌표
        self.end = QPoint()  # 생성할 사각형의 끝 좌표
        self.drag_begin = QPoint()  # 드래그시 생성할 사각형의 시작 좌표
        self.drag_end = QPoint()  # 드래그시 생성할 사각형의 끝 좌표

        # 영상의 좌표를 알기위해 이벤트 처리
        self.ir_video.mousePressEvent = self.mousePressEvent
        self.ir_video.mouseMoveEvent = self.mouseMoveEvent
        self.ir_video.mouseReleaseEvent = self.mouseReleaseEvent
        
        self.setStyleSheet("""
            QTreeWidget::item:selected {
                background-color: transparent;
            }
            QTreeWidget::item:hover {
                background-color: transparent;
            }
            QTreeWidget::item { 
                height: 80px;
            }
        """)

    def radio_button_clicked(self, item):
        self.radioBtn = self.sender()
        custom_id = CustomDBValue.custom_id
        self.select_item = item
        self.item_index = self.ir_tree_widget[custom_id][0].indexFromItem(self.select_item, 0)

        # 선택된 인덱스 저장
        CustomDBValue.camera_id = self.item_index.row()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.begin = event.pos()
            self.end = event.pos()
            self.update()
            self.drag_bool = True
        elif event.button() == Qt.RightButton:  # 마우스 우 클릭시 위젯을 삭제하고 드래그로 사각형을 생성하지 못하게함
            self.delete_widget()
            self.drag_bool = False

    def mouseMoveEvent(self, event):
        if self.drag_bool:
            self.end = event.pos()
            self.drag_begin = self.begin
            self.drag_end = self.end
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_begin = QPoint(0, 0)
            self.drag_end = QPoint(0, 0)
            self.end = event.pos()
            self.update()
            if self.begin.x() < 560 and self.begin.y() < 440:  # 영상의 범위안에서만 위젯을 추가하게 설정
                self.add_widget()


    def ircamera_thread(self):  # IR 카메라 영상 받아옴
        temp = IRCameraData()
        while True:  # 이미지를 계속받아옴
            try:
                if temp.ir_connecting:
                    image = temp.ir_image
                    h, w, c = image.shape
                    qImg = QImage(image, w, h, w * c, QImage.Format_RGB888)
                    self.pixmap = QPixmap.fromImage(qImg)
                    self.drag_rect_draw()
                    self.rect_draw()
                    sleep(0.01)  # 에러발생 방지를 위해 슬립
                    self.ir_video.setPixmap(self.pixmap)  # 화면에 출력
                else:
                    sleep(2)
            except:
                pass

    def add_widget(self):
        custom_id = CustomDBValue.custom_id
        tree_widget = self.ir_tree_widget[custom_id][0]
        camera, rect = self.ircamera_dic[custom_id], self.rect_dic[custom_id]
        camera.append(IRCametaWidgets())
        rect.append([self.begin, self.end])
        camera_id = len(camera) - 1
        self.add_camera(camera[-1], tree_widget, camera_id + 1, '입력')
        # DB 연결
        Camera.insert_Camera(custom_id, camera_id, self.begin.x(), self.begin.y(), self.end.x(), self.end.y(), '입력')

    def delete_widget(self):
        custom_id = CustomDBValue.custom_id
        tree_widget = self.ir_tree_widget[custom_id][0]
        camera, rect = self.ircamera_dic[custom_id], self.rect_dic[custom_id]

        if len(rect) > 0 and len(camera) > 0:
            camera_id = len(camera) - 1
            tree_widget.takeTopLevelItem(camera_id)
            rect.pop()
            camera.pop()
            # DB 연결
            Camera.delete_Camera(custom_id, camera_id)

    def rect_draw(self):
        custom_id = CustomDBValue.custom_id
        if len(self.rect_dic[custom_id]) > 0:
            painter_instance = QPainter(self.pixmap)
            pen_rectangle = QPen(Qt.blue)
            painter_instance.setPen(pen_rectangle)

            font = QFont()
            font.setFamily('Times')
            font.setBold(True)
            font.setPointSize(16)
            painter_instance.setFont(font)

            j = 0
            for i in self.rect_dic[custom_id]:
                j += 1
                painter_instance.drawRect(QRect(i[0], i[1]))
                painter_instance.drawText(i[0], str(j))
                # print('좌표정보:', i[0], i[1])

    def drag_rect_draw(self):
        try:
            painter_instance = QPainter(self.pixmap)
            pen_rectangle = QPen(Qt.blue)
            painter_instance.setPen(pen_rectangle)
            painter_instance.drawRect(QRect(self.drag_begin, self.drag_end))

        except:
            pass

    def db_select_all_camera(self):
        custom_list = Setting.select_Setting(self)
        camera_list = Camera.select_Camera()
        # db에 있는 커스텀의 수 만큼 반복하여 자이로 위젯을 딕셔너리에 삽입함
        for custom_id, name in custom_list:
            # key 값에 리스트 삽입
            self.ir_tree_widget[custom_id] = []
            self.ir_tree_widget[custom_id].append(self.add_tree_widget())
            self.ircamera_dic[custom_id] = []
            self.rect_dic[custom_id] = []

            tree_widget = self.ir_tree_widget[custom_id][0]
            num = 0
            for i in camera_list:
                if custom_id == i[0]:  # db에 저장된 기본키가 custom id인 자이로 값의 수만큼 자이로 위젯을 생성
                    self.ircamera_dic[custom_id].append(IRCametaWidgets())
                    self.rect_dic[custom_id].append([QPoint(i[2], i[3]), QPoint(i[4], i[5])])
                    self.add_camera(self.ircamera_dic[custom_id][num], tree_widget, num + 1, i[6])
                    num += 1

    def add_camera(self, widgets, tree, num, input):
        item = QTreeWidgetItem(tree)
        tree.setItemWidget(item, 0, widgets.label)
        tree.setItemWidget(item, 1, widgets.radio)

        widgets.label.setText(str(num))
        widgets.radio.setText(input)
        widgets.radio.toggled.connect(lambda: self.radio_button_clicked(item))  # 이벤트 연결

    def custom_selected_ircamera(self, tree_widget):
        item = tree_widget.currentItem()
        index = tree_widget.indexFromItem(item)
        custom_id = Setting.select_Setting(self)[index.row()][0]

        self.choose_message.setVisible(False)
        self.ir_video.setVisible(True)
        for key in self.ir_tree_widget.keys():
            tree_widget = self.ir_tree_widget[key][0]
            if key == custom_id:
                tree_widget.setVisible(True)
            else:
                tree_widget.setVisible(False)

    def custom_add_ircamera(self):
        custom_id = Setting.select_Setting(self)[-1][0]
        self.ir_tree_widget[custom_id] = []
        self.ir_tree_widget[custom_id].append(self.add_tree_widget())
        self.ircamera_dic[custom_id] = []
        self.rect_dic[custom_id] = []

    def custom_delete_ircamera(self):
        custom_id = CustomDBValue.custom_id
        del self.ir_tree_widget[custom_id]
        del self.ircamera_dic[custom_id]
        del self.rect_dic[custom_id]

    def add_tree_widget(self):
        tree_widget = QTreeWidget()
        tree_widget.setHeaderHidden(True)
        tree_widget.setRootIsDecorated(False)
        tree_widget.setColumnCount(2)
        tree_widget.setColumnWidth(0, 30)
        tree_widget.setColumnWidth(1, 150)
        self.v_box2.addWidget(tree_widget)
        tree_widget.setVisible(False)
        tree_widget.setStyleSheet("""
                        QTreeWidget::item:selected {
                            background-color: transparent;
                        }
                        QTreeWidget::item:hover {
                            background-color: transparent;
                        }
                        QTreeWidget::item { 
                            height: 65px;
                        }
                    """)
        return tree_widget


class IRCametaWidgets(QWidget):
    def __init__(self, parent=None):
        super(IRCametaWidgets, self).__init__(parent=parent)

        #self.box = QHBoxLayout()
        #self.box.addStretch(1)
        self.label = QLabel('0')
        self.label.setFixedHeight(40)
        self.label.setStyleSheet("""
            border-color: transparent;
            font-size: 25px;
            color: rgb(0, 116, 188);
        """)
        self.radio = QRadioButton('입력')
        self.radio.setFixedSize(140, 40)

        #self.box.addWidget(self.label)
        #self.box.addWidget(self.radio)


class SettingAddDelete:
    def __init__(self):
        self.stack = []

    def add_image(self):
        add_button = QPushButton()
        add_button.setIcon(QIcon('images/plus.png'))
        add_button.setIconSize(QSize(35, 35))
        return add_button

    def delete_image(self):
        delete_button = QPushButton()
        delete_button.setIcon(QIcon('images/minus.png'))
        delete_button.setIconSize(QSize(35, 35))
        return delete_button

    def menu_image(self):
        menu_button = QPushButton()
        menu_button.setIcon(QIcon('images/menu.png'))
        menu_button.setIconSize(QSize(10, 10))
        return menu_button


class KeyList:
    key_code_dic = {
        112: 'F1', 113: 'F2', 114: 'F3', 115: 'F4', 116: 'F5', 117: 'F6',
        118: 'F7', 119: 'F8', 120: 'F9', 121: 'F10', 122: 'F11', 123: 'F12',
        9: 'Tab', 20: 'CapsLock', 16: 'Shift', 27: 'Escape', 13: 'Enter',
        17: 'CtrlLeft', 25: 'CtrlRight', 18: 'Alt', 8: 'Backspace', 32: 'Space',
        145: 'ScrollLock', 19: 'Pause', 45: 'Insert', 36: 'Home', 33: 'PgUp',
        46: 'Delete', 35: 'End', 34: 'PgDn', 37: 'Left', 39: 'Right', 38: 'Up', 40: 'Down',
        96: 'Num0', 97: 'Num1', 98: 'Num2', 99: 'Num3', 100: 'Num4', 101: 'Num5', 102: 'Num6',
        103: 'Num7', 104: 'Num8', 105: 'Num9', 144: 'NumLock'
    }
