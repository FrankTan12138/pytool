#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 全国运力周报
@author: Frank
@date: 2020/01/27

'''
#引入模块
import datetime,time,traceback,sys,os
sys.path.append(r'E:\software\eclipse\workspace\resource')
from op_read_config import read_config
from op_send_mail import send_mail
from op_dingtalk import dingtalk_chatbot



if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="dingtalk_yunli_week_config.ini"
    week_id=datetime.date.today().strftime("%w")  #今天是星期几
    
    if week_id == '1' :   #周次才发送周报       
        try:
            para_name=read_config(os_path,config_file) #读取配置信息
        #base参数
            v_date=str(datetime.date.today() - datetime.timedelta(days=int(para_name['base']['v_para_cnt'])))  #获取上个周日的日期
            v_week_num=str(datetime.datetime.strptime(v_date,'%Y-%m-%d').isocalendar()[0])+str(datetime.datetime.strptime(v_date,'%Y-%m-%d').isocalendar()[1]).zfill(2)  #本年第几周
        #excel部分参数
            excel_path=para_name['excel']['excel_path'] #excel路径
            excel_name=para_name['excel']['excel_name']  #excel名称
            picture_name=para_name['excel']['picture_name'].format(v_week_num)
        #dingtalk参数
            webhook=para_name['dingtalk']['webhook'].format(para_name['dingtalk']['access_token']).replace("\"","")  #api接口
            headers=para_name['dingtalk']['headers']  #headers信息
        #markdwon参数
            title=para_name['markdown']['title']  #title信息
            text=para_name['markdown']['text'].format(v_week_num[0:4],v_week_num[4:6],v_week_num,time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))).replace("\\n","\n") #msg信息内容
            is_at_all=para_name['markdown']['is_at_all']  #是否@所有人
        #邮箱参数
            host_server=para_name['mail']['host_server']  #邮箱服务器ip
            host_port=para_name['mail']['host_port']  #端口
            mail_username=para_name['mail']['user_name']  #登录账户
            mail_password=para_name['mail']['password']  #密码
            sender=para_name['mail']['sender']  #发件邮箱
            receiver=para_name['mail']['receiver'] #收件邮箱
            cc=para_name['mail']['cc']  #抄送
            mail_title=para_name['mail']['mail_title'].format(v_week_num)  #标题
            mail_content=para_name['mail']['mail_content'].format(v_week_num[0:4],v_week_num[4:6]) #内容
            attachment_img=para_name['mail']['attachment_img'] #图片
            attachment_txt=para_name['mail']['attachment_txt'] #txt
            attachment_pdf=para_name['mail']['attachment_pdf'] #pdf
            attachment_excel=excel_path+excel_name.split(".")[0]+"_"+v_week_num+".xlsx" #excel
            attachment_word=para_name['mail']['attachment_word'] #word
        
            print("=====================\n开始进行操作，操作过程会持续一段时间，请稍后.....")
        #通过钉钉发送Markdown
            dingtalk_chatbot=dingtalk_chatbot(webhook)
            dingtalk_chatbot.Dingtalk_markdown(title,text,is_at_all)  #推送信息
            print("钉钉推送信息:享道出行-全国运力周报_{},执行完成！~".format(v_week_num))
    
        #发送邮件
            send_mail(host_server,host_port,mail_username,mail_password,sender,receiver,cc,mail_title,mail_content,attachment_img,attachment_txt,attachment_pdf,attachment_excel,attachment_word)
            print("邮件:享道出行-全国运力周报_{},执行完成！~".format(v_week_num)) 
    
            
            os.remove(excel_path+picture_name+".PNG")  #删除图片
            os.remove(excel_path+excel_name.split(".")[0]+"_"+v_week_num+".xlsx") #删除邮件附件
            print("=====================\n操作结束，界面会在数秒后自动关闭...")
            time.sleep(3)
            
        except:
            traceback.print_exc()
            sys.exit()
    else:
        print("今天是周{}，无需发送周报!~".format(week_id))
        sys.exit()