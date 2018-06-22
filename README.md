# easy_frame
> python 基于Flask的后台框架

- 运行环境:
  python3.6
- 所需模块:
  flask
  pymysql
  schedule
  pyOpenSSL(可选)


### 功能简述:
#### 实例参照配置自动注入(properties.IOCProp)
#### 数据库连接池(mysql.Pool)
#### 配置形式维护参数(properties.__init__)
#### 远程xml维护(mysql,remote)
#### binlog检查增量(调度形式)(mysql.binlog)
#### sql语句分页,变量赋值,批量执行,细粒度事务,调试模式执行详情打印(mysql.__init__)
#### 一键启动(类似springboot)
#### 蓝图形式绑定路径
#### 装饰器形式数据返回(ResponseBody)
#### 装饰器形式配置请求参数装载(AutoParam,FullParam)
#### 装饰器形式配置路径绑定(RequestMapping)

