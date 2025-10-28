# 健康管理平台 - 项目结构

## 项目概述

这是一个基于 FastAPI 构建的健康管理平台后端服务，提供用户认证、健康数据管理、AI 驱动的个性化健康计划生成等功能。

## 技术栈

- **后端框架**: FastAPI
- **数据库**: PostgreSQL (通过 SQLAlchemy ORM)
- **认证**: JWT (JSON Web Token)
- **AI/ML**: TensorFlow, PyTorch, Scikit-learn
- **测试**: PyTest
- **部署**: Docker, Docker Compose

## 项目结构

```
backend/
├── app/                           # 应用主目录
│   ├── __init__.py
│   ├── main.py                   # 应用入口
│   ├── core/                     # 核心配置模块
│   │   ├── __init__.py
│   │   ├── config.py            # 配置文件
│   │   ├── security.py          # 安全认证（JWT）
│   │   └── database.py           # 数据库连接
│   ├── models/                   # 数据库模型
│   │   ├── __init__.py
│   │   ├── user.py              # 用户模型
│   │   └── health_data.py       # 健康数据模型
│   ├── schemas/                  # Pydantic 模式
│   │   ├── __init__.py
│   │   ├── user.py              # 用户模式
│   │   └── health_data.py       # 健康数据模式
│   ├── api/                      # API 路由
│   │   ├── __init__.py
│   │   └── endpoints/           # API 端点
│   │       ├── __init__.py
│   │       ├── auth.py          # 认证端点
│   │       ├── users.py         # 用户端点
│   │       └── health.py        # 健康数据端点
│   └── services/                 # 业务逻辑服务
│       ├── __init__.py
│       ├── user_service.py      # 用户服务
│       ├── health_data_service.py # 健康数据服务
│       └── ai_service.py        # AI 健康计划服务
├── tests/                        # 测试文件
│   ├── __init__.py
│   ├── conftest.py              # 测试配置
│   ├── test_auth.py             # 认证测试
│   ├── test_health_data.py     # 健康数据测试
│   └── test_health_plan.py     # 健康计划测试
├── migrations/                   # 数据库迁移
│   ├── env.py
│   └── script.py.mako
├── alembic.ini                   # Alembic 配置
├── Dockerfile                    # Docker 镜像配置
├── docker-compose.yml           # Docker Compose 配置
├── requirements.txt             # Python 依赖
├── .env.example                 # 环境变量示例
├── .gitignore                   # Git 忽略文件
├── README.md                    # 项目说明
├── start.sh                     # 启动脚本
└── postman_collection.json      # Postman 测试集合

```

## 主要功能模块

### 1. 用户认证 (auth.py)
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录（获取 JWT token）
- `GET /api/auth/me` - 获取当前用户信息

### 2. 用户管理 (users.py)
- `GET /api/users/me` - 获取当前用户信息
- `PUT /api/users/me` - 更新用户信息
- `GET /api/users/{user_id}` - 获取指定用户信息

### 3. 健康数据 (health.py)
#### 数据提交
- `POST /api/health/data` - 提交健康数据（运动/饮食/睡眠）
- 支持的数据类型：`exercise`, `diet`, `sleep`

#### 数据查询
- `GET /api/health/data` - 获取健康数据（支持类型和时间范围过滤）
- `GET /api/health/statistics` - 获取健康数据统计

#### 健康计划
- `POST /api/health/plan` - 生成个性化健康计划
- `GET /api/health/plan` - 获取健康计划列表
- `GET /api/health/plan/{plan_id}` - 获取特定健康计划
- `PUT /api/health/plan/{plan_id}` - 更新健康计划
- `GET /api/health/recommendations` - 获取 AI 推荐建议

## 数据库模型

### User 模型
- 基本信息：username, email, password
- 个人资料：full_name, date_of_birth, gender, height, weight
- 健康目标：activity_level, health_goal

### HealthData 模型
支持三种数据类型：
- **Exercise**: exercise_type, duration, calories_burned, distance, intensity
- **Diet**: meal_type, food_name, calories, protein, carbs, fats, fiber
- **Sleep**: sleep_duration, sleep_quality, bed_time, wake_time

### HealthPlan 模型
- 计划类型：plan_type (exercise/diet/general)
- 计划内容：title, description, duration_days
- 目标设置：calories_target, exercise_minutes_per_day
- AI 生成内容：ai_generated_content, exercise_plan, diet_suggestions

## AI 服务功能

### 个性化健康计划生成
- 分析用户健康数据
- 计算基础代谢率 (BMR)
- 基于用户目标生成个性化计划
- 提供运动计划和饮食建议

### 智能推荐
- 基于用户健康数据分析
- 提供运动频率建议
- 睡眠质量评估和建议
- 饮食调整建议

## 快速开始

### 1. 安装依赖
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置环境
```bash
cp .env.example .env
# 编辑 .env 文件
```

### 3. 启动数据库
```bash
docker-compose up -d db
```

### 4. 运行迁移
```bash
alembic upgrade head
```

### 5. 启动服务
```bash
uvicorn app.main:app --reload
```

### 6. 访问 API 文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发指南

### 运行测试
```bash
pytest tests/
```

### 数据库迁移
```bash
# 创建新迁移
alembic revision --autogenerate -m "description"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

### Docker 部署
```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## API 使用示例

### 1. 注册用户
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### 2. 登录获取 Token
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123"
```

### 3. 提交健康数据
```bash
curl -X POST http://localhost:8000/api/health/data \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data_type": "exercise",
    "date": "2024-01-15",
    "exercise_type": "跑步",
    "duration": 30,
    "calories_burned": 300
  }'
```

### 4. 生成健康计划
```bash
curl -X POST http://localhost:8000/api/health/plan \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 安全注意事项

1. **生产环境配置**
   - 修改默认的 SECRET_KEY
   - 使用强密码
   - 配置 CORS 白名单
   - 启用 HTTPS

2. **数据库安全**
   - 使用环境变量存储敏感信息
   - 定期备份数据库
   - 使用连接池

3. **API 安全**
   - 所有健康数据端点需要认证
   - 验证输入数据
   - 防止 SQL 注入（使用 ORM）

## 扩展功能建议

1. **数据可视化 API**
   - 添加数据导出功能
   - 提供图表数据 API

2. **社交功能**
   - 用户好友系统
   - 健康挑战

3. **通知系统**
   - 邮件提醒
   - 推送通知

4. **高级 AI 功能**
   - 基于机器学习的个性化推荐
   - 健康趋势预测

## 许可证

MIT License

