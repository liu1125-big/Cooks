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
5. [购物车](#5-购物车-cart)
6. [收藏](#6-收藏-favorites)
7. [智能推荐](#7-智能推荐-recommend)

---

**接口总览** (8个模块，31个接口)

| 模块 | 接口数 | 说明 |
|------|--------|------|
| 健康检查 | 2 | 服务状态检查 |
| 用户管理 | 6 | 注册、登录、CRUD操作 |
| 分类管理 | 5 | 菜品分类管理 |
| 菜品管理 | 6 | 菜品CRUD、收藏 |
| 历史记录 | 5 | 选择历史记录管理 |
| 购物车 | 5 | 购物车管理 |
| 收藏 | 4 | 收藏管理 |
| 智能推荐 | 1 | 随机推荐菜品 |

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
  "role": "user",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
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

### 2.3 获取用户列表

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
    "role": "user",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
```

**错误响应**:
```json
// 403: 权限不足（非管理员）
{"detail": "权限不足，需要管理员权限"}
```

---

### 2.4 获取指定用户

```
GET /users/{user_id}
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

**错误响应**:
```json
// 403: 权限不足
{"detail": "权限不足"}

// 404: 用户不存在
{"detail": "用户不存在"}
```

---

### 2.5 更新用户

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

### 2.6 删除用户

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

## 3. 分类管理 (Categories)

### 3.1 创建分类

```
POST /categories
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

**错误响应**:
```json
// 400: 分类名称已存在
{"detail": "分类名称已存在"}

// 403: 权限不足，需要管理员权限
{"detail": "权限不足，需要管理员权限"}
```

---

### 3.2 获取分类列表

```
GET /categories
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
GET /categories/{category_id}
```

**说明**: 获取指定分类详情（公开接口）

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| category_id | int | 分类ID |

**响应**: 同 3.2

**错误响应**:
```json
// 404: 分类不存在
{"detail": "分类不存在"}
```

---

### 3.4 更新分类

```
PUT /categories/{category_id}
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

**错误响应**:
```json
// 400: 分类名称已被其他分类使用
{"detail": "分类名称已被其他分类使用"}

// 404: 分类不存在
{"detail": "分类不存在"}
```

---

### 3.5 删除分类

```
DELETE /categories/{category_id}
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

**错误响应**:
```json
// 400: 该分类下有菜品，无法删除
{"detail": "该分类下有 4 个菜品，无法删除"}

// 404: 分类不存在
{"detail": "分类不存在"}
```

---

## 4. 菜品管理 (Dishes)

### 4.1 创建菜品

```
POST /dishes
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

**错误响应**:
```json
// 400: 指定的分类不存在
{"detail": "指定的分类不存在"}

// 400: 菜品名称已存在
{"detail": "菜品名称已存在"}
```

---

### 4.2 获取菜品列表

```
GET /dishes
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
GET /dishes?category_id=1&difficulty=2
GET /dishes?keyword=鸡丁&enabled=true
```

---

### 4.3 获取菜品详情

```
GET /dishes/{dish_id}
```

**说明**: 获取指定菜品详情（公开接口）

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| dish_id | int | 菜品ID |

**响应**: 同 4.2

**错误响应**:
```json
// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

### 4.4 更新菜品

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

**错误响应**:
```json
// 400: 指定的分类不存在
{"detail": "指定的分类不存在"}

// 400: 菜品名称已被其他菜品使用
{"detail": "菜品名称已被其他菜品使用"}

// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

### 4.5 删除菜品

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
// 400: 该菜品有历史记录，无法删除
{"detail": "该菜品有 1 条历史记录，无法删除"}

// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

### 4.6 切换收藏状态

```
POST /dishes/{dish_id}/favorite
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

**错误响应**:
```json
// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

## 5. 购物车 (Cart)

### 5.1 添加到购物车

```
POST /cart
```

**说明**: 将菜品添加到购物车（需登录）

**请求头**: `Authorization: Bearer <token>`

**请求体**:
```json
{
  "dish_id": 1,              // 菜品ID（必填）
  "quantity": 1              // 数量（默认 1）
}
```

**响应** (201 Created):
```json
{
  "id": 1,
  "user_id": 1,
  "dish_id": 1,
  "quantity": 2,
  "dish_name": "宫保鸡丁",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**说明**: 如果菜品已在购物车中，则累加数量

**错误响应**:
```json
// 404: 菜品不存在
{"detail": "菜品不存在"}
```

---

### 5.2 获取购物车列表

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
    "quantity": 2,
    "dish_name": "宫保鸡丁",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

---

### 5.3 更新购物车数量

```
PUT /cart/{item_id}
```

**说明**: 更新购物车中菜品的数量（需登录）

**请求头**: `Authorization: Bearer <token>`

**路径参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| item_id | int | 购物车项ID |

**请求体**:
```json
{
  "quantity": 3
}
```

**响应**:
```json
{
  "id": 1,
  "user_id": 1,
  "dish_id": 1,
  "quantity": 3,
  "dish_name": "宫保鸡丁",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**错误响应**:
```json
// 404: 购物车项不存在
{"detail": "购物车项不存在"}
```

---

### 5.4 移除购物车项

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

### 5.5 清空购物车

```
DELETE /cart
```

**说明**: 清空当前用户的所有购物车内容（需登录）

**请求头**: `Authorization: Bearer <token>`

**响应**: `204 No Content`

---

## 6. 收藏 (Favorites)

### 6.1 添加收藏

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

### 6.2 获取收藏列表

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
    "category_name": "川菜",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### 6.3 检查收藏状态

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
  "category_name": "川菜",
  "created_at": "2024-01-01T00:00:00"
}
```

**错误响应**:
```json
// 404: 未收藏
{"detail": "未收藏"}
```

---


### 6.4 取消收藏

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

## 7. 智能推荐 (Recommend)

### 7.1 随机推荐

```
GET /recommend/random
```

**说明**: 根据条件随机推荐一个菜品（公开接口）

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| category_id | int | 指定分类ID（可选） |

**响应**:
```json
{
  "id": 1,
  "name": "宫保鸡丁",
  "category_id": 1
}
```

**错误响应**:
```json
// 404: 没有符合条件的菜品
{"detail": "没有符合条件的菜品"}
```

**示例**:
```
GET /recommend/random                                    # 随机推荐任意菜品
GET /recommend/random?category_id=1                     # 在川菜分类中随机推荐
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
|--------|------|-------------|
| 400 | 用户名已存在 | `{"detail": "用户名已存在"}` |
| 400 | 不能删除自己 | `{"detail": "不能删除自己"}` |
| 400 | 该分类下有菜品 | `{"detail": "该分类下有 4 个菜品，无法删除"}` |
| 400 | 该菜品有历史记录 | `{"detail": "该菜品有 1 条历史记录，无法删除"}` |
| 400 | 菜品名称已存在 | `{"detail": "菜品名称已存在"}` |
| 400 | 分类名称已存在 | `{"detail": "分类名称已存在"}` |
| 400 | 无效的角色 | `{"detail": "无效的角色"}` |
| 400 | 用户名已被其他用户使用 | `{"detail": "用户名已被其他用户使用"}` |
| 400 | 指定的分类不存在 | `{"detail": "指定的分类不存在"}` |
| 400 | 该分类有关联数据，无法删除 | `{"detail": "该分类有关联数据，无法删除"}` |
| 400 | 创建用户失败 | `{"detail": "创建用户失败: ..."}` |
| 400 | 更新用户失败 | `{"detail": "更新用户失败: ..."}` |
| 400 | 删除用户失败 | `{"detail": "删除用户失败: ..."}` |
| 400 | 创建分类失败 | `{"detail": "创建分类失败: ..."}` |
| 400 | 更新分类失败 | `{"detail": "更新分类失败: ..."}` |
| 400 | 删除分类失败 | `{"detail": "删除分类失败: ..."}` |
| 400 | 创建菜品失败 | `{"detail": "创建菜品失败: ..."}` |
| 400 | 更新菜品失败 | `{"detail": "更新菜品失败: ..."}` |
| 400 | 删除菜品失败 | `{"detail": "删除菜品失败: ..."}` |
| 400 | 创建历史记录失败 | `{"detail": "创建历史记录失败: ..."}` |
| 400 | 删除历史记录失败 | `{"detail": "删除历史记录失败: ..."}` |
| 400 | 菜品名称已被其他菜品使用 | `{"detail": "菜品名称已被其他菜品使用"}` |
| 400 | 分类名称已被其他分类使用 | `{"detail": "分类名称已被其他分类使用"}` |
| 401 | 用户名或密码错误 | `{"detail": "用户名或密码错误"}` |
| 401 | 认证失败 | `{"detail": "认证失败，请重新登录"}` |
| 403 | 权限不足 | `{"detail": "权限不足，需要管理员权限"}` |
| 403 | 只能查看自己的历史记录 | `{"detail": "只能查看自己的历史记录"}` |
| 403 | 只能删除自己的历史记录 | `{"detail": "只能删除自己的历史记录"}` |
| 404 | 用户不存在 | `{"detail": "用户不存在"}` |
| 404 | 分类不存在 | `{"detail": "分类不存在"}` |
| 404 | 菜品不存在 | `{"detail": "菜品不存在"}` |
| 404 | 历史记录不存在 | `{"detail": "历史记录不存在"}` |
| 404 | 没有符合条件的菜品 | `{"detail": "没有符合条件的菜品"}` |
| 500 | 获取用户列表失败 | `{"detail": "获取用户列表失败: ..."}` |
| 500 | 获取分类列表失败 | `{"detail": "获取分类列表失败: ..."}` |
| 500 | 获取菜品列表失败 | `{"detail": "获取菜品列表失败: ..."}` |
| 500 | 获取历史记录失败 | `{"detail": "获取历史记录失败: ..."}` |
| 500 | 更新收藏状态失败 | `{"detail": "更新收藏状态失败: ..."}` |
| 500 | 批量删除历史记录失败 | `{"detail": "批量删除历史记录失败: ..."}` |

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

1. 调用 `POST /users/register` 注册账号
2. 调用 `POST /users/login` 登录获取 Token
3. 在需要认证的请求 Header 中添加：`Authorization: Bearer <token>`
4. Token 有效期默认配置（如有需要可配置过期时间）