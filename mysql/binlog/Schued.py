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

    def run_target(self):
        print("222")
        return self.__fun


def test(str):
    print(str)
    return test


# _sched.run_pending()

s=sech_obj(fun=test("111"),delay=1)
s.enter()
s2=sech_obj(fun=test("222"),delay=2)
s2.enter()
s3=sech_obj(fun=test("333"),delay=3)
s3.enter()


def run_always():
    while True:
        _sched.run_all()
        time.sleep(1)


run_always()