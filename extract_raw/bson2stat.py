# Extracts raw Cuckoo logs from nvmtrace (using extending-api branch of Cuckoo)

import sys
import os

sys.path.append('../')
from bson_parser.windows import *

# Extracts network stats from event
def getNetwork(event,stats):
    if 'szURL' in event['arguments']:
        stats['url'].add(event['arguments']['szURL'])
    elif 'lpszUrl' in event['arguments']:
        stats['url'].add(event['arguments']['lpszUrl'])

    elif 'lpszServerName' in event['arguments']:
        stats['host'].add(event['arguments']['lpszServerName']) 
    elif 'pNodeName' in event['arguments']:
        stats['host'].add(event['arguments']['pNodeName']) 

    elif 'nServerPort' in event['arguments']:
        stats['port'].add(event['arguments']['nServerPort'])

    elif 'Dns' in event['api']:
        if 'lpstrName' in event['arguments']:
            stats['dns'].add(event['arguments']['lpstrName'])

    return stats

# Extracts stats from Cuckoo BSON data
def extract(bsonDir):
    netStats = dict()
    netStats['url'] = set()
    netStats['host'] = set()
    netStats['port'] = set()
    netStats['dns'] = set()

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
                # Get network statistics
                netStats = getNetwork(e,netStats)

        # Remove temporary BSON file
        os.remove(tmpfn)

    # Return stats
    return {'net': netStats}

def usage():
    sys.stdout.write('usage: python bson2stat.py logs/\n')
    sys.exit(2)

def _main():
    if len(sys.argv) != 2:
        usage()

    bsonDir = sys.argv[1]

    stats = extract(bsonDir)

if __name__ == '__main__':
    _main()
