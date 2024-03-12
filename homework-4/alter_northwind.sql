-- Подключиться к БД Northwind и сделать следующие изменения:
-- 1. Добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)
alter table products alter column unit_price int check (unit_price > 0);

-- 2. Добавить ограничение, что поле discontinued таблицы products может содержать только значения 0 или 1
alter table products alter column discontinued int check (discontinued = 1 or discontinued = 0);

-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)
create table discontinued_products as select * from products where discontinued = 1;

-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Для 4-го пункта может потребоваться удаление ограничения, связанного с foreign_key. Подумайте, как это можно решить, чтобы связь с таблицей order_details все же осталась.
delete order_details from order_details join products on order_details.product_id = products.product_id where discontinued = 1;
delete from products where discontinued = 1;