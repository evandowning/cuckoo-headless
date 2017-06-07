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
    $ # git checkout extending-api  => unstable still
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

## Benefits

### Implemented by analyzer
- Easy to hook additional API calls
- Provides a basic human interaction simulation
  - Clicks on obvious buttons to progress a program/installation's execution
  - Moves mouse randomly
- Performs some trivial disguising to mask the presence of a virtual machine:
  - Change system clock to time of user's choosing
  - Change Windows product ID to random number
  - Change SCSI identifiers to random strings (i.e., qemu, vmware, virtual)
  - Change BIOS values (date, version, manufacturer, product name)
  - Change ACPI values to random ones
  - Change processor name if necessary
  - Change HDD path name to random one
  - Adds random files to the Desktop as misleading evidence that the virtual
    machine is used for tasks other than analyzing malware
    - Also makes it look like MS Office 2012
  - Makes it seem as though the virtual machine has been running for some time
    (randomly between 20 and 600 minutes). Some samples check if VM has been running
    for less than 10 minutes.
- Takes screenshots of OS's GUI for potential visual/graphic analysis
- Keeps track of files created (and potentially moved) by monitored processes

### Implemented by monitor
- Evades trivial sleeping efforts used by malware to delay its execution
  - Replaces value in NtDelayExecution
  - TODO
- Detects attempts of samples to unhook themselves from the monitor
  - **Not currently enabled**
  - TODO
- Disguises the virtual machine to make it look like it has 2 processors and 2GB of extra RAM
- Automatically tracks processes infected by sample
  - TODO
  
## Limitations

As with all malware analysis environments, Cuckoo has it fair share of weaknesses.
Weaknesses, in the case of malware analysis, are ways malware can evade (bypass)
analysis efforts.

- Monitor cannot detect (or deter) indirect calls to API
- Samples can detect monitor DLL loaded into executable
