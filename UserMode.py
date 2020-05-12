import requests
import subprocess
import sys
import json
import os.path
from os import path

#Define workers ip address.
def DefineIp():
    try:
        with open('IpAddress.json', 'r') as f:
            JsonData = json.loads(f.read())
        Worker1_IP = 'http://'+JsonData['worker1']+':1234'
        Worker2_IP = 'http://'+JsonData['worker2']+':1234'
        Worker3_IP = 'http://'+JsonData['worker3']+':1234'
        return Worker1_IP, Worker2_IP, Worker3_IP
    except:
        return "IP error."

def run():
    try:
        #Define workers ip address.
        Worker1_IP, Worker2_IP, Worker3_IP = DefineIp()
        while (1):
            """this while loop can classification 5 mode.
            Arge:
                mode_chose(int): The mode to use.

            Return:
                string(str): Return different mode's information.
            """
            print("Please enter your required items:\n","0.Create and mount memery.; 1.Delete umount memery.; 2.Show Block Device.; 3.Backup.; 4.Restore.;  5.Exit.")
            mode_chose = input("Item selection:")

            if str(mode_chose)==str("0"):
                #The folder name which you want to mount on the namespace
                folder_name = input("folder name:")
                #The pmem blocks size you want to create
                create_size = input("create size:")

                #try to post json to Worker1 /create api
                try:
                    worker = requests.post(Worker1_IP + '/create', json={"folder_name":folder_name,"create_size":create_size})
                    if worker.ok:
                        if str(worker.text)=="Worker1: Your required capacity is too large!(Or the format is incorrect)":
                            pass                    
                        else:
                            print(worker.text+"\n")
                            continue
                except requests.ConnectionError:
                    pass

                #try to post json to Worker2 /create api
                try:
                    worker = requests.post(Worker2_IP + '/create', json={"folder_name":folder_name,"create_size":create_size})
                    if worker.ok:
                        if str(worker.text)=="Worker2: Your required capacity is too large!(Or the format is incorrect)":
                            pass
                        else:
                            print(worker.text+"\n")
                            continue
                except requests.ConnectionError:
                    pass

                #try to post json to Worker3 /create api
                try:
                    worker = requests.post(Worker3_IP + '/create', json={"folder_name":folder_name,"create_size":create_size})
                    if worker.ok:
                        if str(worker.text)=="Worker3: Your required capacity is too large!(Or the format is incorrect)":
                            pass
                        else:
                            print(worker.text+"\n")
                            continue
                except requests.ConnectionError:
                    pass

                print("Your required capacity is too large!(Or the format is incorrect)\n")

            elif str(mode_chose)==str("1"):
                #The peme blocks uuid you want to delete
                Delete_SpaceName = input("The name of the region you need to delete:")

                #try to post json to Worker1 /DeleteUUID api
                try:
                    Worker1_delete = requests.post(Worker1_IP + '/DeleteUUID', json={"UUID":Delete_SpaceName})
                    CallDeleteFun = Worker1_delete.text
                    if str(CallDeleteFun)=="Worker1. Delete Success.":
                        print("Work1. Delete Success.\n")
                        continue
                except requests.ConnectionError:
                    pass

                #try to post json to Worker2 /DeleteUUID api
                try:
                    Worker2_delete = requests.post(Worker2_IP + '/DeleteUUID', json={"UUID":Delete_SpaceName})
                    CallDeleteFun = Worker2_delete.text
                    if str(CallDeleteFun)=="Worker2. Delete Success.":
                        print("Work2. Delete Success.\n")
                        continue
                except requests.ConnectionError:
                    pass

                #try to post json to Worker3 /DeleteUUID api
                try:
                    Worker3_delete = requests.post(Worker3_IP + '/DeleteUUID', json={"UUID":Delete_SpaceName})
                    CallDeleteFun = Worker3_delete.text
                    if str(CallDeleteFun)=="Worker3. Delete Success.":
                        print("Work3. Delete Success.\n")
                        continue
                except requests.ConnectionError:
                    pass

                print("Workers UUID don't exist.\n")

            elif str(mode_chose)==str("2"):
                Read_SpaceName_info = input("The name of the region-info you need to see:")
                if Read_SpaceName_info =="":
                    print("uuid can't be empty.\n")
                    pass
                else:
                    #try to post json to Worker1 /FindUUID api
                    try:
                        FindUUID = requests.post(Worker1_IP + '/FindUUID', json={"UUID":Read_SpaceName_info})
                        CallReadFun = FindUUID.text
                        if str(CallReadFun)!="Worker1. Find Fail.\n":
                            print(CallReadFun)
                            continue
                    except requests.ConnectionError:
                        pass

                    #try to post json to Worker2 /FindUUID api
                    try:
                        FindUUID = requests.post(Worker2_IP + '/FindUUID', json={"UUID":Read_SpaceName_info})
                        CallReadFun = FindUUID.text
                        if str(CallReadFun)!="Worker2. Find Fail.\n":
                            print(CallReadFun)
                            continue
                    except requests.ConnectionError:
                        pass

                    #try to post json to Worker3 /FindUUID api
                    try:
                        FindUUID = requests.post(Worker3_IP + '/FindUUID', json={"UUID":Read_SpaceName_info})
                        CallReadFun = FindUUID.text
                        if str(CallReadFun)!="Worker3. Find Fail.\n":
                            print(CallReadFun)
                            continue
                    except requests.ConnectionError:
                        pass

                    print("Workers Find Fail(wrong uuid).\n")

            elif str(mode_chose)==str("3"):
                BackupUUID = input("The name of the folder(UUID) you need to backup:")
                if BackupUUID=="":
                    print("uuid can't be empty.\n")

                #if Worker1 have exit corresponding pmem block(/FindUUID), then post json to Worker1 /Backup api 
                try:
                    FindUUID = requests.post(Worker1_IP + '/FindUUID', json={"UUID":BackupUUID})
                    CallReadFun = FindUUID.text
                    if str(CallReadFun)!="Worker1. Find Fail.\n":
                        Worker1_Backup = requests.post(Worker1_IP + '/Backup', json={"UUID":BackupUUID})
                        CallBackupFun = Worker1_Backup.text
                        if str(CallBackupFun)=="Worker1. Backup Success.":
                            print("Worker1. Backup Success.\n")
                        continue
                    else:
                        pass
                except requests.ConnectionError:
                    pass

                #if Worker2 have exit corresponding pmem block(/FindUUID), then post json to Worker2 /Backup api
                try:
                    FindUUID = requests.post(Worker2_IP + '/FindUUID', json={"UUID":BackupUUID})
                    CallReadFun = FindUUID.text
                    if str(CallReadFun)!="Worker2. Find Fail.\n":
                        Worker2_Backup = requests.post(Worker2_IP + '/Backup', json={"UUID":BackupUUID})
                        CallBackupFun = Worker2_Backup.text
                        if str(CallBackupFun)=="Worker2. Backup Success.":
                            print("Worker2. Backup Success.\n")
                        continue
                    else:
                        pass
                except requests.ConnectionError:
                    pass

                #if Worker3 have exit corresponding pmem block(/FindUUID), then post json to Worker3 /Backup api
                try:
                    FindUUID = requests.post(Worker3_IP + '/FindUUID', json={"UUID":BackupUUID})
                    CallReadFun = FindUUID.text
                    if str(CallReadFun)!="Worker3. Find Fail.\n":
                        Worker3_Backup = requests.post(Worker3_IP + '/Backup', json={"UUID":BackupUUID})
                        CallBackupFun = Worker3_Backup.text
                        if str(CallBackupFun)=="Worker3. Backup Success.":
                            print("Worker3. Backup Success.\n")
                        continue
                    else:
                        pass
                except requests.ConnectionError:
                    pass

                print("Workers Backup Fail(Check your UUID).\n")

            elif str(mode_chose)==str("4"):
                RestoreUUID = input("The name of the Dump File(UUID) you need to restore:")
                if RestoreUUID=="":
                    print("uuid can't be empty.\n")

                #if Worker1 have exit corresponding pmem block(/FindUUID), then post json to Worker1 /Restore api
                try:
                    Worker1_Restore = requests.post(Worker1_IP + '/FindUUID', json={"UUID":RestoreUUID})
                    CallRestoreFun = Worker1_Restore.text           
                    if (CallRestoreFun)!="Worker1. Find Fail.\n":
                        Worker1_Restore = requests.post(Worker1_IP + '/Restore', json={"UUID":RestoreUUID})
                        CallRestoreFun = Worker1_Restore.text
                        if str(CallRestoreFun)=="Worker1. Restore Success.":
                            print("Worker1. Restore Success.\n")
                        else:
                            print(CallRestoreFun,"\n")
                        continue
                except requests.ConnectionError:
                    pass

                #if Worker2 have exit corresponding pmem block(/FindUUID), then post json to Worker2 /Restore api
                try:
                    Worker2_Restore = requests.post(Worker2_IP + '/FindUUID', json={"UUID":RestoreUUID})
                    CallRestoreFun = Worker2_Restore.text
                    if (CallRestoreFun)!="Worker2. Find Fail.\n":
                        Worker2_Restore = requests.post(Worker2_IP + '/Restore', json={"UUID":RestoreUUID})
                        CallRestoreFun = Worker2_Restore.text
                        if str(CallRestoreFun)=="Worker2. Restore Success.":
                            print("Worker2. Restore Success.\n")
                        else:
                            print(CallRestoreFun,"\n")
                        continue
                except requests.ConnectionError:
                    pass

                #if Worker3 have exit corresponding pmem block(/FindUUID), then post json to Worker3 /Restore api
                try:
                    Worker3_Restore = requests.post(Worker3_IP + '/FindUUID', json={"UUID":RestoreUUID})
                    CallRestoreFun = Worker3_Restore.text
                    if (CallRestoreFun)!="Worker3. Find Fail.\n":
                        Worker3_Restore = requests.post(Worker3_IP + '/Restore', json={"UUID":RestoreUUID})
                        CallRestoreFun = Worker3_Restore.text
                        if str(CallRestoreFun)=="Worker3. Restore Success.":
                            print("Worker3. Restore Success.\n")                                                                                                                        
                        else:
                            print(CallRestoreFun,"\n")
                        continue
                except requests.ConnectionError:
                    pass 

                print("Workers Restore Fail(Check your UUID).\n")

            elif str(mode_chose)==str("5"):
                print("Exit!"+"\n")
                exit(0)


            elif str(mode_chose)==str("D"):
                deleteIP = input("1.delete 88; 2.delete 72; 3.delete 63; 4.delete all;(backup/restore)")
                if str(deleteIP)==str("1"):
                    Worker1_DeleteIP = requests.post(Worker1_IP + '/DeleteBR')
                    CallDeleteIPFun1 = Worker1_DeleteIP.text
                elif str(deleteIP)==str("2"):
                    Worker2_DeleteIP = requests.post(Worker2_IP + '/DeleteBR')
                    CallDeleteIPFun2 = Worker2_DeleteIP.text
                elif str(deleteIP)==str("3"):
                    Worker3_DeleteIP = requests.post(Worker3_IP + '/DeleteBR')
                    CallDeleteIPFun3 = Worker3_DeleteIP.text
                elif str(deleteIP)==str("4"):
                    Worker1_DeleteIP = requests.post(Worker1_IP + '/DeleteBR')
                    CallDeleteIPFun1 = Worker1_DeleteIP.text

                    Worker2_DeleteIP = requests.post(Worker2_IP + '/DeleteBR')
                    CallDeleteIPFun2 = Worker2_DeleteIP.text

                    Worker3_DeleteIP = requests.post(Worker3_IP + '/DeleteBR')
                    CallDeleteIPFun3 = Worker3_DeleteIP.text

                print("\n")

            else:
                print("wrong format(try again).\n")
                continue
    except:
        print("error.")
run()
