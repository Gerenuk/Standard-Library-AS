import csv
import gzip
import io
import webbrowser


class KaggleSubmitter:
    def __init__(self, header, dest_file_getter=None, gzip=True, web_kaggle_urlname=None):
        self.header = header
        self.dest_file_getter = dest_file_getter
        self.gzip = gzip
        self.web_kaggle_urlname = web_kaggle_urlname

    def submit(self, filename, data):
        if self.dest_file_getter:
            filename = self.dest_file_getter(filename)

        if self.gzip or filename.endswith(".gz"):
            file = io.TextIOWrapper(gzip.open(filename, "w"), newline="", write_through=True)
        else:
            file = open(filename, "w", newline="")

        with file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            for row in data:
                writer.writerow(row)
        print("Submission file {} created with {} data points".format(filename, len(data)))

    def open_browser(self):
        if self.web_kaggle_urlname:
            webbrowser.open_new_tab("http://www.kaggle.com/c/{}/submissions/attach".format(self.web_kaggle_urlname))
        else:
            print("No web url configured for KaggleSubmitter")
