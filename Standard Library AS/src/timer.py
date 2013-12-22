import datetime


class Timer:
    def __init__(self, secondsformat="{:.1f}s", timeendformat="%H:%M:%S"):
        self.secondsformat = secondsformat
        self.timeendformat = timeendformat

        self.starttime = datetime.datetime.now()

    def duration(self):
        return datetime.datetime.now() - self.starttime

    def __str__(self):
        return str(self.duration())

    def time_end(self, ratio):
        timenow = datetime.datetime.now()
        timedelta = timenow - self.starttime
        return (timenow + timedelta / ratio).strftime(self.timeendformat)

    def time_left(self, ratio):
        timenow = datetime.datetime.now()
        timedelta = timenow - self.starttime
        seconds_left = (timedelta / ratio * (1 - ratio)).total_seconds()
        return "{}h{}m".format(*divmod(seconds_left // 60, 60))

    def time_taken(self):
        return "{}h{}m".format(*divmod(self.duration().total_seconds // 60, 60))


if __name__ == '__main__':
    import time
    t = Timer()
    time.sleep(2)
    print(t.timeend(0.01))
