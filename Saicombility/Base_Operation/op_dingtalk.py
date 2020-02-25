#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 调用钉钉推送信息
@author: Frank
@date: 2020/01/18
@ps: https://github.com/zhuifengshen/DingtalkChatbot
'''

#引入模块
from dingtalkchatbot.chatbot import DingtalkChatbot

class dingtalk_chatbot:
    def __init__(self,v_webhook):
        self.webhook=v_webhook
    
    #通过钉钉机器人推送文本信息
    def Dingtalk_text(self,v_msg,v_is_at_all):
        webhook = self.webhook   #WebHook地址
        xiaoding = DingtalkChatbot(webhook)   # 初始化机器人小丁
        xiaoding.send_text(msg=v_msg, is_at_all=v_is_at_all)  # Text消息
        
    #通过钉钉机器人推送link信息
    def Dingtalk_link(self,v_title,v_text,v_message_url,v_pic_url):
        webhook = self.webhook   #WebHook地址
        xiaoding = DingtalkChatbot(webhook)   # 初始化机器人小丁
        xiaoding.send_link(title=v_title, text=v_text, message_url=v_message_url, pic_url=v_pic_url)
    
    #通过钉钉机器人推送Markdown消息   
    def Dingtalk_markdown(self,v_title,v_text,v_is_at_all):
        webhook = self.webhook   #WebHook地址
        xiaoding = DingtalkChatbot(webhook)   # 初始化机器人小丁
        xiaoding.send_markdown(title=v_title, text=v_text,is_at_all=v_is_at_all)

        