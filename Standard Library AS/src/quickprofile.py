import cProfile


class QuickProfile:
    def __init__(self, profile_dumpfile=None, print_stats_sort=None):
        if print_stats_sort is True:
            print_stats_sort = "cumulative"
        self.profile_dumpfile = profile_dumpfile
        self.print_stats_sort = print_stats_sort

        self.profiler = cProfile.Profile()

    def __enter__(self):  # TODO arguments?
        self.profiler.enable()

    def __exit__(self):
        self.profiler.disable()
        if self.profile_dumpfile:
            self.profiler.dump_stats(self.profile_dumpfile)
        if self.print_stats_sort:
            self.profiler.print_stats(self.print_stats_sort)
