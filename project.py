import RPi.GPIO as GPIO
import spidev

# 모터 드라이버 연결 PIN
A1A = 5
A1B = 6
# 습도 임계치(%)
HUM_THRESHOLD = 20
# 센서를 물에 담갔을 때의 토양습도센서 출력 값
HUM_MAX = 0
# 모터 드라이버 초기 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(A1A, GPIO.OUT)
GPIO.setup(A1A, GPIO.LOW)
GPIO.setup(A1B, GPIO.OUT)
GPIO.output(A1B, GPIO.LOW)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 500000
# ADC값을 가져오는 함수
def read_spi_adc(adcChannel):
	adcValue = 0
	buff = spi.xfer2([1,(8+adcChannel)<<4, 9])
	adcValue = ((buff[1]&3)<<8)+buff[2]
	return adcValue
