#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 永洪02报表数据入库
@author: Frank
@date: 2019/12/31

'''

#引入模块
import time,datetime,os
import sys,traceback
sys.path.append(r'E:\software\eclipse\workspace\resource')
from op_mysql import operation_table_partition,load_localdata
from op_excel import download_excel

if __name__ == '__main__':
    #参数设置
    v_para_cnt=1  #当前日期向前推几天
    
    os_path="D:\\系统报表\\出行订单报表\\"     #文件路径    
    v_date=str(datetime.date.today() - datetime.timedelta(days=v_para_cnt))
    file_name="运营部-02 出行订单表_" +v_date.replace("-","")+".xlsx"         #文件名称
    
    order_list=['日期','城市','车级','平台','冒泡数','冒泡需求数','呼叫订单数','应答订单数','完单数','完单且支付订单数','GMV','订单实付金额', '需求满足率','冒泡呼叫率','应答率','完单率', \
                '订单支付率','单均应答时长（分）','单均预估接驾时长(分)','单均实际接驾时长（分）', '单均计费里程（公里）','ASP（单均应付）','单均实付','总取消订单数','应答前乘客取消订单数', \
                '应答前乘客取消率','应答后乘客取消订单数','应答后司机取消订单数','应答后取消率','订单差评率','单均预估接驾里程（公里）','单均实际接驾里程（公里）', '乘客3星及3星以下评价率', \
                '乘客4星评价率','乘客5星评价率','乘客6星评价率','升舱订单数','升舱完单占比']
    
    
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
    result_table="res_travel_order_report_d" 
    partition_name="p_"+v_date.replace("-","")
    
    url="http://10.129.109.15:3000/api/public/card/ad0d5316-bceb-4151-b82f-e335f1ebc31f/query/xlsx?parameters=%5B%7B%22type%22%3A%22date%2Fall-options%22%2C%22target%22%3A%5B%22dimension%22%2C%5B%22template-tag%22%2C%22date%22%5D%5D%2C%22value%22%3A%22{}%22%7D%5D".format(v_date)  #下载链接url
    

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