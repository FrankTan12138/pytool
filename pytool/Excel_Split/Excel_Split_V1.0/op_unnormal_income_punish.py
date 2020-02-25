#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 封装程序
@author: Frank
@date: 2019/10/22

'''

#引入模块
from op_read_config import read_config  #读取配置文件
from op_text import read_txt   #读取list表单
from op_excel import read_excel,data_filter,write_excel
from op_send_mail import send_mail
import traceback,sys,os
import time


if __name__ == '__main__':
    os_path=os.getcwd()+"\\config\\"
    config_file="driver_punish_config.ini"
    
    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息
        #根据列表清单对源表数据进行excel拆分
        print("文件名称：{}".format(os_path+para_name['base']['file_name']))
        for write_filenames in read_txt(os_path,str(para_name['condition']['list_name'])+".txt"):
            write_filename=write_filenames.split("\t")[0]
            data_info=read_excel(para_name['base']['input_path'], para_name['base']['file_name'],para_name['base']['sheet_no'])  #读取excel数据
            data_result=data_filter(os_path,config_file,data_info,para_name['base']['title_no'],len(data_info),write_filename)  #数据筛选
            write_excel(para_name['base']['output_path'],write_filename,write_filename,para_name['base']['title_no'],data_result)
        #发送邮件
            receiver_mail=write_filenames.split("\t")[1]
            print("发送给公司：{}        对应邮箱：{}".format(write_filename,receiver_mail))
            send_mail(para_name['mail']['host_server'],para_name['mail']['host_port'],para_name['mail']['user_name'],para_name['mail']['password'],para_name['mail']['sender'],receiver_mail,para_name['mail']['cc'],para_name['mail']['mail_title'],para_name['mail']['mail_content'],para_name['mail']['attachment_img'],para_name['mail']['attachment_txt'],para_name['mail']['attachment_pdf'],para_name['base']['output_path']+write_filename+".xls",para_name['mail']['attachment_word'])
            time.sleep(60)   #暂停60秒
    except:
        traceback.print_exc()
        sys.exit()
