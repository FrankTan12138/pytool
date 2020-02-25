#!/usr/bin/env python
# -*- coding: UTF-8 -*-


'''
@title: 压缩文件
@author: Frank
@date: 2019/10/29

'''
#引入模块
# import zipfile #引入zip管理模块
import paramiko
import os,sys
from urllib.request import urlopen
import requests
from tqdm import tqdm

#下载文件
def download_from_url(url, dst):
    file_size = int(urlopen(url).info().get('Content-Length', -1))
    
#支持断点续下
    if os.path.exists(dst):  
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size

#sftp操作
class op_sftp:
    def __init__(self,host_ip,port,username,password):
            self.host_ip=host_ip
            self.port=port
            self.username=username
            self.password=password

            
    #连接sftp
    def sftp_connect(self):
        try:
            client = paramiko.Transport((self.host_ip,int(self.port)))
            client.connect(username=self.username,password=self.password)
            sftp = paramiko.SFTPClient.from_transport(client)
        except Exception as e:
            print (e)
            sys.exit(1)
        return(sftp)

        
    
    #get下载
    def sftp_get(self,local_path,local_file,remote_path,remote_file):
        try:
            print("开始下载文件：{}".format(local_path+local_file))
            sftp=op_sftp.sftp_connect(self)  #连接sftp
        # 判断远程服务器是否有这个文件
            sftp.file(remote_path+remote_file)
        # 使用get()方法从远程服务器拉去文件
            sftp.get(remote_path+remote_file, local_path+local_file)       
        except IOError as e:
            print (e)
            sys.exit(1)
        finally:
            sftp.close()
        # 测试是否下载成功
        if os.path.isfile(local_path+local_file):
            print("{}下载：success".format(local_path+local_file))
        else:
            print("{}下载：fail".format(local_path+local_file))
        
    #put上传
    def sftp_put(self,local_path,local_file,remote_path,remote_file):
        print("开始上传文件：{}".format(local_path+local_file))
        sftp=op_sftp.sftp_connect(self)  #连接sftp
        # 使用put()方法把本地文件上传到远程服务器
        sftp.put(localpath=local_path+local_file,remotepath=remote_path+remote_file)
        # 测试是否上传成功
        for remote_file1 in sftp.listdir(remote_path):             
            if remote_file == remote_file1:
                print ("{}上传：success".format(local_path+local_file))
        sftp.close()
