# Backend API Documentation

## Authentication Endpoints

### `/api/auth/register`

#### Request Method: POST
#### Authentication Required: No
#### Request Body Example:

```json
{
    "name": "张三",
    "email": "zhangsan123@example.com",
    "password": "zhangsan123213"
}
```

#### Parameters

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| name      | string | Yes      | Username    |
| email     | string | Yes      | User email  |
| password  | string | Yes      | Password    |

#### Response Examples

**Error Response:**

```json
{
    "error":  "api.auth.invalidRequestData",
    "detail": "something clearly"
}
```

**Error Response Fields:**

| Field   | Type   | Required | Description                |
|---------|--------|----------|----------------------------|
| error   | string | Yes      | Error type (i18n key)      |
| detail  | string | No       | Detailed error information |

**Success Response:**

```json
{
    "message": "register success"
}
```

**Success Response Fields:**

| Field   | Type   | Required | Description        |
|---------|--------|----------|--------------------|
| message | string | Yes      | Success message    |

### `/api/auth/login`

#### Request Method: POST
#### Authentication Required: No
#### Request Body Example:

```json
{
    "email": "zhangsan123@example.com",
    "password": "zhangsan123213"
}
```

#### Parameters

| Field   | Type   | Required | Description        |
|---------|--------|----------|--------------------|
| email   | string | Yes      | User email         |
| password| string | Yes      | User password      |

#### Response Examples

**Error Response:**

```json
{
    "error":  "api.auth.incorrectEmailOrPassword",
    "detail": "email or password is wrong"
}
```

**Error Response Fields:**

| Field   | Type   | Required | Description                |
|---------|--------|----------|----------------------------|
| error   | string | Yes      | Error type (i18n key)      |
| detail  | string | No       | Detailed error information |

**Success Response:**

```json
{
    "message": "login success",
    "token":   "token"
}
```

**Success Response Fields:**

| Field   | Type   | Description                |
|---------|--------|----------------------------|
| message | string | Success message            |
| token   | string | JWT token valid for 30 days|

### `/api/auth/verify`

#### Request Method: POST
#### Authentication Required: No
#### Request Body Example:

```json
{
    "token": "verify_token"
}
```

#### Parameters

| Parameter | Type   | Required | Description         |
|-----------|--------|----------|---------------------|
| token     | string | Yes      | Verification token  |

#### Response Examples

**Error Response:**

```json
{
    "error":  "api.auth.invalidVerificationToken",
    "detail": "invalid verification token"
}
```

**Error Response Fields:**

| Field   | Type   | Required | Description                |
|---------|--------|----------|----------------------------|
| error   | string | Yes      | Error type (i18n key)      |
| detail  | string | No       | Detailed error information |

**Success Response:**

```json
{
    "message": "login success"
}
```

**Success Response Fields:**

| Field   | Type   | Required | Description     |
|---------|--------|----------|-----------------|
| message | string | Yes      | Success message |

## User Information Endpoints

### `/api/me`

#### Request Method: GET
#### Authentication Required: Yes
#### Response Examples

**Error Response:**

```json
{
    "error": "api.auth.tokenIsRequired",
    "detail": "Token is required"
}
```

**Error Response Fields:**

| Field   | Type   | Required | Description                |
|---------|--------|----------|----------------------------|
| error   | string | Yes      | Error type (i18n key)      |
| detail  | string | No       | Detailed error information |

**Success Response:**

```json
{
  "email": "zhangsan123@example.com",
  "id": 550707222846377484,
  "name": "张三"
}
```

**Success Response Fields:**

| Field  | Type   | Description      |
|--------|--------|------------------|
| email  | string | User email       |
| id     | int    | User ID          |
| name   | string | Username         |

### `/api/info/{id}`

#### Request Method: GET
#### Authentication Required: No
#### Response Examples

**Error Response:**

```json
{
  "error":  "api.auth.userNotFound",
  "detail": "No users found with the given ID"
}
```

**Error Response Fields:**

| Field   | Type   | Required | Description                |
|---------|--------|----------|----------------------------|
| error   | string | Yes      | Error type (i18n key)      |
| detail  | string | No       | Detailed error information |

**Success Response:**

```json
{
  "email": "zhangsan123@example.com",
  "id": 550707222846377484,
  "name": "张三"
}
```

**Success Response Fields:**

| Field  | Type   | Description     |
|--------|--------|-----------------|
| email  | string | User email      |
| id     | int    | User ID         |
| name   | string | Username        |

## WebSocket Endpoints

### `/api/ws/stream?token={token}`

#### Request Method: WEBSOCKET
#### Authentication Required: Yes
#### Response Examples

**Error Response:**

```json
{
  "error":  "api.auth.userNotFound",
  "detail": "No users found with the given ID"
}
```

**Error Response Fields:**

| Field   | Type   | Required | Description                |
|---------|--------|----------|----------------------------|
| error   | string | Yes      | Error type (i18n key)      |
| detail  | string | No       | Detailed error information |

**Success Response:**

Binary data: 
- Image data starting with `0x89, 0x50, 0x4E, 0x47` (PNG header)
- Audio data starting with `0x43`

**Success Response Fields:**
None (binary data)

### /api/courses/materials
#### 用于用户查询信息的接口
#### 请求方法: POST
#### 需要传入Token: 是
#### 响应体示例:
#### 出现错误时
```json
{
  "error":  "api.courses.failedToUploadFile",
  "detail": "something clearly"
}
```

#### 数据字段说明

| 字段名    | 类型     | 必填 | 描述           |
|--------|--------|----|--------------|
| error  | string | 是  | 错误类型(i18n的键) |
| detail | string | 否  | 错误详细信息       |

#### 上传成功时

```json
{
  "message": "uploadSuccessfully",
  "file": "550707222846377484$quadratic function.docx"
}
```


#### 数据字段说明

| 字段名     | 类型     | 描述      |
|---------|--------|---------|
| message | string | 上传成功的信息 |
| file    | string | 上传后的文件名 |