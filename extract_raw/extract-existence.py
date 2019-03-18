import sys
import os
import numpy as np
from multiprocessing import Pool

import bson2sequence

def extract_wrapper(args):
    return bson2sequence.extract(*args)

# Gets raw files and their base directory names
# NOTE: I assume there's been only one run of each sample
def getFiles(folder,sampleMap):
    # Get base directories
    dirs = os.listdir(folder)

    ignore_dir = ['logs']
    ignore_fn  = ['','dump.pcap','analysis.log','stuff.zip']

    # Get raw files
    for d in dirs:
        # Ignore samples we don't care about
        if d not in sampleMap.keys():
            continue

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
    sys.stdout.write('usage: python extract-existence.py nvmtrace-cuckoo-data/ api.txt label.txt sample_hash.txt output.csv\n')
    sys.exit(2)

def _main():
    if len(sys.argv) != 6:
        usage()

    rawDir = sys.argv[1]
    api_file = sys.argv[2]
    label_file = sys.argv[3]
    samples_file = sys.argv[4]
    outfile = sys.argv[5]

    # If outfile already exists, remove it
    if os.path.exists(outfile):
        os.remove(outfile)

    # Get number of API calls
    a = 0
    apiMap = dict()
    with open(api_file, 'rb') as fr:
        for e,line in enumerate(fr):
            line = line.strip('\n')
            apiMap[line] = e
            a += 1

    # Get label integer values
    labelMap = dict()
    with open(label_file,'r') as fr:
        for e,line in enumerate(fr):
            line = line.strip('\n')
            labelMap[line] = e

    # Get sample labels
    sampleMap = dict()
    with open(samples_file,'r') as fr:
        for line in fr:
            line = line.strip('\n')
            h,c = line.split('\t')
            sampleMap[h] = labelMap[c]

    # Get raw files and their corresponding directory
    rv = getFiles(rawDir,sampleMap)

    # Construct args
    args = [(h,d,raw) for h,d,raw in rv]

    # Extract each raw data file
    pool = Pool(20)
    results = pool.imap_unordered(extract_wrapper, args)

    # Consolidate all features to single CSV file
    with open(outfile, 'a') as fa:
        for e,r in enumerate(results):
            sys.stdout.write('Extracting data: {0}/{1}\r'.format(e+1,len(args)))
            sys.stdout.flush()

            h,seq = r

            # Remove PC from each sequence
            seq = [s.split(' ')[1] for s in seq]

            # Replace API calls with their unique integer value
            # https://stackoverflow.com/questions/3403973/fast-replacement-of-values-in-a-numpy-array#3404089
            seq = np.array(seq)
            newseq = np.copy(seq)
            for k,v in apiMap.iteritems():
                newseq[seq==k] = v
            seq = newseq

            x = np.array([0]*a)

            # Create feature vector for frequency features
            sa = set(seq)

            for i in sa:
                x[int(i)] = 1

            # Append data to CSV file
            fa.write('{0},'.format(h))
            fa.write('{0}'.format(','.join(map(str,x))))
            fa.write(',{0}\n'.format(sampleMap[h]))

    pool.close()
    pool.join()
    sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == '__main__':
    _main()
