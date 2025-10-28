# 快速开始指南

## 前置要求

- Python 3.11+
- PostgreSQL 12+
- Docker 和 Docker Compose（可选）
- Git

## 方法一：使用 Docker（推荐）

### 1. 克隆项目
```bash
git clone <repository-url>
cd health-management-platform
```

### 2. 启动服务
```bash
# 启动所有服务（包括数据库）
docker-compose up -d

# 查看日志
docker-compose logs -f backend
```

### 3. 初始化数据库
```bash
# 进入容器
docker exec -it health_platform_backend bash

# 运行数据库初始化
python init_db.py
```

### 4. 访问 API
- API 文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

## 方法二：本地开发

### 1. 安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，修改数据库配置
```

### 3. 启动数据库
```bash
# 使用 Docker 启动 PostgreSQL
docker-compose up -d db

# 或使用本地 PostgreSQL
# 确保已创建数据库：createdb health_platform
```

### 4. 初始化数据库
```bash
python init_db.py
```

### 5. 启动服务
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 测试 API

### 方法 1：使用 Postman
1. 导入 `postman_collection.json` 到 Postman
2. 设置环境变量：
   - `base_url`: http://localhost:8000
   - `access_token`: (从登录接口获取)

### 方法 2：使用 cURL
```bash
# 1. 注册用户
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "full_name": "测试用户"
  }'

# 2. 登录
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"

# 3. 使用 token 访问 API（替换 YOUR_TOKEN）
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 方法 3：运行测试
```bash
# 运行所有测试
pytest tests/

# 运行特定测试
pytest tests/test_auth.py

# 显示详细输出
pytest -v
```

## 创建第一个健康记录

```bash
# 替换 YOUR_TOKEN
TOKEN="your_token_here"

# 提交运动数据
curl -X POST http://localhost:8000/api/health/data \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data_type": "exercise",
    "date": "2024-01-15",
    "exercise_type": "跑步",
    "duration": 30,
    "calories_burned": 300,
    "distance": 5.0,
    "intensity": "中等"
  }'
```

## 生成 AI 健康计划

```bash
# 生成个性化健康计划（需要用户有完整资料）
curl -X POST http://localhost:8000/api/health/plan \
  -H "Authorization: Bearer $TOKEN"
```

## 常见问题

### 数据库连接失败
- 检查 PostgreSQL 是否运行
- 确认 `.env` 中的数据库配置正确
- 检查端口 5432 是否被占用

### 导入错误
```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

### 端口冲突
```bash
# 修改 docker-compose.yml 中的端口映射
# 或使用不同端口启动
uvicorn app.main:app --port 8001
```

## 开发建议

1. **使用 API 文档**
   - 访问 http://localhost:8000/docs 查看交互式 API 文档
   - 可以直接在浏览器中测试 API

2. **代码热重载**
   - 使用 `--reload` 标志启动服务
   - 代码更改会自动重启服务

3. **调试**
   - 使用 Python 调试器
   - 查看日志输出

## 下一步

- 阅读 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) 了解项目结构
- 阅读 [README.md](README.md) 了解详细功能
- 开始开发前端应用

## 需要帮助？

- 查看项目文档
- 运行测试确保一切正常
- 检查日志输出

