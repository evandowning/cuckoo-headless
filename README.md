# cuckoo-headless
All the functionality of Cuckoo without all of the overhead

Original code for Cuckoo here: https://github.com/cuckoosandbox/cuckoo
Original code for Cuckoo monitor here: https://github.com/cuckoosandbox/monitor

## Requirements
  * Requirements for Cuckoo monitor and Cuckoo
  * Cuckoo monitor
    * sudo apt-get install mingw-w64 python-pip nasm
    * sudo pip install sphinx docutils

## Usage
  * Download cuckoo-headless folder onto target machine.
    ```
    $ git clone https://github.com/evandowning/cuckoo-headless.git
    $ cd cuckoo-headless
    ```
  * Download, compile, and copy cuckoo monitor contents.
    ```
    $ git clone https://github.com/evandowning/monitor.git
    $ git checkout myworking
    $ make
    ```
  * Modify analysis.conf file to specify settings.
  * On target machine run:
    ```
    $ python analyzer.py
    ```
  * Logs will be outputted to log.bson
