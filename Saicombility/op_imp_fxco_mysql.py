#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 风行大数据门户-实时订单看板
@author: Frank
@date: 2019/12/10

'''

#引入模板
import json
from op_text import read_txt
import MySQLdb
import time,datetime
import os
from selenium import webdriver
from urllib.request import unquote

#使用chrome浏览器
chrome_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'  #chrome驱动位置
driver = webdriver.Chrome(executable_path = chrome_driver)     # 创建Chrome对象.


#下载数据
def down_json(city_name,os_path,start_time,end_time):
    for v_city_name in city_name:
        file_name="realTime_Order_Kanban_{}_{}.json".format(v_city_name,end_time.replace("-","")) 
        Crrent_order_url="http://data.saicm.local/dataportal-service/dashboard/realTime_Order_Kanban?city={}&carLevel=210&startTime={}&endTime={}".format(unquote(v_city_name),start_time,end_time)
        driver.get(Crrent_order_url)
        data = driver.find_element_by_tag_name("pre").get_attribute("textContent")
        print("开始下载：{}".format(os_path+file_name))
        with open(os_path+file_name,"wb+")  as file:
            file.write(data.encode("utf-8"))
        file.close()
        print("下载完成：{}".format(os_path+file_name))

#风行大数据门户
def operate_url(url,os_path,username,password,otp,start_time,end_time):
#打开url链接
    driver.get(url)
        
#输入账号&密码&otp        
    driver.find_element_by_id('username').click()    # 点击用户名输入框
    driver.find_element_by_id('username').clear()    # 清空输入框
    driver.find_element_by_id('username').send_keys(username)   #自动输入用户名
        
    driver.find_element_by_id('passwd').click() # 点击密码输入框
    driver.find_element_by_id('passwd').clear()    # 清空输入框
    driver.find_element_by_id('passwd').send_keys(password)   #自动输入密码
    
    driver.find_element_by_id('otp').click() # 点击密码输入框
    driver.find_element_by_id('otp').clear()    # 清空输入框
    driver.find_element_by_id('otp').send_keys(otp) # 点击otp输入框
    
    #采用class定位登陆按钮
    driver.find_element_by_class_name('btn-sm').click() # 点击“登录”按钮
    
    time.sleep(2)
    
    #下载数据
    down_json(city_name,os_path,start_time,end_time)
    
    #关闭浏览器
    driver.quit()

#数据库操作模块
def opera_database(var_host,var_port,var_user,var_password,var_sql,var_para):
    if var_port == "":
        conn=MySQLdb.connect(host=var_host,user=var_user,password=var_password,charset="UTF8")
    else:
        conn=MySQLdb.connect(host=var_host,port=var_port,user=var_user,password=var_password,charset="UTF8")
    cur=conn.cursor()
    cur.execute(var_sql)
    if var_para == str(0) :
        conn.commit()
    elif var_para == str(1) :
        results=cur.fetchall()
        return (results)
    else :
        print('error!')
    cur.close()
    conn.close()

#json字符串数据读取
def read_json(os_path,file_name,order_list,v_city_name):
    json_data=read_txt(os_path,file_name)  #读取json文本
    dict_data=json.loads(json_data[0])   
    order_data=dict_data["data"]
    j=0   #设置初始值
    data_result={}
    for data1 in order_data:
        data_col=""
        for i in range(0,len(data1)):           
            if i == 0:
                data_col="\'"+str(data1[order_list[i]].split(" ")[0])+"\',\'"+str(data1[order_list[i]].split(" ")[1])+"\',\'"+v_city_name+"\'"
            else:
                data_col=(data_col+","+"\'"+str(data1[order_list[i]])+"\'").strip(",")
        data_col="("+data_col+")"       
        data_result[j]=data_col
        j=j+1
    return(data_result) 
      

#将输入导入mysql
def import_Mysqldb(var_host_para,var_port_para,var_user_para,var_password_para,db_name,result_table,end_time,order_list): 
    var_sql="SELECT count(*) FROM information_schema.PARTITIONS where TABLE_SCHEMA=\'"+db_name+"\' and table_name=\'"+result_table+"\' and partition_name=\'p_"+str(v_date).replace("-","")+"\';"
    partition_exists=opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,"1")  #判断分区是否存在
    if partition_exists[0][0] == 0:
        var_sql="alter table "+db_name+"."+result_table+" add partition(partition p_"+str(end_time).replace("-","")+" values in (\'"+str(v_date)+"\'));"
        print("---创建分区完成---")
        opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,"0")  #增加分区
    else:
        var_sql="alter table "+db_name+"."+result_table+" truncate partition p_"+str(end_time).replace("-","")+";"
        opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,"0")  #清空分区
        print("---清空分区完成---")
    #遍历当前有数据的省份    
    for v_city_name in city_name:
        file_name="realTime_Order_Kanban_{}_{}.json".format(v_city_name,end_time.replace("-",""))
        data_result=read_json(os_path,file_name,order_list,v_city_name)  #将数据载入
        print("开始执行，导入程序:")
        imp_data=""
        for i in range(0,len(data_result)):
            imp_data=(imp_data+","+data_result[i]).lstrip(',')
            var_sql="insert into "+db_name+"."+result_table+" values %s" %imp_data
            if (1.0*i/50).is_integer() and i > 0 :
    #             print(var_sql)
                opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,"0")  #数据插入数据库
                imp_data=""
                print("-------满50行，提交第"+str(int(i/50))+"次----")
                time.sleep(2)    #停顿1秒
            else:
                pass
        opera_database(var_host_para,var_port_para,var_user_para,var_password_para,var_sql,"0") #数据插入数据库    
        print("总共"+str(i+1)+"行，程序执行完成!~")
        #删除json文件
        print("删除文本文件！~")
        os.remove(os_path+file_name) 
          

if __name__ == '__main__':
    #本地参数    
    var_host_para="localhost"
    var_port_para=3306
    var_user_para="root"
    var_password_para="root"
    
    username="tankun"
    password="t123456T"
    otp="555116"   #目前要手动录入
    
    
    #数据库目标表
    db_name="data_resource"
    result_table="res_current_order_info_min"
    
    #配置参数
    v_para_cnt=1   #当前日期向前推几天
    os_path="D:\\实时订单数据\\"
    v_date=str(datetime.date.today() - datetime.timedelta(days=v_para_cnt))
    start_time=v_date
    end_time=v_date
    url="http://data.saicm.local/dataportal-service/html/main.html?token=cb0df5c802cf11ea8db3525400adfdb9#"  #登录网址
    
    city_name=['上海市','全国','苏州市','郑州市','杭州市','宁波市']
    order_list=['time_sec','onlineDrivers','listeningDrivers','callOrders','callOrdersSum','demandOrders','answerOrders','answerOrdersSum','completeOrders','completeOrdersSum','payOrders','payOrdersSum','completePaidOrders','completePaidOrdersSum']
    

    operate_url(url,os_path,username,password,otp,start_time,end_time) #下载数据
    import_Mysqldb(var_host_para,var_port_para,var_user_para,var_password_para,db_name,result_table,v_date,order_list) # 导入数据库
    