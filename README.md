# cuckoo-headless
All the functionality of Cuckoo without all of the overhead

Original code for Cuckoo here: https://github.com/cuckoosandbox/cuckoo

## Usage
  * Download cuckoo-headless folder onto target machine.
    ```
    $ git clone https://github.com/evandowning/cuckoo-headless.git
    $ cd cuckoo-headless
    ```
  * Modify analysis.conf file to specify settings.
  * On target machine run:
    ```
    $ python analyzer.py
    ```
  * Logs will be outputted to log.bson
