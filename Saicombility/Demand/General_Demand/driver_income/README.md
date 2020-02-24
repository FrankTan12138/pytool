**一. 需求样式说明: **

(1) 数据需求：将06司机收入报表(剔除部分字段),通过邮件的形式将Excel发送给租赁公司

(2) 剔除的字段：首次出车时间、首次完单时间、IPH、TPH、OIPH、单均实际接驾里程、指定时段在线时长

**二. 涉及到脚本&&脚本说明：**
(1) 文件涉及到的内容：执行Python脚本、配置文件ini，租赁公司邮箱list

(2) Python脚本：op_mysql（对mysql的读写筛选）、op_excel（对excel的读写筛选）、op_read_config(读取配置文件ini中间的内容),op_text(对txt读取文本列表）、op_driver_income_report_d.py（对mysql数据表拆分）、send_mail_company（通过邮件将拆分好的数据进行分发）

(3) 配置ini文件(主要分四块：base\mysql\condition\mail,这块内容我配置好，后期不需要进行改变) , <font color=red>每个城市对应一个ini文件，文件名称命名后缀加上城市名称拼音，例如杭州市：\_hangzhou</font>

(4)租赁公司邮箱list(包括两列：租赁公司名称、租赁公司名称对应的邮箱，中间的分隔符为”\t”，也就是Tab键),<font color=red>每个城市对应一个txt文件，文件名称命名后缀加上城市名称拼音，例如杭州市：\_hangzhou</font>
