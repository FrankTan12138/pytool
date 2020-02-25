#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 对excel的操作
@author: Frank
@date: 2019/10/22

'''

#引入模块
import xlrd
import pandas as pd
import xlwt
from op_read_config import read_config  #读取配置文件


#读取Excel数据
def read_excel(os_path,file_name,sheet_para):
    sheetnames=xlrd.open_workbook(os_path+file_name).sheet_names()   #打开来源数据excel表格
    data=pd.read_excel(os_path+file_name,sheet_name=sheetnames[int(sheet_para)],header=None)   #有标题栏，读取sheet内的数据
    nrows=data.columns.size    #EXCEL列数
    ncols=len(data)
#     print(str(ncols) +"\t" +str(nrows))
    data_result={}
    for i in range(0,ncols):
        data_col=""
        for j in range(0,nrows):
            data_col=(data_col+","+"\'"+str(data.iloc[i,j]).replace("\n","").replace(" ","")+"\'").strip(",")        
        data_result[i]="("+data_col+")"
    return(data_result)

#数据筛选
def data_filter(os_path,config_file,data_info,start_num,end_num,filter_condition):
    para_name=read_config(os_path,config_file)
    data_result1={} #初始化
    j=1  #筛选结果重新序号
    for i in range(int(start_num)-1,end_num):
        data=data_info[i].replace("\'","").replace("(","").replace(")","").split(",")
        if i == 0:
            data_keys=data
            data_result1[i]=list(data)
        else:
            data_values=data
            data_result=dict(zip(data_keys,data_values))
            if data_result[para_name['condition']['filter_name']] == filter_condition:
                data_result1[j]=data_result
                j=j+1 
            else:
                pass
    return(data_result1)


#数据写入Excel
def write_excel(os_path,file_name,sheet_name,start_mun,insert_info):
    work_book=xlwt.Workbook(encoding='utf-8')
    sheet=work_book.add_sheet(sheet_name) #sheet名称
    #写入title数据
    for i in range(int(start_mun)-1,len(insert_info[0])):
        sheet.write(0,i,insert_info[0][i])
    #写入数据
        for j in range(int(start_mun),len(insert_info)):
            sheet.write(j,i,insert_info[j][insert_info[0][i]])
    #数据保存到excel   
    work_book.save(os_path+file_name+".xls")
    print("数据写入Excel-{},执行完成!~".format(file_name))
    


