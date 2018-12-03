# Extracts raw Cuckoo logs from nvmtrace (using extending-api branch of Cuckoo)

import sys
import os

sys.path.append('../')
from bson_parser.windows import *

# Extracts API call sequences from Cuckoo BSON data
def extract(bsonDir,out_fn):
    timeline = dict()

    # Get each bson file
    for fn in os.listdir(bsonDir):
        # Ignore our tmp file
        if fn == 'tmp':
            continue

        # We must write the bson data to a temporary file first
        tmpfn = os.path.join(bsonDir,'tmp')

        # Remove temporary file if it already exists
        if os.path.exists(tmpfn):
            os.remove(tmpfn)

        # Extract log contents
        with open(os.path.join(bsonDir,fn), 'rb') as fr:
            for line in fr:
                if 'BSON\n' == line:
                    continue

                if 'BSON\n' in line:
                    line = line[:-5]

                with open(tmpfn,'ab') as fa:
                    fa.write(line)

        # If nothing was parsed, continue
        if not os.path.exists(tmpfn):
            continue

        mon = WindowsMonitor()
        mon.matched = True

        # Parse BSON file
        rv = mon.parse(tmpfn)

        # Extract data
        for e in rv:
            if 'api' in e:
                api = e['api']
                pc = e['eip']
                ts = str(e['time'])

                if ts not in timeline:
                    timeline[ts] = list()
                timeline[ts].append((pc,api))

        # Remove temporary BSON file
        os.remove(tmpfn)

    # Extract API call sequence (sort by time)
    with open(out_fn,'w') as fw:
        for k,v in sorted(timeline.iteritems(), key=lambda (k,v): int(k)):
            for pc,call in v:
                fw.write('{0} {1}\n'.format(pc,call))

def usage():
    print 'usage: python bson2sequence.py logs/ data.out'
    sys.exit(2)

def _main():
    if len(sys.argv) != 3:
        usage()

    bsonDir = sys.argv[1]
    out_fn = sys.argv[2]

    extract(bsonDir,out_fn)

if __name__ == '__main__':
    _main()
