import time
import os
import itertools
import psutil
'''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ CONSTANT @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'''


'''@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Class @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'''
# def process_gen():
#     '''
#     创建生成器，单次迭以下内容:
#     psutil.Process(pid=20312, name='conhost.exe', status='running', started='11:34:42')
#     进程号，进程名，状态，开始时间
#     '''
#     return psutil.process_iter(attrs=['name'])

# processes = process_gen()
# process_names = [process.info['name'] for process in processes]

def process_gen(attrs='name'):
    '''
    创建生成器，单次迭以下内容:
    psutil.Process(pid=20312, name='conhost.exe', status='running', started='11:34:42')
    进程号，进程名，状态，开始时间
    '''
    return psutil.process_iter(attrs=[attrs])
class Process():
    def __init__(self):
        self.Progress = process_gen()

    #获取progress生成器中的指定属性(attribute)列表
    def get_attr(self,attr='name'):
        attr_list = [i.info[attr] for i in self.Progress]
        return attr_list



class SysAction():
    def shutdown(self,time):
        import os
        os.system('shutdown /s /t {}'.format(time))

    def killProgress_name(self,progress_name):
        os.system('taskkill /F /IM {}'.format(progress_name))

class timetrans():
    def week2number(self,week_name):
        week2num ={
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6,
            'Sunday': 7
        }
        return week2num[week_name]
    def judje_time(self,shut_time,span,curt_time):
        min = 60
        sec = 60
        hou = 24
        open_time = [shut_time[i] + span[i] for i in range(3)]


        tmp_s = open_time[2]%sec
        tmp_m = (open_time[1] + open_time[2]//sec)%min
        tmp_h = (open_time[0] + (open_time[1] + open_time[2]//sec)//min)%hou
        open_time  = [tmp_h,tmp_m,tmp_s]
        print(open_time)
        def judge(curt_time,base_time,is_more:bool):
            sym = '>' if is_more else '<'
            tmp0 = eval('curt_time[0] {} base_time[0]'.format(sym))
            tmp1 = eval('curt_time[0]==base_time[0] and curt_time[1] {} base_time[1]'.format(sym))
            tmp2 = eval('curt_time[0]==base_time[0] and curt_time[1]==base_time[1] and curt_time[2] {} base_time[2]'.format(sym))
            result = tmp0 or tmp1 or tmp2
            print(result)
            return result
        reslut = True if  judge(curt_time,shut_time,True) or judge(curt_time,open_time,False) else False
        return reslut



'''
周天至周五
10点钟后自动关闭P社游戏，
12点钟后自动关闭Steam,荐片
'''
def close_game(shut_time,
               span,
               during_time:'周几到周几',
               pross:'当前时刻的进程类',
               close_name_list:'list:指定关闭的进程名称'):
    '''
    :param shut_time::'list like:[10,11,2]时分秒'
    :param span: :'list like:[10,11,2]时分秒'
    :param during_time: [1,2,3,...] means [Monday,Tuesday,Wednesday,...]
    :param pross: current process
    :return:
    '''

    #当前时间与当前工作日
    curtime = time.strftime('%H:%M:%S')
    curtime = [int(i) for i in curtime.split(':')]
    week_time = timetrans().week2number(time.strftime('%A'))
    in_time = timetrans().judje_time(shut_time,span,curtime)
    in_week = week_time in during_time

    #关闭程序
    if in_time and in_week:
        for sub_close in close_name_list:
            if sub_close in Process().get_attr():
                SysAction().killProgress_name(sub_close)

close_game(shut_time=[17,0,0],span=[2,3,4],during_time=[1,2,3,4,5,6,7],pross=Process(),close_name_list=['steam.exe'])
process = Process()
print(process.get_attr())
