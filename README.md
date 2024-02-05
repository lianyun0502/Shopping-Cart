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

## Database 

這裡的資料庫使用python原生的sqlite3，並且使用sqlalchemy來操作資料庫。

### Schema
* users

| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | varchar(50) | 使用者ID (pk)|
| email | varchar(50) | 使用者信箱 (not null)|
| phone | varchar(50) | 使用者電話 (not null)|
| address | varchar(50) | 使用者地址 (not null)|
| password | varchar(50) | 使用者密碼 (not null)|

* products

| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | int | 商品ID (pk)|
| name | varchar(50) | 商品名稱 |
| price | int | 商品價格 |
| quantity | int | 商品數量 |
| description | text | 商品描述 |
| on_sale_date | datetime | 上架日期 |
| user_id | varchar(50) | 上架者ID |

* carts

| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | int | 購物車ID (pk)|
| user_id | varchar(50) | 使用者ID |


* orders

| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | int | 訂單ID (pk)|
| user_id | varchar(50) | 使用者ID |
| product_id | int | 商品ID |
| quantity | int | 商品數量 |


* cart_items

| 欄位名稱 | 資料型態 | 說明 |
| -------- | -------- | ---- |
| id | int | 購物車商品ID (pk)|
| cart_id | int | 購物車ID |
| product_id | int | 商品ID |
| quantity | int | 商品數量 |
| is_checked_out | boolean | 是否結帳 |


[購物車 schema diagram](https://dbdiagram.io/d/product-65b755f8ac844320aeeb5da4)

## API DOCUMENTATION

關於API的詳細說明文件，fastapi會自動產生，再啟動SERVER後可以透過以下連結查看 [swagger UI](http://127.0.0.1:5000/docs)

## AUTHORS

此版本有加入身分驗證以及授權API，再使用者登入後會產生一個JWT token，某些API每次request時都會檢查token是否合法。

### 使用者登入

在Auth類別裡的第一個POST API 為登入API，
![登入](.\image\login.png)

按下Try it out後只需輸入username和password案execute即可登入。
![登入2](.\image\login2.png)

登入成功後會產生一個JWT token，再每次request時都會檢查token是否合法。
![登入3](.\image\login3.png)

### 授權API

當看到API旁邊有鎖頭的圖示時，就代表每次request時都會檢查token是否合法。
![授權API](.\image\auth.png)

這時只需點開鎖頭圖示，再輸入username和password後案Authorize，如果為已登入帳號，即可使用該API。

Eric的帳號已經建立，可以直接使用
* username: Eric
* password: ericpass

![授權API2](.\image\auth2.png)


### 創建新使用者

在User類別裡的第一個POST API 為創建新使用者API，可以自行創建新帳號。