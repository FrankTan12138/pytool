#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 邮件发送
@author: Frank
@date: 2019/10/22

'''

#引入模块
from op_read_config import read_config  #读取配置文件
from op_text import read_txt   #读取list表单
from op_send_mail import send_mail
import traceback,sys,time

if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="driver_income_config_shanghai.ini"
    
    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息
        
        for write_filenames in read_txt(os_path,str(para_name['condition']['list_name'])+".txt"):
            write_filename=write_filenames.split("\t")[0]
            print("====================================================")
            print("文件名称：{}".format(para_name['base']['output_path']+para_name['base']['output_file']+write_filename+".xls"))
                        
        #发送邮件
            receiver_mail=write_filenames.split("\t")[1]
            print("发送给租赁公司：{}        对应邮箱：{}".format(write_filename,receiver_mail))
            send_mail(para_name['mail']['host_server'],para_name['mail']['host_port'],para_name['mail']['user_name'],para_name['mail']['password'],para_name['mail']['sender'],receiver_mail,para_name['mail']['cc'],para_name['mail']['mail_title'],para_name['mail']['mail_content'],para_name['mail']['attachment_img'],para_name['mail']['attachment_txt'],para_name['mail']['attachment_pdf'],para_name['base']['output_path']+para_name['base']['output_file']+write_filename+".xls",para_name['mail']['attachment_word'])
        
        print("=====================\n操作结束，界面会在数秒后自动关闭...")
        time.sleep(3) #暂停3秒
        
    except:
        traceback.print_exc()
        sys.exit()