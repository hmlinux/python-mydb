--员工信息管理程序

1. 执行bin/目录的的mydb.py进入数据查询控制台
2. 允许用户查询数据库、表（默认数据库：staff、表：staff_staff）
   可使用如下命令查询：
       show databases;
       show tables;
3. 选择staff数据库，可对staff_table表进行数据查询，全表查询或者条件查询，语句用法如下（查询语句不区分大小写）
    select * from staff_table;
    select name,age,phone from staff_table where dept = 'IT';
    SELECT name,age FROM staff_table WHERE age > 22;
    select * from staff_table where enroll_date like "2013";
3. 选择staff数据库，可对staff_table表进行数据插入、更新、删除操作，语句用法如下
    INSERT INTO staff_table VALUES("Jack Ma",23,13012546524,"IT","2014-07-22");
    UPDATE staff_table SET dept="Market",phone=13532016528 WHERE name="Jack Wang";
    DELETE FROM staff_table WHERE staff_id=5;
4. 信息管理程序暂不支持create语句创建数据库或表
5. 输入'exit' 或 'quit' 退出程序
