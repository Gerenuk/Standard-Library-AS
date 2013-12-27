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
        if ratio > 0.01:
            return (self.starttime + self.duration() / ratio).strftime(self.timeendformat)
        else:
            return datetime.timedelta(0)

    def time_left(self, ratio):
        seconds_left = self._time_left(ratio).total_seconds()
        return "{:.0f}h{:02.0f}m".format(*divmod(seconds_left // 60, 60))

    def _time_left(self, ratio):
        if ratio > 0.01:
            return self.duration() / ratio * (1 - ratio)
        else:
            return datetime.timedelta(0)

    def time_taken(self):
        return "{:.0f}h{:02.0f}m".format(*divmod(self.duration().total_seconds() // 60, 60))


if __name__ == '__main__':
    import time
    t = Timer()
    time.sleep(2)
    print(t.timeend(0.01))
