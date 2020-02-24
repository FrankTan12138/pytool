#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 司机出行数据拆分推送 
@author: Frank
@date: 2020/02/08

'''

#引入模块
from op_read_config import read_config  #读取配置文件
from op_text import read_txt   #读取list表单
from op_send_mail import send_mail
import traceback,sys,datetime,time

if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="driver_outside_config.ini"
    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息
        
    #参数设置
        v_para_cnt=para_name['base']['v_para_cnt']
        v_date=str(datetime.date.today() - datetime.timedelta(days=int(para_name['base']['v_para_cnt'])))  #获取上个周日的日期       
        output_path=para_name['base']['output_path']  #输出路径
        city_name_list=para_name['base']['city_name_list'].split(",") # 城市名称
        list_name=para_name['condition']['list_name']  #城市清单列表
    #邮箱配置
        host_server=para_name['mail']['host_server']  #邮箱服务器ip
        host_port=para_name['mail']['host_port']  #端口
        mail_username=para_name['mail']['user_name']  #登录账户
        mail_password=para_name['mail']['password']  #密码
        sender=para_name['mail']['sender']  #发件邮箱
        cc=para_name['mail']['cc']  #抄送
        attachment_img=para_name['mail']['attachment_img'] #图片
        attachment_txt=para_name['mail']['attachment_txt'] #txt
        attachment_pdf=para_name['mail']['attachment_pdf'] #pdf
        attachment_word=para_name['mail']['attachment_word'] #word
        
        print("=====================\n开始进行操作，操作过程会持续一段时间，请稍后.....")
        for write_filenames in read_txt(os_path,list_name+".txt"):
            city_name=write_filenames.split("\t")[0]
            output_file=para_name['base']['output_file'].format(city_name,v_date[0:4]) #输出文件名称
            mail_title=para_name['mail']['mail_title'].format(city_name,v_date[5:7]+v_date[8:10])  #标题
            mail_content=para_name['mail']['mail_content'].format(city_name,v_date[5:7],v_date[8:10]) #内容
            attachment_excel=output_path+output_file+".xls" #excel
        #发送邮件
            receiver_mail=write_filenames.split("\t")[1]
            print("发送给对应的城市：{}        对应邮箱：{}".format(city_name,receiver_mail))
            send_mail(host_server,host_port,mail_username,mail_password,sender,receiver_mail,cc,mail_title,mail_content,attachment_img,attachment_txt,attachment_pdf,attachment_excel,attachment_word)
        print("邮件:司机出行数据_{},执行完成！~".format(v_date.replace("-","")))
        print("=====================\n操作结束，界面会在数秒后自动关闭...")
        time.sleep(3) #暂停3秒
        
    except:
        traceback.print_exc()
        sys.exit()