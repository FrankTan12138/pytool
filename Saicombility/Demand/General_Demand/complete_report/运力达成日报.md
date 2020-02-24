**一. 数据采集**

（1）指标采集：统计日、星期、城市名称、呼叫订单数、完单数、完单率、在线司机数、在线率、完单司机数、人均完单数、呼叫数/在线数、享道应答率、总应答率

（2）采集方式：当前数据出口为FastBi和风行大数据门户对应的两张报表数据。
```
<1> 运营-订单：02出行订单报表
<2> 运营-司机：04司机信息报表
```

**二. 指标数据加工**

（1）指标说明：

| 编号 | 指标名称    | 指标计算        | 来源表 |
|----|---------|-------------|-----|
| 1  | 统计日     |||
| 2  | 星期      |||
| 3  | 城市名称   | | 04司机信息表     |
| 4  | 呼叫订单数  | | 02出行订单报表    |
| 5  | 完单数    | | 02出行订单报表    |
| 6  | 完单率    | | 02出行订单报表    |
| 7  | 在线司机数  | | 04司机信息表     |
| 8  | 在线率     || 04司机信息表     |
| 9  | 完单司机数  | | 02出行订单报表    |
| 10 | 人均完单数   | 完单数/完单司机数   ||
| 11 | 呼叫数/在线数 | 呼叫订单数/在线司机数 ||
| 12 | 享道应答率   || 02出行订单报表    |
| 13 | （总）应答率  || 02出行订单报表    |

(2) 统计周期：
- 统计时间段：每天统计，周日的数据需要计算出本周均值和本周环比
- 发送时间：每天早上9点左右发出

(3) 日数据加工逻辑：
```sql
set @v_acct_day='2020-02-09';  -- 统计日
set @week_id=Date_Format(@v_acct_day,'%w');  -- 统计日为周几
set @v_start_week=DATE_SUB(@v_acct_day,interval WEEKDAY(@v_acct_day) day);  -- 统计周周一
set @v_end_week=DATE_ADD(@v_start_week,interval 6 day); -- 统计周周日
set @v_last_week=DATE_FORMAT(DATE_ADD(@v_start_week, interval -1 day),'%x年第%v周');  -- 统计周上一周
set @v_this_week=DATE_FORMAT(@v_start_week,'%x年第%v周');  -- 这周周数

-- 04 司机信息表
drop table if exists data_tempdb.tmp_driver_complete_report_d01;
create table data_tempdb.tmp_driver_complete_report_d01 as
select t.day_id,case when @week_id='0' then '日' 
when @week_id='1' then '周一'
when @week_id='2' then '周二'
when @week_id='3' then '周三' 
when @week_id='4' then '周四'  
when @week_id='5' then '周五' 
when @week_id='6' then '周六'  end week_id,t.city_name,
t.online_driver_num,t.comp_driver_num,t.online_driver_rate
from (select t.day_id,t.city_name,t.online_driver_num,t.comp_driver_num,concat(round(100*t.online_driver_rate,1),'%') online_driver_rate
from data_resource.res_driver_info_report_d t
where t.day_id=@v_acct_day
and t.car_level='汇总') t;

-- 02 出行订单表
alter table data_report.dm_driver_complete_report_d truncate partition p_20200211;
insert into data_report.dm_driver_complete_report_d
select t.day_id,t.week_id,t.city_name,t1.call_num_d,t1.comp_order_num,t1.comp_order_rate,t.online_driver_num,t.online_driver_rate,t.comp_driver_num,round(t1.comp_order_num/t.comp_driver_num,1) avg_comp_order_num,
round(t1.call_num_d/t.online_driver_num,1) call_online_per,t2.xd_response_rate,t1.response_rate
from data_tempdb.tmp_driver_complete_report_d01 t
left join (select t1.day_id,t1.city_name,t1.call_num_d,t1.comp_order_num,t1.response_rate,t1.comp_order_rate
from data_resource.res_travel_order_report_d t1
where t1.day_id=@v_acct_day and t1.car_level='汇总' and t1.platform_name='汇总') t1
on t.day_id=t1.day_id and t.city_name=t1.city_name
left join (select t2.day_id,t2.city_name,t2.response_rate xd_response_rate
from data_resource.res_travel_order_report_d t2
where t2.day_id=@v_acct_day and t2.car_level='汇总' and t2.platform_name='享道') t2
on t.day_id=t2.day_id and t.city_name=t2.city_name;
commit;
```
(4) 均值、环比数据加工逻辑
```sql
-- 周汇总数据
insert into  data_report.dm_driver_complete_report_w 
select @v_this_week week_id,'本周日均' sign,t.city_name,round(avg(t.call_num_d),2) call_num_d,round(avg(t.comp_order_num),2) comp_order_num,
concat(round(avg(replace(t.comp_order_rate,'%','')),2),'%') comp_order_rate,round(avg(t.online_driver_num),2) online_driver_num,concat(round(avg(replace(t.online_driver_rate,'%','')),2),'%') online_driver_rate,
round(avg(t.comp_driver_num),2) comp_driver_num,round(avg(t.avg_comp_order_num),2) avg_comp_order_num,
round(avg(t.call_online_per),2) call_online_per,concat(round(avg(replace(t.xd_response_rate,'%','')),2),'%') xd_response_rate,concat(round(avg(replace(t.response_rate,'%','')),2),'%') response_rate
from data_report.dm_driver_complete_report_d t
where t.day_id>=@v_start_week and t.day_id<=@v_end_week
group by t.city_name;

insert into data_report.dm_driver_complete_report_w
select @v_this_week week_id,'本周环比' sign,t.city_name,
concat(round(100*(t.call_num_d-t1.call_num_d)/t1.call_num_d,2),'%')  call_num_d,
concat(round(100*(t.comp_order_num-t1.comp_order_num)/t1.comp_order_num,2),'%')  comp_order_num,
concat(round(100*(replace(t.comp_order_rate,'%','')-replace(t1.comp_order_rate,'%',''))/replace(t1.comp_order_rate,'%',''),2),'%')  comp_order_rate,
concat(round(100*(t.online_driver_num-t1.online_driver_num)/t1.online_driver_num,2),'%')  online_driver_num,
concat(round(100*(replace(t.online_driver_rate,'%','')-replace(t1.online_driver_rate,'%',''))/replace(t1.online_driver_rate,'%',''),2),'%')  online_driver_rate,
concat(round(100*(t.comp_driver_num-t1.comp_driver_num)/t1.comp_driver_num,2),'%')  comp_driver_num,
concat(round(100*(t.avg_comp_order_num-t1.avg_comp_order_num)/t1.avg_comp_order_num,2),'%')  avg_comp_order_num,
concat(round(100*(t.call_online_per-t1.call_online_per)/t1.call_online_per,2),'%')  call_online_per,
concat(round(100*(replace(t.xd_response_rate,'%','')-replace(t1.xd_response_rate,'%',''))/replace(t1.xd_response_rate,'%',''),2),'%')  xd_response_rate,
concat(round(100*(replace(t.response_rate,'%','')-replace(t1.response_rate,'%',''))/replace(t1.response_rate,'%',''),2),'%')  response_rate
from (select t.*
from data_report.dm_driver_complete_report_w t
where t.week_id=@v_this_week and t.sign='本周日均') t
left join 
(select t1.*
from data_report.dm_driver_complete_report_w t1
where t1.week_id=@v_last_week and t1.sign='本周日均') t1
on t.city_name=t1.city_name;
```
(5) 最终结果表输出
```sql
drop table if exists data_report.dm_driver_complete_report_output;
create table data_report.dm_driver_complete_report_output as
select t.*
from (select t.*
from data_report.dm_driver_complete_report_d t
where t.day_id>=v_start_week and t.day_id<=v_end_week
union all
select t1.*
from data_report.dm_driver_complete_report_w t1
where t1.week_id=v_this_week) t
order by case when t.city_name='全国' then '1'
when t.city_name='上海市' then '2'
when t.city_name='苏州市' then '3'
when t.city_name='郑州市' then '4'
when t.city_name='杭州市' then '5'
when t.city_name='宁波市' then '6' end,t.day_id;
```
(6) 封装脚本/存储过程

- 存储过程：data_report.sp_dm_driver_complete_report
- 调用方式：call data_report.sp_dm_driver_complete_report('2020-02-14');
