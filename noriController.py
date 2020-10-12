import sys
import multiprocessing
from ui import *
from NORIDB import *
import threading
from time import sleep
from bluetooth import *
import cv2
import imagezmq
import pyautogui as pag
import pydirectinput as pdi  # pyautogui가 안먹힐 때 사용
import numpy as np

hsv = 0
lower_blue1 = 0
upper_blue1 = 0
lower_blue2 = 0
upper_blue2 = 0
lower_blue3 = 0
upper_blue3 = 0

class BlueConnecting(threading.Thread):
    def run(self):
        self.server_sock = BluetoothSocket(RFCOMM)  # RFCOMM 프로토콜로 블루투스 소켓 생성
        self.server_sock.bind(("", PORT_ANY))  # 소켓에 아무 포트번호나 지정
        self.server_sock.listen(1)  # 1개의 접속 요청을 기다림

        port = self.server_sock.getsockname()[1]  # 소켓에 지정된 포트번호 가져오기

        # SDP에서 서비스의 종류를 구분하기 위해 사용. 서버-클라이언트가 같아야 함.
        uuid = "00000004-0000-1000-8000-00805F9B34FB"

        # 블루투스 서비스 등록
        advertise_service(self.server_sock, "SampleServer",
                        service_id=uuid,
                        service_classes=[uuid, SERIAL_PORT_CLASS],
                        profiles=[SERIAL_PORT_PROFILE],
                        )
        print("RFCOMM %d번 port에서 연결 대기중" % port)

        # 접속 요청 승인후 클라이언트와 통신할 전용 소켓 생성
        sock, client_info = self.server_sock.accept()
        print("연결된 클라이언트의 정보:", client_info)

        BlueData.blue_connecting = True
        BlueData.blue_Mac = client_info[0]
        BlueData.blue_port = str(client_info[1])
        self.send_message(sock)
        receiveMessage = threading.Thread(target=self.receive_thread, args=(sock,))
        receiveMessage.start()
        
    def receive_thread(self, sock):
        while True:
            try:
                data = sock.recv(4)
                length = int.from_bytes(data, "little")
                data = sock.recv(length)
                message = data.decode('utf-8')
                if 'wifi' in message:
                    if 'None' in message:
                        WiFiData.wifi_list = 'Fail'
                    else:
                        wifi_list = message.split(':')[1]
                        wifi_list = wifi_list.split(',')
                        WiFiData.wifi_connecting = True
                        WiFiData.wifi_list = wifi_list

                else:
                    rpy_list = message.split(',')  # 받은 문자열을 ','을 기준으로 나눠 리스트에 넣기
                    #print('roll:' + rpy_list[0] + ' pitch:' + rpy_list[1] + ' raw:' + rpy_list[2])
                    rpy = list(map(float, rpy_list))  # 문자열 리스트를 float형으로 변환
                    #rpy = list(map(int, rpy_list))  # 문자열 리스트를 float형으로 변환
                    #print('Roll: ', rpy[0], 'Pitch: ', rpy[1], 'Yaw: ', rpy[2])
                    GyroData.gyro_connecting = True
                    GyroData.gyro_rpy = rpy
                    #sleep(0.001)
            except:
                print('수신오류')
                sleep(2)

    def send_message(self, sock):
        wifi = WiFiInformation()
        if wifi.wifi_state == 'on':
            message = 'wifi:' + wifi.ssid + ',' + wifi.pw + ',' + wifi.ip_address
            length = len(message)
            sock.send(length.to_bytes(4, byteorder="little"))
            sock.send(message.encode('utf-8'))
        else:
            message = 'not connected'
            length = len(message)
            sock.send(length.to_bytes(4, byteorder="little"))
            sock.send(message.encode('utf-8'))

class IRCameraConnecting(threading.Thread):
    def run(self):
        image_hub = imagezmq.ImageHub()  # ImageHub()  클래스 이니셜라이즈
        while True:  # 이미지를 계속받아옴
            rpi_name, image = image_hub.recv_image()  # 이미지받아오면
            image = cv2.resize(image, (560, 440))
            IRCameraData.ir_text = rpi_name
            IRCameraData.ir_image = image  # 이미지를 출력하기 위해 전달
            IRCameraData.ir_connecting = True

            cv2.waitKey(1)
            image_hub.send_reply(b'OK')  # 라즈베리 파이쪽에 응답 받았다 'OK'
            #
            sleep(0.001)


class GyroKeyInput(threading.Thread):
    input_list = []

    def __init__(self, eno, GyroData):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()  # 정지 이벤트

        self.GyroData = GyroData  # roll, pitch, yaw 값들을 받아옴

        # DB에서 설정한 값들을 가져옴
        self.roll_list = RollDB.select_Roll_eno(eno)
        self.pitch_list = PitchDB.select_Pitch_eno(eno)
        self.yaw_list = YawDB.select_Yaw_eno(eno)

    def stop(self):
        self.stop_event.set()  # 스레드 정지 신호
        self.join()  # 정지되기까지 기다리기
        
    def run(self):
        # DB에 저장된 키만틈 input_list에 False를 추가해줌. -> False가 아닌 키를 입력하게 하기위함.
        for i in range(len(self.roll_list)):
            self.input_list.append(False)
        for i in range(len(self.pitch_list)):
            self.input_list.append(False)
        for i in range(len(self.yaw_list)):
            self.input_list.append(False)

        self.gyro_thread(self.roll_list)
        self.gyro_thread(self.pitch_list)
        self.gyro_thread(self.yaw_list)

        while not self.stop_event.is_set():
            if self.GyroData.gyro_connecting:
                rpy = self.GyroData.gyro_rpy
                key_index = 0
                for i in self.roll_list:
                    self.gyro_range_check(key_index, rpy[0], i[2], i[3], i[4].lower())
                    key_index += 1

                for i in self.pitch_list:
                    self.gyro_range_check(key_index, rpy[1], i[2], i[3], i[4].lower())
                    key_index += 1

                for i in self.yaw_list:
                    self.gyro_range_check(key_index, rpy[2], i[2], i[3], i[4].lower())
                    key_index += 1
            else:
                print('자이로 센서가 연결 되지 않음.')
                sleep(2)

    # press_key라는 리스트에 False가 아니면 키가 입력되게 하는 스레드를 시작하는 함수


    def gyro_thread(self, list):
        for i in list:
            input = i[4].lower()
            if '클릭' in input:
                mouse_click = threading.Thread(target=self.mouse_click_thread, args=(input,))
                mouse_click.start()
            elif '이동' in input:
                mouse_move = threading.Thread(target=self.mouse_move_thread, args=(input,))
                mouse_move.start()
            elif '+' in input:  # 단축키(키가 2개)인 경우
                inputs = input.split('+')
                hotkey_press = threading.Thread(target=self.hotkey_press_thread, args=(inputs[0], inputs[1]))
                hotkey_press.start()
            else:
                key_press = threading.Thread(target=self.key_press_thread, args=(input,))
                key_press.start()

    # 설정한 범위안에 값이 들오오면 리스트에 키를 넣고 아니라면 False 를 넣음(동시에 키가 입력되게 하기 위해)
    def gyro_range_check(self, index, rpy, min, max, input):
        if rpy >= min and rpy <= max:
            self.input_list[index] = input
        else:
            self.input_list[index] = False

    # 리스트 press_key안에 False가 아닌 key가 들어있다면 그 key를 입력
    def key_press_thread(self, input):
        print('키보드 프레스 실행')
        while not self.stop_event.is_set():
            while input in self.input_list:
                if self.stop_event.is_set():
                    break
                pdi.keyDown(input)
                # 키를 계속 입력해주기 위해 범위를 벗어날을 때 keyUp을 해준다.
                if input not in self.input_list:
                    pdi.keyUp(input)
                    break
            sleep(0.001)  # 슬립을 살짝 걸어줘야 ui에서의 속도가 빠름

    # 단축키일 경우 키 입력
    def hotkey_press_thread(self, input1, input2):
        print('키보드 단축키 실행')
        key = input1+'+'+input2
        while not self.stop_event.is_set():
            while key in self.input_list:
                if self.stop_event.is_set():
                    break
                pdi.keyDown(input1)
                pdi.keyDown(input2)
                # 키를 계속 입력해주기 위해 범위를 벗어날을 때 keyUp을 해준다.
                if key not in self.input_list:
                    pdi.keyUp(input1)
                    pdi.keyUp(input2)
                    break
            sleep(0.001)

    # 마우스 키 입력 스레드
    def mouse_click_thread(self, input):
        print('마우스 클릭 실행')
        if input == '왼쪽 클릭':
            button = 'left'
        elif input == '오른쪽 클릭':
            button = 'right'
        elif input == '스크롤 클릭':
            button = 'middle'

        while not self.stop_event.is_set():
            while input in self.input_list:
                if self.stop_event.is_set():
                    break

                pdi.mouseDown(button=button)
                # 범위를 벗어날을 때 mouseUp을 해준다.
                if input not in self.input_list:
                    pdi.mouseUp(button=button)
                    break
            sleep(0.001)  # 슬립을 살짝 걸어줘야 ui에서의 속도가 빠름

    # 마우스 이동 스레드
    def mouse_move_thread(self, input):
        print('마우스 무브 실행')
        if input == '위로 이동':
            x, y = 0, 40
        elif input == '아래로 이동':
            x, y = 0, -40
        elif input == '좌측으로 이동':
            x, y = 40, 0
        elif input == '우측으로 이동':
            x, y = -40, 0

        while not self.stop_event.is_set():
            while input in self.input_list:
                if self.stop_event.is_set():
                    break

                pdi.move(x, y, 0.001)
                # 범위를 벗어나면 break
                if input not in self.input_list:
                    break
            sleep(0.001)  # 슬립을 살짝 걸어줘야 ui에서의 속도가 빠름

class CamerakeyInput(threading.Thread):
    input_list=[]

    def __init__(self, eno, IRCameraData):
        threading.Thread.__init__(self)
        # 기본키로 카메라DB 정보를 가져옵니다
        self.rs = Camera.select_Camera_eno(eno)
        self.camera_list = Camera.select_Camera_eno(eno)
        print(self.camera_list)
        print(len(self.camera_list))
        self.IRCameraData = IRCameraData
        self.stop_event = threading.Event()
        print("구간1")
        for i in range(len(self.camera_list)):
            self.IRCameraData.ir_color.append(0)

        print(self.IRCameraData.ir_color[0])


    def stop(self):
        self.stop_event.set()
        self.join()

    def run(self):
        for i in range(len(self.camera_list)):
            self.input_list.append(False)

        sleep(1)
        #self.DBplay_camera()
        #self.camera_image_fix()
        t1=threading.Thread(target=self.DBplay_camera)
        t1.start()
        goo = threading.Thread(target=self.camera_key_press)
        goo.start()
        self.camera_thread(self.camera_list)

    def camera_image_fix(self):
        goo = threading.Thread(target=self.DBplay_camera, args=())
        goo.start()

    def camera_key_press_thread(self):
        goo = threading.Thread(target=self.camera_key_press, args=())
        goo.start()


    def camera_key_press(self):
        while True:
            color = self.IRCameraData.ir_color
            #print('camera_key_press : ',color)
            if self.IRCameraData.ir_connecting and not color == []:
                key_index = 0
                for i in self.camera_list:
                    self.camera_range_check(key_index, color[key_index], 20, 170, i[6].lower())
                    key_index =key_index+1
            else:
                print('카메라 센서연결전')
                sleep(1)

    def camera_thread(self,list):

        for i in list:
            input = i[6].lower()
            if '클릭' in input:
                mouse_click = threading.Thread(target=self.mouse_click_thread, args=(input,))
                mouse_click.start()
            elif '이동' in input:
                mouse_move = threading.Thread(target=self.mouse_move_thread, args=(input,))
                mouse_move.start()
            elif '+' in input:  # 단축키(키가 2개)인 경우
                inputs = input.split('+')
                hotkey_press = threading.Thread(target=self.hotkey_press_thread, args=(inputs[0], inputs[1]))
                hotkey_press.start()
            else:
                key_press = threading.Thread(target=self.key_press_thread, args=(input,))
                key_press.start()

    # 설정한 범위안에 값이 들오오면 리스트에 키를 넣고 아니라면 False 를 넣음(동시에 키가 입력되게 하기 위해)
    def camera_range_check(self, index, color, min, max, input):
        #print(self.input_list[0])
        if color >= min and color <= max:
            self.input_list[index] = input
        else:
            self.input_list[index] = False

    # 리스트 press_key안에 False가 아닌 key가 들어있다면 그 key를 입력
    def key_press_thread(self, input):
        print('키보드 프레스 실행')
        while not self.stop_event.is_set():
            while input in self.input_list:
                #if self.stop_event.is_set():
                #    break
                pdi.keyDown(input)
                # 키를 계속 입력해주기 위해 범위를 벗어날을 때 keyUp을 해준다.
                if input not in self.input_list:
                    pdi.keyUp(input)
                    break
            sleep(0.001)  # 슬립을 살짝 걸어줘야 ui에서의 속도가 빠름

    # 단축키일 경우 키 입력
    def hotkey_press_thread(self, input1, input2):
        print('키보드 단축키 실행')
        key = input1 + '+' + input2
        while True:
            while key in self.input_list:
                pdi.keyDown(input1)
                pdi.keyDown(input2)
                # 키를 계속 입력해주기 위해 범위를 벗어날을 때 keyUp을 해준다.
                if key not in self.input_list:
                    pdi.keyUp(input1)
                    pdi.keyUp(input2)
                    break
            sleep(0.001)

    # 마우스 키 입력 스레드
    def mouse_click_thread(self, input):
        print('마우스 클릭 실행')
        if input == '왼쪽 클릭':
            button = 'left'
        elif input == '오른쪽 클릭':
            button = 'right'
        elif input == '스크롤 클릭':
            button = 'middle'

        while True:
            while input in self.input_list:

                pdi.mouseDown(button=button)
                # 범위를 벗어날을 때 mouseUp을 해준다.
                if input not in self.input_list:
                    pdi.mouseUp(button=button)
                    break
            sleep(0.001)  # 슬립을 살짝 걸어줘야 ui에서의 속도가 빠름

    # 마우스 이동 스레드
    def mouse_move_thread(self, input):
        print('마우스 무브 실행')
        if input == '위로 이동':
            x, y = 0, 40
        elif input == '아래로 이동':
            x, y = 0, -40
        elif input == '좌측으로 이동':
            x, y = 40, 0
        elif input == '우측으로 이동':
            x, y = -40, 0

        while True:
            while input in self.input_list:

                pdi.move(x, y, 0.001)
                # 범위를 벗어나면 break
                if input not in self.input_list:
                    break
            sleep(0.001)  # 슬립을 살짝 걸어줘야 ui에서의 속도가 빠름

    def nothing(self):
        pass

    def mouse_callback(self, event, x, y, flags, param):
        global hsv, lower_blue1, upper_blue1, lower_blue2, upper_blue2, lower_blue3, upper_blue3, threshold
        # 마우스 왼쪽 버튼 누를시 위치에 있는 픽셀값을 읽어와서 HSV로 변환합니다.
        if event == cv2.EVENT_LBUTTONDOWN:
            print(img_color[y, x])
            color = img_color[y, x]
            one_pixel = np.uint8([[color]])
            hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
            hsv = hsv[0][0]

            threshold = cv2.getTrackbarPos('threshold', 'img_result')
            # HSV 색공간에서 마우스 클릭으로 얻은 픽셀값과 유사한 필셀값의 범위를 정합니다.
        if hsv[0] < 10:
            print("case1")
            lower_blue1 = np.array([hsv[0] - 10 + 180, threshold, threshold])
            upper_blue1 = np.array([180, 255, 255])
            lower_blue2 = np.array([0, threshold, threshold])
            upper_blue2 = np.array([hsv[0], 255, 255])
            lower_blue3 = np.array([hsv[0], threshold, threshold])
            upper_blue3 = np.array([hsv[0] + 10, 255, 255])
            #     print(i-10+180, 180, 0, i)
            #     print(i, i+10)

        elif hsv[0] > 170:
            print("case2")
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            upper_blue1 = np.array([180, 255, 255])
            lower_blue2 = np.array([0, threshold, threshold])
            upper_blue2 = np.array([hsv[0] + 10 - 180, 255, 255])
            lower_blue3 = np.array([hsv[0] - 10, threshold, threshold])
            upper_blue3 = np.array([hsv[0], 255, 255])
            #     print(i, 180, 0, i+10-180)
            #     print(i-10, i)
        else:
            print("case3")
            lower_blue1 = np.array([hsv[0], threshold, threshold])
            upper_blue1 = np.array([hsv[0] + 10, 255, 255])
            lower_blue2 = np.array([hsv[0] - 10, threshold, threshold])
            upper_blue2 = np.array([hsv[0], 255, 255])
            lower_blue3 = np.array([hsv[0] - 10, threshold, threshold])
            upper_blue3 = np.array([hsv[0], 255, 255])
            #     print(i, i+10)
            #     print(i-10, i)

        print(hsv[0])
        print("@1", lower_blue1, "~", upper_blue1)
        print("@2", lower_blue2, "~", upper_blue2)
        print("@3", lower_blue3, "~", upper_blue3)

    def DBplay_camera(self):
        cv2.namedWindow('raspberrypi')
        cv2.setMouseCallback('raspberrypi', self.mouse_callback)

        # 결과를 보여주는 윈도우생성
        cv2.namedWindow('img_result')
        # 트랙바
        cv2.createTrackbar('threshold', 'img_result', 0, 255, CamerakeyInput.nothing)
        # 트랙바 위치
        cv2.setTrackbarPos('threshold', 'img_result', 30)
        while True:
            global img_color, img_mask, img_result, i, color

            ret = self.IRCameraData.ir_text
            img_color = cv2.flip(self.IRCameraData.ir_image, 1)

            # ret, img_color = cap.read()
            height, width = img_color.shape[:2]
            img_color = cv2.resize(img_color, (width, height), interpolation=cv2.INTER_AREA)

            # 원본 영상을 HSV 영상으로 변환합니다.
            img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)

            # 범위 값으로 HSV 이미지에서 마스크를 생성합니다.
            img_mask1 = cv2.inRange(img_hsv, lower_blue1, upper_blue1)
            img_mask2 = cv2.inRange(img_hsv, lower_blue2, upper_blue2)
            img_mask3 = cv2.inRange(img_hsv, lower_blue3, upper_blue3)
            img_mask = img_mask1 | img_mask2 | img_mask3

            # 영상 잡티제거 모폴리지연산
            kernel = np.ones((11, 11), np.uint8)

            # 물체에생긴 검은 구멍을 매움 - 검은구멍 : 조명이 밝거나 어두울경우 생김
            img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel)
            img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel)

            img_result = cv2.bitwise_and(img_color, img_color, mask=img_mask)

            # 사이즈 크기 클수록 딜레이 늘어남 현재 500 X 500
            img_result = cv2.resize(img_result, (500, 500))

            for i in range(len(self.rs)):
                roi1 = img_result[self.rs[i][3]:self.rs[i][5],
                       self.rs[i][2]:self.rs[i][4]]  # 파란 사격형의 범위를 roi에 대입
                rec1 = cv2.rectangle(img_result, (self.rs[i][2], self.rs[i][3]),
                                     (self.rs[i][4], self.rs[i][5]),
                                     (255, 0, 0), 5)

                #if roi1 == []:
                #    print('패스')
                #    pass
                #
                #else:
                roi1 = cv2.medianBlur(roi1, 3)  # 해석 필요
                hsv1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv1)  # 색상 채도 명도를 나눔

                #self.IRCameraData.ir_color = h.mean()  # 색상의 평균 값을 추출
                self.IRCameraData.ir_color[i]=h.mean()
                #IRCameraData.ir_color = self.IRCameraData.ir_color
                print("사각형 검출값", i + 1, "번째:", self.IRCameraData.ir_color[i])  # 범위안에 색상 값 출력

                #CamerakeyInput.color3 = self.IRCameraData.ir_color
            cv2.imshow(ret, img_color)
            cv2.imshow('img_mask', img_mask)
            cv2.imshow('img_result', img_result)
            cv2.waitKey(1)

            #        if (self.IRCameraData.ir_color > 20 and self.IRCameraData.ir_color < 150):
            #            pag.keyDown(self.rs[i][6])
            #            pag.keyUp(self.rs[i][6])

class WiFiInformation:
    def __init__(self):
        try:
            self.ssid = os.popen('netsh wlan show interfaces').read()
            self.ssid = self.ssid.split('SSID')[1].split(': ')[1].split('\n')[0].rstrip()

            self.pw = os.popen('netsh wlan show  profiles ' + self.ssid + ' Key = clear').read()
            self.pw = self.pw.split('키 콘텐츠')[1].split(': ')[1].split('\n')[0]

            self.ip_address = os.popen('ipconfig').read()
            self.ip_address = self.ip_address.split('Wi-Fi')[1].split('IPv4 주소')[1].split('서브넷 마스크')[0].split(': ')[1].rstrip()

            self.wifi_state = 'on'
            print('연결된 와이파이의 정보: ', self.ssid, ' ', self.pw, ' ', self.ip_address)

        except:
            print('WiFi를 연결해주세요.')
            self.wifi_state = 'off'


if __name__ == '__main__':
    #poll = multiprocessing.Pool(processes=4)
    #poll.close()

    #WiFiInformation()

    blue_connnect = BlueConnecting()
    blue_connnect.start()

    ir_camera = IRCameraConnecting()
    ir_camera.start()

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

