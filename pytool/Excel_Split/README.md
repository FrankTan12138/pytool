
# <font size=12>版本V1.0：</font>
**一. 涉及到脚本&&脚本说明**

(1) 文件涉及到的内容：执行Python脚本、配置文件ini

(2) Python脚本：op_excel（对excel的读写筛选）、op_send_mail(通过本地安装的Outlook进行发送邮件),op_read_config(读取配置文件ini中间的内容),op_text(对txt读取文本列表),op_unnormal_income_punish (封装两部分操作：对原始Excel数据的拆分以及通过邮件将拆分好的数据进行分发)

(3)配置ini文件(主要分三块：base\condition\mail,这块内容我配置好，后期不需要进行改变)

(4)邮箱list(包括两列：名称、名称对应的邮箱，中间的分隔符为”\t”，也就是Tab键)

**二. 脚本位置存放说明&&调用方法**

(1) 目录/文件说明：

a. config: 放置的是配置ini文件

b. input:存放的是原始数据目录(XXXXXX.xlsx)

c. output: 拆分完成的结果Excel存放目录

d. run.bat:执行脚本运行的bat文件




## <font size=12>更新方式：</font>

(1) 备份出配置文件driver\_punish\_config.ini和company_list.txt 文件

(2) 解压更新版本后的运营包

(3) 直接覆盖掉原有的程序包，同时将备份的配置文件覆盖掉新的同名配置文件


# <font size=4>版本V1.1：</font>

**一. 修改部分：**

（1) 将原整合拆分excel、发送邮件模块的
op\_unnormal\_income\_punish.py，拆分成两个单独的脚本：Excel\_split\_data.py(拆分excel)、send\_mail\_company.py(发送邮件)

（2）将原整合的执行脚本run.bat，拆分成两个脚本run\_split.bat(拆分excel)、run\_mail.bat(发送邮件)

（3）配置文件driver\_punish\_config.ini优化

（4）修复excel有无标题的选择读取问题

**二. 新增部分：**

（1）配置文件driver_punish\_config.ini中，可以拆分多个sheet，sheet的序号中间由逗号隔开。例如：sheet\_no=0,3 表示拆分第一个和第四个sheet

（2）配置文件ini中，多个sheet的筛选项，筛选项中间由逗号隔开，需注意的是筛选项内容须于sheet\_no的页面对应

（3）新增同一个excel里增加sheet模块，从url下载数据，写入excel模块

# <font size=4>版本V1.2：</font>
**一. 修改部分：**

(1) 将原有的两个脚本run\_split.bat(拆分excel)、run\_mail.bat(发送邮件)中默认转为D盘punish文件下的命令，修改为转到两个脚本当前所处的目录下

(2) 原有最终输出的excel只输出拆分的sheet，修改为修改excel内所有的sheet，不拆分的sheet按照原来的格式进行输出。

**二. 新增部分：**

(1) 新增excel截图模块，支持sheet内容易指定区域进行截屏模块

# <font size=4>版本V1.3：</font>

**一. 新增部分：**

(1) 能跨平台使用的新增excel截图模块，支持sheet内容易指定区域进行截屏模块，原截图模块只能在windows系统上使用

(2) 新增excel输出为office2007之后的xlsx格式功能

(3) 新增读写office2007之后的xlsx格式功能

(4) 新增excel内容转置输出功能

**二. 修改部分：**

(1) 重构部分底层代码，减少代码的冗余

# <font size=4>版本V1.3.1：</font>

**一. 修复部分：**

(1) 修复筛选操作后写入excel只显示最后一条记录的问题

(2) 修复在原有的excel内增加sheet中，默认打开格式xlsx为问题(现默认打开格式为xls)

(3) 修复分割excel配置文件参数与程序代码分割参数不一致的问题，现统一为split_sheet_no
