#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 运力达成日报推送
@author: Frank
@date: 2020/02/13

'''
#引入模块
import datetime,time,traceback,sys,os
sys.path.append(r'E:\software\eclipse\workspace\resource')
from op_read_config import read_config
from op_dingtalk import dingtalk_chatbot
# from op_weixin import weixin_chatbot

if __name__ == '__main__':
    os_path=r"D:\Code\para_config\\"
    config_file="dingtalk_complete_report_config.ini"
    
    try:
        para_name=read_config(os_path,config_file) #读取配置信息
    #base参数
        v_date=str(datetime.date.today() - datetime.timedelta(days=int(para_name['base']['v_para_cnt'])))  #获取日期
        city_name_list=para_name['base']['city_name'].split(",")
    #dingtalk参数
        dt_webhook=para_name['dingtalk']['webhook'].format(para_name['dingtalk']['access_token']).replace("\"","")  #api接口
        headers=para_name['dingtalk']['headers']  #headers信息
    #excel部分参数
        excel_path=para_name['excel']['excel_path'] #excel路径
    #weixin部分参数
        wx_webhook=para_name['weixin']['webhook'].format(para_name['weixin']['access_token']).replace("\"","")  #api接口
    #markdwon参数
        title=para_name['markdown']['title']  #title信息
        is_at_all=para_name['markdown']['is_at_all']  #是否@所有人  

        print("=====================\n开始进行操作，操作过程会持续一段时间，请稍后.....")
        dingtalk_chatbot=dingtalk_chatbot(dt_webhook)  #钉钉api接口
#         WeixinChatbot=weixin_chatbot(wx_webhook)   #微信api接口
        for city_name in city_name_list:
            text=para_name['markdown']['text'].format(v_date,city_name,city_name,v_date.replace("-",""),time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))).replace("\\n","\n") #msg信息内容
            picture_name=para_name['excel']['picture_name'].format(city_name,v_date.replace("-","")) #图片名称

#         #微信推送            
#             WeixinChatbot.send_image(excel_path,picture_name+".PNG")
#             print("企业微信推送信息:享道出行-运力达成日报({})_{},执行完成！~".format(city_name,v_date.replace("-","")))
 
        #通过钉钉发送Markdown           
            dingtalk_chatbot.Dingtalk_markdown(title,text,is_at_all)  #推送信息
            print("钉钉推送信息:享道出行-运力达成日报({})_{},执行完成！~".format(city_name,v_date.replace("-","")))

            os.remove(excel_path+picture_name+".PNG")  #删除图片
        print("=====================\n操作结束，界面会在数秒后自动关闭...")
        time.sleep(3)
        
    except:
        traceback.print_exc()
        sys.exit()
