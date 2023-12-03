# ZLR to CSV converter

This tool can convert some specific zlr files to csv format.


# decode.py

This tool can decode files with a simple recording of data.

# decode_v2.py

This tool can decode files containing traces and list type recordings.



# Install virtual environment

## Linux/WSL

To install the virtual environment open a command line within the project folder and run
```
make init
```

## Run the tool

- Update the file name and folder in `decode_v2.py` or `decode.py`
- Change to the main folder with the python files
- run `source vEnv/bin/activate`
- run `python decode_v2.py`

# FAQ

## Which one to use? `decode.py` or `decode_v2.py`

If you are not sure open the original zlr file and check if you find in the XML secion `listTypeMode="Var"`. In that case use `decode_v2.py`

## What datatypes are supportet

- Float32DataType
- StringDataType
- Date64DataType
- Time64DataType

## How long should it take?

The conversion of an 750 MB input file is done within 2:30 minutes and results in a 3.8 GB CSV file

## Open points

- Te variable type elements have a header that is ignored at the moment
- The data block secion has a header that is ignored
- The string sections contain more information. Looks like memory leaks in the ZES
- The length of the string is determined by the header. It's not yet checked if that is done correctly

