#!/usr/bin/python
#coding:utf-8

from future import screen,PINMAP
import time
from machine import UART
from l10n import translate
__version__ = "1.0.5"
class KOI:
    def __init__(self,tx='P2',rx='P12',id=1):
        self.space = ['0']*8
        self.re_temp = []
        self.cmd = None
        self.uart = UART(id,115200,tx=PINMAP[tx],rx=PINMAP[rx])
        self.uart.write('\n\n')
        self.uart.write('K0\r\n')
        time.sleep(0.4)
        flag = ''
        while not('K0' in flag):
            if self.uart.any():
                try:
                    flag = str(self.uart.readline(),'UTF-8')
                    if 'K0' in flag:
                        screen.clear()
                        break
                    else:
                        screen.showmsg(translate("KOI Init Fail,Please Reset"), translate('Warning'))
                except:
                    screen.showmsg(translate("KOI Init Fail,Please Reset"), translate('Warning'))
                    flag = ''
            else:
                self.uart.write('K0\r\n')
                time.sleep(1)
        self.startTime = 0
        self.log = ''




    """
    接收来自KOI对应的K指令，并取出有用的数据
    """
    def _uart_re(self,cmd):
        while self.uart.any():
            try:
                re = str(self.uart.read(),'utf-8')
                re = re.splitlines()
                for i in re:
                    i = i.strip()
                    i = i.split(' ')
                    if i.pop(0) == cmd:
                        self.re_temp = i
                        return i
            except UnicodeError:
                print("UnicodeError")
                return False
            return False
        return False


    def get_re(self,cmd):
        if cmd == self.cmd and self.re_temp:
            return self.re_temp
        else:
            return self.space
        

    """
    KOI资源基础
    """
    # KOI摄像头旋转 / eg: 0:前置 2:后置
    def screen_mode(self,mode,cmd="K6"):
        self.uart.write("%s %s\r\n" %(cmd,mode))
    
    # KOI显示字符串
    def text(self,x,y,delay,text,cmd="K4"):
        self.uart.write("%s %s %s %s %s\r\n" %(cmd,str(x),str(y),str(delay),str(text)))
    
    # KOI拍照截屏 / eg: pic='test.jpg'
    def screen_save(self,pic,cmd="K2"):
        self.uart.write("%s %s\r\n" %(cmd,pic))
    
    # KOI显示图片
    def screen_show(self,pic,cmd="K1"):
        self.uart.write("%s %s\r\n" %(cmd,pic))

    # KOI按键
    def btnValue(self,cmd="K3"):
        self.uart.write("%s\r\n" %(cmd))
        self.cmd = cmd
        time.sleep_ms(200)
        return self._uart_re(cmd)


    """
    yolo模型人脸追踪
    """
    # 人脸模型
    def face_yolo_load(self,cmd="K30"):
        self.uart.write("%s\r\n" %(cmd))
        time.sleep_ms(300)

    # 追踪人脸
    def face_detect(self,cmd="K31"):
        self.uart.write("%s\r\n" %(cmd))
        time.sleep_ms(300)
        self.cmd = cmd
        return self._uart_re(cmd)
        
    # 人脸数量
    def face_count(self,cmd="K32"):
        self.uart.write("%s\r\n" %(cmd))
        time.sleep_ms(300)
        self.cmd = cmd
        return self._uart_re(cmd)

    """
    连接WiFi
    """
    #连接WiFi / eg: router='hogan' pwd='12345678'
    def connect_wifi(self,router,pwd,cmd="K50"):
        self.uart.write("%s %s %s\r\n" %(cmd,router,pwd))
    
    #获取IP并显示
    def get_ip(self,cmd="K54"):
        self.uart.write("%s\r\n" %(cmd))
        self.cmd = cmd
        return self._uart_re(cmd)


    """
    baiduAI
    """
    # baiduAI人脸识别
    def baiduAI_face_detect(self,cmd="K75"):
        self.uart.write("%s\r\n" %(cmd))
        time.sleep_ms(2000) 
        self.cmd = cmd
        return self._uart_re(cmd)
        
    # 将最后一次识别到的人脸添加到baiduAI人脸组
    def baiduAI_face_add(self,face_token,groupName,faceName,cmd="K76"):
        self.uart.write("%s %s %s %s\r\n" %(cmd, face_token, groupName, faceName))

    # 在baiduAI人脸组中搜索人脸 
    def baiduAI_face_search(self,face_token,groupName,cmd="K77"):
        self.uart.write("%s %s %s\r\n" %(cmd, face_token, groupName))
        time.sleep_ms(2000) 
        self.cmd = cmd
        return self._uart_re(cmd)
  
    # koi百度文字转语音
    def baiduAI_tts(self,txt,cmd="K78"):
        self.uart.write("%s %s\r\n" %(cmd, txt))


    """
    KNN特征分类
    """
    # 初始化特征分类器
    def init_cls(self):
        self.uart.write("K40\r\n")

    # 分类器增加标签
    def cls_add_tag(self,id,cmd="K41"):
        self.uart.write("%s %s\r\n" %(cmd,id))

    # 运行分类器
    def cls_run(self,cmd="K42"):
        self.uart.write(cmd + "\r\n")
        time.sleep_ms(1000) 
        self.cmd = cmd
        self._uart_re(cmd)

    # 分类结果
    def cls_result(self,cmd="K42"):
        return self.get_re(cmd)[0]
    
    # 结果误差
    def cls_error(self,cmd="K42"):
        return self.get_re(cmd)[1]

    # 分类器保存模型文件 / eg:'cls.json'
    def cls_save_model(self,model,cmd="K43"):
        self.uart.write("%s %s\r\n" %(cmd,model))

    # 分类器加载模型文件 / eg:'cls.json'
    def cls_load_model(self,model,cmd="K44"):
        self.uart.write("%s %s\r\n" %(cmd,model))


    """
    音频
    """
    # 录制音频 / eg: name='sound.wav'
    def audio_record(self,wav,cmd="K61"):
        self.uart.write("%s %s\r\n" %(cmd,wav))
    
    # 播放音频 / eg: name='sound.wav'
    def audio_play(self,wav,cmd="K62"):
        self.uart.write("%s %s\r\n" %(cmd,wav))

    # 注册语音识别关键字 /eg: key='ni-hao'
    def asr_register_key(self,key,cmd="K64"):
        self.uart.write("%s %s\r\n" %(cmd,key))

    # 获取识别结果
    def asr_result(self):
        try:
            result = self.uart.readline()
            if result:
                result = result.decode()
                if result[:3] == 'K65':
                    data = (result[4:]).strip()
                    return data
            return None
        except UnicodeError:
            return None

    # 口罩识别，检测到人脸？
    def face_mask(self):
        try:
            result = self.uart.readline()
            if result:
                result = result.decode()
                if result[:3] == 'K33':
                    data = (result[4:]).strip()
                    try:
                        data = eval(data)
                    except:
                        #data missing
                        return False
                    self.re_temp = data
                    return True
            return False
        except UnicodeError:
            return False   

    # 口罩识别，属性分析
    # options 1: 主要人脸中心X
    # options 2: 主要人脸中心Y
    # options 3: 主要人脸是否佩戴口罩
    # options 4: 戴口罩人数
    # options 5: 不带口罩人数
    def face_mask_attribute(self,options):
        try:
            data = None
            if options == 1:
                data = self.re_temp[2][0]
            if options == 2:
                data = self.re_temp[2][1]
            elif options == 3:
                data = self.re_temp[2][4]
            elif options == 4:
                data = self.re_temp[0]
            elif options == 5:
                data = self.re_temp[1]
            return data
        except:
            return None

    # 人脸属性，检测到人脸？
    def face_attribute(self):
        try:
            result = self.uart.readline()
            if result:
                result = result.decode()
                if result[:3] == 'K34':
                    data = (result[4:]).strip()
                    try:
                        data = eval(data)
                    except:
                        #data missing
                        return False
                    self.re_temp = data
                    return True
            return False
        except UnicodeError:
            return False   

    # 人脸属性，数量分析
    # options 1: 总人数
    # options 2: 男生数量
    # options 3: 女生数量
    # options 4: 张嘴人数
    # options 5: 微笑人数
    # options 6: 戴眼镜人数
    def face_attribute_num(self,options):
        try:
            data = None
            if options == 1:
                data = self.re_temp[0]
            elif options == 2:
                data = self.re_temp[1]
            elif options == 3:
                data = self.re_temp[0] - self.re_temp[1]
            elif options == 4:
                data = self.re_temp[2]
            elif options == 5:
                data = self.re_temp[3]
            elif options == 6:
                data = self.re_temp[4]
            return data
        except:
            return None

    # 人脸属性，主角分析
    # options 1: 坐标X
    # options 2: 坐标Y
    # options 3: 性别
    # options 4: 是否张嘴
    # options 5: 是否微笑
    # options 6: 是否戴眼镜
    def face_attribute_main(self,options):
        try:
            data = None
            if options == 1:
                data = self.re_temp[5][0]
            elif options == 2:
                data = self.re_temp[5][1]
            elif options == 3:
                data = self.re_temp[5][2]
            elif options == 4:
                data = self.re_temp[5][3]
            elif options == 5:
                data = self.re_temp[5][4]
            elif options == 6:
                data = self.re_temp[5][5]
            return data
        except:
            return None

    def hand_detect(self):
        try:
            result = self.uart.readline()
            if result:
                result = result.decode()
                if result[:3] == 'K70':
                    data = (result[4:]).strip()
                    try:
                        data = eval(data)
                    except:
                        #data missing
                        return False
                    self.re_temp = data
                    return True
            return False
        except UnicodeError:
            return False   
    
    def hand_coordinate(self,options):
        try:
            data = None
            if options == 0:
                data = self.re_temp[0]
            elif options == 1:
                data = self.re_temp[1]
            return data
        except:
            return None


            
    
    # # 设置环境噪声基准
    # def audio_noisetap(self):
    #     self.uart.write("K63\r\n")
    
    # # 添加语音关键词标签 
    # def speech_add_tag(self,id,cmd="K64"):
    #     self.uart.write("%s %s\r\n" %(cmd,id))
    
    # # 识别语音关键词
    # def speech_run(self,cmd="K65"):
    #     self.uart.write(cmd + "\r\n")
    #     time.sleep_ms(3000) 
    #     self.cmd = cmd
    #     self._uart_re(cmd)
    #     return self.get_re(cmd)[0]

    # # 保存语音关键词模型文件 / eg:'cmd.json'
    # def speech_save_model(self,model,cmd="K66"):
    #     self.uart.write("%s %s\r\n" %(cmd,model))

    # # 加载语音关键词模型文件 / eg:'cmd.json'
    # def speech_load_model(self,model,cmd="K67"):
    #     self.uart.write("%s %s\r\n" %(cmd,model))



    """
    扫码
    """
    def scan_qrcode(self,cmd="K20"):
        self.uart.write(cmd + "\r\n")
        time.sleep_ms(1000) 
        self.cmd = cmd
        self._uart_re(cmd)
        return self.get_re(cmd)[0]

    def scan_barcode(self,cmd="K22"):
        self.uart.write(cmd + "\r\n")
        time.sleep_ms(1000) 
        self.cmd = cmd
        self._uart_re(cmd)
        return self.get_re(cmd)[0]

    def scan_Apriltag(self,cmd="K23"):
        self.uart.write(cmd + "\r\n")
        time.sleep_ms(1000) 
        self.cmd = cmd
        return self._uart_re(cmd)

    """
    颜色识别
    """
    # 校准颜色 / eg: name='blue'
    def color_cali(self,name,cmd="K16"):
        self.uart.write("%s %s\r\n" %(cmd,name))
    
    # KOI色块追踪 / eg: name='blue'
    def color_tracking(self,name,cmd="K15"):
        self.uart.write("%s %s\r\n" %(cmd,name))
        time.sleep_ms(100) 
        self.cmd = cmd
        return self._uart_re(cmd)

    #线条识别（name为线条颜色）
    def line_tracking(self,name,cmd="K12"):
        self.uart.write("%s %s\r\n" %(cmd,name))
        time.sleep_ms(100) 
        self.cmd = cmd
        return self._uart_re(cmd)

    # 圆形识别（th为阈值）
    def circle_detect(self,th=2000,cmd="K10"):
        self.uart.write("%s %s\r\n" %(cmd,th))
        time.sleep_ms(100) 
        self.cmd = cmd
        return self._uart_re(cmd)
        
    # 矩形识别（th为阈值）
    def rectangle_detect(self,th=6000,cmd="K11"):
        self.uart.write("%s %s\r\n" %(cmd,th))
        time.sleep_ms(100) 
        self.cmd = cmd
        return self._uart_re(cmd)


    """
    更多
    """
    # 停止人脸追踪yolo模型和特征分类模型
    def stop_kpu(self,cmd="K98"):
        self.uart.write("%s\r\n" %(cmd))
    
    # 重启KOI   
    def reset(self,cmd="K99"):
        self.uart.write("%s\r\n" %(cmd))
        self._wait_koi()