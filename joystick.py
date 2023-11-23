// 조이스틱 기본 코드
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

## up, down, left, right, center
gpio = [5, 6, 16, 20, 21]
## 현재 상태를 저장
stat = [0, 0, 0, 0, 0]
  ​
def print_jog_all():
    print ('up: %d, down: %d, left: %d, right: %d, center: %d' % (stat[0], stat[1], stat[2], stat[3], stat[4]))
  ​
  ​
try :
    for i in range(5):
        GPIO.setup(gpio[i], GPIO.IN)

        cur_stat = 0

        while True:
            for i in range(5):
                cur_stat = GPIO.input(gpio[i])
              
                ## 같지 않다 -> 신호반전, 즉 상태가 바꼈을 경우
                if cur_stat != stat[i]:
                    stat[i] = cur_stat
                    print_jog_all()
              
finally:
    print("cleaning up")
    GPIO.cleanup()