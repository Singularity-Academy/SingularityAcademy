## /api/auth

### /register
#### 请求方法: POST
#### 需要传入Token: 否
#### 请求体示例:
```json
{
    "name": "张三",
    "email": "zhangsan123@example.com",
    "password": "zhangsan123213"
}
```
#### 参数说明
| 参数名      | 类型     | 必填 | 描述     |
|----------|--------|----|--------|
| name     | string | 是  | 用户名字   |
| email    | string | 是  | 用户邮箱地址 |
| password | string | 是  | 用户密码   |

#### 响应体示例:
#### 出现错误时
```json
{
    "error":  "invalid request data",
    "detail": "something clearly"
}
```

#### 数据字段说明

| 字段名    | 类型     | 描述     |
|--------|--------|--------|
| error  | string | 错误类型   |
| detail | string | 错误详细信息 |

#### 注册成功时

```json
{
    "message": "register success"
}
```

#### 数据字段说明

| 字段名     | 类型     | 描述               |
|---------|--------|------------------|
| message | string | 登录成功的消息          |


### /login
#### 用于处理用户登录请求的接口
#### 请求方法: POST
#### 需要传入Token: 否
#### 请求体示例: 
```json
{
    "email": "zhangsan123@example.com",
    "password": "zhangsan123213"
}
```
#### 参数说明
| 参数名      | 类型     | 必填 | 描述     |
|----------|--------|----|--------|
| email    | string | 是  | 用户邮箱地址 |
| password | string | 是  | 用户密码   |

#### 响应体示例: 
#### 出现错误时
```json
{
    "error":  "email or password is wrong",
    "detail": "email or password is wrong"
}
```

#### 数据字段说明

| 字段名    | 类型     | 描述     |
|--------|--------|--------|
| error  | string | 错误类型   |
| detail | string | 错误详细信息 |

#### 登陆成功时

```json
{
    "message": "login success",
    "token":   "token"
}
```

#### 数据字段说明

| 字段名     | 类型     | 描述               |
|---------|--------|------------------|
| message | string | 登录成功的消息          |
| token   | string | 用户有效期30天的JWToken |

### /api/me
#### 用于用户查询自己信息的接口
#### 请求方法: GET
#### 需要传入Token: 是
#### 响应体示例:
#### 出现错误时
```json
{
    "error": "Token is required",
    "detail": "Token is required"
}
```

#### 数据字段说明

| 字段名    | 类型     | 描述     |
|--------|--------|--------|
| error  | string | 错误类型   |
| detail | string | 错误详细信息 |

#### 查询成功时

```json
{
  "email": "zhangsan123@example.com",
  "id": 550707222846377484,
  "name": "张三"
}
```


#### 数据字段说明

| 字段名   | 类型     | 描述      |
|-------|--------|---------|
| email | string | 用户绑定的邮箱 |
| id    | int    | 用户的id   |
| name  | string | 用户的名字   |
