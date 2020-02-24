**一. 数据样式**

(1)拆分需求：将上海司机神访分统计、线上神访数据汇总（供租赁公司反查核实）、线下神访数据汇总，按照租赁公司名称这三个sheet进行拆分

(2)发送对象：各租赁公司的接口邮箱(sf_company_list.txt)

**二. 拆分操作**

(1) 预操作：将龙菁/卢寒发送的神访结果从邮件上下载到D:\神访分结果\下，然后在Excel里进行如下的操作：

[1] sheet-上海司机神访分统计:删除A列，A1:H2的单元格(租赁公司的神访分可能出现读取时错误，建议数值复制粘贴一次)

[2] sheet-线上神访数据汇总（供租赁公司反查核实）:删除第1-第6行、删除D-H列

[3] sheet-线下神访数据汇总:第2-4行

(2) 拆分过程：
[1] sheet-上海司机神访分统计:拆分成两个sheet，上海司机神访分统计(汇总)、上海司机神访分统计(清单)

[2] sheet-线上神访数据汇总（供租赁公司反查核实）:拆分成线上神访数据汇总（供租赁公司反查核实）

[3] sheet-线下神访数据汇总: 拆分成sheet-线下神访数据汇总

(3) 脚本说明

[1] 代码名称：op_exp_sfresult_excel.py

[2] 配置文件：sf_driver_result_config.ini(参数配置)、sf_company_list.txt(租赁公司名称、邮箱清单)

[3] 拆分代码：
```python
        para_name=read_config(os_path,config_file) #读取配置信息
        #根据列表清单对源表数据进行excel拆分
        print("文件名称：{}".format(os_path+para_name['base']['file_name']))
                
        for write_filenames in read_txt(os_path,str(para_name['condition']['list_name'])+".txt"):
            write_filename=write_filenames.split("\t")[0]
             
            print("开始操作：{}-{}".format(write_filename,'上海司机神访分统计（汇总）'))
            data_info=read_excel_dict(para_name['base']['input_path'], para_name['base']['file_name'],int(para_name['base']['sheet_no3']),para_name['base']['title_no'],para_name['base']['order_list'],0,77,8,19)
            data_result(data_info,para_name['base']['output_path'],write_filename,para_name['base']['write_sheet_name4'])
                 
            print("开始操作：{}-{}".format(write_filename,'上海司机神访分统计(清单)'))
            data_info=read_excel(para_name['base']['input_path'], para_name['base']['file_name'],int(para_name['base']['sheet_no3']),para_name['base']['title_no'],para_name['base']['order_list'])  #读取excel数据
            data_result=data_dict_filter(os_path,config_file,data_info,para_name['base']['title_no'],len(data_info),para_name['condition']['row_start'],para_name['condition']['row_end'],write_filename)  #数据筛选
            add_sheet(para_name['base']['output_path'],write_filename,para_name['base']['write_sheet_name3'],para_name['base']['title_no'],data_result)
               
            print("开始操作：{}-{}".format(write_filename,'线上神访数据汇总（供租赁公司反查核实）'))
            data_info=read_excel(para_name['base']['input_path'], para_name['base']['file_name'],int(para_name['base']['sheet_no2']),para_name['base']['title_no'],para_name['base']['order_list'])  #读取excel数据
            data_result=data_filter(os_path,config_file,data_info,para_name['base']['title_no'],len(data_info),write_filename)  #数据筛选
            add_sheet(para_name['base']['output_path'],write_filename,para_name['base']['write_sheet_name2'],para_name['base']['title_no'],data_result)
               
            print("开始操作：{}-{}".format(write_filename,'线下神访数据汇总'))
            data_info=read_excel(para_name['base']['input_path'], para_name['base']['file_name'],int(para_name['base']['sheet_no']),para_name['base']['title_no'],para_name['base']['order_list'])  #读取excel数据
            data_result=data_filter(os_path,config_file,data_info,para_name['base']['title_no'],len(data_info),write_filename)  #数据筛选
            add_sheet(para_name['base']['output_path'],write_filename,para_name['base']['write_sheet_name'],para_name['base']['title_no'],data_result)
              
            time.sleep(3)  #暂停3秒
			
        #发送邮件
            receiver_mail=write_filenames.split("\t")[1]
            print("发送给租赁公司：{}        对应邮箱：{}".format(write_filename,receiver_mail))
            print(para_name['mail']['mail_title'])
            send_mail(para_name['mail']['host_server'],para_name['mail']['host_port'],para_name['mail']['user_name'],para_name['mail']['password'],para_name['mail']['sender'],receiver_mail,para_name['mail']['cc'],para_name['mail']['mail_title'],para_name['mail']['mail_content'],para_name['mail']['attachment_img'],para_name['mail']['attachment_txt'],para_name['mail']['attachment_pdf'],para_name['base']['output_path']+write_filename+".xls",para_name['mail']['attachment_word'])
```

(4) 拆分结果：

[1] 输出路径：D:\神访分结果\output\

