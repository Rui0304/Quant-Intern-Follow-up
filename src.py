#!/usr/bin/env python
# coding: utf-8


import os
#from faker import Faker
import shutil
#import random
import numpy as np


######## Generate a sequence of new directories ########

def mk_dir(disks_path, n):
    # Parameters: disks_path: a string ending with "/", represents the location where to create new subdirectories 
    #             n: the number of directories to generate
    
    for i in range(n):
        p = os.path.join(disks_path, str(i))   # name of each new directory
        try:
            os.mkdir(p)
        except OSError:
            print("Creation of the directory %s failed" % p)




######## Generate a sequence of fake files ########

def sum_to_x(n, x):
    # Parameters: n: an integer, represents the number of the valus in the list
    #             x: an integer, x is equal to the sum of all valus in the returned list
    # return: a list
    
    values = [0.0, x] + list(np.random.uniform(low=0.1,high=x,size=n-1))
    values.sort()
    return [values[i+1] - values[i] for i in range(n)]


def file_generation(data_path):
    # Parameters: data_path: data_path: a string ending with "/", represents the directory path where the fake files are
    
    total_storage_MB = 128  # total storage of files is 128 MB
    weight_ls = []       # the elements will be used during to set file sizes 

    for i in range(88):
        sub_ls = sum_to_x(2, 1.44) 
        for num in sub_ls:
            num = round(num, 2)
            # if num = 0, it doesn't make sence when creating fake data files.
            if num != 0:
                weight_ls.append(num)
        sub_ls = []

    s = sum(weight_ls)   # Caculate the sum of weights in the current weight list

    # Since the total storage of all files should be 128 MB, so the sum of the weights should be equal to 128
    last_weight = round((total_storage_MB - round(s, 2)), 2)
    weight_ls.append(last_weight)

    #print(weight_ls)
    #print(sum(weight_ls))
    #print(len(weight_ls))
    
    one_MB = 1024 * 1024    # 1 MB = 1024 * 1024 Bytes
    total_storage = total_storage_MB * one_MB  # Total storage occupied by files is 128 MB = 128*1024*1024 = 134217728 Bytes
    temp_total = 0 
    for i in range(len(weight_ls)):
        file_size = int(one_MB * weight_ls[i])
        if file_size <= 1509949:  # 1.44 MB = 1509949 Bytes
            f = open(data_path + 'newfile_' + str(i),"wb")
            f.seek(int(one_MB * weight_ls[i]) - 1)
            f.write(b"\0")
            f.close()
            temp_total += os.stat(data_path + 'newfile_' + str(i)).st_size

    if temp_total < total_storage:
        f = open(data_path + 'newfile_' + str(i+1),"wb")
        f.seek(total_storage - temp_total - 1)
        f.write(b"\0")
        f.close()
        temp_total += os.stat(data_path + 'newfile_' + str(i+1)).st_size
    





######## Get combinations of files which make the summary of sizes <= 1509949 Bytes(1.44 MB) ########

def get_comb(sizes, names, target = 1509949):
    # Parameters: sizes: tuple storing the sizes of all the files
    #             target: 1509949 Bytes = 1.44 MB
    #  return: combinations of file names. The files in each combination will be coppied into one floppy disks
    
    #visited = [0] * len(sizes)
    
    # Using two pointers: one is from start of the tuple, and another is from the end of the tuple
    
    left = 0
    res = []

    for i in range(len(sizes)-1, -1, -1):
        right = i
        if left >= right:
            break
        temp = sizes[right]
        comb = []
        comb.append(names[right])
        
        while left < right:
            if temp + sizes[left] > target:
                break
            else:
                temp += sizes[left]
                comb.append(names[left])
                left += 1
        res.append(comb)
        
    return res



######## Copy files to from source directory to detination ########

def backUp(data_path, disks_path , comb_names, n=120):
    # Parameters: data_path: a string ending with "/", represents the directory where the files are 
    #             disks_path: a string ending with "/", represents the directory where the floppy disks are
    #             n: an integer, represents the number of floppy disks
    
    for i in range(n):
        destination_path = os.path.join(disks_path, str(i))
        if i > len(comb_names)-1:
            break
        for name in comb_names[i]:
            file_path = os.path.join(data_path, name)
            shutil.copy(file_path, destination_path)







