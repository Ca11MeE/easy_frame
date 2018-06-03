from threading import Timer,Thread
import sched, time, schedule

_sched = schedule.Scheduler()


class sech_obj:

    def __init__(self,fun,delay):
        self.__fun=fun
        self.__delay=delay

    def enter(self):
        global _sched
        # print(type(fun))
        print(_sched.jobs)
        _sched.every(self.__delay).seconds.do(self.run_target)
        print(_sched.jobs)

    def run(self):
        while True:
            Timer(1, _sched.run_pending).start()
            time.sleep(1)

    def run_target(self):
        self.__fun


def test():
    print("111")


# _sched.run_pending()

s=sech_obj(fun=test(),delay=1)
s.enter()
s.run()

