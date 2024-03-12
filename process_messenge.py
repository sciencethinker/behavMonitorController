'''
构建：
存储进程信息的类对象
1.进程对象
2.时间对象
3.日志对象
4.行为监测与控制对象
5.系统行为对象
'''
import time
import os
import psutil

class Time:
    # frequence = 30
    def __init__(self,time = time.time()):
        '''
        :param time: 时间戳-float
        '''
        self.localTime = time.localtime(time)
        self.time = time

    def ifDuring(self,frontier):

        pass

    def spend(self):
        pass

class Process:
    def __init__(self,pid):
        self.process = psutil.Process(pid)
        started = self.process.create_time()
        self.started = Time(started)
        self.nowTime = Time()

    def freshTime(self):
        self.nowTime = Time()

class System:
    '''
    当前仅支持windows系统
    '''
    def shutdown(self,time):
        os.system('shutdown /s /t {}'.format(time))
    def kill(self,pid):
        os.system('taskkill /PID {}'.format(pid))

class BehavMonCon:
    '''行为监测与控制类'''
    def __init__(self,freshTime = 60):
        self.freshTime = freshTime # 指定监测器刷新频率 /s
        self.processIter = psutil.process_iter()
        self.open = False
        self.taskDict = {}  #tasklist设置监控任务以及应对方案

    def openMonitor(self):
        self.open = True
        while self.open:
            time.sleep(self.freshTime)
            self.processList = psutil.process_iter()
            if self.open:break #拓展：创建可视化窗口设置密码等系列行为要求，可停止open服务

    def closeMonitor(self,*args,**kwargs):
        ''' 拓展：设置密码等系列行为要求，可终止open服务'''
        self.open = False

    def monitor(self):
        pass
    def action(self):
        pass







class Log:
    def __init__(self,filePath):
        self.path = filePath









