#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 司机出行数据拆分
@author: Frank
@date: 2020/02/06

'''

#引入模块
from op_read_config import read_config  #读取配置文件
from op_excel import read_excel,data_filter,add_sheet
from op_text import read_txt   #读取list表单
from op_mysql import operation_table_partition_str,load_localdata
import traceback,sys,datetime,time



if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="driver_outside_config.ini"
    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息

    #参数设置
        v_para_cnt=para_name['base']['v_para_cnt']
        v_date=str(datetime.date.today() - datetime.timedelta(days=int(para_name['base']['v_para_cnt'])))  #获取上个周日的日期       
        input_path=para_name['base']['input_path']  #输入路径
        file_name=para_name['base']['file_name'].format(v_date.replace("-",""))  #原始文件名称
        output_path=para_name['base']['output_path']  #输出路径
        city_name_list=para_name['base']['city_name_list'].split(",") # 城市名称
        split_sheet_no=para_name['base']['split_sheet_no']  #拆分sheet位置
        title_no=para_name['base']['title_no']  #是否有标题
        list_name=para_name['condition']['list_name']  #城市清单列表
    #mysql参数 
        db_ip=para_name['mysql']['db_ip']  #ip地址
        db_port=int(para_name['mysql']['db_port'])  #端口
        db_username=para_name['mysql']['db_username']  #账户
        db_password=para_name['mysql']['db_password']  #密码
        order_list=para_name['mysql']['order_list'].split(",")  #字段名称
        table_schema=para_name['mysql']['table_schema'] #库名
        table_name=para_name['mysql']['table_name']  #表名
        partition_name="p_"+v_date.replace("-","")  #分区名称
        sheet_para=para_name['base']['sheet_para']  #excel第几个sheet
        
        print("=====================\n开始进行操作，操作过程会持续一段时间，请稍后.....")
        print("文件名称：{}".format(input_path+file_name))        
    #根据列表清单对源表数据进行excel拆分
        data_info=read_excel(input_path,file_name,split_sheet_no,title_no,"")  #读取excel数据
        for write_filenames in read_txt(os_path,list_name+".txt"):
            city_name=write_filenames.split("\t")[0]
            output_file=para_name['base']['output_file'].format(city_name,v_date[0:4]) #输出文件名称
            attachment_excel=output_path+output_file+".xls" #excel
  
            data_result=data_filter(os_path,config_file,data_info,title_no,len(data_info),city_name,"0")  #数据筛选
            add_sheet(output_path,output_file,v_date[5:7]+v_date[8:10],title_no,data_result)
        print("数据拆分:Excel_{},执行完成！~".format(file_name))
    #将日数据写入mysql
        operation_table_partition_str(db_ip,db_port,db_username,db_password,table_schema,table_name,partition_name)  #分区操作
        mysql_data=load_localdata(db_ip,db_port,db_username,db_password,input_path,file_name,table_schema,table_name,sheet_para,"",partition_name,"0","")
        mysql_data.imp_excel()
        print("数据入库:Excel_{},执行完成！~".format(file_name))
        
        print("=====================\n操作结束，界面会在数秒后自动关闭...")
        time.sleep(3) #暂停3秒
            
                
    except:
        traceback.print_exc()
        sys.exit()