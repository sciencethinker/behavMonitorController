import os
class System:
    '''
    当前仅支持windows系统
    '''
    def shutdown(self,time):
        os.system('shutdown /s /t {}'.format(time))
    def kill(self,pid):
        os.system('taskkill /PID {}'.format(pid))

