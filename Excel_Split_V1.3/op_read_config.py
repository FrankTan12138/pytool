#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''

@title: 配置参数表读取
@author: Frank
@date: 2019/10/22

'''

#引入模块
import os
import configparser  #引入为了读取ini文件

#读取Excel数据
def read_config(os_path,file_name):
    os.chdir(os_path)   #转到配置文件目录下
    conf = configparser.ConfigParser()   #创建conf对象
    conf.read(file_name, encoding='utf-8')   #读取配置文件内容
    config_info =conf.sections()   #获取所有section
    para_name={}  #初始化
    config_para={}
    for i in range(0,len(config_info)):
        para_name[i]=config_info[i]
        config_para[i]=dict(conf.items(config_info[i]))   #读取配置文件各个模块内信息，并且保存成字典形式
    config_result=dict(zip(list(para_name.values()),config_para.values()))  #将list转化成dict
    return(config_result)