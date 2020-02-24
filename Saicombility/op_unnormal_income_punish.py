#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: Excel拆分封装程序
@author: Frank
@date: 2019/10/22

'''

#引入模块
from op_read_config import read_config  #读取配置文件
from op_text import read_txt   #读取list表单
from op_excel import read_excel,data_filter,write_excel,read_sheet_name,add_sheet
import traceback,sys,time

if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="driver_punish_config.ini"
    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息
        
        #根据列表清单对源表数据进行excel拆分
        print("文件名称：{}".format(para_name['base']['input_path']+para_name['base']['file_name']))
        sheet_name=read_sheet_name(para_name['base']['input_path'], para_name['base']['file_name'])     #原Excel的sheet名称list
        sheet_cnt=len(para_name['base']['split_sheet_no'].split(","))   #需要拆分的sheet数量
        print("=====================\n开始进行操作，操作过程会持续一段时间，请稍后.....")
        #拆分数据
        for write_filenames in read_txt(os_path,str(para_name['condition']['list_name'])+".txt"):
            write_filename=write_filenames.split("\t")[0]
            for i in range(0,len(sheet_name)):
                if i == 0 :
                    data_info=read_excel(para_name['base']['input_path'], para_name['base']['file_name'],i,para_name['base']['title_no'],para_name['base']['order_list'])  #读取excel数据
                    data_result=data_filter(os_path,config_file,data_info,para_name['base']['title_no'],len(data_info),write_filename,"0")  #数据筛选
                    write_excel(para_name['base']['output_path'],para_name['base']['output_file']+write_filename,sheet_name[i],para_name['base']['title_no'],data_result)
                else:
                    data_info=read_excel(para_name['base']['input_path'], para_name['base']['file_name'],i,para_name['base']['title_no'],para_name['base']['order_list'])  #读取excel数据
                    data_result=data_filter(os_path,config_file,data_info,para_name['base']['title_no'],len(data_info),write_filename,i)  #数据筛选
                    add_sheet(para_name['base']['output_path'],para_name['base']['output_file']+write_filename,sheet_name[int(i)],para_name['base']['title_no'],data_result)
        print("=====================\n操作结束，界面会在数秒后自动关闭...")
        time.sleep(3) #暂停3秒
                    
                    
            
    except:
        traceback.print_exc()
        sys.exit()