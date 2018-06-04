from threading import Timer,Thread
import schedule,time

_sched = schedule.Scheduler()



class sech_obj:

    def __init__(self,fun,delay):
        self.__fun=fun
        self.__delay=delay

    def enter(self):
        global _scheds
        # print(type(fun))
        _sched.every(self.__delay).seconds.do(self.__fun)

    def run_target(self):
        return self.__fun

def run():
    while True:
        # print(_sched.jobs)
        _sched.run_pending()
        # print(_sched.jobs)
        time.sleep(1)


print('xml自动更新调度启动')
Thread(target=run).start()