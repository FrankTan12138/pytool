**一. 需求样式说明: **

（1）数据需求：将后台发送的司机出行数据按城市名称进行拆分

（2）数据字段：日期、城市、公司、车牌号、姓名、APP在线时长、APP计费时长、DVR在线时长


**二. 数据入库：**

 （1）操作内容：将数据写入Mysql中，按照日期进行分区操作
 
 （2）对应的表名：data_resource.res_driver_outside_report_d

**三. 涉及到脚本&&脚本说明：**

（1）文件涉及到的内容：执行Python脚本、配置文件ini、城市对应的邮箱list

（2）Python脚本：op_excel(对Excel的读写筛选)、op_read_config(读取配置文件ini中间的内容)、op_text(对txt读取文本列表)、op_outside_data_sep.py(对原始数据拆分)、op_outside_data_sep_mail.py(通过邮件将拆分好的数据进行分发)

（3）配置文件（主要分四块：base\mysql\condition\mail,这块内容配置好后，后期不需要进行更改)

（4）城市对应的发送邮箱list(包括两列：城市名称、对应的发送邮箱，中间的分隔符为"\t"，也就是tab键)
