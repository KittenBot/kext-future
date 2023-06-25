from machine import UART
from future import *
from time import *
import socket
import errno
import ubinascii
import _thread

__version__ = "1.0.8"
VERSIONS = 'K0'
QRCODE = 'K11'
RECOGNIZE = "K12"
PLAYAUDIO = "K15"
ISDARKNESS = "K17"
AUDIOTEST = "K18"
BUTTONSTATE = "K19"
MQQTTCONNECT = "K20"
MQTTSUBSCRIPTION = "K21"
MQTTMESSAGE = "K22"
MQTTSEND = "K23"
SETGRB = "K16"
SETALLRGB = "K25"
class SugarCam:
    def __init__(self,tx,rx):
        self.uart = UART(1,115200,tx=PINMAP[tx],rx=PINMAP[rx])
        
        self.uart.write(bytes('\n\n','utf-8'))
        sleep(0.4)
        flag = ''
        count = 0
        while True:
            if count == 10:
                print("Please try to reset the sugar_cam!!")
                count = 0
            data = self.uart.readline()
            print(data)
            if data:
                try:
                    flag = str(data,'UTF-8')
                    if VERSIONS in flag:
                        pass
                        break
                    else:
                        pass
                except:
                    pass
                    flag = ''
            else:
                self.uart.write('{} \r\n'.format(VERSIONS).encode())
                count+=1
                sleep(1)
    def getQRcode(self):
        data = None
        self.uart.read()
        self.uart.write('{} \r\n'.format(QRCODE).encode())
        sleep(2)
        data = self.uart.read()
        if data:
            try:
                data = data.decode().split(" ")
                if data[0] != QRCODE:
                    return None
                else:
                    if data[1][0:4] == 'None':
                        return None
                    else:
                        data = data[1].replace("\n","").replace("\r","").lstrip().rstrip()
                        return data
            except:
                return None
            
    def isDarkness(self):    
        data = None
        self.uart.read()
        self.uart.write('{} \r\n'.format(ISDARKNESS).encode())
        sleep(0.5)
        data = self.uart.read()
        if data:
            try:
                data = data.decode().split(" ")
                print(data)
                if data[0] != ISDARKNESS:
                    return None
                elif "False" in str(data[1]):
                    return False 
                elif "True" in str(data[1]):
                    return True 
            except:
                return False
            
    def playAudio(self,wav):
        self.uart.write('{} {} \r\n'.format(PLAYAUDIO,wav).encode())
        sleep(1)

    def audioTest(self):
        self.uart.write('{} \r\n'.format(AUDIOTEST).encode())
        sleep(1)

    def setColor(self,color1,color2):
        self.uart.write('{} {} {} \r\n'.format(SETGRB,str(color1).replace(' ',''),str(color2).replace(' ','')).encode())
        sleep(1)

    def setAllColor(self,color1):
        self.uart.write('{} {} \r\n'.format(SETALLRGB,str(color1).replace(' ','')).encode())
        sleep(1)
        

    def recognize(self,sec):
        data = None
        data = self.uart.read()
        self.uart.write('{} {} \r\n'.format(RECOGNIZE,sec).encode())
        num=0
        while num != 12:
            sleep(1)
            data = self.uart.read()
            if data:
                try:
                    data = data.decode().split(",")
                    if data[0] != RECOGNIZE:
                        return None
                    else:
                        if data[1][0:4] == 'None':
                            return None
                        else:
                            data = data[1]
                            if data[-2:] == "\r\n":
                                data = data[:-2]
                            print(len(data))
                            return data
                except:
                    return None
            num+=1
    def buttonState(self,button):
        data = None
        self.uart.read()
        self.uart.write('{} {} \r\n'.format(BUTTONSTATE,button).encode())
        sleep(1.5)
        data = self.uart.read()
        if data:
            try:
                data = data.decode().split(" ")
                if data[0] != BUTTONSTATE:
                    return None
                else:
                    if len(data)!=4:
                        return None
                    if data[1] != button:
                        return None
                    return bool(int(data[2]))
            except:
                return None

class FPV:
  def __init__(self,ip,secret):
    self.ip = ip
    self.secret = secret
    self.status = False

  def setStatus(self,status):
      self.status = status
      if self.status:
          _thread.start_new_thread(self.startMonitor,(9233,))

  def decodeCmd(self,data):
      cmds = data.split(' ')
      if len(cmds) < 2:
          return
      if cmds[0] == "K1":
          buff = ubinascii.a2b_base64(cmds[1])
          fb.loadjpg(buff)
          screen.refresh()
  
  def startMonitor(self, port=9233):
      ip = self.ip
      secret = self.secret
      cmd = "K1 %s \r\n" %secret
      s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      s.bind(socket.getaddrinfo("0.0.0.0", 17758)[0][-1])
      addr = socket.getaddrinfo(ip, port)[0][-1]
      t0 = ticks_ms()
      s.setblocking(False)
      # s.settimeout(1)
      try:
        res = s.sendto(cmd, addr)
      except OSError as e:
        if e.args[0] == 118:
          _sync = screen.sync
          screen.sync = 1
          screen.clear()
          screen.showmsg(translate('Connect wifi first'), translate("Camera connect fail"), type='err')
          screen.sync = _sync
          print("Please connect wifi first")
        # 处理其他类型的 OSError 异常
        else:
          print(e)
      data = b""
      print("Monitor start")
      while self.status:
          try:
              rx, addr = s.recvfrom(16*1024)
              print("rx", len(data), addr)
              if rx:
                  data += rx
                  _tmp = data.split(b'\n')
                  if len(_tmp) > 1:
                      data = _tmp[-1]
                      try:
                          self.decodeCmd(_tmp[0].decode('utf-8'))
                      except:
                          pass
          except OSError as err:
              if err.args[0] != errno.EAGAIN and err.args[0] != errno.EWOULDBLOCK:
                  raise
              else:
                  sleep_ms(100)
          if ticks_diff(ticks_ms(), t0) > 8000:
              t = s.sendto(cmd, addr)
              print("send to", addr, t)
              t0 = ticks_ms() 
      _thread.exit()    
    