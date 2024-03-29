# NoriController
 
 <br/>
 <br/>

```
## 버전정보 Python 3.7.3
```

##### 라즈베리파이와 센서를 이용한  데스크탑 기반 무선컨트롤러 프로젝트



##### * 사진을 클릭하면 영상이 실행됩니다.

[![Nori Controller Video](https://img.youtube.com/vi/WPgMmYe8V9c/0.jpg )](https://www.youtube.com/watch?v=WPgMmYe8V9c)


## 시연영상 (youtube) : "https://www.youtube.com/watch?v=WPgMmYe8V9c"
## 상세설명 (youtube) : "https://www.youtube.com/watch?v=t_fK7xvhH1s"


</br>
</br>


코드리뷰 
---------------------- 
```
### 1.카메라센서 
###    -카메라 송수신(라즈베리파이(클라이언트) ---->  윈도우프로그램(서버))
###    -카메라 키설정 
### 2.윈도우프로그램 UI 
```
 


### -카메라 송수신

 #### __IRCameraServer.py__
 
 ```
 
 카메라 영상을 수신받기 위해 imagezmq를 사용한다. 
 또한 다른 프로세스가 자원을 사용할 수 있게 메모리 쉐어로 자원을 공유한다.
 ```
 
 ```
 class IRCameraServer(threading.Thread):
    def run(self):
        image_hub = imagezmq.ImageHub()  # ImageHub()  클래스 이니셜라이즈

        # 프로세스끼리 자원을 공유할 수 있게 메모리에 등록(메모리 쉐어)
        manager = Manager()
        image_memory = manager.list()
        image_memory.append(False)  # 연결 상태
        image_memory.append(None)  # 이미지

        IRCameraData.ir_camera_memory = image_memory

        while True:  # 이미지를 계속받아옴
            rpi_name, image = image_hub.recv_image()  # 이미지받아오면
            image = cv2.resize(image, (560, 440))
            image = cv2.flip(image, 1)
            image_memory[0] = True  # 연결 상태 저장
            image_memory[1] = image # 이미지 저장

            cv2.waitKey(1)
            image_hub.send_reply(b'OK')  # 라즈베리 파이쪽에 응답 받았다 'OK'
            #sleep(0.001)
```

 #### __IRCameraClient.py__
 
 ```
  카메라 영상을 송신하기 위해 imagezmq를 사용한다.
  ```
  
  ```
  class IRCameraClient(threading.Thread):
	def __init__(self, wifi_ip):
		threading.Thread.__init__(self)
		self.ip_address = wifi_ip: # 블루투스 통신으로 수신 받은 PC의 IP 주소

	def run(self):
		# 카메라 영상 송신
		sender = imagezmq.ImageSender(connect_to='tcp://' + self.ip_address + ':5555')  # ImageSender 초기화 해서 5555포트로 접속 한다
		rpi_name = socket.gethostname()  # 각 이미지와 함께 RPi 호스트 이름 송신
		picam = VideoStream(usePiCamera=True).start()
		time.sleep(2.0)

                # 카메라로 찍은 이미지를 계속 송신한다.
		while True:
			image = picam.read()  
			sender.send_image(rpi_name, image)
			time.sleep(0.001)
   ```
   
  ### -카메라 키설정 
  #### __CamerakeyInput.py__
   ```
    class IRCameraConnecting(threading.Thread):
          ...
     def mouse_callback(self, event, x, y, flags, param):
       
        # 마우스 왼쪽 버튼 누를시 위치에 있는 픽셀값을 읽어와서 HSV로 변환합니다.
        if event == cv2.EVENT_LBUTTONDOWN:
            print(img_color[y, x])
            color = img_color[y, x]
            one_pixel = np.uint8([[color]])
            hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
            hsv = hsv[0][0]

            threshold = cv2.getTrackbarPos('threshold', 'img_result')
         ..

            img_color=cv2.resize(img_color,(width,height) interpolation=cv2.INTER_AREA)

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
            img_result = cv2.resize(img_result, (560, 440))

            #커스텀에(DB)에 저장된 지정한 영역 표시 
            for i in range(len(self.camera_list)): 
                roi1 = img_result[self.camera_list[i][3]:self.camera_list[i][5],
                       self.camera_list[i][2]:self.camera_list[i][4]  
                rec1 = cv2.rectangle(img_result, (self.camera_list[i][2], self.camera_list[i][3]),
                                     (self.camera_list[i][4], self.camera_list[i][5]),
                                     (0, 0, 255), 1)

                roi1 = cv2.medianBlur(roi1, 3)  
                hsv1 = cv2.cvtColor(roi1, cv2.COLOR_BGR2HSV)

                h, s, v = cv2.split(hsv1)  # 색상 채도 명도를 나눔
                #print('Test2', i, self.color_list)

                self.input.color_list[i] = h.mean()  # 색상의 평균 값을 추출

            #컨트롤러 영상전달화면
            cv2.imshow('raspberrypi', img_color)

            #특정색깔 검출화면
            cv2.imshow('img_result', img_result)
            cv2.waitKey(1)
            sleep(0.001)
```
	  
</br>	



### -윈도우프로그램 UI 

 #### UI.py
 
 
 ```
  PyQt5의 GUI 버튼으로 컨트롤러의 버튼, 기울기, 카메라 입력에 대한 프로세스를 실행, 종료한다.
 ```
 
 ```
 def execute_favorites(self):
        index = self.item_index.row()  # 목록에서 선택한 커스텀의 위치를 알아내기
        custom_id = Favorites.select_Favorites()[index][0]  # 즐겨찾기 DB의 index로 custom_id 알아내기
        print('선택한 즐겨찾기의 기본키를 넘겨주기', custom_id)
        try:
            # 다른 커스텀이 실행중이라면 자이로 입력과 카메라 입력을 실행하지 않음
            if self.button_exe or self.gyro_exe or self.camera_exe:  
                ErrorMessage('실행중인 커스텀을 종료해주세요.')
            else:
                if ButtonData.button_memory[0]:
                    # 프로세스 생성 후 실행
                    self.button_input = ButtonKeyInput(custom_id, ButtonData.button_memory)
                    self.button_input.start()
                    self.button_exe = True
                    print('버튼 입력 시작')
                    OkMessage('선택한 커스텀을 실행합니다.')
                else:
                    print('버튼 연결 오류')
                    ErrorMessage('커스텀 실행 중 오류가 발생했습니다.')

                if GyroData.gyro_memory[0]:
                    # 프로세스 생성 후 실행
                    self.gyro_input = GyroKeyInput(custom_id, GyroData.gyro_memory)
                    self.gyro_input.start()
                    self.gyro_exe = True
                    print('자이로 입력 시작')
                else:
                    print('자이로 연결 오류')
                if IRCameraData.ir_camera_memory[0]:
                    # 카메라 DB가 비어 있다면 프로세스를 실행하지 않음
                    if Camera.select_Camera_eno(custom_id) != []:  
                        # 프로세스 생성 후 실행
                        self.camera_input = CamerakeyInput(custom_id, IRCameraData.ir_camera_memory)
                        self.camera_input.start()
                        self.camera_exe = True
                        print('카메라 입력 시작')
                else:
                    print('카메라 연결 오류')
        except:
            print('즐겨찾기 실행 오류')
            ErrorMessage('커스텀 실행 중 오류가 발생했습니다.')

	    def end_favorites(self):
		try:
		    if self.button_exe:
			self.button_input.terminate() # 프로세스 종료
			self.button_exe = False
			print('버튼 입력 끝내기')
		    if self.gyro_exe:
			self.gyro_input.terminate()  # 프로세스 종료
			self.gyro_exe = False
			print('자이로 입력 끝내기')
		    if self.camera_exe:
			self.camera_input.terminate()  # 프로세스 종료
			self.camera_exe = False
			print('카메라 입력 끝내기')
		    OkMessage('실행중인 커스텀을 종료합니다.')
		except:
		    print('끝내기 오류')
		    ErrorMessage('커스텀 종류 중 오류가 발생했습니다.')
``` 

