#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 批量发送邮件
@author: Frank
@date: 2019/10/15

@用法：
python op_send_mail_spec.py  
--username  "tankun@saicmobility.com" 
--password "T123456t" 
--sender  "tankun@saicmobility.com" 
--receiver  "tankun@saicmobility.com" 
--Cc "" 
--mail_title   "测试邮件" 
--mail_content   "Hi,\n\n 这是一封测试邮件!~" 
--attachment_excel "D:\\司机收入报表\\环亚尊享汽车租赁有限公司_2019-10-16.xls" 
--attachment_word "" 
--attachment_txt "" 
--attachment_pdf "" 
--attachment_img "" 

'''
#引入模块
import argparse
from op_send_mail import send_mail


if __name__ == '__main__':
     
    parser = argparse.ArgumentParser()
    #邮箱设置
    parser.add_argument("--host_server", help="服务器ip", dest="host_server", required=True)
    parser.add_argument("--host_port", help="邮箱密码", dest="host_port", required=True)
    parser.add_argument("--username", help="邮箱用户名", dest="username", required=True)
    parser.add_argument("--password", help="邮箱密码", dest="password", required=True)
    parser.add_argument("--sender", help="发件者", dest="sender", required=True)
    parser.add_argument("--receiver", help="收件者", dest="receiver", required=True)
    parser.add_argument("--Cc", help="抄送者", dest="cc", required=True)
      
    #邮件内容    
    parser.add_argument("--mail_title", help="邮件标题", dest="mail_title")
    parser.add_argument("--mail_content", help="邮件内容", dest="mail_content")
    parser.add_argument("--attachment_img", help="图像附件", dest="attachment_img")
    parser.add_argument("--attachment_txt", help="txt文本附件", dest="attachment_txt")
    parser.add_argument("--attachment_pdf", help="pdf附件", dest="attachment_pdf")
    parser.add_argument("--attachment_excel", help="excel附件", dest="attachment_excel")
    parser.add_argument("--attachment_word", help="word附件", dest="attachment_word")
    args = parser.parse_args()
              
    #发送邮件
    send_mail(args.host_server,args.host_port,args.username,args.password，args.sender,args.cc,args.receiver,args.mail_title,args.mail_content,args.attachment_img,args.attachment_txt,args.attachment_pdf,args.attachment_excel,args.attachment_word)  