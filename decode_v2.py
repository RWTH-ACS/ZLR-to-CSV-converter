# Copyright (c) 2023 Manuel Pitz, RWTH Aachen University
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



coloredlogs.install(level='DEBUG',
fmt='%(asctime)s %(levelname)-8s %(name)s[%(process)d] %(message)s',
field_styles=dict(
    asctime=dict(color='green'),
    hostname=dict(color='magenta'),
    levelname=dict(color='white', bold=True),
    programname=dict(color='cyan'),
    name=dict(color='blue')))
logging.info("Program Start")

def BlockOffset(h, d):
    #unknown data in the beginning of each block
    size = 16
    header = h.read(size)

def Float32DataType(h, d):
    size = 4
    headerSize = 8
    if d["cnt"] > 1:
        header = h.read(headerSize)
    raw = h.read(d["cnt"] * size)
    data = unpack(f"<{d['cnt']}f", raw)

    return list(data)

def StringDataType(h, d):
    size = 1
    headerSize = 8
    if d["cnt"] > 1:
        header = h.read(headerSize)
    
    raw = h.read(d["cnt"] * size)
    lenght = unpack_from("<Q", raw, 0)    
    data = unpack_from(f"<{int(lenght[0]-1)}s", raw, 8)
    data = [e.decode("utf-8") for e in data]
    
    return data


def Date64DataType(h, d):
    size = 8
    raw = h.read(d["cnt"] * size)
    #could be that here also a header is needed
    data = unpack(f"<{d['cnt']}Q", raw)

    data = [datetime.fromtimestamp(e/1000000000).strftime('%Y-%m-%d %H:%M:%S,%f') for e in data]
    return data


def Time64DataType(h, d):
    size = 8
    raw = h.read(d["cnt"] * size)
    #could be that here also a header is needed
    data = unpack(f"<{d['cnt']}Q", raw)
    
    data = [e/1000000000 for e in data]

    return data
    
    
decoder = {
    "BlockOffset" : BlockOffset,
    "Float32DataType" : Float32DataType,
    "StringDataType" : StringDataType,
    "Date64DataType" : Date64DataType,
    "Time64DataType" : Time64DataType    
}    

def main():

    logging.info("Parse header")


    fname = "log_13"
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

    dataMap = {}
    dataMap["blockOffset"] = {
        "dataType" : "BlockOffset",
        "cnt" : 1,
        "skip" : True
    }

    for measurand in headerData["recordHeader"]["table"]["columns"]["tableColumn"]:
        dType = measurand["measurand"]["@dataType"]
        varBlockSize = measurand["measurand"]["@varBlockSize"]
        name = measurand["measurand"]["measurandRequest"]["@symbol"]
        if "@param1" in measurand["measurand"]["measurandRequest"]:
            name = name + measurand["measurand"]["measurandRequest"]["@param1"]
            
        ## Detect expected data cnt
        if measurand["measurand"]["@listTypeMode"] == "None":
            cnt = 1
        elif measurand["measurand"]["@listTypeMode"] == "Var" and measurand["measurand"]["@dataType"] == "StringDataType":
            cnt =int(measurand["measurand"]["@varBlockSize"])
        elif measurand["measurand"]["@listTypeMode"] == "Var" and "@param3" in measurand["measurand"]["measurandRequest"]:
            cnt = int(measurand["measurand"]["measurandRequest"]["@param3"]) + 1
        else:
            logging.error("Could not parse header! Abort!")
            exit(1)
            
        dataMap[name] = {
            "dataType" : measurand["measurand"]["@dataType"],
            "cnt" : cnt,
            "skip" : False
        }
        
    logging.info("Parse data")

    data = []
    for i in range(numberOfMeasurements):
        data.append({})
        for elm in dataMap:
            col = dataMap[elm]
            if col["dataType"] not in decoder:
                logging.error(f"Hanlder for {col['dataType']} not available")
                exit(1)
            d = decoder[col['dataType']](fh, col)
            if not col["skip"]:
                data[-1][elm] = d

    logging.info("Write csv")


    with open(ffolder + fname + ".csv", 'w') as f:
        fieldNames = []
        for col in dataMap:
            if dataMap[col]["skip"]:
                continue
            fieldNames.append(col)
        f.write(','.join(fieldNames)+"\n")

        #Write data
        lines = []
        for block in data:
            line = []
            
            length = 0
            colLen = {}
            for col in dataMap:
                if col in block:
                    if len(block[col]) > length:
                        length = len(block[col])
                    colLen[col] = len(block[col])
                    line.append("")
            
            
            
            for i in range(length):
                colPos = 0
                for col in dataMap:
                    if col in block:
                        if i >= colLen[col]:
                            line[colPos] = ''
                        else:
                            line[colPos] = str(block[col][i])
                        colPos = colPos + 1
                f.write(','.join(line)+"\n")
            
    logging.info("Program end")




if __name__ == "__main__":
    main()