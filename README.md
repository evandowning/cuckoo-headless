# cuckoo-headless
All the functionality of Cuckoo without all of the overhead

Original code for Cuckoo here: https://github.com/cuckoosandbox/cuckoo

Original code for Cuckoo monitor here: https://github.com/cuckoosandbox/monitor

## Requirements
  * Requirements for Cuckoo monitor and Cuckoo
  * Cuckoo monitor
    * sudo apt-get install mingw-w64 python-pip nasm
    * sudo pip install sphinx docutils

## Analyzer Usage
  * Download cuckoo-headless folder onto target machine.
    ```
    $ git clone https://github.com/evandowning/cuckoo-headless.git
    $ cd cuckoo-headless
    ```
  * Download, compile, and copy cuckoo monitor contents.
    ```
    $ git clone https://github.com/evandowning/monitor.git
    $ cd monitor
    $ git checkout myworking
    $ make
    $ cp -r bin ../windows-analyzer
    $ cd ../windows-analyzer
    ```
  * Modify analysis.conf file to specify settings.
  * On target machine run:
    Open command prompt in Administrator mode
    ```
    $ cd windows-analyer
    $ python analyzer.py
    ```
  * Logs will be outputted to stuff/ folder

## Parsing BSON file

I have also provided code to parse the resulting log.bson file.

```
$ cd bson-parser
$ python parser.py log.bson
```
