#!/usr/bin/env python3
"""
数据库初始化脚本
"""
from app.core.database import Base, engine
from app.models import user, health_data

def init_db():
    """初始化数据库表"""
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")


if __name__ == "__main__":
    init_db()

