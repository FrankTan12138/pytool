#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 神访分结果表拆分
@author: Frank
@date: 2019/12/11
'''


#引入模块
from op_send_mail import send_mail
from op_excel import read_excel,data_filter,add_sheet
from op_read_config import read_config
from op_text import read_txt
import traceback,sys
import pandas as pd
import xlrd,xlwt
import time


#读取Excel数据指定区域
def read_excel_dict(os_path,file_name,sheet_para,var_para,order_list,column_start,column_end,row_start,row_end):
    sheetnames=xlrd.open_workbook(os_path+file_name).sheet_names()   #打开来源数据excel表格
    data=pd.read_excel(os_path+file_name,sheet_name=sheetnames[int(sheet_para)],header= eval(var_para.replace("1","None")))   #有标题栏，读取sheet内的数据
    data=data.iloc[int(column_start):int(column_end),int(row_start):int(row_end)]
    if len(order_list) > 0:
        data=data[order_list]
    else:
        pass
    nrows=data.columns.size    #EXCEL列数
    ncols=len(data)
#     print(str(ncols) +"\t" +str(nrows))
    data_result={}
    for i in range(0,ncols):
        data_col=""
        for j in range(0,nrows):
            data_col=(data_col+","+"\'"+str(data.iloc[i,j]).replace("nan","").replace("\n","").replace(" ","")+"\'").strip(",")        
        data_result[i]="("+data_col+")"
    return(data_result)


#区域数据筛选
def data_dict_filter(os_path,config_file,data_info,start_num,end_num,row_start,row_end,filter_condition):
    para_name=read_config(os_path,config_file)
    data_result1={} #初始化
    j=1  #筛选结果重新序号
    for i in range(int(start_num)-1,end_num):
        data=data_info[i].replace("\'","").replace("(","").replace(")","").split(",")[int(row_start):int(row_end)]
        if i == 0:
            data_keys=data
            data_result1[i]=list(data)
        else:
            data_values=data
            data_result=dict(zip(data_keys,data_values))
            if data_result[para_name['condition']['filter_name1']] == filter_condition:
                data_result1[j]=data_result
                j=j+1 
            else:
                pass
    return(data_result1)    

#数据写入Excel
def data_result(data_info,os_path,file_name,sheet_name):
    work_book=xlwt.Workbook(encoding='utf-8')
    sheet=work_book.add_sheet(sheet_name) #sheet名称
    for j in range(0,len(data_info)):
        data=data_info[j].replace("\'","").replace("(","").replace(")","").split(",")
        for i in range(0,len(data)):
            sheet.write(j,i,data[i])
    work_book.save(os_path+file_name+".xls")
    print("数据写入Excel-{}：sheet-{},执行完成!~".format(file_name,sheet_name))
            
    




if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="sf_driver_result_config.ini"
    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息
        #根据列表清单对源表数据进行excel拆分
        print("文件名称：{}".format(os_path+para_name['base']['file_name']))
                
        for write_filenames in read_txt(os_path,str(para_name['condition']['list_name'])+".txt"):
            write_filename=write_filenames.split("\t")[0]
              
            print("开始操作：{}-{}".format(write_filename,'上海司机神访分统计（汇总）'))
            data_info=read_excel_dict(para_name['base']['input_path'], para_name['base']['file_name'],int(para_name['base']['sheet_no3']),para_name['base']['title_no'],para_name['base']['order_list'],0,77,8,19)
            data_result(data_info,para_name['base']['output_path'],write_filename,para_name['base']['write_sheet_name4'])
           
        for write_filenames in read_txt(os_path,str(para_name['condition']['list_name'])+".txt"):
            write_filename=write_filenames.split("\t")[0]
                  
            print("开始操作：{}-{}".format(write_filename,'上海司机神访分统计(清单)'))
            data_info=read_excel(para_name['base']['input_path'], para_name['base']['file_name'],int(para_name['base']['sheet_no3']),para_name['base']['title_no'],para_name['base']['order_list'])  #读取excel数据
            data_result=data_dict_filter(os_path,config_file,data_info,para_name['base']['title_no'],len(data_info),para_name['condition']['row_start'],para_name['condition']['row_end'],write_filename)  #数据筛选
            add_sheet(para_name['base']['output_path'],write_filename,para_name['base']['write_sheet_name3'],para_name['base']['title_no'],data_result,"0")
                
            print("开始操作：{}-{}".format(write_filename,'线上神访数据汇总（供租赁公司反查核实）'))
            data_info=read_excel(para_name['base']['input_path'], para_name['base']['file_name'],int(para_name['base']['sheet_no2']),para_name['base']['title_no'],para_name['base']['order_list'])  #读取excel数据
            data_result=data_filter(os_path,config_file,data_info,para_name['base']['title_no'],len(data_info),write_filename,"0")  #数据筛选
            add_sheet(para_name['base']['output_path'],write_filename,para_name['base']['write_sheet_name2'],para_name['base']['title_no'],data_result)
                
            print("开始操作：{}-{}".format(write_filename,'线下神访数据汇总'))
            data_info=read_excel(para_name['base']['input_path'], para_name['base']['file_name'],int(para_name['base']['sheet_no']),para_name['base']['title_no'],para_name['base']['order_list'])  #读取excel数据
            data_result=data_filter(os_path,config_file,data_info,para_name['base']['title_no'],len(data_info),write_filename,"0")  #数据筛选
            add_sheet(para_name['base']['output_path'],write_filename,para_name['base']['write_sheet_name'],para_name['base']['title_no'],data_result)
               
            time.sleep(3)  #暂停3秒
        #发送邮件
            receiver_mail=write_filenames.split("\t")[1]
            print("发送给租赁公司：{}        对应邮箱：{}".format(write_filename,receiver_mail))
            send_mail(para_name['mail']['host_server'],para_name['mail']['host_port'],para_name['mail']['user_name'],para_name['mail']['password'],para_name['mail']['sender'],receiver_mail,para_name['mail']['cc'],para_name['mail']['mail_title'],para_name['mail']['mail_content'],para_name['mail']['attachment_img'],para_name['mail']['attachment_txt'],para_name['mail']['attachment_pdf'],para_name['base']['output_path']+write_filename+".xls",para_name['mail']['attachment_word'])


    except:
        traceback.print_exc()
        sys.exit()