# Cooks API 接口文档

> 基于 FastAPI 构建的餐饮点餐应用后端 API

**基础 URL**: `http://localhost:8000`

**认证方式**: JWT Bearer Token

**请求格式**: `Content-Type: application/json`

---

## 目录

1. [健康检查](#1-健康检查)
2. [用户管理](#2-用户管理-users)
3. [菜品管理](#3-菜品管理-dishes)
4. [购物车](#4-购物车-cart)
5. [收藏](#5-收藏-favorites)
6. [历史记录](#6-历史记录-history)
7. [食材采购](#7-食材采购-buy)

---

**接口总览** (7个模块，32个接口)

| 模块 | 接口数 | 说明 |
|------|--------|------|
| 健康检查 | 2 | 服务状态检查 |
| 用户管理 | 6 | 注册、登录、CRUD操作 |
| 菜品管理 | 5 | 菜品CRUD |
| 购物车 | 4 | 购物车管理 |
| 收藏 | 4 | 收藏管理 |
| 历史记录 | 4 | 历史订单管理 |
| 食材采购 | 7 | 采购记录管理 |

---

## 1. 健康检查

### 1.1 获取服务状态

```
GET /
```

**说明**: 检查服务是否正常运行

**请求参数**: 无

**响应示例**:
```json
{
  "message": "Cooks API is running"
}
```

---

### 1.2 健康检查

```
GET /health
```

**说明**: 检查服务健康状态

**请求参数**: 无

**响应示例**:
```json
{
  "status": "healthy"
}
```

---

## 2. 用户管理 (Users)

### 2.1 用户注册

```
POST /users/register
```

**说明**: 注册新用户

**请求体**:
```json
{
  "username": "string",      // 用户名（必填，唯一）
  "password": "string",      // 密码（必填）
  "nickname": "string",      // 昵称（必填）
  "role": "user"             // 角色：user/admin（默认 user）
}
```

**响应** (201 Created):
```json
{
  "id": 1,
  "username": "john",
  "nickname": "约翰",
  "role": "user"
}
```

**错误响应**:
```json
// 400: 用户名已存在
{"detail": "用户名已存在"}

// 400: 无效的角色
{"detail": "无效的角色"}
```

---

### 2.2 用户登录

```
POST /users/login
```

**说明**: 用户登录，获取 JWT Token

**请求体**:
```json
{
  "username": "string",
  "password": "string"
}
```

**响应**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**使用 Token**: 在后续请求的 Header 中添加:
```
Authorization: Bearer <access_token>
```

**错误响应**:
```json
// 401: 用户名或密码错误
{"detail": "用户名或密码错误"}
```

---

### 2.3 获取当前用户信息

```
GET /users/me
```

**说明**: 获取当前登录用户信息

**请求头**: `Authorization: Bearer <token>`

**响应**:
```json
{
  "id": 1,
  "username": "john",
  "nickname": "约翰",
  "role": "user"
}
```

---

### 2.4 获取用户列表

```
GET /users
```

**说明**: 获取所有用户列表（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**权限**: 仅 `admin` 角色可访问

**响应**:
```json
[
  {
    "id": 1,
    "username": "john",
    "nickname": "约翰",
    "role": "user"
  }
]
```

**错误响应**:
```json
// 403: 权限不足（非管理员）
{"detail": "权限不足，需要管理员权限"}
```

---

### 2.5 获取指定用户

```
GET /users/{user_id}
```

**说明**: 获取指定用户信息

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | int | 用户ID |

**权限**: 普通用户只能查看自己，管理员可查看所有用户

**响应**:
```json
{
  "id": 1,
  "username": "john",
  "nickname": "约翰",
  "role": "user"
}
```

**错误响应**:
```json
// 403: 权限不足
{"detail": "权限不足"}

// 404: 用户不存在
{"detail": "用户不存在"}
```

---

### 2.6 更新用户

```
PUT /users/{user_id}
```

**说明**: 更新用户信息（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | int | 用户ID |

**请求体** (所有字段可选):
```json
{
  "username": "string",
  "nickname": "string",
  "password": "string",
  "role": "user" | "admin"
}
```

**响应**: 返回更新后的用户信息

**错误响应**:
```json
// 400: 用户名已被其他用户使用
{"detail": "用户名已被其他用户使用"}

// 400: 无效的角色
{"detail": "无效的角色"}

// 404: 用户不存在
{"detail": "用户不存在"}
```

---

### 2.7 删除用户

```
DELETE /users/{user_id}
```

**说明**: 删除用户（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | int | 用户ID |

**响应**:
```json
{
  "message": "用户删除成功"
}
```

**错误响应**:
```json
// 400: 不能删除自己
{"detail": "不能删除自己"}

// 404: 用户不存在
{"detail": "用户不存在"}
```

---

## 3. 菜品管理 (Dishes)

### 3.1 创建菜品

```
POST /dishes
```

**说明**: 创建新菜品（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "category": "string",       // 菜品分类（必填）
  "name": "string",           // 菜品名称（必填，唯一）
  "remark": "string"          // 菜品介绍（可选）
}
```

**响应** (201 Created):
```json
{
  "id": 1,
  "category": "川菜",
  "name": "宫保鸡丁",
  "remark": "经典川菜"
}
```

**错误响应**:
```json
// 400: 菜品名称已存在
{"detail": "菜品名称已存在"}

// 403: 权限不足，需要管理员权限
{"detail": "权限不足，需要管理员权限"}
```

---

### 3.2 获取菜品列表

```
GET /dishes
```

**说明**: 获取菜品列表（公开接口）

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| keyword | string | 按菜品名称模糊搜索（可选） |
| category | string | 按分类名称筛选（可选） |
| skip | int | 跳过记录数（默认 0） |
| limit | int | 返回记录数（默认 100，最大 1000） |

**响应**:
```json
[
  {
    "id": 1,
    "category": "川菜",
    "name": "宫保鸡丁",
    "remark": "经典川菜"
  }
]
```

**示例**:
```
GET /dishes?category=川菜
GET /dishes?keyword=鸡丁
```

---

### 3.3 获取菜品详情

```
GET /dishes/{dish_id}
```

**说明**: 获取指定菜品详情（公开接口）

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 菜品ID |

**响应**:
```json
{
  "id": 1,
  "category": "川菜",
  "name": "宫保鸡丁",
  "remark": "经典川菜"
}
```

**错误响应**:
```json
// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

### 3.4 更新菜品

```
PUT /dishes/{dish_id}
```

**说明**: 更新菜品信息（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 菜品ID |

**请求体** (所有字段可选):
```json
{
  "category": "string",
  "name": "string",
  "remark": "string"
}
```

**响应**: 返回更新后的菜品信息

**错误响应**:
```json
// 400: 菜品名称已被其他菜品使用
{"detail": "菜品名称已被其他菜品使用"}

// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

### 3.5 删除菜品

```
DELETE /dishes/{dish_id}
```

**说明**: 删除菜品（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 菜品ID |

**响应**:
```json
{
  "message": "菜品删除成功"
}
```

**错误响应**:
```json
// 400: 该菜品有关联数据，无法删除
{"detail": "该菜品有关联数据，无法删除"}

// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

## 4. 购物车 (Cart)

### 4.1 添加到购物车

```
POST /cart
```

**说明**: 将菜品添加到购物车（需登录）

**请求头**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "dish_id": 1               // 菜品ID（必填）
}
```

**响应** (201 Created):
```json
{
  "id": 1,
  "user_id": 1,
  "dish_id": 1,
  "dish_name": "宫保鸡丁"
}
```

**业务规则**:
- 同一用户不能重复添加同一道菜
- 若已存在，提示：该菜品已在购物车中，请勿重复添加

**错误响应**:
```json
// 400: 该菜品已在购物车中，请勿重复添加
{"detail": "该菜品已在购物车中，请勿重复添加"}

// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

### 4.2 获取购物车列表

```
GET /cart
```

**说明**: 获取当前用户的购物车列表（需登录）

**请求头**: `Authorization: Bearer <token>`

**响应**:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "dish_id": 1,
    "dish_name": "宫保鸡丁"
  }
]
```

---

### 4.3 移除购物车项

```
DELETE /cart/{item_id}
```

**说明**: 从购物车移除指定菜品（需登录）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| item_id | int | 购物车项ID |

**响应**: `204 No Content`

**错误响应**:
```json
// 404: 购物车项不存在
{"detail": "购物车项不存在"}
```

---

### 4.4 清空购物车

```
DELETE /cart
```

**说明**: 清空当前用户的所有购物车内容（需登录）

**请求头**: `Authorization: Bearer <token>`

**响应**: `204 No Content`

---

## 5. 收藏 (Favorites)

### 5.1 添加收藏

```
POST /favorites/{dish_id}
```

**说明**: 收藏指定菜品（需登录）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 菜品ID |

**响应** (201 Created):
```json
{
  "message": "收藏成功",
  "dish_id": 1
}
```

**说明**: 如果已收藏，返回 `{"message": "已收藏", "dish_id": 1}`

**错误响应**:
```json
// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

### 5.2 获取收藏列表

```
GET /favorites
```

**说明**: 获取当前用户的收藏列表（需登录）

**请求头**: `Authorization: Bearer <token>`

**响应**:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "dish_id": 1,
    "dish_name": "宫保鸡丁",
    "category": "川菜"
  }
]
```

---

### 5.3 检查收藏状态

```
GET /favorites/{dish_id}
```

**说明**: 检查指定菜品是否已收藏（需登录）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 菜品ID |

**响应**:
```json
{
  "id": 1,
  "user_id": 1,
  "dish_id": 1,
  "dish_name": "宫保鸡丁",
  "category": "川菜"
}
```

**错误响应**:
```json
// 404: 未收藏
{"detail": "未收藏"}
```

---

### 5.4 取消收藏

```
DELETE /favorites/{dish_id}
```

**说明**: 取消指定菜品的收藏（需登录）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 菜品ID |

**响应**: `204 No Content`

**错误响应**:
```json
// 404: 收藏不存在
{"detail": "收藏不存在"}
```

---

## 6. 历史记录 (History)

### 6.1 提交订单

```
POST /history/submit
```

**说明**: 提交订单，将购物车中的菜品写入历史记录（需登录）

**请求头**: `Authorization: Bearer <token>`

**业务规则**:
- 将购物车中的菜品写入历史记录
- 保存下单时间
- 自动清空购物车

**响应**:
```json
{
  "message": "订单提交成功",
  "order_id": "ORD20260612153000",
  "total_count": 3
}
```

**错误响应**:
```json
// 400: 购物车为空，无法提交订单
{"detail": "购物车为空，无法提交订单"}
```

---

### 6.2 获取历史记录列表

```
GET /history
```

**说明**: 获取当前用户的历史订单列表（需登录）

**请求头**: `Authorization: Bearer <token>`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| start_date | datetime | 开始时间（可选） |
| end_date | datetime | 结束时间（可选） |

**响应**:
```json
[
  {
    "id": 1,
    "user_id": 1,
    "dish_id": 1,
    "dish_name": "宫保鸡丁",
    "category": "川菜",
    "time": "2026-06-12T15:30:00"
  }
]
```

**说明**: 按下单时间倒序排列

---

### 6.3 删除历史记录

```
DELETE /history/{history_id}
```

**说明**: 删除指定的历史记录（需登录，只能删除自己的记录）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| history_id | int | 历史记录ID |

**响应**: `204 No Content`

**错误响应**:
```json
// 404: 历史记录不存在
{"detail": "历史记录不存在"}
```

---

### 6.4 清空历史记录

```
DELETE /history
```

**说明**: 清空当前用户的所有历史记录（需登录）

**请求头**: `Authorization: Bearer <token>`

**响应**: `204 No Content`

---

## 7. 食材采购 (Buy)

### 7.1 新增采购记录

```
POST /buy
```

**说明**: 新增食材采购记录（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "name": "string",          // 食材名称（必填）
  "price": 6.0,              // 采购单价（必填）
  "number": 5.0,             // 采购数量（必填）
  "date": "2026-06-12"       // 采购日期（必填）
}
```

**响应** (201 Created):
```json
{
  "id": 1,
  "name": "番茄",
  "price": 6.0,
  "number": 5.0,
  "date": "2026-06-12",
  "user_id": 1,
  "user_name": "管理员"
}
```

**错误响应**:
```json
// 403: 权限不足，需要管理员权限
{"detail": "权限不足，需要管理员权限"}
```

---

### 7.2 获取采购记录列表

```
GET /buy
```

**说明**: 查询采购记录列表（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| name | string | 按食材名称筛选（可选） |
| start_date | date | 开始日期（可选） |
| end_date | date | 结束日期（可选） |

**响应**:
```json
[
  {
    "id": 1,
    "name": "番茄",
    "price": 6.0,
    "number": 5.0,
    "date": "2026-06-12",
    "user_id": 1,
    "user_name": "管理员"
  }
]
```

---

### 7.3 获取采购记录详情

```
GET /buy/{buy_id}
```

**说明**: 获取指定采购记录详情（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| buy_id | int | 采购记录ID |

**响应**: 同 7.2

**错误响应**:
```json
// 404: 采购记录不存在
{"detail": "采购记录不存在"}
```

---

### 7.4 更新采购记录

```
PUT /buy/{buy_id}
```

**说明**: 更新采购记录（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| buy_id | int | 采购记录ID |

**请求体** (所有字段可选):
```json
{
  "name": "string",
  "price": 6.0,
  "number": 5.0,
  "date": "2026-06-12"
}
```

**响应**: 返回更新后的采购记录

**错误响应**:
```json
// 404: 采购记录不存在
{"detail": "采购记录不存在"}
```

---

### 7.5 删除采购记录

```
DELETE /buy/{buy_id}
```

**说明**: 删除采购记录（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| buy_id | int | 采购记录ID |

**响应**: `204 No Content`

**错误响应**:
```json
// 404: 采购记录不存在
{"detail": "采购记录不存在"}
```

---

### 7.6 日统计

```
GET /buy/stats/daily
```

**说明**: 获取指定日期的采购支出统计（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| target_date | date | 目标日期（可选，默认当天） |

**响应**:
```json
{
  "total_amount": 150.0,
  "total_count": 5,
  "period": "2026-06-12"
}
```

**计算公式**: 总支出 = 单价 × 数量

---

### 7.7 月统计

```
GET /buy/stats/monthly
```

**说明**: 获取指定月份的采购支出统计（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| year | int | 年份（可选，默认今年） |
| month | int | 月份（可选，默认当月） |

**响应**:
```json
{
  "total_amount": 3500.0,
  "total_count": 45,
  "period": "2026-06"
}
```

---

## 附录

### 错误响应格式

所有接口错误响应统一格式：
```json
{
  "detail": "错误描述信息"
}
```

#### 错误响应示例

| 状态码 | 场景 | 错误响应 JSON |
|--------|------|---------------|
| 400 | 用户名已存在 | `{"detail": "用户名已存在"}` |
| 400 | 不能删除自己 | `{"detail": "不能删除自己"}` |
| 400 | 菜品名称已存在 | `{"detail": "菜品名称已存在"}` |
| 400 | 菜品名称已被其他菜品使用 | `{"detail": "菜品名称已被其他菜品使用"}` |
| 400 | 无效的角色 | `{"detail": "无效的角色"}` |
| 400 | 用户名已被其他用户使用 | `{"detail": "用户名已被其他用户使用"}` |
| 400 | 该菜品已在购物车中，请勿重复添加 | `{"detail": "该菜品已在购物车中，请勿重复添加"}` |
| 400 | 购物车为空，无法提交订单 | `{"detail": "购物车为空，无法提交订单"}` |
| 400 | 该菜品有关联数据，无法删除 | `{"detail": "该菜品有关联数据，无法删除"}` |
| 401 | 用户名或密码错误 | `{"detail": "用户名或密码错误"}` |
| 401 | 认证失败 | `{"detail": "认证失败，请重新登录"}` |
| 403 | 权限不足 | `{"detail": "权限不足，需要管理员权限"}` |
| 404 | 用户不存在 | `{"detail": "用户不存在"}` |
| 404 | 菜品不存在 | `{"detail": "菜品不存在"}` |
| 404 | 历史记录不存在 | `{"detail": "历史记录不存在"}` |
| 404 | 采购记录不存在 | `{"detail": "采购记录不存在"}` |
| 404 | 收藏不存在 | `{"detail": "收藏不存在"}` |
| 404 | 未收藏 | `{"detail": "未收藏"}` |
| 404 | 购物车项不存在 | `{"detail": "购物车项不存在"}` |
| 500 | 服务器内部错误 | `{"detail": "获取用户列表失败: ..."}` |

### 常见 HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 204 | 请求成功，无返回内容 |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 角色说明

| 角色 | 说明 |
|------|------|
| admin | 管理员，拥有所有权限 |
| user | 普通用户，仅能操作自己的数据 |

### 认证流程

1. 调用 `POST /users/register` 注册账号
2. 调用 `POST /users/login` 登录获取 Token
3. 在需要认证的请求 Header 中添加：`Authorization: Bearer <token>`
4. Token 有效期默认配置（如有需要可配置过期时间）

### 数据库表结构

#### user 表（用户表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 主键，自增 |
| username | varchar(50) | 用户名，唯一 |
| password | varchar(255) | 密码（加密存储） |
| nickname | varchar(50) | 昵称 |
| role | varchar(20) | 角色（user/admin） |

#### dish 表（菜品表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 主键，自增 |
| category | varchar(50) | 菜品分类 |
| name | varchar(100) | 菜品名称，唯一 |
| remark | text | 菜品介绍 |

#### cart 表（购物车表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 主键，自增 |
| user_id | int | 用户ID，外键 |
| dish_id | int | 菜品ID，外键 |

**约束**: 联合唯一 `UNIQUE(user_id, dish_id)`

#### favorite 表（收藏表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 主键，自增 |
| user_id | int | 用户ID，外键 |
| dish_id | int | 菜品ID，外键 |

**约束**: 联合唯一 `UNIQUE(user_id, dish_id)`

#### history 表（历史记录表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 主键，自增 |
| user_id | int | 用户ID，外键 |
| dish_id | int | 菜品ID，外键 |
| time | datetime | 下单时间 |

#### buy 表（食材采购表）

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | int | 主键，自增 |
| name | varchar(100) | 食材名称 |
| price | float | 采购单价 |
| number | float | 采购数量 |
| date | date | 采购日期 |
| user_id | int | 采购人员ID，外键 |