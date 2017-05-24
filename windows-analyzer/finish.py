import sys
import os
import time
import shutil
import requests

def compress(path):
    if not os.path.exists(path):
        print 'Error: {0} does not exist'.format(path)
        sys.exit(1)

    shutil.make_archive(path, 'zip', path)

    return path + '.zip'

def usage():
    print 'usage: python finish.py ip'
    sys.exit(2)

def _main():
    if len(sys.argv) != 2:
        usage()

    # Get IP address and port number
    ip = sys.argv[1]

    # Compress target folder
    path = compress("stuff")

    files = {'file': ('stuff.zip', open(path,'rb').read())}
    r = requests.post("http://{0}/upload".format(ip), files=files)

if __name__ == '__main__':
    _main()
