from future import PINMAP
from machine import UART
import time
__version__ = "1.0.0"

class SugarMP3:
    def __init__(self,tx='P2',rx='P12',id=1):
        self.uart = UART(id,115200,tx=PINMAP[tx],rx=PINMAP[rx])
        while True:
            time.sleep(0.5)
            self.uart.write(bytes('K0\n','utf-8'))
            data = self.uart.readline()
            if data:
                try:
                    data = data.decode()
                    if data[0] == 'K' and data[1] == '0':
                        break
                except:
                    pass

    def mp3_mode(self):
        self.uart.write("K1\n")
        time.sleep(0.3)

    def pause(self):
        self.uart.write("K2\n")
        time.sleep(0.3)

    def stop(self):
        self.uart.write("K3\n")
        time.sleep(0.3)

    def next(self):
        self.uart.write("K4\n")
        time.sleep(0.3)

    def prev(self):
        self.uart.write("K5\n")
        time.sleep(0.3)

    def select_file(self,fileName):
        self.uart.write("K6 %s\n" %(fileName))
        time.sleep(0.3)

    def select_id(self,id):
        self.uart.write("K7 %s\n" %(id))
        time.sleep(0.3)
    
    def tts_mode(self):
        self.uart.write("K8\n")
        time.sleep(0.3)

    def play_text(self,text):
        self.uart.write("K9 %s\n" %(text))
        time.sleep(0.3)
    
