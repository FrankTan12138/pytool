#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 对mysql的操作
@author: Frank
@date: 2019/10/22

'''

#引入模块
import MySQLdb
import sys
import traceback
import time
# import os
from op_excel import read_excel
from op_text import read_txt,read_csv


#mysql数据库操作
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
    

#判断表是否存在
def exists_table(var_host,var_port,var_user,var_password,table_schema,table_name): 
    var_sql="select count(*)   from information_schema.tables \
    where TABLE_SCHEMA='"+table_schema+"' and TABLE_NAME='"+table_name+"';" 
    if_exists_table=opera_database(var_host,var_port,var_user,var_password,var_sql,"1")
    return(if_exists_table[0][0])


#判断是否普通表还是分区表
def if_partition_table(var_host,var_port,var_user,var_password,table_schema,table_name):
    var_sql="select count(distinct partition_expression)  from information_schema.partitions \
    where TABLE_SCHEMA='"+table_schema+"' and TABLE_NAME='"+table_name+"';" 
    if_partition_table=opera_database(var_host,var_port,var_user,var_password,var_sql,"1")
    return(if_partition_table[0][0])


#判断分区表的分区是否存在
def exists_partition(var_host,var_port,var_user,var_password,table_schema,table_name,partition_name):
    var_sql="select count(*) from information_schema.`PARTITIONS` \
    where TABLE_SCHEMA='"+table_schema+"' and table_name='"+table_name+"' \
    and partition_name='"+partition_name+"';"
    if_exists_partition=opera_database(var_host,var_port,var_user,var_password,var_sql,"1") 
    return(if_exists_partition[0][0])
        
#分区表创建/清空分区
def operation_table_partition(var_host,var_port,var_user,var_password,table_schema,table_name,partition_name):
    try:
        #判断分区表的特定分区是否存在
        if_partition=exists_partition(var_host,var_port,var_user,var_password,table_schema,table_name,partition_name)
        if if_partition > 0 :
            var_sql="alter table "+table_schema+"."+table_name+" truncate partition "+partition_name+";"
            opera_database(var_host,var_port,var_user,var_password,var_sql,"0")  #清空分区
            print("---清空分区完成---")
        else:
            var_sql="alter table "+table_schema+"."+table_name+" add partition (partition "+partition_name+" values in (\'"+partition_name[2:6]+"-"+partition_name[6:8]+"-"+partition_name[8:10]+"\'));"
            opera_database(var_host,var_port,var_user,var_password,var_sql,"0")  #创建分区
            print("---创建分区完成---")
        return 0
    except:
        traceback.print_exc()
        return 1

#执行本地数据数据导入
class load_localdata:
    def __init__(self,var_host,var_port,var_user,var_password,local_path,local_filename,table_schema,table_name,sheet_para,var_sep,partition_name,var_para,order_list):
        self.var_host=var_host
        self.var_port=var_port
        self.var_user=var_user
        self.var_password=var_password
        self.local_path=local_path
        self.local_filename=local_filename
        self.table_schema=table_schema
        self.table_name=table_name
        self.sheet_para=sheet_para
        self.var_sep=var_sep
        self.partition_name=partition_name
        self.order_list=order_list
        self.var_para=var_para
        

    #导入excel数据        
    def imp_excel(self):
        data_excel=read_excel(self.local_path,self.local_filename,self.sheet_para,self.var_para,self.order_list)
        print("开始执行，导入程序:")
        try:
            imp_data=""
            for i in range(0,len(data_excel)):
                imp_data=(imp_data+","+data_excel[i]).lstrip(',')
                var_sql="insert into "+self.table_schema+"."+self.table_name+" values %s" %imp_data
                if (1.0*i/500).is_integer() and i > 0 :
        #             print(var_sql)
                    opera_database(self.var_host,self.var_port,self.var_user,self.var_password,var_sql,"0")  #数据插入数据库
                    imp_data=""
                    print("---满500行，提交第"+str(int(i/500))+"次----")
                    time.sleep(2)    #停顿1秒
                else:
                    pass
            opera_database(self.var_host,self.var_port,self.var_user,self.var_password,var_sql,"0")  #数据插入数据库
            print("总共"+str(i+1)+"行，程序执行完成!~")
        except:
            traceback.print_exc()
            sys.exit()
            
    #导入txt数据       
    def imp_txt(self):
        data_txt=read_txt(self.local_path,self.local_filename)
        print("开始执行，导入程序:")
        imp_data=""
        i=0  #初始化
        try:
            for data in data_txt:
                i=i+1
                imp_data=(imp_data+","+"(\'"+"','".join(data.split(self.var_sep))+"\')").lstrip(',')
                var_sql="insert into "+self.table_schema+"."+self.table_name+" values %s" %imp_data
                if (1.0*i/500).is_integer() and i > 0 :
            #             print(var_sql)
                        opera_database(self.var_host,self.var_port,self.var_user,self.var_password,var_sql,"0")  #数据插入数据库
                        imp_data=""
                        print("---满500行，提交第"+str(int(i/500))+"次----")
                        time.sleep(2)    #停顿1秒
                else:
                    pass
            opera_database(self.var_host,self.var_port,self.var_user,self.var_password,var_sql,"0")  #数据插入数据库
            print("总共"+str(i)+"行，程序执行完成!~")
        except:
            traceback.print_exc()
            sys.exit() 
     
    #导入csv数据        
    def imp_csv(self): 
        data_csv=read_csv(self.local_path,self.local_filename)
        print("开始执行，导入程序:")
        try:
            imp_data=""
            for i in range(0,len(data_csv)):
                imp_data=(imp_data+","+"(\'"+"','".join(data_csv[i])+"\')").lstrip(',')
                var_sql="insert into "+self.table_schema+"."+self.table_name+" values %s" %imp_data
                if (1.0*i/500).is_integer() and i > 0 :
                #   print(var_sql)
                    opera_database(self.var_host,self.var_port,self.var_user,self.var_password,var_sql,"0")  #数据插入数据库
                    imp_data=""
                    print("---满500行，提交第"+str(int(i/500))+"次----")
                    time.sleep(2)    #停顿1秒
                else:
                    pass                
            opera_database(self.var_host,self.var_port,self.var_user,self.var_password,var_sql,"0")  #数据插入数据库
            print("总共"+str(i+1)+"行，程序执行完成!~")
        except:
            traceback.print_exc()
            sys.exit()
    
    
    #判断表是否存在
    def exists_table(self):
        #判断表是否存在
        if_exist_table=exists_table(self.var_host,self.var_port,self.var_user,self.var_password,self.table_schema,self.table_name)
        if if_exist_table > 0:  #如果存在
            #判断是否是分区表
            if_part_table=if_partition_table(self.var_host,self.var_port,self.var_user,self.var_password,self.table_schema,self.table_name)
            if if_part_table > 0 :
                operation_table_partition(self.var_host,self.var_port,self.var_user,self.var_password,self.table_schema,self.table_name,self.partition_name)
            return 0
        else:
            print("涉及到表：{}.{}不存在".format(self.table_schema,self.table_name))
            return 1
                  
                              
             
    #导入数据到数据库
    def load_localdata(self):
        if load_localdata.exists_table(self) == 0 :            
            if self.local_filename.split(".")[1] =="txt":
                load_localdata.imp_txt(self)
            elif self.local_filename.split(".")[1] == "csv":
                load_localdata.imp_csv(self)
            elif self.local_filename.split(".")[1] == "xlsx" or self.local_filename.split(".")[1] == "xls":
                load_localdata.imp_excel(self)
            else:
                print("目前只支持csv,txt,Excel数据导入.....")
                sys.exit()
        else:
            sys.exit()  #退出系统
             
#数据导出
class export_data:
    def __init__(self,var_host,var_port,var_user,var_password,var_sql):
        self.var_host=var_host
        self.var_port=int(var_port)
        self.var_user=var_user
        self.var_password=var_password
        self.var_sql=var_sql
        
    #读取mysql数据库里的数据
    def read_mysql(self):
        mysql_data=opera_database(self.var_host,self.var_port,self.var_user,self.var_password,self.var_sql,"1")
        mysql_data1=[]
        cnt=[] #计数器
        for i in range(0,len(mysql_data)):
            cnt.append(i+1)  #预留一列，增加标题
            mysql_data1.append(str(mysql_data[i]))
        mysql_data=dict(zip(cnt,mysql_data1))
        return(mysql_data)
        
    
    #数据筛选
    def data_filter(self,filter_name,filter_condition,title_name):
        data_info=export_data.read_mysql(self)   #读取mysql数据表的结果
        data_info_title={0:str('(\'')+"\',\'".join(title_name)+str('\')')}  #标题列表
        data_info=dict(list(data_info_title.items())+list(data_info.items()))  #合并成目标字典列
        data_result1={} #初始化
        j=1  #筛选结果重新序号
        for i in range(0,len(data_info)):
            data=data_info[i].replace("\'","").replace("(","").replace(")","").split(",")
            if i == 0:
                data_keys=data
                data_result1[i]=list(data)
            else:
                data_values=data
                data_result=dict(zip(data_keys,data_values))
                if len(filter_name) == 0 :
                    data_result1[i]=data_result
                elif data_result[filter_name].strip()== filter_condition :  #去除字符串的空格
                    data_result1[j]=data_result
                    j=j+1
                else:
                    pass
        return(data_result1)  