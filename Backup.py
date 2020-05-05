import sys
import json
import subprocess
import os.path
from os import path


def Find():
    try:
        data = sys.argv
        DumpFile = '/mnt/backup/'+data[1]+'.dump'
        FileState = str(path.exists(DumpFile))
        if FileState == "False":
            backup(data[1], data[2])
        else:
            DeleteDumpFile = subprocess.call(["rm -r " + DumpFile], shell=True)
            backup(data[1], data[2])
    except:
        return "Fail"

def backup(data1,data2):
    try:
        MntFolder = '/mnt/' + data1 + "/" + data2
        BackupSpaceResponse = subprocess.call(["xfsdump -l 0 -L boot_all -M boot_all -f /mnt/backup/" + data1 +".dump "+ MntFolder], shell=True)
        
        return BackupSpaceResponse
    except:
        return "Fail"

Find()
