# 할일
'''
초음파센서 주석처리 -> 안되면
글자 폰트 수정하기 -> 일단 보고나서

1. 가로세로 모드 생각해보기
→ 스텝모터 사용하기
→ 선택 칸에 세로모드로 추가

2. blueterm 적용가능한지보기
→ 폰에서 제품 등록가능하게 구현용
'''

# 링크
'''
초음파센서
https://rasino.tistory.com/349

디스플레이
https://www.instructables.com/Raspberry-Pi-Monitoring-System-Via-OLED-Display-Mo/
https://github.com/adafruit/Adafruit_Python_SSD1306

조이스틱
https://github.com/mheidenreich/joystick/blob/main/joystick.py - 안될경우 참고하기
https://youtu.be/fX225p-Sh58 - 영상

스텝모터
https://blog.naver.com/elepartsblog/221444212815
'''

# 시간, 스레드
import time
import threading

# 초음파센서, 조이스틱, 스텝 모터
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

# 디스플레이 스레드 작동 코드
def paint():
    global idleTime, doing, ultraSonic
    global joyUpCheck, joyDownCheck, joyClickCheck
    global main, select, vhmode
    global btnYCount, btnYCount_Select
    global file_path

    # 디스플레이 가로, 세로
    width = disp.width
    height = disp.height

    # 글자 padding 및 갭 단위: px
    padding = 2
    text_gap = 20

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
                draw.text((5, 0), 'VH-Mode1', font=font, fill=255)
                draw.text((5, 10), 'VH-Mode2', font=font, fill=255)
                image = image.rotate(90, expand=True)

            # 디스플레이에 이미지 적용 및 출력
            disp.image(image)
            disp.display()

        time.sleep(1)

# cen을 일단 클릭으로 설정. 무엇인지 물어봐야할 듯.
# 버튼 스레드 작동 코드
def btn():
    global idleTime, doing, ultraSonic
    global joyUpCheck, joyDownCheck, joyClickCheck
    global main, select, vhmode
    global btnYCount, btnYCount_Select
    global file_path
    while doing:
        # 변수 초기화
        # up, down, left, right, cen
        stat = [0, 0, 0, 0, 0]
        tmp_stat = [0, 0, 0, 0, 0]
        index_stat = -1
        diff_stat = 0
        cur_stat = 0

        # 조이스틱 값 받아오기
        for i in range(5):
            cur_stat = GPIO.input(GPIO_joy[i])

            if cur_stat != stat[i]:
                tmp_stat[i] = stat[i]
                stat[i] = cur_stat
                if tmp_stat[i] - stat[i] > diff_stat:
                    idleTime = 100
                    diff_stat = tmp_stat[i] - stat[i]
                    # up, down, left, right, cen
                    index_stat = i
                if i == 5:
                    index_stat = i

        # 절전모드 아닐 때,
        # 디스플레이 상호작용
        if ultraSonic:
            if index_stat == 0:
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

            if index_stat == 1:
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

            if index_stat == 4:
                if main:
                    if(btnYCount == len(data_array) - 1):
                        doing = False
                    elif(btnYCount != len(data_array) - 3 and btnYCount != 0):
                        main = False
                        select = True
                    elif(btnYCount == len(data_array) - 2): 
                        global dir
                        for cnt in range(0,step):
                            GPIO.output(AIN1,sig[0])
                            GPIO.output(BIN1,sig[1])
                            GPIO.output(AIN2,sig[2])
                            GPIO.output(BIN2,sig[3])
                            time.sleep(0.01)
                            sig.rotate(dir)
                        dir=dir*-1
                        main = False
                        vhmode = True

                if select:
                    if btnYCount_Select == 0:
                        #제품명 선택한거. 없애는지 여부? -> 인덱스 선택 1, 2 한정걸기
                        print("Nothing", end='')
                    if btnYCount_Select == 1:
                        #해당 제품 삭제
                        del data_array[btnYCount]
                        main = True
                        select = False
                        btnYCount = 0
                    if btnYCount_Select == 2:
                        #뒤로가기
                        main = True
                        select = False
                        btnYCount_Select = 0

        time.sleep(0.5)

# 기본 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

'''
 핀, 변수 설정
'''
# 초음파센서랑 스텝모터 핀 바꿔야 함.

# 디스플레이
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 초음파 센서
TRIG = 23
ECHO = 24

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)

# 조이스틱
GPIO_joy = [5, 6, 16, 20, 21]

for i in range(5):
    GPIO.setup(GPIO_joy[i], GPIO.IN)

# 스텝 모터
AIN1=22
BIN1=23
AIN2=24
BIN2=25
sig=deque([1,0,0,0])
step=100
dir=1
GPIO.setup(AIN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(BIN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(AIN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(BIN2,GPIO.OUT,initial=GPIO.LOW)
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
global idleTime, doing, ultraSonic
global joyUpCheck, joyDownCheck, joyClickCheck
global main, select, vhmod
global btnYCount, btnYCount_Select
global file_path
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
file_path = '1.txt' # 파일경로

#텍스트 뽑아내기
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data_array = [line.strip() for line in lines]

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

# 무한 반복 코드
# 라즈베리파이 가동 후, 종료까지 여기서 갇힘.
while doing:
    # 초음파센서 확인하는 부분 만일 문제 지속발생 시, 유기하기.
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
    
    # 초음파센서 2초 딜레이 필요.
    time.sleep(2)

# GPIO 정리
GPIO.cleanup()

# 값 저장하기
data_array = data_array[:-3] # 인덱스 뒤에 3개 삭제
try:
    with open(file_path, 'w', encoding='utf-8') as output_file:
        for item in data_array:
            output_file.write("%s\n" % item)
except Exception as e:
    print(f"파일 저장 중 오류 발생: {e}")