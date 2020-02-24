**一. 数据模块：**司机高中低频沉默无完单月汇总数据、司机高中低频沉默无完单月清单数据

**二. 汇总数据：**统计自然月的高中低频的汇总数据

(1) 加工涉及代码：
```sql
/*设置参数*/
	set @v_acct_day='201901';
	set @v_start_day=cast(concat(@v_acct_day,'01') as date);
	set @v_end_day=last_day(@v_start_day);
	
/*汇总数据*/
	delete from data_report.dm_driver_comp_order_sign_m where month_id=@v_acct_day;	
	insert into data_report.dm_driver_comp_order_sign_m
	select substr(replace(t.day_id,'-',''),1,6) month_id,t.city_name,t.comp_order_sign,count(*) comp_order_sign_cnt
	from(select t.*,case when t.total_comp_order_num>=400 then '高频'
	when t.total_comp_order_num<400 and t.total_comp_order_num>=200 then '中频'
	when t.total_comp_order_num<200 and t.total_comp_order_num>=50 then '低频'
	when t.total_comp_order_num>0 and t.total_comp_order_num<50 then '沉默'
	when t.total_comp_order_num=0 then '无完单' end comp_order_sign
	from (select @v_acct_day day_id,t.city_name,t.driver_id,sum(t.comp_order_num) total_comp_order_num
	from data_resource.res_driver_income_report_d t
	where t.day_id>=@v_start_day and t.day_id<=@v_end_day
	group by t.city_name,t.driver_id) t )t
	group by substr(replace(t.day_id,'-',''),1,6),t.city_name,t.comp_order_sign;
```
(2) **数据表名称：**data_report.dm_driver_comp_order_sign_m

**三. 清单数据：**司机在自然月的标签清单

(1)  **加工涉及代码：**
```sql
-- 插入新的司机
drop table if exists data_tempdb.tmp_driver_person_comp_order_sign_m01;
create table data_tempdb.tmp_driver_person_comp_order_sign_m01 as
select distinct t.city_name,t.driver_id
from data_report.dm_driver_person_comp_order_sign_m t
union all
select t.city_name,t.driver_id
from  (select t.driver_id,t.city_name
from data_mid.mid_driver_person_comp_order_sign_m t
where t.month_id=@v_acct_day) t
where not exists(select t1.driver_id,t1.city_name
from data_report.dm_driver_person_comp_order_sign_m t1
where t.city_name=t1.city_name and t.driver_id=t1.driver_id);

-- 增加标签
drop table if exists data_tempdb.tmp_driver_person_comp_order_sign_m02;
create table data_tempdb.tmp_driver_person_comp_order_sign_m02 as
select t.*,t1.comp_order_sign m01
from data_tempdb.tmp_driver_person_comp_order_sign_m01 t
left join (select t1.city_name,t1.driver_id,t1.comp_order_sign
from data_mid.mid_driver_person_comp_order_sign_m t1
where t1.month_id=@v_acct_day) t1
on t.city_name=t1.city_name and t.driver_id=t1.driver_id;

-- 关联上新标签
drop table if exists data_tempdb.tmp_driver_person_comp_order_sign_m03;
create table data_tempdb.tmp_driver_person_comp_order_sign_m03 as
select t.*,t1.m01
from data_report.dm_driver_person_comp_order_sign_m t
left join data_tempdb.tmp_driver_person_comp_order_sign_m02 t1
on t.city_name=t1.city_name and t.driver_id=t1.driver_id;

--替换掉原来的表
drop table if exists data_report.dm_driver_person_comp_order_sign_m;
create table data_report.dm_driver_person_comp_order_sign_m as
select t.*
from data_tempdb.tmp_driver_person_comp_order_sign_m03 t;
```
(2) **数据表名称：**data_report.dm_driver_person_comp_order_sign_m(当年数据)、data_report.dm_driver_person_comp_order_sign_y（历年数据）

(3) **调用方式：** call sp_dm_driver_comp_order_sign_m('201901')

**四. 涉及到脚本&&脚本说明：**

(1) 文件涉及到的内容：除了上述计算运行的存储过程外，还有执行Python脚本、配置文件ini、城市对应的邮箱list

(2) Python脚本：op_excel(对Excel的读写筛选)、op_read_config(读取配置文件ini中间的内容)、op_text(对txt读取文本列表)、op_mysql(对mysql的操作)、op_driver_comp_order_sign.py(将计算完成的数据按规范写入excel)、op_driver_comp_order_sign_mail.py(将excel按照城市对应的邮箱进行发送)

(3) 配置文件（主要分四块：base\condition\mysql\mail,这块内容配置好后，后期不需要进行更改)

(4) 城市对应的发送邮箱list(包括两列：城市名称、对应的发送邮箱，<font color=red>中间的分隔符为”\t”</font>，也就是tab键)

**五. 注意事项：** 

(1) 中间表分区事项：dm_driver_comp_order_sign_m(全量汇总数据)、mid_driver_person_comp_order_sign_m(个体完单数据中间表)
当data_resource.res_driver_income_report_d(司机收入表)有新增城市时候，需要添加对应的城市分区。下面以宁波市为例：

```sql
-- 新增宁波市分区
alter table data_report.dm_driver_comp_order_sign_m add partition(partition p_ningbo values in ('宁波市'));
alter table data_mid.mid_driver_person_comp_order_sign_m add partition(partiion p_ningbo values in ('宁波市'));
```
