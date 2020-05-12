from flask import Flask, request, jsonify
import json
import subprocess
import sys
import socket
import os.path
from os import path
app = Flask(__name__)

#Configure local ip
def Check_Local_IP():
    try:
        with open('IpAddress.json', 'r') as f:
            JsonData = json.loads(f.read())
        Worker1_IP = JsonData['worker1']
        Worker2_IP = JsonData['worker2']
        Worker3_IP = JsonData['worker3']

        LocalIp = get_host_ip()
        if LocalIp == Worker1_IP:
            Worker_IP = "Worker1"
        elif LocalIp == Worker2_IP:
            Worker_IP = "Worker2"
        else:
           Worker_IP = "Worker3"

        return Worker_IP
    except:
        print("error")

#Use /create function to create pmem block
@app.route('/create', methods=['GET', 'POST'])
def message():
    #Configure local ip
    Worker_IP = Check_Local_IP()
    
    #data have two value:folder_name and create_size
    data = request.json
    
    #if folder_name or create_size were empty 
    if str(data['folder_name'])=="" or str(data['create_size'])=="":
        return Worker_IP+": Folder name or size can't be empty"
    
    if str(data['folder_name'])!="" and str(data['create_size'])!="":
        try:
            #Define the pmem block by create_size
            Create_size = subprocess.check_output(["ndctl", "create-namespace", "-m", "fsdax", "-s", data['create_size']]).decode(sys.stdout.encoding)
            json_acceptable_string = Create_size.replace("'", "\"")
            blockdevName = json.loads(json_acceptable_string)
            de = "mkfs.xfs ../../dev/"+ blockdevName['blockdev']
            a = subprocess.call([de + " -f"], shell=True)

            #Use FolderCreate.py by pmem block uuid and folder_name to create the mount folder 
            Create_command = "python3 FolderCreate.py " + blockdevName['uuid'] +" "+ data['folder_name']
            CallCreateFun = subprocess.check_output([Create_command],shell=True).decode(sys.stdout.encoding)
            MntCreateFolderName = "/mnt/"+blockdevName['uuid'] +"/"+ data['folder_name']   
            subprocess.call(["mount -o dax /dev/" + blockdevName['blockdev'] + " " + MntCreateFolderName], shell=True)
            
            #append folder_name 、 MntCreateFolderName(uuid+folder_name) and the ip location  to pmem block attribute
            with open('./uuidFile/'+blockdevName['uuid']+'.json', 'w') as f:
                blockdevName.update({"LastFolderName":data['folder_name']})
                blockdevName.update({"FolderName":MntCreateFolderName})
                GetHostIP = get_host_ip()
                blockdevName.update({"IP":GetHostIP})
                json.dump(blockdevName, f)

            #after create success, return works numbers and uuid attribute    
            create_return = Worker_IP+": Create already.\nThe uuid corresponding to the space you created as follows:\n" + blockdevName['uuid']
            return create_return
        
        except subprocess.CalledProcessError as grepexc:
            #all the input value only have number without G/g in the last word
            if str(grepexc.returncode)=="129":
                return Worker_IP+": size format error."
           
            elif str(grepexc.returncode)=="237":
                subprocess.call(["rm -r ../../mnt/"+data['folder_name']], shell=True)
                return Worker_IP+": Your required capacity is too large!(Or the format is incorrect)"

            #all the input value only have char without number in it
            else:
                return Worker_IP+": error code.", grepexc.returncode, grepexc.output



#Use get_host_ip() function to get local ip     
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip



#Use /Backup function to backup local pmem block folder
@app.route('/Backup', methods=['GET', 'POST'])
def Backup():
    try:
        #Configure local ip
        Worker_IP = Check_Local_IP()
        
        #data have value:peme block uuid
        BackupUUIDName = request.json

        #BackupUUIDName include value "uuid"
        with open('./uuidFile/'+BackupUUIDName['UUID']+'.json', 'r') as f:
            UUIDJsonData = json.loads(f.read())
        MntUUID = UUIDJsonData['uuid']
        MntFolder = UUIDJsonData['LastFolderName']

        #Use Backup.py to backup pmem block by XFS dump
        CallBackup_command = "python3 Backup.py " + MntUUID +" "+ MntFolder
        CallBackup_test = subprocess.check_output([CallBackup_command],shell=True).decode(sys.stdout.encoding)
        return Worker_IP+". Backup Success."
    except:
        return ""


#Use /Restore function to restore local pmem block folder
@app.route('/Restore', methods=['GET', 'POST'])
def Restore():
    try:
        #Configure local ip
        Worker_IP = Check_Local_IP()
       
        #data have value:peme block uuid
        RestoreUUIDName = request.json

        #Check corresponding uuid dump file in backup folder
        if str(path.exists("/mnt/backup/" + RestoreUUIDName['UUID'] + ".dump"))!="False":
            
            #RestoreUUIDName include value "uuid"
            with open('./uuidFile/'+RestoreUUIDName['UUID']+'.json', 'r') as f:
                UUIDJsonData = json.loads(f.read())
            MntUUID = UUIDJsonData['uuid']
            MntFolder = UUIDJsonData['LastFolderName']

            #Use Restore.py to restore pmem block by XFS restore
            CallRestore_command = "python3 Restore.py " + MntUUID + " " + MntFolder
            CallRestore_test = subprocess.check_output([CallRestore_command],shell=True).decode(sys.stdout.encoding)
            return Worker_IP+". Restore Success."
        else:
            return Worker_IP+". Restore Fail(doesn't exit dump file in backup folder)."
    except:
        return Worker_IP+". Restore Fail."

#Use /DeleteUUID to delete local pmem block
@app.route('/DeleteUUID', methods=['GET', 'POST'])
def DeleteUUID():
    #Configure local ip
    Worker_IP = Check_Local_IP()
    
    #DeleteUUIDName include value "uuid"
    DeleteUUIDName = request.json

    #Use DeletePmem.py to delete local pmem block by DeleteUUIDName['UUID'](uuid)
    #DeletePmem.py include umount and ndctl destroy-namespace from local 
    Delete_command = "python3 DeletePmem.py " + DeleteUUIDName['UUID']
    CallDeleteFun = subprocess.check_output([Delete_command],shell=True).decode(sys.stdout.encoding)
    if str(CallDeleteFun)=="Success\n":
        
        #while umount and ndctl destroy-namespace success, also delete the folder in /mnt and uuid json file in /home/thomas/uuidFile/
        subprocess.call(["rm -r /mnt/" + DeleteUUIDName['UUID']], shell=True)
        subprocess.call(["rm -r /home/thomas/uuidFile/" + DeleteUUIDName['UUID']+".json"], shell=True)
        return Worker_IP+". Delete Success."
    else:
        return Worker_IP+". No this UUID."

#Use /FindUUID to find the uuid corresponding to the pmem blocks 
@app.route('/FindUUID', methods=['GET', 'POST'])
def FindUUID():
    #Configure local ip
    Worker_IP = Check_Local_IP()
    
    #FindUUID include value "uuid"
    FindUUIDName = request.json

    #Use ReadUUID.py to pintf the pmem block attribute by FindUUIDName['UUID'](uuid)
    Read_command = "python3 ReadUUID.py " + FindUUIDName['UUID']
    CallReadFun_test = subprocess.check_output([Read_command],shell=True).decode(sys.stdout.encoding)
    if str(CallReadFun_test)==Worker_IP+". Find Fail.":
        return Worker_IP+". Find Fail.\n"
    else:
        return CallReadFun_test

#Use /availcapacity to return the local Capacity and AvailCapacity on all pmem node
@app.route('/availcapacity', methods = ['GET', 'POST'])
def run():
    try:
        #Configure local ip
        Worker_IP = Check_Local_IP()
        
        availcapacity = subprocess.check_output(["ipmctl show -region"],shell=True).decode(sys.stdout.encoding)
        return availcapacity
    except:
        return Worker_IP+". return Fail."

#Use /blkdev to return the local ndctl list attribute
@app.route('/blkdev', methods = ['GET', 'POST'])
def runTwo():
    try:
        #Configure local ip
        Worker_IP = Check_Local_IP()
        
        blkdev = subprocess.check_output(["ndctl list -N"],shell=True).decode(sys.stdout.encoding)
        return blkdev
    except:
        return Worker_IP+". return Fail."

#Use /DeleteBR to delete folders restore and backup files
@app.route('/DeleteBR', methods = ['GET', 'POST'])
def DeleteBR():
    subprocess.check_output(["rm -rf /mnt/restore/*"],shell=True).decode(sys.stdout.encoding)
    subprocess.check_output(["rm -rf /mnt/backup/*"],shell=True).decode(sys.stdout.encoding)



if __name__ == "__main__":
    app.run(host='',port= , debug=True)
