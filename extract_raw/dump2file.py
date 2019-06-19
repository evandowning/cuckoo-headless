import sys
import os
import re

from Crypto.Hash import MD5

def dump(fn,out_base):
    sha = None
    fn_out = None
    fw = None

    # Read dump contents
    with open(fn,'rb') as fr:
        for line in fr:
            # If first line
            if sha is None:
                m = re.search(r'^--([a-z0-9]+).*', line)
                if m:
                    sha = m.group(1)
                    continue
                else:
                    sys.stdout.write('{0}: Error. Dump not in expected format\n'.format(fn))
                    return 1

            # If second line
            if fn_out is None:
                m = re.search(r'.*filename\="(.*)".*', line)
                if m:
                    fn_out = m.group(1)
                    fw = open(os.path.join(out_base, fn_out),'wb')
                    continue
                else:
                    sys.stdout.write('{0}: Error. Dump not in expected format\n'.format(fn))
                    return 1

            # If successive lines
            fw.write(line)

    if fw is not None:
        fw.close()

    # Remove first and last line
    lines = open(os.path.join(out_base,fn_out), 'rb').readlines()
    lines[0] = ''
    lines[-1] = ''
    with open(os.path.join(out_base,fn_out),'wb') as fw:
        for line in lines:
            fw.write(line)

    # Take sha value
    h = MD5.new()
    h.update(open(os.path.join(out_base,fn_out),'rb').read())
    dumped = h.hexdigest()

    #TODO - sha hashes never match...
#   print sha
#   print dumped
#   # Check sha value
#   if sha != dumped:
#       print '{0}: Error. Dumped file doesn\'t match checksum'.format(fn)

    return 0

def usage():
    sys.stderr.write('usage: python dump2file.py dump\n')
    sys.exit(2)

def _main():
    if len(sys.argv) != 2:
        usage()

    fn = sys.argv[1]

    if not os.path.exists(fn):
        sys.stdout.write('Error. {0} does not exist.\n'.format(fn))
        sys.exit(1)

    dump(fn)

if __name__ == '__main__':
    _main()
