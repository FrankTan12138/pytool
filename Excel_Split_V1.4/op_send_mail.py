#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 批量发送邮件
@author: Frank
@date: 2019/10/15

'''
#引入模块
import smtplib
from email.mime.text import MIMEText
# from smtplib import SMTP_SSL
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from win32com.client.gencache import EnsureDispatch as Dispatch
import os,traceback,sys



#发送邮件
def send_mail(host_server,host_port,username,password,sender,receiver,cc,mail_title,mail_content,attachment_img,attachment_txt,attachment_pdf,attachment_excel,attachment_word):
    
    #收件人多人的问题
    try:
        receiver=receiver.split(',')
    except:
        traceback.print_exc()
        sys.exit()
        
    #抄送多人的问题 
    try:
        cc = cc.split(",")
        receiver_all=receiver+cc
    except:
        cc =list("")   
        receiver_all=receiver+cc
        
        
    try:
        smtp = smtplib.SMTP(host_server,host_port)
        smtp.ehlo()  # 向邮箱发送SMTP 'ehlo' 命令
        smtp.starttls()
        
        smtp.login(username,password)  #登录邮箱
        msg=MIMEMultipart('related')
        msg['Subject'] = Header(mail_title, 'utf-8')
        msg["From"] = sender
        msg["To"] = ','.join(receiver)
        msg["Cc"] = ','.join(cc)
        msgAlternative=MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        
        
        #邮件正文中换行符的问题
        try:
            mail_content=mail_content.replace("\\n","\n")
        except:
            mail_content=""
        
        
        #邮件正文
        content=MIMEText(mail_content, 'plain', 'utf-8')
        msgAlternative.attach(content)
        
        
        #image attach
        if attachment_img:
            mail_body='<b>%s</b><br><img src="cid:%s"><br>' % (mail_content,attachment_img)
            msgText = MIMEText(mail_body,'html','utf-8')
            msgAlternative.attach(msgText)
            with open(attachment_img,"rb") as fp:
                msgImage=MIMEImage(fp.read())
            msgImage.add_header('Content_id','<{}>'.format(attachment_img))
            msg.attach(msgImage)
            
        #pdf attach
        if attachment_pdf:
            with open(attachment_pdf,"rb") as fp:
                fileMsg=MIMEBase('application','pdf')
                fileMsg.setpayload(fp.read())
                encode_base64(fileMsg)
                fileMsg.add_header('Content-Disposition','attachment',filename=os.path.split(attachment_pdf)[1])
                msg.attach(fileMsg)
        
        #txt attach
        if attachment_txt:
            file_name=os.path.split(attachment_txt[1])
            att1=MIMEText(open(attachment_txt,'rb').read(),'base','utf-8')
            att1["Content-Disposition"]=f'attachment;filename="{file_name}"'
            msg.attach(att1)
        
        #excel attach
        if attachment_excel:
            part=MIMEBase('application','vnd.ms-excel')
            with open(attachment_excel,"rb") as fp:
                part.set_payload(fp.read())
                encode_base64(part)
                part.add_header('Content-Disposition','attachment',filename=os.path.split(attachment_excel)[1])
            msg.attach(part)
                
                
        #word attach
        if attachment_word:
            with open(attachment_word,"rb") as fp:
                part=MIMEApplication(fp.read())
                part.add_header('Content-Disposition','attachment',filename=os.path.split(attachment_word)[1])
                part.set_charset('utf-8')
                part.attach(part)
                
                
        smtp.sendmail(sender,receiver_all,msg.as_string())  #发送邮件
        smtp.quit()
        print('执行发送结果：Success!~')
    except:
        print('执行发送结果：Fail!~')
        traceback.print_exc()
        
#下载附件并且返回邮件信息 
def save_attachments(One_Folder,Two_Folder,Title,Attachment_File,Local_Path):
#调用windows api接口    
    outlook = Dispatch("Outlook.Application")
    mapi = outlook.GetNamespace("MAPI")
    Accounts = mapi.Folders
    
    try:       
        for Account in Accounts :
            Folders = Account.Folders
            for First_Folder in Folders:
                if First_Folder.Name == One_Folder:
                    Second_Folder=First_Folder.Folders
                    for Target_Folder in Second_Folder:
                        if Target_Folder.Name == Two_Folder :
                            Item=Target_Folder.Items
                            for email_name in Item:
                                if Title != "" :
                                    if email_name.Subject == Title:
                                        file1=[]  #初始化
                                        for i in range(1,len(email_name.Attachments)+1): 
                                            if Attachment_File == "":
                                                file1.append(email_name.Attachments.Item(i).FileName) #list输出
                                                mail_info={
                                                        'subject' : email_name.Subject.split(";"),
                                                        'sender'  : email_name.SenderName.split(";"),
                                                        'receiver': email_name.To.split(";"),
                                                        'cc'      : email_name.CC.split(";"),
                                                        'content' : email_name.Body.replace('\n', '').replace('\r', '').split(";"),
                                                        'file'    : email_name.Attachments.Item(i).FileName.split(";"),
                                                        'receivedTime' : str(email_name.ReceivedTime).split(";")
                                                        }
                                            elif email_name.Attachments.Item(i).FileName == Attachment_File:
                                                email_name.Attachments.Item(i).SaveAsFile(os.path.join(Local_Path,email_name.Attachments.Item(i).FileName)) #下载附件
                                                mail_info={
                                                        'subject' : email_name.Subject.split(";"),
                                                        'sender'  : email_name.SenderName.split(";"),
                                                        'receiver': email_name.To.split(";"),
                                                        'cc'      : email_name.CC.split(";"),
                                                        'content' : email_name.Body.replace('\n', '').replace('\r', '').split(";"),
                                                        'file'    : email_name.Attachments.Item(i).FileName.split(";"),
                                                        'receivedTime' : str(email_name.ReceivedTime).split(";")
                                                        }
                                                break
                                            else:
                                                continue
                                            email_name.Attachments.Item(i).SaveAsFile(os.path.join(Local_Path,email_name.Attachments.Item(i).FileName)) #下载附件
                                            mail_info['file']=file1 #所有附件                                       
                                else:
                                    return("邮件title不能为空！~")  
        return(mail_info)                                              
    except:
        traceback.print_exc()
        sys.exit()
                