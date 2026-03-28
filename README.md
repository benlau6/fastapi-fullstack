# fastapi-edu-lite

## 介绍

基于 `benlau6/fastapi-fullstack` 改造的轻量教务管理系统，包含前后端配套、JWT 认证、管理员权限与基础数据 CRUD。

## 功能范围（第一版）

- 管理员登录（JWT）
- 学生管理 CRUD
- 教师管理 CRUD
- 课程管理 CRUD
- 班级管理 CRUD
- 统一响应结构 `{code,message,data}`
- 前端中文界面（菜单、按钮、提示、表头）

## 默认账号

- 用户名：`admin`
- 密码：`admin123`

## 本地启动

### 后端

```bash
cd backend/app
/workspace/.venv/bin/pip install -r requirements.txt
/workspace/.venv/bin/pip install httpx pydantic-settings
/workspace/.venv/bin/pytest -q
/workspace/.venv/bin/python -m uvicorn app.main:app --reload --port 3000
```

后端文档：`http://127.0.0.1:3000/docs`

### 前端

```bash
cd frontend/app
PATH="/workspace/tools/node-v20.19.5-musl/bin:$PATH" npm install
PATH="/workspace/tools/node-v20.19.5-musl/bin:$PATH" npm run test:unit -- --runInBand tests/unit/views/login.cn.spec.js tests/unit/views/dashboard.cn.spec.js tests/unit/views/menu.cn.spec.js tests/unit/views/messages.cn.spec.js
PATH="/workspace/tools/node-v20.19.5-musl/bin:$PATH" npm run build:prod
```

## 验收检查

- 后端测试：`23 passed`
- 前端中文单测：`4 passed`
- 前端构建：`build:prod` 成功
- 四模块接口与页面已联通，删除返回 `200 + data:null`
- 错误语义：`401/403/409/422` 已覆盖

## 说明

- 本仓库为模板改造版，保留了部分原始示例代码目录。
- 当前目标是“轻量可用第一版”，后续可扩展选课、成绩与多角色权限。


<small>

You may also wanna check [fastapi-pynamodb-lambda-simple](https://github.com/benlau6/fastapi-pynamodb-lambda-simple.git) or [fastapi-pynamodb-lambda-versioning](https://github.com/benlau6/fastapi-pynamodb-lambda-versioning) for using FastAPI on AWS

</small>

