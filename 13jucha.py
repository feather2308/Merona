'''
 핀, 변수 설정
'''
# GPIO 번호로 입력할 것.
# 스텝모터
StepPins = [, , , ] # IN1, IN2, IN3, IN4
# 버튼
btnup = 
btndown = 
btnselect = 
# 초음파
TRIG = 
ECHO = 
# 가스
MQ5 = 
# LED
led_r = 17
led_y = 27
led_g = 22
# 파일경로 + 텍스트 내용 수정하기 양식 : 'name | 1Day(2000-00-00'
file_path = '1.txt' 



# ADC
import spidev

# 날짜, 시간, 스레드
import datetime
import time
import threading

# 초음파센서, 스텝 모터
import RPi.GPIO as GPIO

# 디스플레이
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

# 디스플레이
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# 스텝 모터
from collections import deque

def blackPaint():
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    disp.image(image)
    disp.display()

# 디스플레이 스레드 작동 코드
def paint():
    global idleTime, doing, ultraSonic
    global main, select, vhmode
    global btnYCount, btnYCount_Select
    global file_path

    # 디스플레이 가로, 세로
    width = disp.width
    height = disp.height

    # 글자 padding 및 갭 단위: px
    padding = 2
    text_gap = 10

    # 폰트 불러오기
    font = ImageFont.load_default()

    # 폰트 불러올거면 쓰기.
    #font = ImageFont.truetype('파일경로/파일명.ttf', 폰트크기)

    # 영어원문. 혹시 몰라서 놔둠.
    # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    #font = ImageFont.truetype('Minecraftia.ttf', 8)

    while doing:
        if ultraSonic:
            # 이미지 생성 1비트로 초기화
            image = Image.new('1', (width, height))

            # 그림 이미지드로우 객체로 가져오기
            draw = ImageDraw.Draw(image)

            # 배경 초기화
            draw.rectangle((0,0,width,height), outline=0, fill=0)

            if main:
                # 제품 목록 글자 적기
                # 마지막 전인가 아닌가 확인하는 제어문
                if btnYCount != len(data_array):
                    i = 0
                    # 제품 목록 출력
                    for k in range(0, len(data_array)):
                        draw.text((15 + padding, padding + text_gap * (i - btnYCount)), data_array[k], font=font, fill=255)
                        i += 1
                    # 현재 선택 출력
                    draw.text((padding, padding + text_gap * 0), "-", font=font, fill=255)
                else:
                    i = 0
                    # 제품 목록 출력
                    for k in range(0, len(data_array)):
                        draw.text((15 + padding, padding + text_gap * (i - btnYCount + 1)), data_array[k], font=font, fill=255)
                        i += 1
                    # 현재 선택 출력
                    draw.text((padding, padding + text_gap * 1), "-", font=font, fill=255)

            if select:
                draw.text((15 + padding, padding + text_gap * 0), data_array[btnYCount], font=font, fill=255)
                draw.text((15 + padding, padding + text_gap * 1), "Delete", font=font, fill=255)
                draw.text((15 + padding, padding + text_gap * 2), "Back", font=font, fill=255)
                draw.text((padding, padding + text_gap * btnYCount_Select), "-", font=font, fill=255)
            
            if vhmode:
                image = Image.new('1', (height, width))
                draw = ImageDraw.Draw(image)
                draw.rectangle((0, 0, height, width), outline=0, fill=0)

                draw.text((5, 0), 'VH', font=font, fill=255)
                draw.text((5, 10), 'Mode', font=font, fill=255)

                image = image.rotate(90, expand=True)

            # 디스플레이에 이미지 적용 및 출력
            disp.image(image)
            disp.display()

        time.sleep(0.5)

# 버튼 스레드 작동 코드
def btn():
    global btnup, btndown, btnselect
    global idleTime, doing, ultraSonic
    global main, select, vhmode
    global btnYCount, btnYCount_Select
    global file_path
    while doing:
        # 절전모드 아닐 때,
        # 디스플레이 상호작용
        if ultraSonic:
            if GPIO.input(btnup) == GPIO.HIGH:
                idleTime = 100
                if main:
                    if btnYCount > len(data_array) - 2:
                        btnYCount = len(data_array) - 1
                    else:
                        btnYCount += 1
                if select:
                    if btnYCount_Select > 1:
                        btnYCount_Select = 2
                    else:
                        btnYCount_Select += 1

            if GPIO.input(btndown) == GPIO.HIGH:
                idleTime = 100
                if main:
                    if btnYCount < 1:
                        btnYCount = 0
                    else:
                        btnYCount -= 1
                if select:
                    if btnYCount_Select < 1:
                        btnYCount_Select = 0
                    else:
                        btnYCount_Select -= 1

            if GPIO.input(btnselect) == GPIO.HIGH:
                idleTime = 100
                if main:
                    if(btnYCount == len(data_array) - 1):
                        doing = False
                    elif(btnYCount != len(data_array) - 3):
                        main = False
                        select = True
                    elif(btnYCount == len(data_array) - 2): 
                        # 스텝모터 시계방향 100스텝
                        global StepPins, Seq, StepCount, StepCounter
                        i = 0
                        while i < 100 :
                            for pin in range(0, 4):
                                xpin = StepPins[pin]
                                if Seq[StepCounter][pin] != 0:
                                    GPIO.output(xpin, True)
                                else:
                                    GPIO.output(xpin, False)
                            StepCounter += 1
                            if StepCounter == StepCount:
                                StepCounter = 0
                            if StepCounter < 0:
                                StepCounter = StepCount
                            time.sleep(0.01)
                        
                        main = False
                        vhmode = True

                if select:
                    if btnYCount_Select == 0:
                        #해당 제품 삭제
                        del data_array[btnYCount]
                        main = True
                        select = False
                        btnYCount = 0
                    if btnYCount_Select == 1:
                        #뒤로가기
                        main = True
                        select = False
                        btnYCount_Select = 0
        time.sleep(0.2)

def read_gas_ppm():
    # MCP3002를 통해 아날로그 값을 읽어오는 함수
    adc_data = spi.xfer2([1, (8 + MCP3002_CHANNEL) << 4, 0])
    adc_value = ((adc_data[1] & 3) << 8) + adc_data[2]
    return adc_value

# 가스 스레드
def mq5():
    while doing:
        gas_ppm = read_gas_ppm()
        if gas_ppm < 25:
            GPIO.output(led_g, GPIO.HIGH)
            GPIO.output(led_y, GPIO.LOW)
            GPIO.output(led_r, GPIO.LOW)
        elif 25 <= gas_ppm < 40:
            GPIO.output(led_g, GPIO.LOW)
            GPIO.output(led_y, GPIO.HIGH)
            GPIO.output(led_r, GPIO.LOW)
        else:
            GPIO.output(led_g, GPIO.LOW)
            GPIO.output(led_y, GPIO.LOW)
            GPIO.output(led_r, GPIO.HIGH)
        print(f"Gas PPM: {gas_ppm}")
        time.sleep(1)
    spi.close()

# 기본 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
spi = spidev.SpiDev()
spi.open(0, 0)
# MCP3002의 채널 설정
MCP3002_CHANNEL = 0
# 센서 입력 핀 설정
SENSOR_PIN = 17
GPIO.setup(SENSOR_PIN, GPIO.IN)

# 디스플레이
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 초음파 센서
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)

# 버튼
GPIO.setup(btnup, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btndown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnselect, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 스텝 모터
for pin in StepPins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)
StepCounter = 0
StepCount = 4
Seq = [[0, 0, 0, 1],
       [0, 0, 1, 0],
       [0, 1, 0, 0],
       [1, 0, 0, 0]]
ReSeq = [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]]

# MQ5 가스센서
GPIO.getup(MQ5,GPIO.IN)

# LED 핀 설정
GPIO.setup(led_r, GPIO.OUT)
GPIO.setup(led_y, GPIO.OUT)
GPIO.setup(led_g, GPIO.OUT)
'''
 핀 변수 설정 끝
'''
# 대기 시간 2초
print("준비 중.", end='')
time.sleep(0.5)
print(".", end='')
time.sleep(0.5)
print(".", end='')
time.sleep(1)

# 디스플레이 기본설정
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()

# 사용하는 변수 초기화
idleTime = 5
doing = True
ultraSonic = False
joyUpCheck = False
joyDownCheck = False
joyClickCheck = False
main = True # 메인, 선택
select = False
vhmode = False
btnYCount = 0 # y축 조작 횟수
btnYCount_Select = 0

# 날짜 변경
# 파일 열기 (읽기 모드)
with open(file_path, 'r', encoding='utf-8') as file:
    # 파일 내용 읽기
    content = [line.strip() for line in file if line.strip()]

strlist1 = []
strlist2 = []
for i in range(0, len(content)):
    strlist1.append(content[i].split(' | ')[1].split('('))
    strlist2.append(content[i].split(' | ')[0])
    strlist2.append((datetime.datetime.now() - datetime.datetime.strptime(strlist1[i][1], '%Y-%m-%d')).days)

newlist = []
for i in range(0, len(strlist2)-1, 2):
    combine = strlist2[0 + i] + ' | ' + str(strlist2[1 + i]) + ' Day(' + datetime.datetime.now().strftime("%Y-%m-%d")
    newlist.append(combine)

# 파일 열기 (쓰기 모드)
with open(file_path, 'w', encoding='utf-8') as file:
    # 편집된 내용을 파일에 쓰기
    for item in newlist:
        file.write(item + '\n')

data_array = []

#텍스트 뽑아내기
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    temp = [line.strip() for line in lines]
    for element in temp:
        data_array.append(element.split('(')[0])

    # 인덱스 3개 추가댐. 삭제에서 3개 삭제함.
    data_array.extend(['----------', 'VH-Mod', 'End'])
except FileNotFoundError:
    print(f"파일을 찾을 수 없습니다: {file_path}")
    data_array = []

# 디스플레이 스레드
disp_t = threading.Thread(target=paint)
disp_t.start()

# 버튼 스레드
btn_t = threading.Thread(target=btn)
btn_t.start()

# 가스 스레드
mq5_t = threading.Thread(target=mq5)
mq5_t.start()

# 무한 반복 코드
# 라즈베리파이 가동 후, 종료까지 여기서 갇힘.
while doing:
    # 초음파센서 확인하는 부분.
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()
    
    distance = (stop - start) * 34300 / 2

    # 거리 조건걸기 및 절전모드 관리
    if distance < 30:
        ultraSonic = True
        idleTime = 100
    else:
        ultraSonic = False

    # 유휴상태에서 깼을 때, 초음파센서 사용 안함.
    while ultraSonic:
        idleTime -= 1
        if idleTime == 0:
            ultraSonic = False
            time.sleep(1)
            blackPaint()
        time.sleep(1)
    
    # 초음파센서 2초 딜레이 필요.
    time.sleep(2)

# GPIO 정리
GPIO.cleanup()

# 값 저장하기
data_array = data_array[:-3] # 인덱스 뒤에 3개 삭제

try:
    with open(file_path, 'w', encoding='utf-8') as output_file:
        for item in data_array:
            timestamped_item = f"{item}({datetime.datetime.now().strftime('%Y-%m-%d')}"
            output_file.write("%s\n" % timestamped_item)
except Exception as e:
    print(f"파일 저장 중 오류 발생: {e}")