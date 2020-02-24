#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: VIN码车牌号对照表
@author: Frank
@date: 2020/01/08

'''

#引入模板
from op_read_config import read_config
from op_mysql import export_data,operation_table_partition,opera_database
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import traceback,sys,time,datetime

#使用chrome浏览器
chrome_driver = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'  #chrome驱动位置
driver = webdriver.Chrome(executable_path = chrome_driver)     # 创建Chrome对象.


#车辆数据抓取
def crash_info(inpurt_info):
    driver.find_elements_by_class_name('el-input__inner')[3].click() # 点击用户名输入框
    driver.find_elements_by_class_name('el-input__inner')[3].send_keys(Keys.CONTROL,'a') # 全选
    driver.find_elements_by_class_name('el-input__inner')[3].send_keys(Keys.BACK_SPACE) #清空输入框
    driver.find_elements_by_class_name('el-input__inner')[3].send_keys(inpurt_info)  #输入相关信息
    #采用class定位登陆按钮
    driver.find_elements_by_class_name('el-button--primary')[6].click() # 点击“搜索”按钮
    time.sleep(1)
    title_name=[]  #初始化
    data=[]
    for i in range(1,11):
        class_name="el-table_1_column_{}".format(str(i))
        title_name.append(driver.find_elements_by_class_name(class_name)[0].get_attribute("textContent"))        
        data.append(driver.find_elements_by_class_name(class_name)[1].get_attribute("textContent")) 
    data_result=dict(zip(title_name,data))
    return(data_result)
  
#登录MIS系统
def operate_url(login_url,username,password,otp,info_url):
    driver.get(login_url) #打开url链接
      
    driver.find_elements_by_class_name('ant-tabs-tab')[1].click()    #跳转到SSO登录
    time.sleep(1) #停顿1秒
    
    #输入账号&密码&otp        
    driver.find_elements_by_class_name('ant-input')[2].click()    # 点击用户名输入框
    driver.find_elements_by_class_name('ant-input')[2].clear()    # 清空输入框
    driver.find_elements_by_class_name('ant-input')[2].send_keys(username)   #输入用户名
          
    driver.find_elements_by_class_name('ant-input')[3].click() # 点击密码输入框
    driver.find_elements_by_class_name('ant-input')[3].clear()    # 清空输入框
    driver.find_elements_by_class_name('ant-input')[3].send_keys(password)   #输入密码
      
    driver.find_elements_by_class_name('ant-input')[4].click() # 点击密码输入框
    driver.find_elements_by_class_name('ant-input')[4].clear()    # 清空输入框
    driver.find_elements_by_class_name('ant-input')[4].send_keys(otp) # 点击otp输入框
      
    time.sleep(2)
      
    #采用class定位登陆按钮
    driver.find_elements_by_class_name('ant-btn')[1].click() # 点击“登录”按钮
      
    time.sleep(5)
    
    driver.get(info_url)  #打开url链接      
    time.sleep(1)  #这里必须要暂停数秒，否则网站可能加载补完整
       

        


if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="driver_num_id_config.ini"
    
    web_otp="603570"  #验证码
    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息
        mysql_data=export_data(para_name['db_info']['db_ip'],int(para_name['db_info']['db_port']),para_name['db_info']['db_username'],para_name['db_info']['db_password'],para_name['db_info']['db_sql'])
        driver_num_list=mysql_data.read_mysql()  #读取车牌号列表数据
        operation_table_partition(para_name['db_info']['db_ip'],int(para_name['db_info']['db_port']),para_name['db_info']['db_username'],para_name['db_info']['db_password'],para_name['db_info']['table_schema'],para_name['db_info']['table_name'],"p_"+str(datetime.date.today()).replace("-",""))
        operate_url(para_name['web_info']['web_loginurl'],para_name['web_info']['web_username'],para_name['web_info']['web_password'],web_otp,para_name['web_info']['web_crashurl']) #登录MIS系统
        imp_data=""  #初始化
        print("时间{}，开始执行，导入程序:".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        for i in range(1,len(driver_num_list)+1):  #编号从1开始
            driver_num=driver_num_list[i].split(",")[0].split("\'")[1]   #取出车牌号
            data_result=crash_info(driver_num)  #获取列表信息
            data_result=list(data_result.values()) #将字典列的值化为list
            data_result.append(str(datetime.date.today())) #list里增加当前时间
            data_result=str(data_result).replace("[","(").replace("]",")")  #list转为str
        #数据入库    
            imp_data=(imp_data+","+data_result).lstrip(',')
            var_sql="insert into "+para_name['db_info']['table_schema']+"."+para_name['db_info']['table_name']+" values %s" %imp_data
            if (1.0*i/10).is_integer() and i > 0 :
                opera_database(para_name['db_info']['db_ip'],int(para_name['db_info']['db_port']),para_name['db_info']['db_username'],para_name['db_info']['db_password'],var_sql,"0")  #数据插入数据库
                imp_data=""
                print("---满10行，提交第"+str(int(i/10))+"次----")
                time.sleep(2)    #停顿1秒
            else:
                pass
        opera_database(para_name['db_info']['db_ip'],int(para_name['db_info']['db_port']),para_name['db_info']['db_username'],para_name['db_info']['db_password'],var_sql,"0")  #数据插入数据库
        print("时间{},总共".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))+str(i+1)+"行，程序执行完成!~")
    
    #关闭浏览器
        driver.quit()
    
    except:
        traceback.print_exc()
        sys.exit()