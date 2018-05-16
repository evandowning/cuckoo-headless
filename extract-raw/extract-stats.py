import sys
import os
import shutil
import zipfile
from multiprocessing import Pool
import dateutil.parser as dateparser
import datetime

import dump2file
import bson2stat

def extract(h,d,raw):
    # Dump file contents
    dump2file.dump(os.path.join(d,raw))

    # Uncompress zip file
    # From: https://stackoverflow.com/questions/3451111/unzipping-files-in-python
    zippath = os.path.join(d,'stuff.zip')
    with zipfile.ZipFile(zippath,'r') as zip_ref:
        zip_ref.extractall(d)

    # Parse bson files and extract data
    stats = bson2stat.extract(os.path.join(d,'logs'))

    # Parse amount of time malware ran
    # From: https://stackoverflow.com/questions/3346430/what-is-the-most-efficient-way-to-get-first-and-last-line-of-a-text-file#18603065
    with open(os.path.join(d,'analysis.log'),'r') as fr:
        start = fr.readline()
        fr.seek(-2, os.SEEK_END)
        while fr.read(1) != b"\n":   # Until EOL is found...
            fr.seek(-2, os.SEEK_CUR) # ...jump back the read byte plus one more.
        end = fr.readline()

    # Compute total time elapsed
    startStr = ' '.join(start.split(' ')[:2])
    endStr = ' '.join(end.split(' ')[:2])
    startTime = dateparser.parse(startStr)
    endTime = dateparser.parse(endStr)

    # Clean up files
    for fn in os.listdir(d):
        # Don't remove raw file
        if fn == raw:
            continue

        path = os.path.join(d,fn)

        # If directory
        if os.path.isdir(path):
            shutil.rmtree(path)
        # If file
        else:
            os.remove(path)

    # Return stats
    return h,{'stats': stats, 'time': endTime-startTime}

def extract_wrapper(args):
    return extract(*args)

# Gets raw files and their base directory names
# NOTE: I assume there's been only one run of each sample
def getFiles(folder):
    # Get base directories
    dirs = os.listdir(folder)

    ignore_dir = ['logs']
    ignore_fn  = ['','dump.pcap','analysis.log','stuff.zip']

    # Get raw files
    for d in dirs:
        for directory,dirname,files in os.walk(os.path.join(folder,d)):
            # Ignore directories
            base = os.path.basename(directory)
            if base in ignore_dir:
                continue

            for fn in files:
                # Ignore files
                if fn not in ignore_fn:
                    yield (d,directory,fn)

def usage():
    print 'usage: python extract-stats.py /data/arsa/nvmtrace-cuckoo-data/malware output-samples-ran output-samples-host'
    sys.exit(2)

def _main():
    if len(sys.argv) != 4:
        usage()

    rawDir = sys.argv[1]
    outRan = sys.argv[2]
    outHost = sys.argv[3]

    # Get raw files and their corresponding directory
    rv = getFiles(rawDir)

    # Construct args
    args = [(h,d,raw) for h,d,raw in rv]

    finalStats = dict()
    ranHashes = list()
    hostHashes = list()

#   #TODO - debugging
#   for h,d,raw in args:
#       h,finalStats[h] = extract(h,d,raw)
#       print h, finalStats[h]
#   return

    # Extract each raw data file
    pool = Pool(20)
    results = pool.imap_unordered(extract_wrapper, args)
    for e,r in enumerate(results):
        h = r[0]
        finalStats[h] = r[1]
        sys.stdout.write('Extracting data: {0}/{1}\r'.format(e+1,len(args)))
        sys.stdout.flush()
    pool.close()
    pool.join()
    sys.stdout.write('\n')
    sys.stdout.flush()

    # Compute final stats
    numran = 0
    numnet = 0
    for h in finalStats:
        if finalStats[h]['time'] >= datetime.timedelta(minutes=2):
            numran += 1 
            ranHashes.append(h)

            if len(finalStats[h]['stats']['net']['host']) >= 3:
                numnet += 1
                hostHashes.append(h)

    # Print final stats
    print 'Stats:'
    print 'Total samples: ',len(args)
    print 'Number of samples which ran for 2 minutes: ', numran
    print 'Number of samples which ran for 2 minutes and contacted 3 or more 3 hosts: ', numnet

    # Print hashes of stats
    with open(outRan,'w') as fw:
        for h in ranHashes:
            fw.write('{0}\n'.format(h))

    with open(outHost,'w') as fw:
        for h in hostHashes:
            fw.write('{0}\n'.format(h))

if __name__ == '__main__':
    _main()
