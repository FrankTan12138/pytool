#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 司机订单标签月报推送
@author: Frank
@date: 2020/02/08

'''
#引入模块
import datetime,time,traceback,sys,os
sys.path.append(r'E:\software\eclipse\workspace\resource')
from op_text import read_txt   #读取list表单
from op_read_config import read_config
from op_send_mail import send_mail

if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="driver_comp_order_sign_config.ini"
    today=str(datetime.date.today()) #取今天的日期
    
    #每月1号执行    
    if today[8:10] == '01' :
        try:
            para_name=read_config(os_path,config_file) #读取配置信息
        #base参数
            v_date=str(datetime.date.today() - datetime.timedelta(days=int(para_name['base']['v_para_cnt'])))  #获取上个周日的日期           
        #excel部分参数
            excel_path=para_name['excel']['excel_path'] #excel路径
        #mysql参数
            city_name_list=para_name['mysql']['city_name'].split(",") #城市名称 
        #邮箱参数
            host_server=para_name['mail']['host_server']  #邮箱服务器ip
            host_port=para_name['mail']['host_port']  #端口
            mail_username=para_name['mail']['user_name']  #登录账户
            mail_password=para_name['mail']['password']  #密码
            sender=para_name['mail']['sender']  #发件邮箱
            receiver=para_name['mail']['receiver'] #收件邮箱
            cc=para_name['mail']['cc']  #抄送
            mail_title=para_name['mail']['mail_title'].format(v_date[0:4]+v_date[5:7])  #标题
            attachment_img=para_name['mail']['attachment_img'] #图片
            attachment_txt=para_name['mail']['attachment_txt'] #txt
            attachment_pdf=para_name['mail']['attachment_pdf'] #pdf
            attachment_word=para_name['mail']['attachment_word'] #word
            list_name=str(para_name['condition']['list_name'])
            
            print("=====================\n开始进行操作，操作过程会持续一段时间，请稍后.....") 
            for city_name in city_name_list:
                excel_name=para_name['excel']['excel_name'].format(city_name)   #excel名称 
                mail_content=para_name['mail']['mail_content'].format(city_name,v_date[0:4],v_date[5:7]) #内容
                attachment_excel=excel_path+excel_name.split(".")[0]+"_"+v_date[0:4]+v_date[5:7]+".xlsx" #excel
                for city_name1 in read_txt(os_path,list_name+".txt"):
                    city_name2=city_name1.split("\t")[0]  #读取list里面的城市名称
                    if city_name2 == city_name:
                    #发送邮件
                        receiver_mail=city_name1.split("\t")[1]  #对应的发送邮箱
                        print("城市名称：{}        对应邮箱：{}".format(city_name,receiver_mail))
                        send_mail(host_server,host_port,mail_username,mail_password,sender,receiver_mail,cc,mail_title,mail_content,attachment_img,attachment_txt,attachment_pdf,excel_path+excel_name.split(".")[0]+"_"+v_date[0:4]+v_date[5:7]+".xlsx",attachment_word)
            
            
            os.remove(excel_path+excel_name.split(".")[0]+"_"+v_date[0:4]+v_date[5:7]+".xlsx") #删除邮件附件
            print("=====================\n操作结束，界面会在数秒后自动关闭...")
            time.sleep(3) #暂停3秒
        
        except:
            traceback.print_exc()
            sys.exit()