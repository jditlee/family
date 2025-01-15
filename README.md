<p align="center">
	<img alt="logo" src="https://oscimg.oschina.net/oscnet/up-d3d0a9303e11d522a06cd263f3079027715.png">
</p>
<h1 align="center" style="margin: 30px 0 30px; font-weight: bold;">Family</h1>
<h4 align="center">基于RuoYi-Vue3+FastAPI家庭管理系统</h4>
<p align="center">
    <a href="https://github.com/jditlee/family"><img src="https://img.shields.io/github/stars/jditlee/family?style=social"></a>
    <img src="https://img.shields.io/badge/python-≥3.9-blue">
    <img src="https://img.shields.io/badge/MySQL-≥5.7-blue">
</p>

## 平台简介

Family是围绕家庭来做的一个家庭管理系统，包含了日常消费记录，收支统计，家庭趣事分享等等功能。

* 前端采用Vue3、Element Plus，基于<u>[RuoYi-Vue3-FastAPI](https://github.com/insistence/RuoYi-Vue3-FastAPI)</u>项目修改。
* 后端采用FastAPI、sqlalchemy、MySQL（PostgreSQL）、Redis、OAuth2 & Jwt,基于<u>[RuoYi-Vue3-FastAPI](https://github.com/insistence/RuoYi-Vue3-FastAPI)</u>项目修改。
* 权限认证使用OAuth2 & Jwt，支持多终端认证系统。
* 支持加载动态权限菜单，多方式轻松权限控制。
* 特别鸣谢：
  - <u>[RuoYi-Vue3-FastAPI](https://github.com/insistence/RuoYi-Vue3-FastAPI)</u>

## 内置功能

1.  用户管理：用户是系统操作者，该功能主要完成系统用户配置。
2.  角色管理：角色菜单权限分配、设置角色按机构进行数据范围权限划分。
3.  菜单管理：配置系统菜单，操作权限，按钮权限标识等。
4.  部门管理：配置系统组织机构（公司、部门、小组）。
5.  岗位管理：配置系统用户所属担任职务。
6.  字典管理：对系统中经常使用的一些较为固定的数据进行维护。
7.  参数管理：对系统动态配置常用参数。
8.  通知公告：系统通知公告信息发布维护。
9.  操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
10. 登录日志：系统登录日志记录查询包含登录异常。
11. 在线用户：当前系统中活跃用户状态监控。
12. 定时任务：在线（添加、修改、删除）任务调度包含执行结果日志。
13. 服务监控：监视当前系统CPU、内存、磁盘、堆栈等相关信息。
14. 缓存监控：对系统的缓存信息查询，命令统计等。
15. 系统接口：根据业务代码自动生成相关的api接口文档。

## 演示图


## 项目开发及发布相关

### 开发

```bash
# 克隆项目
git clone https://github.com/jditlee/family.git

# 进入项目根目录
cd family
```

#### 前端
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install 或 yarn --registry=https://registry.npmmirror.com

# 建议不要直接使用 cnpm 安装依赖，会有各种诡异的 bug。可以通过如下操作解决 npm 下载速度慢的问题
npm install --registry=https://registry.npmmirror.com

# 启动服务
npm run dev 或 yarn dev
```

#### 后端
```bash
# 进入后端目录
cd backend

# 如果使用的是MySQL数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements.txt
# 如果使用的是PostgreSQL数据库，请执行以下命令安装项目依赖环境
pip3 install -r requirements-pg.txt

# 配置环境
在.env.dev文件中配置开发环境的数据库和redis

# 运行sql文件
1.新建数据库family(默认，可修改)
-- todo：数据库脚本待更新
2.如果使用的是MySQL数据库，使用命令或数据库连接工具运行sql文件夹下的ruoyi-fastapi.sql；如果使用的是PostgreSQL数据库，使用命令或数据库连接工具运行sql文件夹下的ruoyi-fastapi-pg.sql

# 运行后端
python3 app.py --env=dev
```

#### 访问
```bash
# 默认账号密码
账号：admin
密码：admin123

# 浏览器访问
地址：http://localhost:80
```

### 发布

#### 前端
```bash
# 构建测试环境
npm run build:stage 或 yarn build:stage

# 构建生产环境
npm run build:prod 或 yarn build:prod
```

#### 后端
```bash
# 配置环境
在.env.prod文件中配置生产环境的数据库和redis

# 运行后端
python3 app.py --env=prod
```

## 🎙 功能与建议
目前项目处于开发初期，新功能正在持续添加中，如果你对软件有任何功能与建议，欢迎在 Issues 中提出

项目的进展与未来计划在 Issue 中详细介绍，内部也包含对未来功能的意见征询等，如果对 Family 的未来感兴趣，欢迎参与讨论。

如果你也喜欢本软件的设计思想，欢迎提交 pr，非常感谢你对我们的支持！


## 交流与赞助

