# python-saleae-cli
This is a basic command line utility to automate the Saleae Logic software.

This tool can be used to automatically take a series of shorter captures over an extended time period. For example, if a 24 hour capture can't be recorded in a single run due to memory limitations, this utility could be used to automatically take 24 captures of one hour each.

### Prerequisites
- Saleae Logic software running with the socket API enabled. [instructions](https://support.saleae.com/saleae-api-and-sdk/socket-api)
- [ppannuto python-saleae](https://github.com/ppannuto/python-saleae) library installed.

### Usage

The utility allows the user to set the number of captures and the duration of each capture. It also optionally supports three different save operations:
1. save captures. If the `--save-captures` option is used, the utility will save each capture to the folder specified with the filename `N.logicdata`, where N is the index of the capture.
2. export captures. If the `--export-data` option is used, the utility will export each capture to the folder specified using the default csv export options provided by the [ppannuto python-saleae](https://github.com/ppannuto/python-saleae) library (thanks for that feature!) 
3. export analyzers. If the `--export-analyzers` option is used, the utility will export each of the analyzers that are currently active in the capture to the specified folder. They will be named with the format `N_Analyzer Name.csv`, where N is the index of the capture and `Analyzer Name` is the user editable analyzer name in the software.

### Examples

**Take 1 second long capture without saving anything.**
```
python saleae_cli.py
```

**Just take 5 captures, each 0.1 seconds long, without saving anything.**
```
python saleae_cli.py --capture-count 5 --capture-duration 0.1
```
**Take 24 captures, each 1 hour long, exporting the analyzers to an 'export' folder on the desktop.**

(Windows)
```
python saleae_cli.py --capture-count 24 --capture-duration 3600 --export-analyzers \Users\<Your User Name>\Desktop\export
```
(Linux or MacOS)
```
python saleae_cli.py --capture-count 24 --capture-duration 3600 --export-analyzers ~/Desktop/export
```
**Take 100 captures, each 10 seconds long, saving all outputs to the same 'export' folder on the desktop**

(Windows)
```
python saleae_cli.py --capture-count 100 --capture-duration 10 --save-captures \Users\<Your User Name>\Desktop\export --export-analyzers \Users\<Your User Name>\Desktop\export --export-data \Users\<Your User Name>\Desktop\export
```
(Linux or MacOS)
```
python saleae_cli.py --capture-count 3 --capture-duration 0.1 --save-captures ~/Desktop/export --export-analyzers ~/Desktop/export --export-data ~/Desktop/export
```



**Print out the CLI help**

`python saleae_cli.py --help`

```
Saleae Command Line Interface Capture Utility

optional arguments:
  -h, --help            show this help message and exit
  --capture-count COUNT
                        number of captures to repeat
  --capture-duration SECONDS
                        duration of each capture in seconds
  --save-captures PATH  if specified, saves each capture to the specified
                        directory
  --export-data PATH    if specified, exports the raw capture to the sepcified
                        directory
  --export-analyzers PATH
                        if specified, exports each analyzer to the specified
                        directory
  --ip IP               optional, IP address to connect to. Default localhost
  --port PORT           optional, Port to connect to. Default 10429
  ```
