#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
@title: 企业微信推送
@author: Frank
@date: 2020/01/21

'''

#引入模块
import requests
import base64,hashlib

#微信推送机器人
class weixin_chatbot:
#企业微信接口 
    def __init__(self,webhook):
        self.webhook=webhook
        self.headers={'Content-Type': 'application/json;charset=utf-8'}
        
#image
    def send_image(self,os_path,image_name):
    # 图片base64码
        with open(os_path+image_name,"rb") as f:
            base64_data = base64.b64encode(f.read())
    # 图片的md5值
        file = open(os_path+image_name, "rb")
        md = hashlib.md5()
        md.update(file.read())
        res1 = md.hexdigest()
            
    # 信息内容
        data = {
                "msgtype": "image",
                "image": {
                    "base64": base64_data,
                    "md5": res1
                }
            }    

        result = requests.post(self.webhook, headers=self.headers, json=data)
        return(result.text)
    
#markdown
    def send_markdown(self, content):
    #信息内容
        data = {
            "msgtype": "markdown",
            "markdown": {
                        "content": content
                    }
            } 
        result = requests.post(self.webhook, headers=self.headers, json=data) 
        return(result.text)  
    
#news
    def send_news(self,title,description,picurl):
    #信息内容
        data = {
                "msgtype": "news",
                "news": {
                    "articles" : [
                    {
                        "title" : title,
                        "description" : description,
                        "url" : picurl,
                        "picurl" : picurl
                    }
                    ]
                }
               }
        result = requests.post(self.webhook, headers=self.headers, json=data) 
        return(result.text)
#text
    def send_text(self,content,mentioned_list,mentioned_mobile_list):
    #信息内容
        data = {
                "msgtype": "text",
                "text": {
                            "content": content,
                            "mentioned_list": mentioned_list,
                            "mentioned_mobile_list": mentioned_mobile_list
                            }
                } 
        result = requests.post(self.webhook, headers=self.headers, json=data) 
        return(result.text)       