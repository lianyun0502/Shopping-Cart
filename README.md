# Shopping Cart
簡單購物車API與資料庫練習，主要會有:
* 簡單登入
* 新增、修改、刪除、查詢商品
* 商品加入、修改、取消加入購物車和查詢購物車內容，
* 並且可以結帳，結帳後會產生訂單，並且可以查詢訂單內容。



## 環境建置與需求

* python >= v3.8
* fastapi
* uvicorn
* sqlalchemy

## 安裝與執行步驟

## Database Scehma

### users
| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | varchar(50) | 使用者ID (pk)|
| email | varchar(50) | 使用者信箱 (not null)|
| phone | varchar(50) | 使用者電話 (not null)|
| address | varchar(50) | 使用者地址 (not null)|
| cart_id | int | 購物車ID (unique)|

### products
| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | int | 商品ID (pk)|
| name | varchar(50) | 商品名稱 |
| price | int | 商品價格 |
| quantity | int | 商品數量 |
| description | text | 商品描述 |
| on_sale_date | datetime | 上架日期 |

### carts
| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | int | 購物車ID (pk)|


### orders
| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | int | 訂單ID (pk)|
| user_id | varchar(50) | 使用者ID |
| product_id | int | 商品ID |
| quantity | int | 商品數量 |


### cart_items
| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | int | 購物車商品ID (pk)|
| cart_id | int | 購物車ID |
| product_id | int | 商品ID |
| quantity | int | 商品數量 |
| is_checked_out | boolean | 是否結帳 |


[購物車 schema diagram](https://dbdiagram.io/d/product-65b755f8ac844320aeeb5da4)

# API

### 用戶

* 登入
[post] /login
```json
{
    "email": ""
    "password": ""
}
```

* 新增用戶

[post] /users
```json
{
    "email": "",
    "password": "",
    "phone": "",
    "address": ""
}
```

* 修改用戶

[patch] /users/{user_id}
```json
{
    "email": "",
    "password": "",
    "phone": "",
    "address": ""
}
```

* 刪除用戶

[delete] /users/{user_id}

### 商品

* 新增商品

[post] /products
```json
{
    "name": "product name",
    "price": 100,
    "quantity": 10,
    "description": "product description",
    "on_sale_date": "current time"
}
```

* 修改商品

[patch] /products/{product_id}
```json
{
    "name": "product name",
    "price": 100,
    "quantity": 10,
    "description": "product description",
    "on_sale_date": "current time"
}
```
* 刪除商品

[delete] /products/{product_id}

* 查詢商品

[get] /products/{product_id}

* 查詢所有商品

[get] /products

### 購物車

* 新增商品到購物車

[post] /carts/{cart_id}/items
```json
{
    "product_id": 1,
    "quantity": 10
}
```

* 修改購物車內商品

[patch] /carts/{cart_id}/items/{item_id}
```json
{
    "quantity": 10
    "is_checked_out": true
}
```
* 刪除購物車內商品

[delete] /carts/{cart_id}/items/{item_id}

* 查詢購物車內商品

[get] /carts/{cart_id}/items/{item_id}

* 查詢購物車內所有商品

[get] /carts/{cart_id}/items

* 購物車結帳

[post] /carts/{cart_id}/checkout


### 訂單

* 新增訂單

[post] /orders
```json
{
    "user_id": "user id",
    "product_id": 1,
    "quantity": 10
}
```

* 查詢訂單

[get] /orders/{order_id}

## 記錄想到的問題

* 1/30

1. 購物車結帳前，購物車裡面有選項表示最後是否要結帳(ex. ui checkbox)，有想到兩種方式，需思考哪種方式比較好 (暫時選a)

    a. 每次打勾都修改購物車內商品的is_checked_out，最後結帳時，後端只要查詢is_checked_out為true的商品即可

    b. 每次打勾由前端記錄狀態，最後結帳時送body給後端去最後結帳
