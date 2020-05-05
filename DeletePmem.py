import sys
import json
import subprocess
def run():
    try:
        #data[1]:pmem block uuid
        data = sys.argv
        with open('./uuidFile/'+ data[1] +'.json' , 'r') as reader:
            jf = json.loads(reader.read())
        DeleteDev = jf['dev']
        DeleteBlockdev = jf['blockdev']
        DeleteBlockdevResponse = subprocess.call(["umount -l /dev/"+DeleteBlockdev], shell=True)
        DeleteNameSpaceResponse = subprocess.call(["ndctl destroy-namespace " + DeleteDev +  " -f"], shell=True)
        print("Success")
    except:
        print("Fail")

run()
