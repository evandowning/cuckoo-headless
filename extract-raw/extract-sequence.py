import sys
import os
import shutil
import zipfile
from multiprocessing import Pool

import dump2file
import bson2sequence

def extract(h,d,raw,outDir):
    # Dump file contents
    dump2file.dump(os.path.join(d,raw))

    # Uncompress zip file
    # From: https://stackoverflow.com/questions/3451111/unzipping-files-in-python
    zippath = os.path.join(d,'stuff.zip')
    with zipfile.ZipFile(zippath,'r') as zip_ref:
        zip_ref.extractall(d)

    # Parse bson files and extract data
    bson2sequence.extract(os.path.join(d,'logs'),os.path.join(outDir,h))

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
    print 'usage: python extract-sequence.py /data/arsa/nvmtrace-cuckoo-data/output /data/arsa/output-sequences'
    sys.exit(2)

def _main():
    if len(sys.argv) != 3:
        usage()

    rawDir = sys.argv[1]
    outDir = sys.argv[2]
    
    # Create output directory if it doesn't already exist
    if not os.path.exists(outDir):
        os.mkdir(outDir)

    # Get raw files and their corresponding directory
    rv = getFiles(rawDir)

    # Construct args
    args = [(h,d,raw,outDir) for h,d,raw in rv]

#   #TODO - debugging
#   for h,d,raw,outDir in args:
#       extract(h,d,raw,outDir)
#   return

    # Extract each raw data file
    pool = Pool(20)
    results = pool.imap_unordered(extract_wrapper, args)
    for e,r in enumerate(results):
        sys.stdout.write('Extracting data: {0}/{1}\r'.format(e+1,len(args)))
        sys.stdout.flush()
    pool.close()
    pool.join()
    sys.stdout.write('\n')
    sys.stdout.flush()

if __name__ == '__main__':
    _main()
