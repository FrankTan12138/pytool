#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 永洪06报表数据入库
@author: Frank
@date: 2019/10/16

'''

#引入模块
import xlrd
import pandas as pd
import MySQLdb
import time,datetime,os
# import shutil
import urllib
from urllib.request import unquote
import traceback
import sys

#下载数据文件
def download_excel(url,os_path,file_name):
    print(unquote(url))
    print("开始下载：{}".format(file_name))
    try:
        urllib.request.urlretrieve(url,os_path+file_name)  #下载文件，并保存到指定文件夹
        print("下载完成：{}".format(file_name))
    except:
        traceback.print_exc()
        sys.exit()


#数据库操作模块
def opera_database(var_host,var_port,var_user,var_password,var_sql,var_para):
    if var_port == "":
        conn=MySQLdb.connect(host=var_host,user=var_user,password=var_password,charset="UTF8")
    else:
        conn=MySQLdb.connect(host=var_host,port=var_port,user=var_user,password=var_password,charset="UTF8")
    cur=conn.cursor()
    if var_para == str(2):
        var_sql_para1=var_sql.split(",")[0]
        var_sql_para2=var_sql.split(",")[1]
        cur.callproc(var_sql_para1,[var_sql_para2])        
    elif var_para == str(0) :
        cur.execute(var_sql)
        conn.commit()
    elif var_para == str(1) :
        cur.execute(var_sql)
        results=cur.fetchall()
        return (results)
    else :
        print('error!')
    cur.close()
    conn.close()
    
#读取Excel数据
def read_excel(os_path,file_name,sheet_para,head_para,order_list):
    sheetnames=xlrd.open_workbook(os_path+file_name).sheet_names()   #打开来源数据excel表格
    if head_para == 0 :
        data=pd.read_excel(os_path+file_name,sheet_name=sheetnames[sheet_para],header=None) #没有标题栏，读取sheet内的数据
    else:
        data=pd.read_excel(os_path+file_name,sheet_name=sheetnames[sheet_para],header=0)   #有标题栏，读取sheet内的数据
    data=data[order_list]  #按照原字段顺序输出
    nrows=data.columns.size    #EXCEL列数
    ncols=len(data)
#     print(str(ncols) +"\t" +str(nrows))
    data_result={}
    for i in range(1,ncols):
        data_col=""
        for j in range(0,nrows):
            if j == 0:
                data_col="\'"+str(data.iloc[i,0]).replace(" 00:00:00","")+"\'"  #剔除小时分钟秒
            else:
                data_col=(data_col+","+"\'"+str(data.iloc[i,j])+"\'").strip(",")        
        data_result[i]="("+data_col+")".replace("nan","")
    return(data_result)
    

#将数据导入临时表里
def import_Mysqldb(var_host_para,var_port_para,var_user_para,var_password_para,var_para,db_name,result_table,v_date,os_path,file_name,sheet_para,head_para): 
    var_sql="SELECT count(*) FROM information_schema.PARTITIONS where TABLE_SCHEMA=\'"+db_name+"\' and table_name=\'"+result_table+"\' and partition_name=\'p_"+str(v_date).replace("-","")+"\';"
    partition_exists=opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,"1")  #判断分区是否存在
    if partition_exists[0][0] == 0:
        var_sql="alter table "+db_name+"."+result_table+" add partition(partition p_"+str(v_date).replace("-","")+" values in (\'"+str(v_date)+"\'));"
        print("---创建分区完成---")
        opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,"0")  #增加分区
    else:
        var_sql="alter table "+db_name+"."+result_table+" truncate partition p_"+str(v_date).replace("-","")+";"
        opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,"0")  #清空分区
        print("---清空分区完成---")
        
    data_excel=read_excel(os_path,file_name,sheet_para,head_para,order_list) #读取EXCEL的数据 
    print("开始执行，导入程序:")
    imp_data=""
    for i in range(1,len(data_excel)+1):
        imp_data=(imp_data+","+data_excel[i]).lstrip(',')
        var_sql="insert into "+db_name+"."+result_table+" values %s" %imp_data
        if (1.0*i/500).is_integer() and i > 0 :
#             print(var_sql)
            opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,var_para)  #数据插入数据库
            imp_data=""
            print("-------满500行，提交第"+str(int(i/500))+"次----")
            time.sleep(2)    #停顿1秒
        else:
            pass
    opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,var_para) #数据插入数据库    
    print("总共"+str(i+1)+"行，程序执行完成!~")


if __name__ == '__main__':
    #参数设置
    v_para_cnt=1   #当前日期向前推几天
    
    os_path="D:\\系统报表\\司机收入报表\\"     #文件路径
    v_date=str(datetime.date.today() - datetime.timedelta(days=v_para_cnt))
    file_name="运营部-06 司机收入报表_" +v_date.replace("-","")+".xlsx"         #文件名称
    order_list=['统计日期','城市名称','司机id','司机名字','车牌号','司机车级','司机电话','司机公司名称','司机状态','司机分类','完单数','预约单完单量',\
                'A级订单完单量','B级订单完单量','C级订单完单量','司机绑定车辆时间','司机首次完单时间','司机应收','司机实收','司机分成收入','预约单分成收入',\
                'A级订单司机分成收入','B级订单司机分成收入','C级订单司机分成收入','司机奖励收入','附加费','取消费','司机收入','司机扣款','在线时长','计费时长',\
                '点火时长','司机指派完单率','TPH','IPH','OIPH','当日服务分','服务分','应答订单数','预约单应答订单数','A级应答订单数','B级应答订单数',\
                'C级应答订单数','司机有责取消订单数','司机有责取消订单数A级','司机有责取消订单数B级','司机有责取消订单数C级','预约单司机有责取消数','指定时间段在线时长',\
                '实际单均接驾里程','早高峰应答订单数','晚高峰应答订单数','平峰应答订单数']
    
    sheet_para=0 #默认第一个sheet
    head_para=1
    var_para="0"
    
    #本地参数    
    var_host_para="localhost"
    var_port_para=3306
    var_user_para="root"
    var_password_para="root"
    
    
    #数据库目标表
    db_name="data_resource"
    result_table="res_driver_income_report_d" 
    v_city_name_list=['昆山市']
   
    
    url="http://10.129.109.15:3000/api/public/card/0504072d-d8f3-413d-a2f9-a02f1e946bb3/query/xlsx?parameters=%5B%7B%22type%22%3A%22date%2Fall-options%22%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22date%22%5D%5D%2C%22value%22%3A%22{}%22%7D%5D".format(v_date)  #下载链接url
       
    
#     os.rename("D:\\运营部-06 司机收入报表.xlsx","D:\\"+file_name)   #将Excel数据表重命名
#     shutil.move("D:\\"+file_name,os_path+file_name)  #将目标文件放到指定的目录夹下

    download_excel(url,os_path,file_name)  #下载数据文件
    
    print("文件名称：{}".format(os_path+file_name))
    print("将数据导入本地mysql")      #数据导入本地mysql
    import_Mysqldb(var_host_para,var_port_para,var_user_para,var_password_para,var_para,db_name,result_table,v_date,os_path,file_name,sheet_para,head_para)  #将数据加载入mysql
    
    #调用存储过程，拆分昆山市数据
    for v_city_name in v_city_name_list:
        call_procedure=db_name+".sp_"+result_table
        call_procedure_para=v_date+"#"+v_city_name
        var_sql=""+call_procedure+","+call_procedure_para
        print("开始执行地级城市拆分操作：{}".format(v_city_name))
        opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,"2")
        print("执行完成！~")
     
    time.sleep(2)  #暂停2秒
          
    #删除excel文件
    os.remove(os_path+file_name) 