# Cooks API 接口文档

> 基于 FastAPI 构建的点餐应用后端 API

**基础 URL**: `http://localhost:8000`

**认证方式**: JWT Bearer Token

**请求格式**: `Content-Type: application/json`

---

## 目录

1. [健康检查](#1-健康检查)
2. [用户管理](#2-用户管理-users)
3. [分类管理](#3-分类管理-categories)
4. [菜品管理](#4-菜品管理-dishes)
5. [历史记录](#5-历史记录-history)
6. [智能推荐](#6-智能推荐-recommend)

---

## 1. 健康检查

### 获取服务状态

```
GET /
GET /health
```

**说明**: 检查服务是否正常运行

**请求参数**: 无

**响应示例**:
```json
{
  "message": "Cooks API is running"
}
```

```json
{
  "status": "healthy"
}
```

---

## 2. 用户管理 (Users)

### 2.1 用户注册

```
POST /api/users/register
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
  "role": "user",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**错误码**:
- `400`: 用户名已存在 / 无效的角色

---

### 2.2 用户登录

```
POST /api/users/login
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

**错误码**:
- `401`: 用户名或密码错误

---

### 2.3 获取用户列表

```
GET /api/users
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
    "role": "user",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

**错误码**:
- `403`: 权限不足（非管理员）

---

### 2.4 获取指定用户

```
GET /api/users/{user_id}
```

**说明**: 获取指定用户信息

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | int | 用户ID |

**权限**: 
- 管理员可查看任意用户
- 普通用户只能查看自己

**响应**: 同 2.3

**错误码**:
- `403`: 权限不足
- `404`: 用户不存在

---

### 2.5 更新用户

```
PUT /api/users/{user_id}
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

**错误码**:
- `400`: 用户名已被其他用户使用 / 无效的角色
- `404`: 用户不存在

---

### 2.6 删除用户

```
DELETE /api/users/{user_id}
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

**错误码**:
- `400`: 不能删除自己
- `404`: 用户不存在

---

## 3. 分类管理 (Categories)

### 3.1 创建分类

```
POST /api/categories
```

**说明**: 创建菜品分类（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "name": "string",          // 分类名称（必填，唯一）
  "sort": 0,                 // 排序权重（默认 0）
  "enabled": true            // 是否启用（默认 true）
}
```

**响应** (201 Created):
```json
{
  "id": 1,
  "name": "川菜",
  "sort": 1,
  "enabled": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**错误码**:
- `400`: 分类名称已存在
- `403`: 权限不足

---

### 3.2 获取分类列表

```
GET /api/categories
```

**说明**: 获取所有分类列表（公开接口，无需认证）

**响应**:
```json
[
  {
    "id": 1,
    "name": "川菜",
    "sort": 1,
    "enabled": true,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

**排序规则**: 按 `sort` 字段升序排列

---

### 3.3 获取分类详情

```
GET /api/categories/{category_id}
```

**说明**: 获取指定分类详情（公开接口）

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| category_id | int | 分类ID |

**响应**: 同 3.2

**错误码**:
- `404`: 分类不存在

---

### 3.4 更新分类

```
PUT /api/categories/{category_id}
```

**说明**: 更新分类信息（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| category_id | int | 分类ID |

**请求体** (所有字段可选):
```json
{
  "name": "string",
  "sort": 0,
  "enabled": true
}
```

**响应**: 返回更新后的分类信息

**错误码**:
- `400`: 分类名称已被其他分类使用
- `404`: 分类不存在

---

### 3.5 删除分类

```
DELETE /api/categories/{category_id}
```

**说明**: 删除分类（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| category_id | int | 分类ID |

**响应**:
```json
{
  "message": "分类删除成功"
}
```

**错误码**:
- `400`: 该分类下有菜品，无法删除
- `404`: 分类不存在

---

## 4. 菜品管理 (Dishes)

### 4.1 创建菜品

```
POST /api/dishes
```

**说明**: 创建新菜品（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "name": "string",          // 菜品名称（必填，唯一）
  "category_id": 1,          // 分类ID（必填）
  "difficulty": 1,            // 难度等级 1-5（默认 1）
  "favorite": false,          // 是否收藏（默认 false）
  "enabled": true,            // 是否启用（默认 true）
  "remark": "string",         // 备注（可选）
  "image_url": "string",      // 图片URL（可选）
  "created_by": 1             // 创建者ID（可选）
}
```

**响应** (201 Created):
```json
{
  "id": 1,
  "name": "宫保鸡丁",
  "category_id": 1,
  "difficulty": 2,
  "favorite": false,
  "enabled": true,
  "remark": "经典川菜",
  "image_url": "https://example.com/gongbao.jpg",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**错误码**:
- `400`: 分类不存在 / 菜品名称已存在

---

### 4.2 获取菜品列表

```
GET /api/dishes
```

**说明**: 获取菜品列表（公开接口）

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| keyword | string | 按菜品名称模糊搜索（可选） |
| category_id | int | 按分类ID筛选（可选） |
| favorite | bool | 按收藏状态筛选（可选） |
| difficulty | int | 按难度等级筛选（可选） |
| enabled | bool | 按启用状态筛选（可选） |
| skip | int | 跳过记录数（默认 0） |
| limit | int | 返回记录数（默认 100，最大 1000） |

**响应**:
```json
[
  {
    "id": 1,
    "name": "宫保鸡丁",
    "category_id": 1,
    "difficulty": 2,
    "favorite": false,
    "enabled": true,
    "remark": "经典川菜",
    "image_url": "https://example.com/gongbao.jpg",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

**示例**:
```
GET /api/dishes?category_id=1&difficulty=2
GET /api/dishes?keyword=鸡丁&enabled=true
```

---

### 4.3 获取菜品详情

```
GET /api/dishes/{dish_id}
```

**说明**: 获取指定菜品详情（公开接口）

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 菜品ID |

**响应**: 同 4.2

**错误码**:
- `404`: 菜品不存在

---

### 4.4 更新菜品

```
PUT /api/dishes/{dish_id}
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
  "name": "string",
  "category_id": 1,
  "difficulty": 3,
  "favorite": true,
  "enabled": false,
  "remark": "string",
  "image_url": "string"
}
```

**响应**: 返回更新后的菜品信息

**错误码**:
- `400`: 指定的分类不存在 / 菜品名称已被其他菜品使用
- `404`: 菜品不存在

---

### 4.5 删除菜品

```
DELETE /api/dishes/{dish_id}
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

**错误码**:
- `400`: 该菜品有历史记录，无法删除
- `404`: 菜品不存在

---

### 4.6 切换收藏状态

```
POST /api/dishes/{dish_id}/favorite
```

**说明**: 切换菜品的收藏状态（需登录）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 菜品ID |

**响应**:
```json
{
  "message": "收藏状态已更新",
  "favorite": true
}
```

**错误码**:
- `404`: 菜品不存在

---

## 5. 历史记录 (History)

### 5.1 创建历史记录

```
POST /api/history
```

**说明**: 记录菜品选择历史（需登录）

**请求头**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "dish_id": 1,              // 菜品ID（必填）
  "selected_by": 1,          // 选择人ID（可选，默认当前登录用户）
  "selected_method": "random" | "manual",  // 选择方式（必填）
  "comment": "string"       // 备注（可选）
}
```

**响应** (201 Created):
```json
{
  "id": 1,
  "dish_id": 1,
  "selected_by": 1,
  "selected_method": "random",
  "comment": "今天想吃点辣",
  "created_at": "2024-01-01T00:00:00"
}
```

**错误码**:
- `400`: 指定的菜品不存在

---

### 5.2 获取历史记录

```
GET /api/history
```

**说明**: 获取历史记录列表（需登录）

**请求头**: `Authorization: Bearer <token>`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| start_date | datetime | 开始时间（可选，ISO格式） |
| end_date | datetime | 结束时间（可选，ISO格式） |
| dish_id | int | 按菜品ID筛选（可选） |
| selected_by | int | 按选择人筛选（可选） |
| selected_method | string | 按选择方式筛选（可选） |
| skip | int | 跳过记录数（默认 0） |
| limit | int | 返回记录数（默认 50，最大 500） |

**权限说明**:
- 管理员可查看所有历史记录
- 普通用户只能查看自己的历史记录

**响应**:
```json
[
  {
    "id": 1,
    "dish_id": 1,
    "selected_by": 1,
    "selected_method": "random",
    "comment": "今天想吃点辣",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### 5.3 获取单条历史记录

```
GET /api/history/{history_id}
```

**说明**: 获取指定历史记录（需登录）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| history_id | int | 历史记录ID |

**权限说明**:
- 管理员可查看任意记录
- 普通用户只能查看自己的记录

**响应**: 同 5.2

**错误码**:
- `403`: 权限不足
- `404`: 历史记录不存在

---

### 5.4 删除历史记录

```
DELETE /api/history/{history_id}
```

**说明**: 删除指定历史记录（需登录）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| history_id | int | 历史记录ID |

**权限说明**:
- 管理员可删除任意记录
- 普通用户只能删除自己的记录

**响应**:
```json
{
  "message": "历史记录删除成功"
}
```

**错误码**:
- `403`: 只能删除自己的历史记录
- `404`: 历史记录不存在

---

### 5.5 批量删除历史记录

```
DELETE /api/history
```

**说明**: 批量删除历史记录（仅管理员）

**请求头**: `Authorization: Bearer <token>`

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 按菜品ID筛选删除（可选） |
| selected_by | int | 按选择人筛选删除（可选） |
| days | int | 删除 N 天前的记录（可选） |

**响应**:
```json
{
  "message": "成功删除 10 条历史记录"
}
```

**示例**:
```
DELETE /api/history?days=30     # 删除30天前的所有记录
DELETE /api/history?dish_id=1  # 删除菜品ID为1的所有记录
```

---

## 6. 智能推荐 (Recommend)

### 6.1 随机推荐

```
GET /recommend/random
```

**说明**: 根据条件随机推荐一个菜品（公开接口）

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| category_id | int | 指定分类ID（可选） |
| exclude_days | int | 排除最近 N 天内选择过的菜品（可选） |

**响应**:
```json
{
  "id": 1,
  "name": "宫保鸡丁",
  "category_id": 1
}
```

**错误码**:
- `404`: 没有符合条件的菜品

**示例**:
```
GET /recommend/random                                    # 随机推荐任意菜品
GET /recommend/random?category_id=1                     # 在川菜分类中随机推荐
GET /recommend/random?exclude_days=7                     # 排除最近7天选过的菜品
GET /recommend/random?category_id=2&exclude_days=14      # 组合使用
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

### 常见 HTTP 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
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

1. 调用 `POST /api/users/register` 注册账号
2. 调用 `POST /api/users/login` 登录获取 Token
3. 在需要认证的请求 Header 中添加：`Authorization: Bearer <token>`
4. Token 有效期默认配置（如有需要可配置过期时间）