#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""PyBluez simple example rfcomm-client.py
Simple demonstration of a client application that uses RFCOMM sockets intended
for use with rfcomm-server.
Author: Albert Huang <albert@csail.mit.edu>
$Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $
"""

import sys
import os
import threading
import bluetooth
import time
from MPU6050 import MPU6050
import socket
from imutils.video import VideoStream
import imagezmq


class NoriClient:
	def __init__(self):
		addr = None
		if len(sys.argv) < 2:  # 실행 인자가 없을 때
			print("지정된 장치가 없습니다. 근처의 모든 블루투스 기기를 검색합니다.")
		else:  # 실행 인자로 블루투스 맥주소를 넣을 때
			addr = sys.argv[1]
			print("서버를 검색합니다. {}...".format(addr))

		# 서비스 검색
		# SDP (Service Discovery Protocol) 주변에 사용가능한 서비스를 찾는 프로토콜
		# SDP 에서 서비스의 종류를 구분하기 위해 사용. 서버-클라이언트가 같아야 함.
		uuid = "00000004-0000-1000-8000-00805F9B34FB"
		service_matches = bluetooth.find_service(uuid=uuid, address=addr)  # 블루투스 서비스 찾기

		if len(service_matches) == 0:  # 검색 실패
			print("서버의 서비스를 찾을 수 없습니다.")
			sys.exit(0)

		first_match = service_matches[0]  # 검색한 서비스의 정보
		port = first_match["port"]  # 서버 포트번호
		name = first_match["name"]  # 서버 이름
		host = first_match["host"]  # 서버 맥 주소
		print("port:{}, name:{}, address:{} 연결 중...".format(port, name, host))

		# 클라이언트 블루투스 소켓 생성
		sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		sock.connect((host, port))  # 서버로 접속 요청
		print("연결되었습니다.")

		sendMessage = threading.Thread(target=self.send_tread, args=(sock,))
		receiveMessage = threading.Thread(target=self.receive_thread, args=(sock,))
		sendMessage.start()
		receiveMessage.start()

	def send_tread(self, sock):
		__author__ = 'Geir Istad'  # MPU6050_example.py의 내용 - roll, pitch, yaw를 사용하기 위함
		i2c_bus = 1
		device_address = 0x68
		# The offsets are different for each device and should be changed
		# accordingly using a calibration procedure
		x_accel_offset = -5489
		y_accel_offset = -1441
		z_accel_offset = 1305
		x_gyro_offset = -2
		y_gyro_offset = -72
		z_gyro_offset = -5
		enable_debug_output = True

		mpu = MPU6050(i2c_bus, device_address, x_accel_offset, y_accel_offset,
					  z_accel_offset, x_gyro_offset, y_gyro_offset, z_gyro_offset,
					  enable_debug_output)

		mpu.dmp_initialize()
		mpu.set_DMP_enabled(True)
		mpu_int_status = mpu.get_int_status()
		print(hex(mpu_int_status))

		packet_size = mpu.DMP_get_FIFO_packet_size()
		print(packet_size)
		FIFO_count = mpu.get_FIFO_count()
		print(FIFO_count)

		count = 0
		FIFO_buffer = [0] * 64

		FIFO_count_list = list()
		while True:
			FIFO_count = mpu.get_FIFO_count()
			mpu_int_status = mpu.get_int_status()

			# If overflow is detected by status or fifo count we want to reset
			if (FIFO_count == 1024) or (mpu_int_status & 0x10):
				mpu.reset_FIFO()
			# print('overflow!')
			# Check if fifo data is ready
			elif (mpu_int_status & 0x02):
				# Wait until packet_size number of bytes are ready for reading, default
				# is 42 bytes
				while FIFO_count < packet_size:
					FIFO_count = mpu.get_FIFO_count()
				FIFO_buffer = mpu.get_FIFO_bytes(packet_size)
				accel = mpu.DMP_get_acceleration_int16(FIFO_buffer)
				quat = mpu.DMP_get_quaternion_int16(FIFO_buffer)
				grav = mpu.DMP_get_gravity(quat)
				roll_pitch_yaw = mpu.DMP_get_euler_roll_pitch_yaw(quat, grav)
				# print('roll: ' + str(roll_pitch_yaw.x))
				# print('pitch: ' + str(roll_pitch_yaw.y))
				# print('yaw: ' + str(roll_pitch_yaw.z))
				message = str(int(roll_pitch_yaw.x)) + ',' + str(int(roll_pitch_yaw.y)) + ',' + str(
					int(roll_pitch_yaw.z))  # roll, pitch, yaw를 합쳐서 보내기
				length = len(message)
				sock.sendall(length.to_bytes(4, byteorder="little"))
				sock.sendall(message.encode('utf-8'))
				# print('roll:'+str(int(roll_pitch_yaw.x))+' pitch:'+str(int(roll_pitch_yaw.y))+' yaw:'+str(int(roll_pitch_yaw.z)))
				time.sleep(0.08)  # 0.1초 마다 전송

	def receive_thread(self, sock):
		while True:
			data = sock.recv(4)
			length = int.from_bytes(data, "little")
			data = sock.recv(length)
			message = data.decode('utf-8')
			print('receive: ', message)
			if 'wifi' in message:
				print(message)
				IRCamera(sock, message)
				break
			else:
				print('PC를 와이파이에 연결 후 다시 시도해 주세요.')
				break


class IRCamera:
	def __init__(self, sock, wifi_list):
		# 라즈베리파이에서 와이파이 스캔을 통해 잡히는 SSID 리스트
		self.scan_wifi_ssid_list = self.scan_wifi()  # 와이파이 스캔
		if self.scan_wifi_ssid_list == []:
			print('와이파이를 찾지 못했습니다.')
		print('연결 가능한 WiFi: ', self.scan_wifi_ssid_list)


		print(wifi_list)
		wifi_list = wifi_list.split(':')[1]
		wifi_list = wifi_list.split(',')

		self.wifi_ssid = wifi_list[0]
		self.wifi_pw = wifi_list[1]
		self.ip_address = wifi_list[2]

		self.wifi_connect()  # 와이파이 연결
		self.send_wifi_information(sock)  # 블루투스 통신으로 연결 가능한 와이파이 리스트를 보냄

		# 카메라 영상 송신
		sender = imagezmq.ImageSender(connect_to='tcp://' + self.ip_address + ':5555')  # ImageSender 초기화 해서 5555포트로 접속 한다
		rpi_name = socket.gethostname()  # send RPi hostname with each image
		picam = VideoStream(usePiCamera=True).start()
		time.sleep(2.0)

		while True:
			image = picam.read()
			sender.send_image(rpi_name, image)
	
	def scan_wifi(self):
		wifi_list = []
		wifi = os.popen('sudo iw wlan0 scan').read()
		wifi = wifi.split('\n')
		for i in wifi:
			if 'SSID' in i:
				if '*' in i:
					continue
				else:
					temp = i.split('SSID: ')
					wifi_list.append(temp[1])
		return wifi_list

	def current_wifi(self):
		wifi_current = os.popen('sudo iwconfig').read()  # 현재 연결된 wifi
		if 'ESSID' in wifi_current:
			temp = wifi_current.split('ESSID:')[1].split('\n')[0].rstrip()  # ssid를 추출함
			wifi_current = temp[1:-1]
		else:
			wifi_current = 'None'
			print('연결된 WiFi 없음')

		return wifi_current

	def send_wifi_information(self, sock):
		wifi_current = self.current_wifi()
		temp = 'wifi:' + wifi_current
		for j in self.scan_wifi_ssid_list:
			temp = temp + ',' + j
		message = temp
		length = len(message)
		sock.sendall(length.to_bytes(4, byteorder="little"))
		sock.sendall(message.encode('utf-8'))

	def wifi_connect(self):
		wifi_current = self.current_wifi()
		if self.wifi_ssid in self.scan_wifi_ssid_list:  # PC에 연결된 WiFi의 SSID가 라즈베리파이가 찾은 WiFi의 SSID 리스트 중에 있다면 실행
			if self.wifi_ssid == wifi_current:  # 이미 PC의 WiFi와 라즈베리파이의 WiFi가 같다면 연결하지않음
				print('와이파이가 이미 연결되어 있음 ', wifi_current)
				pass
			
			else:
				print('와이파이 접속중....')
				os.system('sudo ifconfig wlan0 up')  # 무선랜 ON
				os.system('sudo killall wpa_supplicant')  # 현재 실행중인 와이파이 OFF

				# 암호가 있는 경우(주의사항: 랜카드가 WiFi 5G 신호를 잡지 못함)
				os.system('sudo wpa_passphrase ' + self.wifi_ssid + ' ' + self.wifi_pw + '> wifi/wpa_psk.conf')  # 연결 시 사용할 psk 저장
				os.system('sudo wpa_supplicant -B -i wlan0 -c wifi/wpa_psk.conf')  # 와이파이 연결
				os.system('sudo dhclient wlan0')  # ip 할당받기
	
				# 암호가 없는 경우
				""" 현재 근처에 바밀번호가 없는 와이파이가 없어서 Test 불가
				os.system('sudo iwconfig wlan0 essid' + self.wifi_name + '')
				os.system('dhclient wlan0')
				"""
		else:
			print('PC에 연결된 WiFi를 찾지 못했습니다.')


if __name__ == "__main__":
	client = NoriClient()



# print('연결 끊어짐')
# sock.close()


