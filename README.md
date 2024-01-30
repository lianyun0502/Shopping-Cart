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


[購物車 schema diagram](https://dbdiagram.io/d/product-65b755f8ac844320aeeb5da4)

# API

### 登入

* 登入

### 商品

* 新增商品
* 修改商品
* 刪除商品
* 查詢商品

### 購物車

* 新增商品到購物車
* 修改購物車內商品
* 刪除購物車內商品
* 查詢購物車內商品


### 訂單

* 結帳
* 查詢訂單
