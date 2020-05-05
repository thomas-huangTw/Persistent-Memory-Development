import sys
import json
import subprocess
import os.path
from os import path

def Find():
    try:
        #data[1]:pmem block uuid; data[2]:pmem block LastFolderName 
        data = sys.argv
        DumpFile = '/mnt/restore/' + data[1]
        FileState = str(path.exists(DumpFile))
        if FileState == "False":
            restore(data[1], data[2])
        else:
            DeleteDumpFile = subprocess.call(["rm -r " + DumpFile ], shell=True)
            restore(data[1], data[2])
    except:
        return "Fail"
#Use restore function to create restore dump file folder and XFS restore
def restore(data1,data2):
    try:
        CreateFolder1 = subprocess.check_output(["mkdir /mnt/restore/" + data1],shell=True).decode(sys.stdout.encoding)
        CreateFolder2 = subprocess.check_output(["mkdir /mnt/restore/" + data1 + "/" + data2],shell=True).decode(sys.stdout.encoding)
        RestoreResponse = subprocess.call(["xfsrestore -f /mnt/backup/" + data1 +".dump -L boot_all /mnt/restore/" + data1 + "/" + data2], shell=True)
        return RestoreResponse
    except:
        return "Fail"

Find()
