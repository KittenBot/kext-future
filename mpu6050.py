import machine
import math
import time
ACC_REST = 400

__version__ = "1.0.0"

class Accel():
    def __init__(self, addr=0x69):
        self.iic = machine.I2C(0)
        self.addr = addr
        self.iic.writeto(self.addr, bytearray([107, 0]))
        self.vals = {}

    def get_raw_values(self):
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def bytes_toint(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        self.vals["AcX"] = self.bytes_toint(raw_ints[0], raw_ints[1])
        self.vals["AcY"] = self.bytes_toint(raw_ints[2], raw_ints[3])
        self.vals["AcZ"] = self.bytes_toint(raw_ints[4], raw_ints[5])
        self.vals["Tmp"] = self.bytes_toint(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        self.vals["GyX"] = self.bytes_toint(raw_ints[8], raw_ints[9])
        self.vals["GyY"] = self.bytes_toint(raw_ints[10], raw_ints[11])
        self.vals["GyZ"] = self.bytes_toint(raw_ints[12], raw_ints[13])
        return self.vals

    def get_posture(self):
        self.get_values()
        x = self.vals["AcX"]/16*-1
        y = self.vals["AcY"]/16*-1
        z = self.vals["AcZ"]/16*-1

        shakeDect = False
        if (x < -1600) or (x > 1600):
            shakeDect = True
        if (y < -1600) or (y > 1600):
            shakeDect = True
        if (z < -1600) or (z > 1600):
            shakeDect = True
        detGes = ""
        if shakeDect:
            detGes ='shakeDect'
        elif y > 2*400:
            detGes='tilt_left'#左倾
        elif x*x+y*y+z*z < 200*200:
            detGes='freefall'
        elif y < -2*400:
            detGes='tilt_right'#右倾
        elif x > 1.3*400:
            detGes='tilt_down'#倒立
        elif x < -1.3*400:
            detGes='tilt_up'#正立
        elif z < -2*400:
            detGes='face_up'#面朝上
        elif z > 2*400:
            detGes='face_down'#面朝下
        time.sleep(0.05)
        return detGes
    
    def pitch(self):
        try:
            self.get_values()
            return math.atan2(self.vals["AcY"]*-1, math.sqrt(self.vals["AcX"]*self.vals["AcX"] + self.vals["AcZ"]*self.vals["AcZ"])) * 180/math.pi
        except:
            return None
    def roll(self):
        try:
            self.get_values()
            return math.atan2(self.vals["AcX"]*-1, math.sqrt(self.vals["AcY"]*self.vals["AcY"] + self.vals["AcZ"]*self.vals["AcZ"])) * 180/math.pi
        except:
            return None

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            #print(self.get_values())
            #print()
            #print()
            print(self.get_values())