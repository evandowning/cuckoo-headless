import sys
import os
from multiprocessing import Pool

import bson2sequence

def extract_wrapper(args):
    return bson2sequence.extract(*args)

# Gets raw files and their base directory names
# NOTE: I assume there's been only one run of each sample
def getFiles(folder,hashes):
    # Get base directories
    dirs = os.listdir(folder)

    ignore_dir = ['logs']
    ignore_fn  = ['','dump.pcap','analysis.log','stuff.zip']

    # Get raw files
    for d in dirs:
        # Ignore hashes we don't care about
        if d not in hashes:
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
    print 'usage: python extract-sequence.py nvmtrace-cuckoo-data/ sample_hash.txt out_sequences/'
    sys.exit(2)

def _main():
    if len(sys.argv) != 4:
        usage()

    rawDir = sys.argv[1]
    hashFN = sys.argv[2]
    outDir = sys.argv[3]

    # Create output directory if it doesn't already exist
    if not os.path.exists(outDir):
        os.mkdir(outDir)

    # Get list of hashes to consider
    hashes = list()
    with open(hashFN,'r') as fr:
        for line in fr:
            hashes.append(line.split('\t')[0])

    # Get raw files and their corresponding directory
    rv = getFiles(rawDir,hashes)

    # Construct args
    args = [(h,d,raw) for h,d,raw in rv]

    # Extract each raw data file
    pool = Pool(20)
    results = pool.imap_unordered(extract_wrapper, args)
    for e,r in enumerate(results):
        sys.stdout.write('Extracting data: {0}/{1}\r'.format(e+1,len(args)))
        sys.stdout.flush()

        h,seq = r

        # Write sequence to file
        path = os.path.join(outDir,h)
        with open(path,'w') as fw:
            for s in seq:
                fw.write('{0}\n'.format(s))

    pool.close()
    pool.join()
    sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == '__main__':
    _main()
