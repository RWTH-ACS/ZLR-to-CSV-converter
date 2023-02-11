# Copyright (c) 2020 Manuel Pitz, RWTH Aachen University
#
# Licensed under the Apache License, Version 2.0, <LICENSE-APACHE or
# http://apache.org/licenses/LICENSE-2.0> or the MIT license <LICENSE-MIT or
# http://opensource.org/licenses/MIT>, at your option. This file may not be
# copied, modified, or distributed except according to those terms.
import sys
from pathlib import Path
import xmltodict

# Add project path to system path to facilitate imports of the digital twin submodules
project_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(project_dir))

import coloredlogs, logging, sys
from struct import *
from datetime import datetime
import csv



coloredlogs.install(level='DEBUG',
fmt='%(asctime)s %(levelname)-8s %(name)s[%(process)d] %(message)s',
field_styles=dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='white', bold=True),
    programname=dict(color='cyan'),
    name=dict(color='blue')))
logging.info("Program Start")

def handle_Float32DataType(d): # datapoint
    return d

def handle_Date64DataType(d): # absolute time of sample
    return datetime.fromtimestamp(d/1000000000).strftime('%Y-%m-%d %H:%M:%S,%f')

def handle_Time64DataType(d): # this could be time between samples
    return d/1000000000



def main():
    fname = "log_2023-2-09T21-38-47"
    ffolder = "./example/"

    fh = open(ffolder + fname + ".zlr", "rb")
    endOfHeader = False
    xmlData = r''
    while not endOfHeader:
        line = fh.readline()
        line = line.decode("utf-8")
        
        if "ZLREOH" in line:
            endOfHeader = True
        else:
            xmlData = xmlData + line
    headerData = xmltodict.parse(xmlData)

    numberOfMeasurements = int(headerData["recordHeader"]["table"]["@numRows"])

    dataPattern = ''
    dataSize = 0
    dataHandler = []
    data = []
    fieldNames = []
    for measurand in headerData["recordHeader"]["table"]["columns"]["tableColumn"]:
        dType = measurand["measurand"]["@dataType"]
        if dType == "Float32DataType":
            fieldNames.append("Value")
            dataPattern = dataPattern + "f"
            dataSize = dataSize + 4
            dataHandler.append(handle_Float32DataType)
        elif dType == "Date64DataType":
            fieldNames.append("Datetime")
            dataPattern = dataPattern + "Q"
            dataSize = dataSize + 8
            dataHandler.append(handle_Date64DataType)
        elif dType == "Time64DataType":
            fieldNames.append("Sample duration")
            dataPattern = dataPattern + "Q"
            dataSize = dataSize + 8
            dataHandler.append(handle_Time64DataType)

    for i in range(numberOfMeasurements):
        dataBlock = fh.read(dataSize)
        try:
            dataRaw = unpack("<" + dataPattern, dataBlock)
            data.append([])
            for i in range(len(dataHandler)):
                data[-1].append(dataHandler[i](dataRaw[i]))
        except:
            logging.info("read error")

        

    with open(ffolder + fname + ".csv", 'w') as f:
        write = csv.writer(f)
        
        write.writerow(fieldNames)
        write.writerows(data)






if __name__ == "__main__":
    main()