#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 读取list数据
@author: Frank
@date: 2019/10/25

'''

import csv


#将txt列表读入
def read_txt(os_path,file_name):
    print("txt文本路径：\"{}\"".format(os_path+file_name))
    f=open(os_path+file_name,encoding="UTF-8")
    data=f.read().split("\n")
    return(data)

#将csv列表读入
def read_csv(os_path,file_name):
    csv_data={}
    i=0  #初始值
    with open(os_path+file_name,encoding="UTF-8-sig") as csvfile:
        csvfile_data=csv.reader(csvfile)
        for data in csvfile_data:
            csv_data[i]=data
            i=i+1
    return(csv_data)
