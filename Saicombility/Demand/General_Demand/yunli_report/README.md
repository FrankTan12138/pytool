**<font size=18>日报V1.0</font>**

**一. 数据采集：**

（1）  出行订单报表(运营-订单02)：呼叫订单数、应答率

（2） 司机信息报表(运营-司机04)：有效司机数(当前有效运力)、新增完单司机数、在线司机数、服务封禁、风控封禁、在线率、人均在线时长、人均计费时长、人均完单数、TPH、IPH、人均奖励收入、单均实际接驾时长(分钟)

（3）  司机分层数据报表(运营-司机24): 20单及以上司机数、(10,20）单司机数、(0,10）单司机数

（4） 司机收入报表(运营-司机06)：完单司机数[需要通过完单数加工]

**二. 指标数据加工：**

（1）出行订单数据(运营-订单02)：取出字段日期、城市名称、呼叫订单数、应答率。限制条件车型为汇总、平台为汇总，时间选择T和T-7做同比。

```sql
set @v_acct_day='2020-01-02';

-- 运营-订单 02-出行订单报表
drop table if exists data_tempdb.tmp_capacity_health_report_d01;
create table data_tempdb.tmp_capacity_health_report_d01 as
select t.day_id,t.city_name,t.call_num_d,t.response_rate
from data_resource.res_travel_order_report_d t
where t.car_level='汇总' and t.platform_name='汇总' and t.day_id=@v_acct_day
union all
select t.day_id,t.city_name,t.call_num_d,t.response_rate
from data_resource.res_travel_order_report_d t
where t.car_level='汇总' and t.platform_name='汇总' and t.day_id=date_add(@v_acct_day,interval -7 day);
```
（2） 司机信息报表(运营-司机04)：取出字段有效司机数(当前有效运力)、新增完单司机数、在线司机数、服务封禁、风控封禁、在线率、人均在线时长、人均计费时长、人均完单数、TPH、IPH、人均奖励收入、单均实际接驾时长(分钟)，并且关联在02出行订单取数的表上。限制的条件车型为汇总，时间选择T和T-7做同比
```sql
-- 运营-司机 04-司机信息报表
drop table if exists data_tempdb.tmp_capacity_health_report_d02;
create table data_tempdb.tmp_capacity_health_report_d02 as
select t.*,t1.eff_driver_num,t1.na_comp_order_driver_num,t1.online_driver_num,t1.serv_forb_num,t1.col_forb_num,
t1.online_driver_rate,t1.avg_driver_online_dt,t1.avg_driver_income_dt,t1.avg_comp_order_driver_num,t1.tph,t1.iph,
t1.avg_driver_reward_income,t1.avg_act_dt
from data_tempdb.tmp_capacity_health_report_d01 t
left join (select t1.day_id,t1.city_name,t1.eff_driver_num,
t1.na_comp_order_driver_num ,t1.online_driver_num,t1.serv_forb_num,t1.col_forb_num,
concat(round(t1.online_driver_rate*100,1),'%') online_driver_rate,round(t1.avg_driver_online_dt,2)  avg_driver_online_dt,
round(t1.avg_driver_income_dt,2) avg_driver_income_dt,round(t1.avg_comp_order_driver_num,2) avg_comp_order_driver_num,
round(t1.tph,2) tph,round(t1.iph,2) iph,round(t1.avg_driver_reward_income,2)  avg_driver_reward_income,round(t1.avg_act_dt,2) avg_act_dt
from data_resource.res_driver_info_report_d t1
where t1.day_id=@v_acct_day and t1.car_level='汇总'
union all 
select t1.day_id,t1.city_name,t1.eff_driver_num,
t1.na_comp_order_driver_num ,t1.online_driver_num,t1.serv_forb_num,t1.col_forb_num,
concat(round(t1.online_driver_rate*100,1),'%') online_driver_rate,round(t1.avg_driver_online_dt,2)  avg_driver_online_dt,
round(t1.avg_driver_income_dt,2) avg_driver_income_dt,round(t1.avg_comp_order_driver_num,2) avg_comp_order_driver_num,
round(t1.tph,2) tph,round(t1.iph,2) iph,round(t1.avg_driver_reward_income,2)  avg_driver_reward_income,round(t1.avg_act_dt,2) avg_act_dt
from data_resource.res_driver_info_report_d t1
where t1.day_id=date_add(@v_acct_day,interval -7 day) and t1.car_level='汇总') t1
on t.day_id=t1.day_id and t.city_name=t1.city_name;
```

（3）司机分层数据报表(运营-司机24)：取出字符20单及以上司机数、(10,20）单司机数、(0,10）单司机数，关联上02出行订单和04司机信息所取出的字段。限制条件时间选择T和T-7做同比。
```sql
-- 运营-司机 24 司机分层数据报表
drop table if exists data_tempdb.tmp_capacity_health_report_d03;
create table data_tempdb.tmp_capacity_health_report_d03 as
select t.*,t1.twenty_plus_comp_driver_num,t1.ten_twenty_comp_driver_num,t1.zero_ten_comp_driver_num
from data_tempdb.tmp_capacity_health_report_d02 t
left join (select t1.day_id,t1.city_name,
ifnull(sum(case when t1.driver_level='0单' then t1.driver_cnt end),0) zero_comp_driver_num,
ifnull(sum(case when t1.driver_level='(0,10)单' then t1.driver_cnt end),0) zero_ten_comp_driver_num,
ifnull(sum(case when t1.driver_level='[10,20)单' then t1.driver_cnt end),0) ten_twenty_comp_driver_num,
ifnull(sum(case when t1.driver_level='20单及以上' then t1.driver_cnt end),0) twenty_plus_comp_driver_num
from data_resource.res_driver_classfic_info_report_d t1
where t1.day_id=@v_acct_day
group by t1.day_id,t1.city_name
union all
select t1.day_id,t1.city_name,
ifnull(sum(case when t1.driver_level='0单' then t1.driver_cnt end),0) zero_comp_driver_num,
ifnull(sum(case when t1.driver_level='(0,10)单' then t1.driver_cnt end),0) zero_ten_comp_driver_num,
ifnull(sum(case when t1.driver_level='[10,20)单' then t1.driver_cnt end),0) ten_twenty_comp_driver_num,
ifnull(sum(case when t1.driver_level='20单及以上' then t1.driver_cnt end),0) twenty_plus_comp_driver_num
from data_resource.res_driver_classfic_info_report_d t1
where t1.day_id=date_add(@v_acct_day,interval -7 day)
group by t1.day_id,t1.city_name) t1
on t.day_id=t1.day_id and t.city_name=t1.city_name;
```
（4） 完单司机数加工，从06司机收入表里进行汇总，城市中苏州市、昆山市合并成苏州市。同时对城市名称进行排序，排序规则以模板为准。
```sql
-- 运营-司机 06司机收入报表
drop table if exists data_tempdb.tmp_capacity_health_report_d04;
create table data_tempdb.tmp_capacity_health_report_d04 as
select t.*,t1.comp_order_driver_num,
case when t.city_name='全国' then 1 
when t.city_name='上海市' then 2
when t.city_name='苏州市' then 3
when t.city_name='郑州市' then 4
when t.city_name='杭州市' then 5
when t.city_name='宁波市' then 6 end  city_order
from data_tempdb.tmp_capacity_health_report_d03 t
left join(select t1.day_id,case when t1.city_name in ('昆山市','苏州市') then '苏州市' else t1.city_name end city_name,
sum(case when t1.comp_order_num>0 then 1 else 0 end) comp_order_driver_num
from data_resource.res_driver_income_report_d t1
where t1.day_id=v_acct_day
group by t1.day_id,case when t1.city_name in ('昆山市','苏州市') then '苏州市' else t1.city_name end
union all
select t1.day_id,'全国' city_name,sum(case when t1.comp_order_num>0 then 1 else 0 end) comp_order_driver_num
from data_resource.res_driver_income_report_d t1
where t1.day_id=@v_acct_day
group by t1.day_id
union all
select t1.day_id,case when t1.city_name in ('昆山市','苏州市') then '苏州市' else t1.city_name end city_name,
sum(case when t1.comp_order_num>0 then 1 else 0 end) comp_order_driver_num
from data_resource.res_driver_income_report_d t1
where t1.day_id=date_add(@v_acct_day,interval -7 day)
group by t1.day_id,case when t1.city_name in ('昆山市','苏州市') then '苏州市' else t1.city_name end
union all
select t1.day_id,'全国' city_name,sum(case when t1.comp_order_num>0 then 1 else 0 end) comp_order_driver_num
from data_resource.res_driver_income_report_d t1
where t1.day_id=date_add(@v_acct_day,interval -7 day)
group by t1.day_id) t1
on t.day_id=t1.day_id and t.city_name=t1.city_name;
```
（5） 数据保存到最终表里，并且增加更新时间
```sql
-- report
alter table data_report.dm_capacity_health_report_d add partition (partition p_20200103 values in ('2020-01-03'));
insert into data_report.dm_capacity_health_report_d
select t.*,DATE_FORMAT(now(),'%x-%m-%d') update_time
from data_tempdb.tmp_capacity_health_report_d03  t 
order by city_order;
```

**三. Excel表格展示处理：**

（1)  将最终表的数据复制出来，并且进行转置，去掉更新时间、日期、城市名称后复制到Excel模板的input(sheet名称)中。

（2）模板的数据会进行自动的二次加工，生成最终的展示的模板。最终模板添加上同比数据。

**四. 涉及到脚本&&脚本说明：**

（1）文件涉及到的内容：除了上述计算运行的存储过程外，还有执行Python脚本、配置文件ini

（2）Python脚本：op_excel(对Excel的读写筛选)、op_read_config(读取配置文件ini中间的内容)、op_text(对txt读取文本列表)、op_mysql(对mysql的操作)、op_country_yunli_daily_screen.py(将计算完成的数据按规范写入excel并且进行截图上传至阿里云)、op_country_yunli_daily_mail.py(将excel按照城市对应的邮箱进行发送以及钉钉推送)

（3） 配置文件（主要分六块：base\condition\mysql\aliyun\dingtalk\mail,这块内容配置好后，后期不需要进行更改)

**五. 发送邮件：**

（1）将Excel模板整体copy到新的Excel里

（2）将新Excel命名为享道运力经营报表\_20200102,并将其作为附件发送给王焱、李小龙、周曦炜、徐顺杰、张承喻、金艳

**六. 封装脚本/存储过程：**

（1）存储过程：data_report.dm_capacity_health_report_d

（2）调用方式：call data_report.sp_dm_capacity_health_report_d('2020-01-02');


**<font size=6>日报V1.1</font>**

**一. 修改部分**

（1）完单司机数：修改为统计周7天完单司机数的均值，原口径为统计周有完单的司机(去重)数值。

 ```sql
 drop table if exists data_tempdb.tmp_capacity_health_report_w04;
 create table data_tempdb.tmp_capacity_health_report_w04 as
 select t.*,t1.comp_order_driver_num,
 case when t.city_name='全国' then 1 
 when t.city_name='上海市' then 2
 when t.city_name='苏州市' then 3
 when t.city_name='郑州市' then 4
 when t.city_name='杭州市' then 5
 when t.city_name='宁波市' then 6 end  city_order
 from data_tempdb.tmp_capacity_health_report_w03 t
 left join(select v_this_week week_id,t1.city_name,round(avg(t1.comp_driver_num),0) comp_order_driver_num
from data_resource.res_driver_info_report_d t1
where t1.day_id>=v_start_week and t1.day_id<=v_end_week
group by t1.city_name) t1
on t.week_id=t1.week_id and t.city_name=t1.city_name;
 ```


**<font size=6>周报V1.0</font>**


**一. 数据采集：**

（1）  出行订单报表(运营-订单02)：呼叫订单数、应答率

（2） 司机信息报表(运营-司机04)：有效司机数(当前有效运力)、新增完单司机数、在线司机数、服务封禁、风控封禁、在线率、人均在线时长、人均计费时长、人均完单数、TPH、IPH、人均奖励收入、单均实际接驾时长(分钟)

（3）  司机分层数据报表(运营-司机24): 20单及以上司机数、(10,20）单司机数、(0,10）单司机数

（4） 司机收入报表(运营-司机06)：完单司机数[需要通过完单数加工]

**二. 指标数据加工：**

（1）出行订单数据(运营-订单02)：取出字段日期、城市名称、呼叫订单数、应答率，数值七天均取均值。限制条件车型为汇总、平台为汇总，时间选择T周和T-1周做环比。

```sql
-- 运营-订单 02-出行订单报表
set @v_acct_day='2020-01-01'；
set @v_start_week=DATE_SUB(v_acct_day,interval WEEKDAY(v_acct_day) day);   -- 统计周周一
set @v_end_week=DATE_ADD(@v_start_week,interval 6 day); -- 统计周周日
set @v_this_week=DATE_FORMAT(@v_start_week,'%x%v');
set @v_last_week=DATE_FORMAT(DATE_ADD(@v_start_week, interval -1 day),'%x%v');  -- 统计周上一周

drop table if exists data_tempdb.tmp_capacity_health_report_w01;
create table data_tempdb.tmp_capacity_health_report_w01 as
select v_this_week week_id,t.city_name,round(avg(t.call_num_d),0) call_num_w,concat(round(avg(replace(t.response_rate,"%","")),2),'%') response_rate_w
from data_resource.res_travel_order_report_d t
where t.car_level='汇总' and t.platform_name='汇总' 
and t.day_id>=@v_start_week and t.day_id<=@v_end_week
group by t.city_name;
```
（2） 司机信息报表(运营-司机04)：取出字段有效司机数(当前有效运力)、新增完单司机数、在线司机数、服务封禁、风控封禁、在线率、人均在线时长、人均计费时长、人均完单数、TPH、IPH、人均奖励收入、单均实际接驾时长(分钟)七天数据取均值，并且关联在02出行订单取数的表上。限制的条件车型为汇总，时间选择T周和T-1周做环比

```sql
-- 运营-司机 04-司机信息报表
drop table if exists data_tempdb.tmp_capacity_health_report_w02;
create table data_tempdb.tmp_capacity_health_report_w02 as
select t.*,t1.online_driver_num_w,t1.eff_driver_num_w,t1.na_comp_order_driver_num_w,t1.serv_forb_num_w,t1.col_forb_num_w,
t1.online_driver_rate_w,t1.avg_driver_online_dt_w,t1.avg_driver_income_dt_w,t1.avg_comp_order_driver_num_w,t1.tph_w,t1.iph_w,
t1.avg_driver_reward_income_w,t1.avg_act_dt_w
from data_tempdb.tmp_capacity_health_report_w01 t
left join (select @v_this_week week_id,t1.city_name,round(avg(t1.eff_driver_num),0) eff_driver_num_w,
round(avg(t1.na_comp_order_driver_num),0) na_comp_order_driver_num_w,round(avg(t1.online_driver_num),0) online_driver_num_w,round(avg(t1.serv_forb_num),0) serv_forb_num_w ,round(avg(t1.col_forb_num),2) col_forb_num_w,
concat(round(avg(t1.online_driver_rate)*100,1),'%') online_driver_rate_w,round(avg(t1.avg_driver_online_dt),2)  avg_driver_online_dt_w,
round(avg(t1.avg_driver_income_dt),2) avg_driver_income_dt_w,round(avg(t1.avg_comp_order_driver_num),2) avg_comp_order_driver_num_w,
round(avg(t1.tph),2) tph_w,round(avg(t1.iph),2) iph_w,round(avg(t1.avg_driver_reward_income),2)  avg_driver_reward_income_w,round(avg(t1.avg_act_dt),2) avg_act_dt_w
from data_resource.res_driver_info_report_d t1
where t1.day_id>=@v_start_week and t1.day_id<=@v_end_week and t1.car_level='汇总'
group by t1.city_name) t1
on t.week_id=t1.week_id and t.city_name=t1.city_name;
```
（3）司机分层数据报表(运营-司机24)：取出字符20单及以上司机数、(10,20）单司机数、(0,10）单司机数，关联上02出行订单和04司机信息所取出的字段。限制条件时间选择T周和T-1周做环比。
```sql
-- 运营-司机 24 司机分层数据报表
drop table if exists data_tempdb.tmp_capacity_health_report_w03;
create table data_tempdb.tmp_capacity_health_report_w03 as
select t.*,t1.twenty_plus_comp_driver_num,t1.ten_twenty_comp_driver_num,t1.zero_ten_comp_driver_num
from data_tempdb.tmp_capacity_health_report_w02 t
left join (select v_this_week week_id,t1.city_name,
ifnull(round(avg(case when t1.driver_level='0单' then t1.driver_cnt end),0),0) zero_comp_driver_num,
ifnull(round(avg(case when t1.driver_level='(0,10)单' then t1.driver_cnt end),0),0) zero_ten_comp_driver_num,
ifnull(round(avg(case when t1.driver_level='[10,20)单' then t1.driver_cnt end),0),0) ten_twenty_comp_driver_num,
ifnull(round(avg(case when t1.driver_level='20单及以上' then t1.driver_cnt end),0),0) twenty_plus_comp_driver_num
from data_resource.res_driver_classfic_info_report_d t1
where t1.day_id>=@v_start_week  and t1.day_id<=@v_end_week
group by t1.city_name) t1
on t.week_id=t1.week_id and t.city_name=t1.city_name;
```
（4） 完单司机数加工，从06司机收入表里进行汇总，城市中苏州市、昆山市合并成苏州市。同时对城市名称进行排序，排序规则以模板为准。
```sql
-- 运营-司机 06司机收入报表
drop table if exists data_tempdb.tmp_capacity_health_report_w04;
create table data_tempdb.tmp_capacity_health_report_w04 as
select t.*,t1.comp_order_driver_num,
case when t.city_name='全国' then 1 
when t.city_name='上海市' then 2
when t.city_name='苏州市' then 3
when t.city_name='郑州市' then 4
when t.city_name='杭州市' then 5
when t.city_name='宁波市' then 6 end  city_order
from data_tempdb.tmp_capacity_health_report_w03 t
left join(select v_this_week week_id,case when t1.city_name in ('昆山市','苏州市') then '苏州市' else t1.city_name end city_name,
count(distinct t1.driver_id) comp_order_driver_num
from data_resource.res_driver_income_report_d t1
where t1.day_id>=@v_start_week  and t1.day_id<=@v_end_week
and t1.comp_order_num>0
group by case when t1.city_name in ('昆山市','苏州市') then '苏州市' else t1.city_name end
union all
select v_this_week week_id,'全国' city_name,count(distinct t1.driver_id) comp_order_driver_num
from data_resource.res_driver_income_report_d t1
where t1.day_id>=@v_start_week  and t1.day_id<=@v_end_week
and t1.comp_order_num>0) t1
on t.week_id=t1.week_id and t.city_name=t1.city_name;
```
（5） 数据保存到最终表里，并且增加更新时间
```sql
--  report
insert into data_report.dm_capacity_health_report_week
select t.*,DATE_FORMAT(now(),'%x-%m-%d') update_time
from data_tempdb.tmp_capacity_health_report_w04  t 
order by city_order;
commit;

-- 输出表
drop table if exists data_report.dm_capacity_health_report_week_output;
create table data_report.dm_capacity_health_report_week_output as
select t.*
from data_report.dm_capacity_health_report_week t
where t.week_id in (v_this_week,v_last_week);
```
**三. Excel表格展示处理：**
（1)  将最终表的数据复制出来，并且进行转置，去掉更新时间、日期、城市名称后复制到Excel模板的input(sheet名称)中。

（2）模板的数据会进行自动的二次加工，生成最终的展示的模板。最终模板添加上同比数据。

（2）模板的数据会进行自动的二次加工，生成最终的展示的模板。最终模板添加上同比数据。


**四. 涉及到脚本&&脚本说明：**

（1）文件涉及到的内容：除了上述计算运行的存储过程外，还有执行Python脚本、配置文件ini

（2）Python脚本：op_excel(对Excel的读写筛选)、op_read_config(读取配置文件ini中间的内容)、op_text(对txt读取文本列表)、op_mysql(对mysql的操作)、op_country_yunli_week_screen.py(将计算完成的数据按规范写入excel并且进行截图上传至阿里云)、op_country_yunli_week_mail.py(将excel按照城市对应的邮箱进行发送以及钉钉推送)

（3） 配置文件（主要分六块：base\condition\mysql\aliyun\dingtalk\mail,这块内容配置好后，后期不需要进行更改)

**五. 发送邮件：**
（1）将Excel模板整体copy到新的Excel里

（2）将新Excel命名为享道运力经营报表\_202001,并将其作为附件发送给李小龙、黄鹏飞

**六. 封装脚本/存储过程：**

（1）存储过程：data_report.dm_capacity_health_report_week

（2）调用方式：call data_report.sp_dm_capacity_health_report_week('2020-01-01');