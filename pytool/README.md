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




## <font size=12>更新方式：</font>

(1) 备份出配置文件driver\_punish\_config.ini和company_list.txt 文件

(2) 解压更新版本后的运营包

(3) 直接覆盖掉原有的程序包，同时将备份的配置文件覆盖掉新的同名配置文件

