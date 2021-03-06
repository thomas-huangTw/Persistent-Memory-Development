# Persistent-Memory-Development
Development PMEM Management APIs
# Contact
thomashuang@iii.org.tw
# running environment
Ubuntu 18.04.4 LTS  
Python 3.6.9
# Environment install before running
(a)Install Flask    
    ```
    pip install Flask
    ```  
# User instructions
First of all, we will divide users into User Mode and Manager Mode.  
The User Mode part is used by general user clients. Persistent Memory in User Mode can be store、 delete、 select、 back up and restore. Among of them, the selecting、backup and recovery actions are  corresponds to a single pmem block.  
The Manager Mode part is used by the general manager client. It can be store、 delete、 and select the Persistent Memory. The action for selecting is the Persistent Memory machine of node Capacity and AvailCapacity.  

# User Mode example
***running Usermode.py***  
(a)Create and mount memery(Scanf 0)  
`Input : Folder name and size you need`
- Define and create the size of ndctl create-namespace -m fsdax  
- Define and create the folder which you need to mount on create-namespace  
- mkfs.xfs the create-namespace “blockdev”

(b)Delete umount memery(Scanf 1)  
`Input : The “uuid” pmem block which you want to delete`
- Umount the namespace’s “blockdev” by uuid that you insert  
- Destroy-namespace by “uuid” that you insert

(c)Show Block Device(Scanf 2)  
`The “uuid” pmem block which you want to list`
- ndctl list namespace by “uuid” that you insert

(d)Backup(Scanf 3)  
`The “uuid” pmem block which you want to backup`
- Dump xfs to a local host by “uuid” that you insert

(e)Restore(Scanf 4)  
`The “uuid” pmem block which you want to restore`
- Restore xfs to a local host by “uuid” that you insert

(f)Exit(Scanf 5)  
- Exit the program

#  Manager Mode example
***running ManagerMode.py***  
(a),(b)Just list the User Mode(a),(b)  

(c)Show Block Device(Scanf 2)    
- List Capacity and AvailCapacity  

(d)Exit(Scanf 3)  
- Exit the program

