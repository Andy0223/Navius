# 数据库迁移指南 - 从单一 HealthData 表拆分成三个独立表

## 变更概述

将 `health_data` 表拆分成：
- `exercise_data` - 运动数据表
- `diet_data` - 饮食数据表  
- `sleep_data` - 睡眠数据表

## 迁移步骤

### 1. 创建新的表结构

新表会通过 SQLAlchemy 自动创建，或手动运行：

```sql
-- 创建 exercise_data 表
CREATE TABLE exercise_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    exercise_type VARCHAR(100) NOT NULL,
    duration FLOAT NOT NULL,
    calories_burned FLOAT,
    distance FLOAT,
    intensity VARCHAR(50),
    date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_exercise_data_user_id ON exercise_data(user_id);
CREATE INDEX idx_exercise_data_date ON exercise_data(date);

-- 创建 diet_data 表
CREATE TABLE diet_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    meal_type VARCHAR(50) NOT NULL,
    food_name VARCHAR(200) NOT NULL,
    calories FLOAT NOT NULL,
    protein FLOAT,
    carbs FLOAT,
    fats FLOAT,
    fiber FLOAT,
    date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_diet_data_user_id ON diet_data(user_id);
CREATE INDEX idx_diet_data_date ON diet_data(date);

-- 创建 sleep_data 表
CREATE TABLE sleep_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    sleep_duration FLOAT NOT NULL,
    sleep_quality VARCHAR(50) NOT NULL,
    bed_time TIMESTAMP,
    wake_time TIMESTAMP,
    date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sleep_data_user_id ON sleep_data(user_id);
CREATE INDEX idx_sleep_data_date ON sleep_data(date);
```

### 2. 迁移现有数据

```sql
-- 迁移运动数据
INSERT INTO exercise_data (
    id, user_id, exercise_type, duration, calories_burned, 
    distance, intensity, date, notes, created_at, updated_at
)
SELECT 
    id, user_id, exercise_type, duration, calories_burned,
    distance, intensity, date, notes, created_at, updated_at
FROM health_data
WHERE data_type = 'exercise'
AND exercise_type IS NOT NULL
AND duration IS NOT NULL;

-- 迁移饮食数据
INSERT INTO diet_data (
    id, user_id, meal_type, food_name, calories,
    protein, carbs, fats, fiber, date, notes, created_at, updated_at
)
SELECT 
    id, user_id, meal_type, food_name, calories,
    protein, carbs, fats, fiber, date, notes, created_at, updated_at
FROM health_data
WHERE data_type = 'diet'
AND meal_type IS NOT NULL
AND food_name IS NOT NULL
AND calories IS NOT NULL;

-- 迁移睡眠数据
INSERT INTO sleep_data (
    id, user_id, sleep_duration, sleep_quality,
    bed_time, wake_time, date, notes, created_at, updated_at
)
SELECT 
    id, user_id, sleep_duration, sleep_quality,
    bed_time, wake_time, date, notes, created_at, updated_at
FROM health_data
WHERE data_type = 'sleep'
AND sleep_duration IS NOT NULL
AND sleep_quality IS NOT NULL;
```

### 3. 更新序列（如果需要保持ID连续性）

```sql
-- 更新序列
SELECT setval('exercise_data_id_seq', COALESCE((SELECT MAX(id) FROM exercise_data), 1), true);
SELECT setval('diet_data_id_seq', COALESCE((SELECT MAX(id) FROM diet_data), 1), true);
SELECT setval('sleep_data_id_seq', COALESCE((SELECT MAX(id) FROM sleep_data), 1), true);
```

### 4. 删除旧表（在确认数据迁移成功后）

```sql
-- ⚠️ 警告：只在确认数据迁移成功后才执行
-- DROP TABLE health_data;
```

## API 变更

### 新端点（推荐使用）

- `POST /api/health/exercise` - 创建运动数据
- `GET /api/health/exercise` - 获取运动数据
- `POST /api/health/diet` - 创建饮食数据
- `GET /api/health/diet` - 获取饮食数据
- `POST /api/health/sleep` - 创建睡眠数据
- `GET /api/health/sleep` - 获取睡眠数据

### 向后兼容端点

- `POST /api/health/data` - 仍然支持，会根据 `data_type` 自动路由
- `GET /api/compare/data` - 仍然支持，可以查询所有类型的数据

## 优势

1. ✅ **零 NULL 值** - 每个表只存储相关字段
2. ✅ **更好的查询性能** - 直接查询对应表，无需过滤
3. ✅ **类型安全** - 数据库层面强制约束堵字段
4. ✅ **易于扩展** - 添加新数据类型只需新建表
5. ✅ **独立索引** - 每个表可以有针对性优化

