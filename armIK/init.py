from adafruit_servokit import ServoKit
import time

pca = ServoKit(channels=16)

MIN_ANG  =[80, 80, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
MAX_ANG  =[90, 90, 90, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180, 180]
def init():
    for i in range(nbPCAServo):
        pca.servo[i].set_pulse_width_range(MIN_IMP[i] , MAX_IMP[i])

for i in range(1,16):
    pca.servo[i].angle = 80
time.sleep(5)
for i in range(16):
    pca.servo[i].angle = 80
