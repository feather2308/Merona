# 할일
'''
초음파센서 주석처리 -> 안되면
글자 폰트 수정하기 -> 일단 보고나서?
버튼 코드 받기
버튼 입력 받는 방법 보기
버튼 입력 값의 사이 딜레이 필요함

1. 가로세로 모드 생각해보기
→ 스텝모터 사용하기
→ 선택 칸에 세로모드로 추가

2. blueterm 적용가능한지보기
→ 폰에서 제품 등록가능하게 구현용
'''

# 시간, 스레드
import time
import threading

# 초음파센서
import RPi.GPIO as GPIO

# 디스플레이
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

# 디스플레이
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# 디스플레이 스레드 작동 코드
def paint():
    # 디스플레이 가로, 세로
    width = disp.width
    height = disp.height

    # 폰트 불러오기
    font = ImageFont.load_default()

    while doing:
        if ultraSonic:
            if main:
                # 이미지 생성 1비트로 초기화
                image = Image.new('1', (width, height))

                # 그림 이미지드로우 객체로 가져오기
                draw = ImageDraw.Draw(image)

                # 배경 초기화
                draw.rectangle((0,0,width,height), outline=0, fill=0)

                padding = 2
                text_gap = 20

                # 폰트 불러올거면 쓰기.
                #font = ImageFont.truetype('파일경로/파일명.ttf', 폰트크기)

                # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
                # Some other nice fonts to try: http://www.dafont.com/bitmap.php
                #font = ImageFont.truetype('Minecraftia.ttf', 8)

                # 제품 목록 글자 적기
                # 마지막 전인가 아닌가 확인하는 제어문
                if btnYCount != len(data_array):
                    i = 0
                    # 제품 목록 출력
                    for k in range(0, len(data_array)):
                        draw.text((15 + padding, padding + text_gap * (i - btnYCount)), data_array[k], font=font, fill=255)
                        i += 1
                    # 현재 선택 출력
                    draw.text((padding, padding + text_gap * 0), "▷", font=font, fill=255)
                else:
                    i = 0
                    # 제품 목록 출력
                    for k in range(0, len(data_array)):
                        draw.text((15 + padding, padding + text_gap * (i - btnYCount + 1)), data_array[k], font=font, fill=255)
                        i += 1
                    # 현재 선택 출력
                    draw.text((padding, padding + text_gap * 1), "▷", font=font, fill=255)

                # 디스플레이에 이미지 적용 및 출력
                disp.image(image)
                disp.display()

            if select:
                width = disp.width
                height = disp.height
                image = Image.new('1', (width, height))
                draw = ImageDraw.Draw(image)
                draw.rectangle((0,0,width,height), outline=0, fill=0)

                padding = 2
                text_gap = 20
                font = ImageFont.load_default()

                # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
                # Some other nice fonts to try: http://www.dafont.com/bitmap.php
                # font = ImageFont.truetype('Minecraftia.ttf', 8)

                draw.text((15 + padding, padding + text_gap * 0), data_array[btnYCount], font=font, fill=255)
                draw.text((15 + padding, padding + text_gap * 1), "삭제하기", font=font, fill=255)
                draw.text((15 + padding, padding + text_gap * 2), "뒤로가기", font=font, fill=255)

                draw.text((padding, padding + text_gap * btnYCount_Select), "▷", font=font, fill=255)

                disp.image(image)
                disp.display()

        time.sleep(1)

# 버튼 스레드 작동 코드
def btn():
    '''
    버튼이 어케 작동하는지 봐야함!!!!!
    <b>중요 매우</b>
    '''

    # 절전모드 아닐 때,
    # 디스플레이 상호작용
    if ultraSonic:
        if joyUpCheck:
            if main:
                if btnYCount > data_array.len() - 2:
                    btnYCount = data_array.len() - 1
                else:
                    btnYCount += 1
            if select:
                if btnYCount_Select > 1:
                    btnYCount_Select = 2
                else:
                    btnYCount_Select += 1

        if joyDownCheck:
            if main:
                if btnYCount < 1:
                    btnYCount = 0;
                else:
                    btnYCount -= 1
            if select:
                if btnYCount_Select < 1:
                    btnYCount_Select = 0;
                else:
                    btnYCount_Select -= 1
        if joyClickCheck:
            if main:
                if(btnYCount == len(data_array) - 1):
                    doing = False
                elif(btnYCount != len(data_array) - 2):
                    main = False
                    select = True
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
    time.sleep(0.1)

# 기본 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

'''
 핀 설정
'''
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
'''
 핀 설정 끝
'''

# 대기 시간 2초
print("준비 중.", end='')
time.sleep(0.5)
print(".", end='')
time.sleep(0.5)
print(".", end='')
time.sleep(1)

# y축 조작 횟수
btnYCount = 0
btnYCount_Select = 0

# 디스플레이 기본설정
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
disp.begin()
disp.clear()
disp.display()

#텍스트 뽑아내기
file_path = '파일경로/파일명.확장자'
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

data_array = []
for line in lines:
    data_array.append(line.strip())
data_array.append('----------')
data_array.append('끝내기')

# 디스플레이 스레드
disp_t = threading.Thread(target=paint)
disp_t.start()

# 버튼 스레드
btn_t = threading.Thread(target=btn)
btn_t.start()

# 사용하는 변수 초기화
idleTime = 5
doing = True
ultraSonic = False
joyUpCheck = False
joyDownCheck = False
joyClickCheck = False

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