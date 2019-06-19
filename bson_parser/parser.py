import sys
import os
from windows import *

def usage():
    sys.stderr.write('usage: python parser.py log.bson\n')
    sys.exit(1)

def _main():
    if len(sys.argv) != 2:
        usage()

    # Remove shit in BSON file used by Cuckoo server...
    fn = sys.argv[1]
    newfn = fn + '-modified'

    # If the new datafile already exists, remove it
    if os.path.exists(newfn):
        os.remove(newfn)

    with open(fn, 'rb') as fr:
        for line in fr:
            if 'BSON\n' == line:
                continue

            if 'BSON\n' in line:
                line = line[:-5]

            with open(newfn,'ab') as fa:
                fa.write(line)

#   # Remove last character (useless newline)
#   with open(newfn, 'rb+') as fr:
#       fr.seek(-1, os.SEEK_END)
#       fr.truncate() 
#   return

    mon = WindowsMonitor()
    mon.matched = True

    # Parse BSON file
    rv = mon.parse(newfn)

    # Print each system event
    for e in rv:
        sys.stdout.write('{0}\n'.format(e))

    # Return list of processes
    # associated with the events
    procs = mon.run()

    sys.stdout.write('\n\nProcesses:\n')
    for p in procs:
        sys.stdout.write('\t{0}\n'.format(p['process_name']))
    sys.stdout.write('\n')

    # Remove temporary BSON file
    os.remove(newfn)

if __name__ == '__main__':
    _main()
