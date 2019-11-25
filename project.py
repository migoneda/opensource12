import RPi.GPIO as GPIO
import spidev
import time

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
# 센서 값을 백분율로 변환하기 위한 Map 함수
def Map(value, min_adc, max_adc, min_hum, max_hum):
	adc_range = max_adc - min_adc
	hum_range = max_hum - min_hum
	scale_factor = float(adc_range)/float(hum_range)
	return min_hum + ( (value - min_adc)/scale_factor )

try:
	adcChannal = 0
	while True:
		adcValue = read_spi_adc(adcChannel)
		 #가져온 데이터를 %단위로 변화. 습도  높을수록 낮은 값을 반환하므로
		#100에서 빼주어 습도가 높을수록 백분율이 높아지도록 계산
		hum = 100 - int(Map(adcValue, HUM_MAX, 1023, 0 ,100))
		if hum < HUM_THRESHOLD:
			GPIO.output(A1A,GPIO.HIGH) # 워터펌프 가동
			GPIO.output(A1B,GPIO.LOW)
		else:
			GPIO.output(A1A,GPIO.LOW)
			GPIO.output(A1B,GPIO.LOW)
		time.sleep(0.5)
finally:
	GPIO.cleanup()
	spi.close()

