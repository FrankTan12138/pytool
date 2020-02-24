#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 全国运力日报
@author: Frank
@date: 2020/01/16

'''
#引入模块
import datetime,time,traceback,sys,os
sys.path.append(r'E:\software\eclipse\workspace\resource')
from op_read_config import read_config
from op_send_mail import send_mail
from op_dingtalk import dingtalk_chatbot



if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="dingtalk_yunli_daily_config.ini"
    
    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息
    #base参数
        today=str(datetime.date.today()) #根据updatetime从mysql中取要求的数据
        v_date=str(datetime.date.today() - datetime.timedelta(days=int(para_name['base']['v_para_cnt'])))  #获取日期        
    #excel部分参数
        excel_path=para_name['excel']['excel_path'] #excel路径
        excel_name=para_name['excel']['excel_name']  #excel名称
        picture_name=para_name['excel']['picture_name'].format(v_date.replace("-",""))
    #dingtalk参数
        webhook=para_name['dingtalk']['webhook'].format(para_name['dingtalk']['access_token']).replace("\"","")  #api接口
        headers=para_name['dingtalk']['headers']  #headers信息
    #markdwon参数
        title=para_name['markdown']['title']  #title信息
        text=para_name['markdown']['text'].format(v_date,v_date.replace("-",""),time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))).replace("\\n","\n") #msg信息内容
        is_at_all=para_name['markdown']['is_at_all']  #是否@所有人
    #邮箱参数
        host_server=para_name['mail']['host_server']  #邮箱服务器ip
        host_port=para_name['mail']['host_port']  #端口
        mail_username=para_name['mail']['user_name']  #登录账户
        mail_password=para_name['mail']['password']  #密码
        sender=para_name['mail']['sender']  #发件邮箱
        receiver=para_name['mail']['receiver'] #收件邮箱
        cc=para_name['mail']['cc']  #抄送
        mail_title=para_name['mail']['mail_title'].format(v_date[5:7]+v_date[8:10])  #标题
        mail_content=para_name['mail']['mail_content'].format(v_date[0:4],v_date[5:7],v_date[8:10]) #内容
        attachment_img=para_name['mail']['attachment_img'] #图片
        attachment_txt=para_name['mail']['attachment_txt'] #txt
        attachment_pdf=para_name['mail']['attachment_pdf'] #pdf
        attachment_excel=excel_path+excel_name.split(".")[0]+"_"+v_date.replace("-","")+".xlsx" #excel
        attachment_word=para_name['mail']['attachment_word'] #word
    
        print("=====================\n开始进行操作，操作过程会持续一段时间，请稍后.....")
    #通过钉钉发送Markdown
        dingtalk_chatbot=dingtalk_chatbot(webhook)
        dingtalk_chatbot.Dingtalk_markdown(title,text,is_at_all)  #推送信息
        print("钉钉推送信息:享道出行-全国运力日报_{},执行完成！~".format(v_date.replace("-","")))

    #发送邮件
        send_mail(host_server,host_port,mail_username,mail_password,sender,receiver,cc,mail_title,mail_content,attachment_img,attachment_txt,attachment_pdf,attachment_excel,attachment_word)
        print("邮件:享道出行-全国运力日报_{},执行完成！~".format(v_date.replace("-",""))) 

        
        os.remove(excel_path+picture_name+".PNG")  #删除图片
        os.remove(excel_path+excel_name.split(".")[0]+"_"+v_date.replace("-","")+".xlsx") #删除邮件附件
        print("=====================\n操作结束，界面会在数秒后自动关闭...")
        time.sleep(3)
        
    except:
        traceback.print_exc()
        sys.exit()
        