# Persistent-Memory-Development
Development PMEM Management APIs
# Contact
thomashuang@iii.org.tw
# running environment
Ubuntu 18.04.4 LTS  
Python 3.6.9
# Environment install before running
(a)Install Flask    
    ```shell= 
    pip install Flask
    ```
# User Mode example
(a)Create and mount memery(Scanf 0)  
＊ Define and create the size of ndctl create-namespace -m fsdax 
＊ Define and create the folder which you need to mount on create-namespace
＊ mkfs.xfs the create-namespace “blockdev” 
