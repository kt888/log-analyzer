from collections import defaultdict, Counter
import argparse


class Log:
    def __init__(self, log):
        self.log = log

    @property
    def date_info(self):
        return self.log.split(']')[0]

    @property
    def request_type(self):
        return self.log.split(']')[1].split()[0].replace('\"', '')

    @property
    def request_content(self):
        return self.log.split(']')[1].split()[1]

    @property
    def http_code(self):
        if self.log.split(']')[1].split()[2].split('/')[0] == 'HTTP':
            return int(self.log.split(']')[1].split()[-2])

    @property
    def request_bytes(self):
        return int(self.log.split(']')[1].split()[-1])


class LogAnalyzer:
    def __init__(self, file):
        self.file = file
        self.agg_bytes = defaultdict(int)
        self.counter = Counter()
        self.aggregate_bytes()

    def aggregate_bytes(self):
        for raw_log in self.file:
            log = Log(raw_log)
            if log.http_code == 200:
                self.agg_bytes[log.request_content] += log.request_bytes
                self.counter.update([log.request_content])
    
    def query(self, k):
        for elem in self.counter.most_common(k):
            key, count = elem
            print('{}\t{}'.format(key, self.agg_bytes[key]))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', help='input file', type=argparse.FileType('r'))
    parser.add_argument('--k', help='10', default=10, type=int)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    i = LogAnalyzer(args.input)
    i.query(args.k)



