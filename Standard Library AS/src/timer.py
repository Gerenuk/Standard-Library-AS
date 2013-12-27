import datetime


class Timer:
    def __init__(self,
                 timedelta_format="{hour:.0f}h{min:02.0f}m{sec:02.0f}s",
                 time_format="%H:%M:%S",
                 text_format="Est. finish: {timetextend} (+{timetextleft})"):
        self.timedelta_format = timedelta_format
        self.time_format = time_format
        self.text_format = text_format

        self.start()

    def start(self):
        self.starttime = datetime.datetime.now()

    def __str__(self):
        return "Timer({})".format(self._format_time(self.starttime))

    def info(self, ratio=None):  # TODO: handle out of range
        if ratio is not None:
            now = datetime.datetime.now()
            timedelta_passed = now - self.starttime
            time_end = self.starttime + timedelta_passed / ratio
            timedelta_left = time_end - now
            return {"timestart":self.starttime,
                    "timetextstart":self._format_time(self.starttime),
                    "timepassed":timedelta_passed,
                    "timetextpassed":self._format_timedelta(timedelta_passed),
                    "timenow":now,
                    "timetextnow":self._format_time(now),
                    "timeleft":timedelta_left,
                    "timetextleft":self._format_timedelta(timedelta_left),
                    "timeend":time_end,
                    "timetextend":self._format_time(time_end),
                    }
        else:
            now = datetime.datetime.now()
            timedelta_passed = now - self.starttime
            return {"timestart":self.starttime,
                    "timepassed":timedelta_passed,
                    "timetextpassed":self._format_timedelta(timedelta_passed),
                    "timenow":now,
                    }

    def text(self, ratio=None):
        return self.text_format.format(**self.info(ratio))

    def _format_timedelta(self, timedelta):
        minutes, seconds = divmod(timedelta.total_seconds(), 60)
        hours, minutes = divmod(minutes, 60)
        return self.timedelta_format.format(hour=hours, min=minutes, sec=seconds)

    def _format_time(self, time):
        return time.strftime(self.time_format)


if __name__ == '__main__':
    import time
    from pprint import pprint
    t = Timer()
    time.sleep(2)
    pprint(t.info(0.1))
    print(t.text(0.1))
