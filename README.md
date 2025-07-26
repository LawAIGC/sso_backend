# SSO Backend Python

一个基于 Flask 的单点登录（SSO）后端服务，提供用户管理、角色权限控制和菜单管理功能。

## 🚀 功能特性

- **用户管理**: 用户注册、登录、信息管理
- **角色权限**: 基于角色的访问控制（RBAC）
- **菜单管理**: 动态菜单配置和权限控制
- **JWT认证**: 基于 JWT 的身份认证和授权
- **RESTful API**: 标准的 REST API 接口
- **数据库支持**: SQLite

## 🛠️ 技术栈

- **框架**: Flask 3.1.1
- **数据库ORM**: Flask-SQLAlchemy 3.1.1
- **身份认证**: Flask-JWT-Extended 4.7.1
- **数据库**: SQLite（默认）
- **WSGI服务器**: Waitress 3.0.2
- **Python版本**: Python 3.7+

## 📁 项目结构

```
sso-backend-python/
├── app.py              # Flask应用主文件
├── api.py              # API路由定义
├── models.py           # 数据库模型
├── const.py            # 常量定义
├── exts.py             # 扩展初始化
├── restful.py          # RESTful响应工具
├── wsgi.py             # WSGI入口文件
├── requirements.txt    # 项目依赖
├── .env.example        # 环境变量示例
├── Dockerfile          # Docker配置
└── services/           # 业务逻辑层
    ├── __init__.py
    ├── user.py         # 用户服务
    ├── role.py         # 角色服务
    ├── menu.py         # 菜单服务
    └── ability.py      # 权限服务
```

## 🚀 快速开始

### 环境要求

- Python 3.7+
- pip

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd sso-backend-python
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，配置相关参数
   ```

5. **运行应用**
   ```bash
   # 开发模式
   python app.py
   
   # 生产模式
   python wsgi.py
   ```

应用将在 `http://localhost:9001` 启动。

## 🐳 Docker 部署

```bash
# 启动服务 
`docker-compose up -d --build`

# 查看服务状态
`docker-compose ps`

# 查看日志（可选）
`docker-compose logs -f`
```

## 📚 API 文档

### 认证相关

- `POST /api/v1/auth/login` - 用户登录
   - `username: str`
   - `password: str`
- `POST /api/v1/change_password` - 修改密码
   - `user_id: int`
   - `password: str`
- `POST /api/v1/forgot_password` - 忘记密码
   - `username: str`
- `POST /api/register_verification` - 发送注册邮箱验证码
   - `email: str`
- `POST /api/register_user` - 注册用户
   - `username: str`
   - `email: str`
   - `dept: str`
   - `code: str`
- `POST /api/change_password_verification` - 发送修改密码邮箱验证码
   - `username: str`
   - `email: str`
- `POST /api/change_password_by_email` - 通过邮箱验证码修改密码
   - `username: str`
   - `email: str`
   - `password: str`
   - `code: str`
- `GET /api/v1/auth/verify ` - 返回用户信息


### 用户管理

- `GET /api/permission/user/inner/list` - 获取用户列表
   - `name: str`
- `GET /api/permission/user/detail`     - 获取用户详情
   - `user_id: int`
- `POST /api/permission/user/create`    - 创建用户
   - `user_name: str`
   - `email: str`
   - `description: str`
   - `real_name: str`
   - `roleinfos: str: [object]`
      - `role_id: str`
- `POST /api/permission/user/update`    - 更新用户信息
   - `user_id: int`
   - `user_name: str`
   - `email: str`
   - `description: str`
   - `real_name: str`
   - `roleinfos: str: [object]`
      - `role_id: str`
- `POST /api/permission/user/detail`    - 删除用户
   - `user_id: int`

### 角色管理

- `GET /api/permission/role/getlist` - 获取角色列表
   - `name: str`
- `GET /api/permission/role/detail`  - 获取角色详情
   - `role_id: int`
- `POST /api/permission/role/create` - 创建角色
   - `permission_ids: str`
   - `role_name: str`
   - `description: str`
- `POST /api/permission/role/update` - 更新角色
   - `role_id: int`
   - `permission_ids: str`
   - `role_name: str`
   - `description: str`
- `POST /api/permission/role/delete` - 删除角色
   - `role_id: int`

### 菜单管理

- `GET /api/permission/api/menu/list` - 获取菜单列表
   - `pn: int`
   - `size: int`

### 能力管理

- `GET /api/permission/per/getlist`  - 获取能力列表
   - `permission: str`
- `GET /api/permission/per/detail`   - 获取能力详情
   - `permission_id: int`
- `POST /api/permission/per/delete`  - 删除能力
   - `permission_id: int`
- `POST /api/permission/per/create`  - 添加能力
   - `name: str`
   - `menu_ids: [int]`
- `POST /api/permission/per/update`  - 能力编辑
   - `id: int`
   - `name: str`
   - `menu_ids: [int]`

## 🔧 配置说明

### 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `APP_NAME` | 应用名称 | User Management Backend |
| `APP_ENV` | 运行环境 | development |
| `SERVER_HOST` | 服务器地址 | 0.0.0.0 |
| `SERVER_PORT` | 服务器端口 | 9001 |
| `JWT_SECRET_KEY` | JWT密钥 | your-secret-key-here |

### 数据库配置

默认使用 SQLite 数据库，数据文件位于 `data.db`。生产环境建议使用 PostgreSQL 或 MySQL。

## 🏗️ 数据模型

### User（用户）
- id: 用户ID
- username: 用户名
- email: 邮箱
- password: 密码（加密存储）
- real_name: 真实姓名
- phone: 手机号
- status: 用户状态（active/inactive/suspended）
- roles: 关联角色

### Role（角色）
- id: 角色ID
- name: 角色名称
- description: 角色描述
- status: 角色状态
- users: 关联用户
- abilities: 关联权限

### Menu（菜单）
- id: 菜单ID
- path: 菜单路径
- menu_name: 菜单名称
- pid: 父菜单ID
- menu_type: 菜单类型
- sort: 排序

## 🔒 安全特性

- 密码加密存储（Werkzeug）
- JWT 令牌认证
- 基于角色的访问控制
- SQL注入防护
- CORS 支持

## 🧪 测试

```bash
# 运行测试
python -m pytest

# 运行测试并生成覆盖率报告
python -m pytest --cov=.
```

## 📝 开发指南

### 添加新的API端点

1. 在 `api.py` 中定义路由
2. 在 `services/` 目录下实现业务逻辑
3. 在 `models.py` 中定义数据模型（如需要）
4. 更新API文档


**注意**: 在生产环境中使用前，请确保：
1. 更改默认的JWT密钥
2. 配置适当的数据库
3. 启用HTTPS
4. 配置适当的CORS策略
5. 设置适当的日志级别

层级结构设计

├── 用户
    多对多 ├── 角色
              多对多 ├── 能力
                        多对多 ├── 菜单

由菜单构建能力 能力构建角色 角色构建用户
实际场景就是用户账号登录后，通过角色、能力、菜单等字段，做到入口权限、功能权限、数据权限的管控

默认菜单
名称 权限中心 
名称 云管平台
名称 大屏总览
名称 资源编排

默认能力
名称 权限中心    菜单名称 权限中心
名称 云管平台    菜单名称 云管平台
名称 大屏总览    菜单名称 大屏总览
名称 资源编排    菜单名称 资源编排

默认角色
名称 user    能力名称 大屏总览
名称 admin   能力名称 权限中心 云管平台 大屏总览 资源编排 

默认用户
名称 user    角色名称 user
名称 admin   角色名称 admin

