---
title: MySQL数据库
tag: sql
article_header:
  type: overlay
  theme: dark
  background_color: '#203028'
  background_image:
    gradient: 'linear-gradient(135deg, rgba(34, 139, 87 , .4), rgba(139, 34, 139, .4))'
    src: /assets/images/cover3.jpg
---

MySQL的基本使用如查询、插入、删除数据；查询、创建、删除数据库、表格；约束设置、表及字段的注释；使用过程中遇到的一些问题如：登陆、连接错误、密码设置等；Python、Excel连接MySQL数据库。
<!--more-->

## 数据库操作

### 基本操作
```sql
-- 查询数据库：
SHOW DATABASES;
-- 选择数据库
USE database_name;
-- 查询表：
SHOW TABLES;
-- 创建数据库：
CREATE DATABASE data_name;
-- 删除数据库：
DROP DATABASE data_name;
-- 创建表:
CREATE TABLE table_name (column_name column_type);
-- 删除表:
DROP TABLE table_name;
-- 插入数据：
INSERT INTO table_name
( field1, field2,...fieldN )  
VALUES
( value1, value2,...valueN );
-- 修改/更新数据：
UPDATE table_name SET field1=new-value1, field2=new-value2
[WHERE Clause];
-- 查询数据：
SELECT column_name,column_name FROM table_name
[WHERE Clause] [LIMIT N][ OFFSET M]
-- 删除数据, where 字句为空时，删除表内所有内容：
DELETE FROM table_name [WHERE Clause]
```

注意其中的table_name, column_name与MySQL关键词重复时可使用``` ` ```来标注使用 `'` 是非法的  

### 约束设置

- 主键约束(primary key)
能够唯一确定表中的一条记录；

```sql
CREATE table user (
id int PRIMARY KEY,
name char(20)
);
CREATE table user (
    id int,
    name char(20),
    passwd varchar(30)
    PRIMARY KEY (id, name)
);
-- 联合主键，任何字段都不可为空，二者有一个不重复就可以(或的关系)； 
```

alter add/drop/modify (也适用于其他约束修改)

```sql
-- 向已有表中添加主键约束
alter table table_name ADD primary key(field)
-- 删除表中已有主键约束
alter table table_name DROP primary key(field)
-- 通过修改的方式添加
alter table table_name MODIFY field field_type primary key
```

- 自增约束(auto_increment)

```sql
-- 插入数据时id会自动增长
CREATE table user (
    id int, auto_increment
    name char(20),
    passwd varchar(30)
    PRIMARY KEY (id, name)
);
```

- 唯一约束(unique), 可在创建时设置，或使用alter修改

```sql
CREATE table user (
id int unique,
name char(20)
);
CREATE table user (
    id int,
    name char(20),
    passwd varchar(30)
    unique (id, name) 或的关系
);
```

- 非空约束(not null)

- 默认约束(default) 插入字段时，没有传入值使用默认值
  
```sql
CREATE table user (
id int default 10,
name char(20)
);
```

- 外键约束 父表，子表关系：关联自动中主表中没有的值，副表不可以使用；主表被副表引用时，不可以被删除

### 表及字段注释

```sql
-- 1 创建表的时候写注释
create table test1
(
    field_name int comment '字段的注释'
)comment='表的注释';
-- 2 修改表的注释
alter table test1 comment '修改后的表的注释';
-- 3 修改字段的注释  注意：字段名和字段类型照写就行
-- 4 查看表注释的方法
--在生成的SQL语句中看
show create table test1;
--在元数据的表里面看
use information_schema;
select * from TABLES where TABLE_SCHEMA='my_db' and TABLE_NAME='test1'
-- 5 查看字段注释的方法
--5.1 show命令
show full columns from test1;
-- or
show full fields from tablename;
--5.2 在元数据的表里面看
use information_schema;
select * from COLUMNS where TABLE_SCHEMA='my_db' and TABLE_NAME='test1'
```

## 遇到的问题及解决方案

### 创建MySQL用户和用户组
ubuntu上使用apt安装时已经自动创建了mysql用户组及mysql用户，如果没有可以使用一下命令添加：
```bash
groupadd mysql # 添加mysql用户组
useradd -r -g mysql -s /bin/false mysql # 创建一个系统用户并添加到mysql用户组
```
### 远程连接、登陆错误
1. 远程连接时遇到次错误：
    ```
    Fix: ERROR 2003 (HY000): Can’t connect to MySQL server on ‘hsot’ (111)
    ```
    解决方案：注释掉`/etc/mysql/mysql.conf.d/mysqld.cnf`中`bind-address = 127.0.0.1`（不同设备配置文件位置可不同）  

2. 修改后依然不能成功远程登陆，错误变为:
    ```
    Host 'host' is not allowed to connect to this MySQL server
    ```
    解决方案：由于账户不允许远程登陆，修改账户权限
    ```sql
    -- 查询用户可登陆位置 
    -- localhost ：只允许该用户在本地登录，不能远程登录。
    -- % ：允许在除本机之外的任何一台机器远程登录。
    -- ip地址 ：具体的IP表示只允许该用户从特定IP登录。
    select host,user from mysql.user where user='test';
    +-----------+------------------+
    | host      | user             |
    +-----------+------------------+
    | localhost | test             |
    +-----------+------------------+
    -- 修改登陆权限,并刷新
    update user set host = '%' where user = 'test';
    FLUSH   PRIVILEGES;
    ```
    
3. 本机使用`mysql -uroot -p`登陆时出现错误,但可以使用`sudo mysql`直接登陆；
    ```
    ERROR 1698 (28000): Access denied for user 'root'@'localhost'，
    ````
    解决方案：1、修改认证方式；2、创建一个与系统用户同名新的数据库用户^[1]

    ```sql
    -- 1、新版MySQL默认使用auth_socket认证方式，可以修改为mysql_native_password认证方式使用密码登陆。
    -- sudo mysql 登陆后修改认证方式
    UPDATE user SET plugin='mysql_native_password' WHERE User='root';
    FLUSH PRIVILEGES;
    
    -- 2、使用默认认证方式，创建系统同名用户作为MySQL用户
    -- 创建一个用系统用户同名的本机用户
    CREATE USER '系统用户名'@'localhost' IDENTIFIED BY '密码';
    -- 给该用户所有数据库的所有权限
    GRANT ALL PRIVILEGES ON *.* TO '系统用户名'@'localhost';
    -- 更新认证方式
    UPDATE user SET plugin='auth_socket' WHERE User='YOUR_SYSTEM_USER';
    FLUSH PRIVILEGES;
    -- 查看用户认证方式
    select user, plugin from mysql.user;
    +------------------+-----------------------+
    | user             | plugin                |
    +------------------+-----------------------+
    | root             | caching_sha2_password |
    | sysusername      | auth_socket           |
    +------------------+-----------------------+
    5 rows in set (0.00 sec)
    ```

### 密码问题
1. 修改密码，修改MySQL用户密码有多种方式，这里列出两种方式：
- 在终端使用`mysqladmin`命令修改
   ```bash
   mysqladmin -uroot -p'旧密码' password '新密码'
   ```
- 在MySQL中修改
    ```sql
    alter user 'user'@'host' identified [with 加密方式] by '密码';
    ```

2. MySQL安装后会为root用户在error.log中生成一个随机密码
    ```sql
    -- 查看error.log文件位置
    select @@log_error;
    +--------------------------+
    | @@log_error              |
    +--------------------------+
    | /var/log/mysql/error.log |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

3. 密码不符合安全要求，出现错误
    ```
    ERROR 1819 (HY000): Your password does not satisfy the current policy requirements
    ```
    设置符合要求的密码或者修改密码安全等级(validate_password_policy)有以下取值：
    
    Policy|Tests Performed
    -|-
    0 or LOW | Length
    1 or MEDIUM | Length; numeric, lowercase/uppercase, and special characters
    2 or STRONG | Length; numeric, lowercase/uppercase, and special characters; dictionary file

    ```sql
    -- 修改validate_password_policy参数的值
    -- 设置密码安全要求为0级
    set global validate_password_policy=0;
    ```
    设置密码安全等级要求validate_password插件必须已经安装（MySQL5.7是默认安装的）

    ```sql
    -- 查看validate_password设置
    show variables like 'validate_password%';
    +--------------------------------------+--------+
    | Variable_name                        | Value  |
    +--------------------------------------+--------+
    | validate_password.check_user_name    | ON     |
    | validate_password.dictionary_file    |        |
    | validate_password.length             | 8      |
    | validate_password.mixed_case_count   | 1      |
    | validate_password.number_count       | 1      |
    | validate_password.policy             | MEDIUM |
    | validate_password.special_char_count | 1      |
    +--------------------------------------+--------+
    7 rows in set (0.01 sec)
    ```

### MySQL数据存储位置

```sql
-- 查看数据存储位置
show global variables like '%datadir';
+---------------+-----------------+
| Variable_name | Value           |
+---------------+-----------------+
| datadir       | /var/lib/mysql/ |
+---------------+-----------------+
1 row in set (0.01 sec)
```

## Python连接数据库

[PyMysql](https://pymysql.readthedocs.io/en/latest/modules/index.html) 是一个纯 Python 实现的 MySQL 客户端操作库，支持事务、存储过程、批量执行等。如使用 "sha256_password" or "caching_sha2_password" 认证需要额外安装:`python3 -m pip install PyMySQL[rsa]`

1. 连接数据库  
   `pymysql.connect()`

   ```python
   db = pymysql.connect(host='localhost',
                        port=3306,
                        user='root',
                        password='root',
                        db='demo',
                        charset='utf8')
   ```

   参数|描述
   -|-
   host|数据库服务器地址，默认 localhost
   user|用户名，默认为当前程序运行用户
   password (passwd)|登录密码，默认为空字符串
   database (db)|默认操作的数据库
   port |Tests数据库端口，默认为 3306
   charset| 数据库编码
   ...|...
2. 创建游标对象  
使用 `cursor()` 方法创建一个游标对象 cursor, 默认返回的数据类型为元组，可以自定义设置返回类型。支持5种游标类型：  
    - Cursor: 默认，元组类型
    - DictCursor: 字典类型
    - DictCursorMixin: 支持自定义的游标类型，需先自定义才可使用
    - SSCursor: 无缓冲元组类型
    - SSDictCursor: 无缓冲字典类型
    游标类型的设置可在创建连接是通过`cursorclass`参数指定，也可在初始化游标对象使用`cursor`参数时指定

    ```python
    db = pymysql.connect(user='root',
                        password='root',
                        db='demo',
                        cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    ```

    所有的数据查询操作均基于游标，我们可以通过`cursor.scroll(num, mode)`控制游标的位置。

    ```python
    cursor.scroll(1, mode='relative') # 相对当前位置移动
    cursor.scroll(2, mode='absolute') # 相对绝对位置移动
    ```

3. 数据库操作  
   `cursor.execute(sql, args)` 执行单条/多条 SQL语句  

   ```python
   # 创建数据表
    effect_row = cursor.execute('''
    CREATE TABLE `users` (
    `name` varchar(32) NOT NULL,
    `age` int(10) unsigned NOT NULL DEFAULT '0',
    PRIMARY KEY (`name`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ''')
    # 插入数据(元组或列表)
    effect_row = cursor.execute('INSERT INTO `users` (`name`, `age`) VALUES (%s, %s)', ('mary', 18))
    # 插入数据(字典)
    info = {'name': 'fake', 'age': 15}
    effect_row = cursor.execute('INSERT INTO `users` (`name`, `age`) VALUES (%(name)s, %(age)s)', info)
    # 批量插入
    effect_row = cursor.executemany(
        'INSERT INTO `users` (`name`, `age`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE age=VALUES(age)', [
            ('hello', 13),
            ('fake', 28),
        ])
    connection.commit()
    ############################
    fetchone(): # 该方法获取下一个查询结果集。结果集是一个对象
    fetchall(): # 接收全部的返回结果行.
    fetchmany(n): #　获取前n条数据.
    rowcount: # 这是一个只读属性，并返回执行execute()方法后影响的行数。
   ```

4. 提交操作  
   INSERT、UPDATE、DELETE 等修改数据的语句需手动执行`db.commit()`完成对数据修改的提交.
5. 关闭数据库连接  
    ```python
    cursor.close() # 关闭游标
    db.close() #关闭数据库
    ```

6. 事务处理  
   开启事务 `connection.begin()`；
   提交修改 `connection.commit()`；
   回滚事务 `connection.rollback()`。

## Excel连接mysql
1. 首先下载安装合适版本的[Connector/ODBC](https://dev.mysql.com/downloads/connector/odbc/)（如果已安装过MySQL，应该已经安装了）
2. 在**控制面板**-**管理工具**找到**ODBC数据源**  
![8kEKdU.png](https://s2.ax1x.com/2020/03/11/8kEKdU.png)
3. 双击进入设置界面，按下图流程设置：
![8kZbIU.png](https://s2.ax1x.com/2020/03/11/8kZbIU.png)
![8kZhxs.png](https://s2.ax1x.com/2020/03/11/8kZhxs.png)
![8kZoq0.png](https://s2.ax1x.com/2020/03/11/8kZoq0.png)
![8kZWGQ.png](https://s2.ax1x.com/2020/03/11/8kZWGQ.png)

4. Excel导入数据
Excel中**数据**-**获取数据**-**自其他来源**-**从ODBC**然后选择之前在管理程序中新建的数据源。

---

[1]:[解决 MySQL 的 ERROR 1698 (28000): Access denied for user root@localhost_数据库_Just for funnnnnnnnnnnn-CSDN博客](https://blog.csdn.net/jlu16/article/details/82809937)