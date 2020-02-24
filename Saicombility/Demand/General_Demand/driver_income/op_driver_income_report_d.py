#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 司机收入日报处理
@author: Frank
@date: 2020/01/06

'''

#引入模块
from op_read_config import read_config  #读取配置文件
from op_text import read_txt   #读取list表单
from op_excel import write_excel
import traceback,sys,datetime,time
from op_mysql import export_data



if __name__ == '__main__':
    os_path= r"D:\Code\para_config\\"
    config_file="driver_income_config_shanghai.ini"

    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息
        v_para_cnt=int(para_name['base']['para_cnt'])
        v_date=str(datetime.date.today() - datetime.timedelta(days=v_para_cnt))  #日期，默认昨天
        print("=====================\n开始进行操作，操作过程会持续一段时间，请稍后.....")
        for write_filenames in read_txt(os_path,str(para_name['condition']['list_name'])+".txt"):
            write_filename=write_filenames.split("\t")[0]
            mysql_data=export_data(para_name['base']['host_ip'],para_name['base']['port'],para_name['base']['db_user'],para_name['base']['db_pwd'],para_name['mysql']['var_sql'])  #导出数据表里的数据
            data_info=mysql_data.data_filter(para_name['condition']['filter_name'], write_filename, para_name['mysql']['title_name'].split(","))
            write_excel(para_name['base']['output_path'],para_name['base']['output_file']+write_filename,v_date,para_name['base']['title_no'],data_info)
        print("=====================\n操作结束，界面会在数秒后自动关闭...")
        time.sleep(3) #暂停3秒
        
    except:
        traceback.print_exc()
        sys.exit()