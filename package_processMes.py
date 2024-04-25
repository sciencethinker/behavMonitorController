'''
构建：
存储进程信息的类对象
1.进程对象
2.时间对象
3.日志对象
4.行为监测与控制对象
5.系统行为对象

已经定义的类：
1.Interval    区间对象
2.Time        时间对象
3.Process
4.Monitor
5.Controller
6.BehavMonCtrl
'''
import time
import numpy as np
import psutil
def get_pid_by_name(name):
    pass

#定义区间，使用in判断值是否在区间中
class Interval:
    def __init__(self,start,end,open=(True,True),cycle=None):
        self.start = start
        self.end = end
        self.open = open
        self.cycle = cycle
        #当num为None时，默认为顺序结构
        if self.cycle == None and self.start > self.end:
            raise Exception("haven\'t set cycle for this Interval,so start must smaller than end! your start:{0} -- end:{1}".format(start,end))
        if self.start > self.end:self.end += self.cycle

    # use “in” to judge num is in or not in interval
    def __contains__(self, num):
        return self.inTerval(num)

    def inTerval(self,num):
        if num < self.start:
            num += self.cycle

        compare = lambda intr,operator,boundary:eval("{0}{1}{2}".format(intr,operator,boundary))
        loper = '>' + '=' if self.open[0] else '>'
        roper = '<' + '=' if self.open[1] else '<'
        is_in = True if compare(num,loper,self.start) and compare(num,roper,self.end) else False
        return is_in

class TimeInterval:
    '''
    时间区间实例构建方式:
        instance = TimeInterval(timeInterval)
    '''
    Allday_cycle = 24 * 60 * 60  # 一整天的秒数为一个cycle
    AlldayLinear = [60 ** 2, 60, 1]#指定全天的线性转换方式 1hour = 3600s ,1min = 60s ,1s = 1s --> [a,b,c].T[3600,60,1] --> scalar = 3600a + 60b + 1c
    #全局线性时间线性转换方式
    LinearMa = np.eye(9)  # 生成9*9单位阵
    LinearMa[8, 6] = 1  #调整week 使得传入week + 1 localtime中week从周一为0，周天为6 矫正为1开始，7结束
    LinearMa[3:,8] = np.array(AlldayLinear + [0,0,0]) #构建allday向量-->[0,0,0,3600,60,1,0,0,0] 仅hour min sec具有加性关系
    # 1hour = 3600s ,1min = 60s ,1s = 1s --> [a,b,c] --> scalar = 3600a + 60b + 1c
    def __init__(self,year=None,mon=None,mday=None,
                 hour=None,min=None,sec=None,
                 week=None,yday=None,allday=None,
                 isdst=None):
        '''
        构建指定的时间区间
        :param year: 年 (start,end,ifopen:Tuple)
        :param mon:  月 (int,int,(True,False))
        :param mday: 月中第几天 表示次序 (int,int,(True,False))
        :param hour: 小时 ...
        :param min: 分钟  ...
        :param sec: 秒   ...
        :param week: 单周区间 ...
        :param yday: 一年中的天数区间  *******((hour,min,sec),(hour,min,sec)),(True,False))********
        :param allday:一整天的所有秒数，如果想要规定在一天的某个时刻至某个时刻的区间，则使用这个关键字参数构建，而不是hour,min,sec
        :param isdst:是否是夏令时
        '''

        #创建时间区间 em.Interval(*(startY,endY,),365)
        self.yearitv = Interval(*year,None) if year else None
        self.monitv = Interval(*mon,cycle=31) if mon else None
        self.mdayitv = Interval(*mday,cycle=31) if mday else None
        self.houritv = Interval(*hour,cycle=24) if hour else None
        self.minitv = Interval(*min,cycle=60) if min else None
        self.secitv = Interval(*sec,cycle=60) if sec else None
        self.weekitv = Interval(*week,cycle=7) if week else None
        self.ydayitv = Interval(*yday,cycle=365) if yday else None
        self.alldayitv = None
        if allday:
            allday = list(allday)
            allday[0] = self.transTime(allday[0],TimeInterval.AlldayLinear) #index0: start time
            allday[1] = self.transTime(allday[1],TimeInterval.AlldayLinear) #index1: end time
            self.alldayitv = Interval(*allday,cycle=TimeInterval.Allday_cycle)
        self.isdst = isdst
        #timeIntervalList以列表的形式记录所有时间区间

        self.timeIntervalList = [self.ydayitv,self.monitv,self.mdayitv,self.houritv,self.minitv,self.secitv,
                                 self.weekitv,self.ydayitv,self.alldayitv] #9种时间
    def transTime(self,timeVec,linearVec):
        '''
        将时间向量(a,b,c)通过线性的方式 转换为标量
        :param args:
        :param kwargs:
        :return:
        '''
        #将timeVec与linearVec转换为np向量
        if not timeVec.__class__ == np.ndarray:timeVec = np.array(timeVec)
        if not linearVec.__class__ == np.ndarray:linearVec = np.array(linearVec)
        #线性变换
        scalar = np.dot(timeVec,linearVec)
        return scalar

    def inTimeInterval(self,time):
        '''
        判定时间是否在设置的时间区间内
        :param time: 支持__contains__索引操作 --> 且时间向量应为[year,mon,monday,hour,min,sec,week,yday,isdst]
        :return:
        '''
        initv = True
        #time --> np.arry(y,mon,mday,hour,min,sec,week,allday) 线性变换
        time = np.array(list(time[:-1])+[1]) #去除index-1的isidst,并在最后一列加1，使其可以添加固定常数 len=8
        time = np.dot(time,TimeInterval.LinearMa) #len = 9
        for i,itv in enumerate(self.timeIntervalList):
            if itv == None:continue
            initv = time[i] in itv
            if initv == False:break
        return initv

    def __contains__(self, time):
        return self.inTimeInterval(time)

    def inIterval(self,localTime):
        pass

class Time:
    # frequence = 30s
    def __init__(self,curtime = time.time()):
        '''
        :param time: 时间戳-float
        '''
        self.localTime = time.localtime(curtime)
        self.time = curtime

    def ifDuring(self,timeFrontier):
        self.localTime in timeFrontier

    @staticmethod
    def during(now,start):
        during = now.time - start.time
        return during

class Process:
    def __init__(self,pid):
        self.process = psutil.Process(pid)
        started = self.process.create_time()
        self.startTime = Time(started)
        self.nowTime = Time()

    def freshTime(self):
        self.nowTime = Time()

    def duringTime(self):
        during = Time.during(self.nowTime,self.startTime)
        return during



class Monitor:
    pass

class Controller:
    def __init__(self):
        pass

class BehavMonCtrl:
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
    '''
    log类对象，监控违规信息与操作记录
    '''
    def __init__(self,filePath):
        self.path = filePath


if __name__ == '__main__':
    alldayitv= ([15,0,0],[1,0,0])
    teitv = TimeInterval(allday=alldayitv)
    print('1',Time().localTime in teitv)




