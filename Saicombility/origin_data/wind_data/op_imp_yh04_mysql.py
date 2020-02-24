#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 永洪04报表数据入库
@author: Frank
@date: 2019/12/11

'''

#引入模块
import time,datetime,os
import sys
import traceback
sys.path.append(r'E:\software\eclipse\workspace\resource')
from op_mysql import operation_table_partition,load_localdata
from op_excel import download_excel



if __name__ == '__main__':
    #参数设置
    v_para_cnt=1   #当前日期向前推几天
    
    os_path="D:\\系统报表\\司机信息报表\\"     #文件路径    
    v_date=str(datetime.date.today() - datetime.timedelta(days=v_para_cnt))
    file_name="运营部-04 司机信息报表_" +v_date.replace("-","")+".xlsx"         #文件名称
    
    order_list=['日期','城市名称','车级','累计注册司机数','累计完单司机数','新增注册司机数','有效司机数','新增完单司机数',\
                '在线司机数','应答司机数','完单司机数','打开APP未出车司机数','司机在线率','司机人均在线时长(小时)','司机人均计费时长(小时)',\
                '计费时长占比','服务时长占比','单均实际接驾时长(分钟)','司机订单应收',\
                '司机人均订单应收','司机奖励收入','司机订单数','完单司机在线时长','司机人均奖励收入','司机人均完单数',\
                '完单司机TPH（平均每小时、每人接单量）','完单司机IPH（平均每小时、每人流水收入）','完单司机OIPH（平均每小时、每人流水收入）',\
                '月完单司机数','打开APP司机数','服务封禁数','风控封禁数',\
                '在线时长','计费时长','服务时长','接驾时长','司机收入','额外收入']
    
    
    sheet_para=0 #默认第一个sheet
    head_para="0"
    var_para="0"
    
    #本地参数    
    var_host_para="localhost"
    var_port_para=3306
    var_user_para="root"
    var_password_para="root"
    
    
    #数据库目标表
    db_name="data_resource"
    result_table="res_driver_info_report_d" 
    partition_name="p_"+v_date.replace("-","")
    
    url="http://10.129.109.15:3000/api/public/card/69c6d2d8-f89d-4f97-939e-41777adc5a23/query/xlsx?parameters=%5B%7B%22type%22%3A%22date%2Fall-options%22%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22date%22%5D%5D%2C%22value%22%3A%22{}%22%7D%5D".format(v_date)  #下载链接url
    

    download_excel(url,os_path,file_name)  #下载数据文件
     
    print("文件名称：{}".format(os_path+file_name))
    print("将数据导入本地mysql")      #数据导入本地mysql
    partition_result=operation_table_partition(var_host_para,var_port_para,var_user_para,var_password_para,db_name,result_table,partition_name)
    if partition_result == 0:
        data=load_localdata(var_host_para,var_port_para,var_user_para,var_password_para,os_path,file_name,db_name,result_table,var_para,"","",head_para,order_list)
        data.imp_excel()
    else:
        traceback.print_exc()
        sys.exit()
      
    time.sleep(2)  #暂停2秒
           
    #删除excel文件
    os.remove(os_path+file_name) 