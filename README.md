# NoriController

제작인원 : 2명 (졸업작품)

------------------

## 버전정보 Python 3.7.3
------------------

라즈베리파이와 센서를 이용한  데스크탑 기반 무선컨트롤러 프로젝트



*사진을 클릭하면 영상이 실행됩니다.

[![Nori Controller Video](https://img.youtube.com/vi/WPgMmYe8V9c/0.jpg )](https://www.youtube.com/watch?v=WPgMmYe8V9c)


## 시연영상 (youtube) : "https://www.youtube.com/watch?v=WPgMmYe8V9c"
## 상세설명 (youtube) : "https://www.youtube.com/watch?v=t_fK7xvhH1s"


코드리뷰 
---

 IRCameraServer.py
 
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
