import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def paint():
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = 2
    text_gap = 20

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    #font = ImageFont.truetype('Minecraftia.ttf', 8)

    file_path = '/바탕화면경로찾기/text.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    data_array = []
    i = 0
    for line in lines:
        data_array.append(line.strip())
        draw.text((padding, padding + text_gap * (i - btnYCount)), line.strip(), font=font, fill=255)
        i += 1
    

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

#y축 조작 횟수
btnYCount = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# 여기서부터 수정하세요.
'''
주석처리
1. 만약 초음파센서 값
프린트 제어 불린값

2. 프린트
메모장 값 불러와서 출력하기
여러줄 및 만약 겟 헤이츠 넘어가면 출력금지
여러줄 출력할때 인덱스 곱하기 헤이츠 지정한값
글자 폰트 수정하기

3. 버튼 입력받아서 출력 y축 값으로 제어하기
if(btnYCount < 1):
    btnYCount = 0;
else if(btnYCount >= data_array.len()):
    btnYCount = data_array.len() - 1
else:
    btnYCount += 1
버튼 입력 값의 사이 딜레이 필요함

4. 버튼 입력받아서 해당 값 들어가서
/
제품
삭제
뒤로가기
/
출력하기

5. 값 임시로 적어넣기
나중에 blueterm? 긴빠이쳐오기
'''


# Display image.
disp.image(image)
disp.display()