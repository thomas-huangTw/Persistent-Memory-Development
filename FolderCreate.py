import sys
import json
import subprocess
def run():
    data = sys.argv 
    try:
        CreateFolder1 = subprocess.check_output(["mkdir /mnt/"+ data[1]],shell=True).decode(sys.stdout.encoding)
        CreateFolder2 = subprocess.check_output(["mkdir /mnt/"+ data[1] +"/"+ data[2]],shell=True).decode(sys.stdout.encoding)
        print("FolderCreateSuccess")
    except subprocess.CalledProcessError as e:
        print("FolderCreateFail")
    
run()
