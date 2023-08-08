from future import PINMAP
from machine import UART
__version__ = "1.0.0"

class SugarMP3:
    def __init__(self,tx='P2',rx='P12',id=1):
        self.uart = UART(id,115200,tx=PINMAP[tx],rx=PINMAP[rx])

    def mp3_mode(self):
        self.uart.write("K1\n")

    def pause(self):
        self.uart.write("K2\n")

    def stop(self):
        self.uart.write("K3\n")

    def next(self):
        self.uart.write("K4\n")

    def prev(self):
        self.uart.write("K5\n")

    def select_file(self,fileName):
        self.uart.write("K6 %s\n" %(fileName))

    def select_id(self,id):
        self.uart.write("K7 %s\n" %(id))
    
    def tts_mode(self):
        self.uart.write("K8\n")

    def play_text(self,text):
        self.uart.write("K9 %s\n" %(text))
    
