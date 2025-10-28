#!/bin/bash

echo "=== 健康管理平台启动脚本 ==="

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "创建 .env 文件..."
    cp .env.example .env
    echo "请编辑 .env 文件配置数据库连接和其他参数"
fi

# 检查数据库
echo "检查数据库连接..."
if ! pg_isready -h localhost -p 5432 -U postgres > /dev/null 2>&1; then
    echo "PostgreSQL 未运行，使用 Docker Compose 启动..."
    docker-compose up -d db
    echo "等待数据库启动..."
    sleep 5
fi

# 运行数据库迁移
echo "运行数据库迁移..."
alembic upgrade head

# 启动服务
echo "启动服务..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

